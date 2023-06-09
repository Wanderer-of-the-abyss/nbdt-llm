# nbdt-llm
Repository for exploring recommendation using language model for NBDT journal. We use a finetuned version of [arazd/MIReAD](https://huggingface.co/arazd/MIReAD) trained on journal classification to create our embeddings. You can find the model on huggingface at [biodatlab/MIReAD-Neuro](https://huggingface.co/biodatlab/MIReAD-Neuro)

## Usage

All notebooks were written in colab and run using a free-tier GPU environment. The code assumes that you are running in a GPU environment. Please change `.cuda()` or `'cuda'` to `.cpu()` or `'cpu'` as necessary if you do not have access to a GPU environment.

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

### Finetuning your own model

Use the notebook [finetune_model.ipynb](notebooks/finetune_model.ipynb) and follow the instructions. 
You will need a dataset of paper abstracts with the title, abstract and journal. Load that in to the notebook at - 
```py
data = pd.read_csv('your_data.csv')
data.info()
```

