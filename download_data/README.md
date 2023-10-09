# Scripts to download data from neuroscience journals

## ARXIV
[This](https://github.com/Wanderer-of-the-abyss/nbdt-llm/blob/main/download_data/extract_ARXIV_from_kaggle.ipynb) notebook details how to download and filter data from the arxiv dataset available on [Kaggle](https://www.kaggle.com/datasets/Cornell-University/arxiv)

- You will need to use this script to download Kaggle data directly from your terminal

```python
pip install -q kaggle
from google.colab import files
files.upload()
mkdir ~/.kaggle # upload your kaggle username file

cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d Cornell-University/arxiv

```
- Then you need to divide the data into chunks, as the dataset is huge
```python
split -l 350000 /content/arxiv-metadata-oai-snapshot.json
```
- Then filter the data as you need, based on the categories mentioned on the [ARXIV](https://arxiv.org/category_taxonomy)

## BIOARXIV

```python
import requests 
import json

url = 'https://api.biorxiv.org/details/biorxiv/2019-01-01/2023-01-01/{}/json?category=neuroscience'
articles1 = []
cursor = 0
count = 0
while count < 100000:
    results1 = requests.get(url.format(cursor)).json()
    articles1 += results1['collection']
    count += len(results1['collection'])
    cursor += 100
    print(f'Fetched {len(results1["collection"])} articles. Total count: {count}')
```
As you can see in the above code use the bioarxiv API URL and change the variables i.e. range within which the data is to be requested, as required, it is recommended to keep the `count` less than 100000, as it requestING more than that in a single run blocks your access for some time.

For more information about more features visit the BIOARXIV API page: https://api.biorxiv.org/

## PLOS_ONE
```python
import requests
import json

articles = []  # Define an empty list to store the articles

for i in range(0, 14000, 100):
    # Define the query parameters
    query = "neuroscience"
    fields = "title,author,abstract,journal,subject_facet"
    filter = "publication_date:[2019-01-01T00:00:00Z TO 2023-12-31T23:59:59Z], subject_facet:“/Neuroscience/”"
    start = i
    rows = 100

    # Construct the query URL
    url = f"http://api.plos.org/search?q={query}&fl={fields}&fq={filter}&start={start}&rows={rows}"

    # Send the request and get the response
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()

        # Append the articles from this page to the list
        articles.extend(data['response']['docs'])

    else:
        # Print an error message
        print(f"Request failed with status code {response.status_code}")

# Print the total number of articles collected
print(f"Collected {len(articles)} articles.")

```

The `start` refers to the page number and the `rows` refers to the max number of data rows present in that page (i.e 100). You can change the `fields` to include extra features for the requested data.

For more information on the API visit the PLOS_ONE API page: https://api.plos.org/

## PSY-ARXIV
```python
import requests
import json

# Define the base URL for the OSF API
base_url = "https://api.osf.io/v2/nodes/?filter[category]=project&filter[date_created][gte]=2019-01-01T00:00:00.000Z&filter[date_created][lt]=2023-01-01T00:00:00.000Z&filter[preprint]=psyarxiv&page[size]=100"

# Iterate over the pages
for page in range(1, 10):
    # Create the URL for the current page
    page_url = base_url + "&page=" + str(page)

    # Make a GET request to the current page URL
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response of the current page
        data = json.loads(response.text)

        # Process the articles of the current page
        articles = data['data']
        # Do something with the articles...

        # Print the number of articles extracted in this iteration
        num_articles = len(articles)
        print("Number of articles extracted in iteration", page, ":", num_articles)

    else:
        # Print an error message if the request was not successful
        print("Error: Failed to retrieve data from", page_url)
        break  # Exit the loop if there was an error
```

Here you can include the parts of the data you want, by editing the `base_url` and then iterate over `k` pages.
For more information on how to edit the `base_url` visit: https://developer.osf.io/
