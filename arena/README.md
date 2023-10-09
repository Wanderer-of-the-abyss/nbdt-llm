# NBDT ARENA

## Installation

On the git bash command line, clone the repo 
```python
git clone repo_link
```

Navigate to the arena folder by `cd ` commands and install all the dependencies.
After all the libraries are installed you can run the app with the `streamlit` run command.

```python
cd nbdt-llm
cd arena
pip install -r requirements.txt
streamlit run app.py
```

## Creating vector database 
To build your own vector database based on custom data, you can use this [script](https://github.com/Wanderer-of-the-abyss/nbdt-llm/blob/main/arena/Build_VecStore.ipynb), by default this script creates a vector database by using the [MIReAD_large model](https://huggingface.co/biodatlab/MIReAD-Neuro-Large), but can be changed with all the available models in HugggingFace.
To change the data source for creating the vector database, just change these sections of the code:

![image](https://github.com/Wanderer-of-the-abyss/nbdt-llm/assets/91069648/7215e518-73e5-4477-9d65-db0060f3489a)

Currently, the code is intended for the default data we used to create the embeddings.

Default data for creating vector database:  

- nbdt_data:  https://drive.google.com/file/d/1-123xEqdY9uNhgoYjayroHr70kRaP3rj/view

- aliases: https://github.com/Wanderer-of-the-abyss/nbdt-llm/blob/main/arena/id_list.csv


