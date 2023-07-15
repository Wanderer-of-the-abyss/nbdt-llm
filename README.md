# Exploring LLM recommendation for NBDT Journal

Repository for exploring recommendation using language model for [NBDT journal](https://nbdt.scholasticahq.com/). We use a finetuned version of [arazd/MIReAD](https://huggingface.co/arazd/MIReAD) trained on journal classification to create our embeddings. You can find the model on huggingface at [biodatlab/MIReAD-Neuro](https://huggingface.co/biodatlab/MIReAD-Neuro)

## Usage

All notebooks were written in colab. The code assumes that you are running in a GPU environment. Please change `.cuda()` or `'cuda'` to `.cpu()` or `'cpu'` as necessary if you do not have access to a GPU environment.

Indexes created by different models for using in Langchain are availabe on the [Hugging Face Space](https://huggingface.co/spaces/biodatlab/NBDT-Recommendation-Engine). Download the folder you require into your working directory.

### Usage to build a pinecone database of your abstracts with our model

Use the notebook [build_abstract_database.ipynb](notebooks/build_abstract_database.ipynb) and follow the instructions.
You will need to create an account on [Pinecone](https://www.pinecone.io/) for this. The free tier allows the creation of 1 index.
After creation of the account you can see your API key and ENV code in the API Keys section on your organization page. Those need to go in the notebook at -

```py
PINECONE_API_KEY = ""
PINECONE_ENV = ""
```

### Usage to query the pinecone database

Use the notebook [fetch_recommendations.ipynb](notebooks/fetch_recommendations.ipynb) and follow the instructions.
You will need to have an index on [Pinecone](https://www.pinecone.io/) for this.
Your API key and ENV code can be found in the API Keys section on your organization page. Those need to go in the notebook at -

```py
PINECONE_API_KEY = ""
PINECONE_ENV = ""
```

The name of your index must go in at - 

```py
index_name = 'reviewer-assignment'          # Replace with your index name
index = pinecone.GRPCIndex(index_name)
```

### Usage to build your own LangChain VecStore

Use the notebook [build_vecstore.ipynb](notebooks/build_vecstore.ipynb) and follow the instructions.
The notebook provides an 'index' folder with files named 'index.faiss' and 'index.pkl' which can be loaded in to the model at inference time

### Usage to query the LangChain VecStore and deploy the Gradio app

Use the notebook [inference.ipynb](notebooks/inference.ipynb) and follow the instructions.

### Finetuning your own model
#### Journal Classification Task
Use the notebook [finetune_model_normal.ipynb](notebooks/finetune_model_normal.ipynb) and follow the instructions. 
You will need a dataset of paper abstracts with the title, abstract and journal. Load that in to the notebook at - 

```py
data = pd.read_csv('your_data.csv')
data.info()
```

#### Contrastive Learning Task
Use the notebook [finetune_model_contr.ipynb](notebooks/finetune_model_contr.ipynb) and follow the instructions. 
You will need a dataset of paper abstracts with the title, abstract and journal. Load that in to the notebook at - 

```py
data = pd.read_csv('your_data.csv')
data.info()
```


