import streamlit as st
import csv
import random
import pickle
import uuid
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
import os
import warnings
from streamlit_cookies_manager import EncryptedCookieManager
from typing import Tuple, List, Any, Union
import requests

# Initialize cookie manager and set up warnings
cookies = EncryptedCookieManager(
    prefix="LUL/streamlit-cookies-manager/",
    password=os.environ.get("COOKIES_PASSWORD", "uDnda87,kGFdi&jh.kjsk/jk4DF369*^jhGks"),
)
warnings.filterwarnings("ignore")

user_id = cookies.get('user_id')  # Attempt to retrieve the user ID cookie

if user_id is None:
    user_id = str(uuid.uuid4())  # Generate a random user ID
    cookies['user_id'] = user_id  # Set the cookie

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# URLs of your remote files
article_list_url = "https://huggingface.co/spaces/atrytone/ArenaTester/resolve/main/article_list.pkl"


# Local paths where the files will be downloaded
article_list_path = "article_list_2.pkl"


# Download the files
download_file(article_list_url, article_list_path)


# Now load the files from the local paths
with open(article_list_path, "rb") as articles:
    article_list = tuple(pickle.load(articles))
    

# Set up constants
INDEXES = ["miread_large", "miread_contrastive", "scibert_contrastive"]
MODELS = [
    "biodatlab/MIReAD-Neuro-Large",
    "biodatlab/MIReAD-Neuro-Contrastive",
    "biodatlab/SciBERT-Neuro-Contrastive",
]
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

# Initialize embeddings and vector databases
faiss_embedders = [HuggingFaceEmbeddings(
    model_name=name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs) for name in MODELS]

vecdbs = [FAISS.load_local(index_name, faiss_embedder)
          for index_name, faiss_embedder in zip(INDEXES, faiss_embedders)]

def get_matchup() -> Tuple[str, str]:
    choices = INDEXES
    left, right = random.sample(choices, 2)
    return left, right

def get_comp(prompt: str) -> Tuple[List[Any], List[Any]]:
    left, right = get_matchup()
    left_output = inference(prompt, left)
    right_output = inference(prompt, right)
    return left_output, right_output

def get_article() -> str:
    return random.choice(article_list)

def send_result(l_output: List[Any], r_output: List[Any], prompt: str, pick: str) -> str:
    with open('results.csv', 'a') as res_file:
        writer = csv.writer(res_file)
        row = [user_id, l_output, r_output, prompt, pick]
        writer.writerow(row)
    new_prompt = get_article()
    return new_prompt

def get_matches(query: str, db_name: str = "miread_contrastive") -> List[Tuple[Any, float]]:
    """
    Wrapper to call the similarity search on the required index
    """
    matches = vecdbs[INDEXES.index(db_name)].similarity_search_with_score(query, k=30)
    return matches

def inference(query: str, model: str = "miread_contrastive") -> List[List[Union[int, float, str]]]:
    """
    This function processes information retrieved by the get_matches() function
    Returns - Streamlit output for the authors, abstracts, and journals tabular output
    """
    matches = get_matches(query, model)
    auth_counts = {}
    n_table = []
    scores = [round(match[1].item(), 3) for match in matches]
    min_score = min(scores)
    max_score = max(scores)

    def normaliser(x: float) -> float:
        return round(1 - (x-min_score)/max_score, 3)

    i = 1
    for match in matches:
        doc = match[0]
        score = round(normaliser(round(match[1].item(), 3)), 3)
        title = doc.metadata['title']
        author = doc.metadata['authors'][0].title()
        date = doc.metadata.get('date', 'None')
        link = doc.metadata.get('link', 'None')

        # For authors
        record = [score, author, title, link, date]
        if auth_counts.get(author, 0) < 2:
            n_table.append([i, ]+record)
            i += 1
            if auth_counts.get(author, 0) == 0:
                auth_counts[author] = 1
            else:
                auth_counts[author] += 1

    return n_table[:10]




if 'button_pressed' not in st.session_state:
    st.session_state['button_pressed'] = None

if 'l_output_df' not in st.session_state:
    st.session_state['l_output_df'] = None

if 'r_output_df' not in st.session_state:
    st.session_state['r_output_df'] = None

# Using st.write for HTML content:
st.write(
    """
    <h1 style='text-align: center; color: #0066cc;'>NBDT Recommendation Engine Arena</h1>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    <p style='font-size: 18px; text-align: center; color: #333;'>
    NBDT Recommendation Engine for Editors is a tool for neuroscience authors/abstracts/journals recommendation built for NBDT journal editors.
    It aims to help an editor find similar reviewers, abstracts, and journals for a given submitted abstract.
    To get a recommendation, paste a `title[SEP]abstract` or `abstract` in the text box below and click the appropriate 'Get Comparison' button.
    Then, explore the suggested lists of authors, abstracts, and journals.
    The data in our current demo includes authors associated with the NBDT Journal, and we regularly update it for the latest publications.
    </p>
    """,
    unsafe_allow_html=True
)

article = get_article()
prompt = st.text_area("Enter Abstract", article, height=200)
action_btn = st.button("Get Comparison")

# Create a layout with two columns for Model A and Model B results
col1, col2 = st.columns(2)

if action_btn:
    l_output, r_output = get_comp(prompt)
    l_output_df = pd.DataFrame(l_output, columns=['No', 'Score', 'Name', 'Title', 'Link', 'Date'])
    r_output_df = pd.DataFrame(r_output, columns=['No', 'Score', 'Name', 'Title', 'Link', 'Date'])

    st.session_state['l_output_df'] = l_output_df
    st.session_state['r_output_df'] = r_output_df
    
    # Display Model A results in the first column
    with col1:
        st.write("Model A Results:")
        st.dataframe(st.session_state['l_output_df'], width=800)
    
    # Display Model B results in the second column
    with col2:
        st.write("Model B Results:")
        st.dataframe(st.session_state['l_output_df'], width=800)



    # Align "Model A is better" and "Model B is better" buttons horizontally
    st.write("")  # Add some space
    st.markdown("### Choose the Better Model:")
    columns = st.columns(2)  # Create two columns for buttons and store them in a variable
    with st.container():  # Create a container for alignment
      with columns[0]:
        l_btn = st.button("Model A is better")
      with columns[1]:
        r_btn = st.button("Model B is better")



    if l_btn or r_btn:
        # Store which button was pressed
        st.session_state['button_pressed'] = 'Model A' if l_btn else 'Model B'
        # Send the result
        send_result(st.session_state['l_output_df'], st.session_state['l_output_df'], prompt, st.session_state['button_pressed'])
        # Reset session state to prevent re-triggering
        st.session_state['button_pressed'] = None
        # You could provide feedback or further instructions to the user here, if needed.
        st.write(f"You selected {st.session_state['button_pressed']} as better.")
