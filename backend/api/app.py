import pandas as pd
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from pathlib import Path

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

# Get the path of the current script
script_dir = Path(__file__).resolve().parent
DATASETS_PATH = script_dir /  '../data'

# user_query = "How many genders are depressed."

def get_dataset_info(df):

    columns = df.columns.tolist()
    description = df.describe()

    non_numeric_columns = df.select_dtypes(exclude=['number'])
    unique_values = {col: non_numeric_columns[col].unique().tolist() for col in non_numeric_columns.columns}
    return columns, description, unique_values

def generate_pandas_query(columns, description, unique_values, user_query):
    client = OpenAI()
    # context = "You are writting python duckdb query to use on pandas dataset called 'df'. Use no schema. Use only 'from df'. Columns list: {}. Here is short statistics of dataframe {}.  Here is information about unique values in non-numeric columns: {} Convert natural language query into a raw runnable duckdb sql string. Conditions: No formatting. Returned output should be able to run. Oneliner only. Absolutely make sure to select everything that is asked in prompt if it is possible!".format(columns, description,unique_values)

    context = (
        "You are writting python duckdb query to use on pandas dataset called 'df'."
        "Use no information_schema."
        "Use only 'FROM df'."
        "Columns list: {}. Must keep the structure."
        "Here is short statistics of dataframe {}."
        "Here is information about unique values in non-numeric columns: {}."
        "Convert natural language query into a raw runnable duckdb sql string."
        "Conditions: No formatting. Returned output should be able to run. Oneliner only. Absolutely make sure to select everything that is asked in prompt if it is possible!"
        "Output is raw string, which will be then filled in duckdb.query(str(RAWSTRINGQUERY)).df()"
    ).format(columns, description, unique_values)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user", 
                "content": "Context: {} \nUser query: {}".format(context,user_query)
            }
        ]
    )

    # Extract and return the generated query
    raw_output = response.choices[0].message.content.strip('"')

    # Remove unwanted backticks or "json" markers
    if raw_output.startswith("```sql"):
        raw_output = raw_output[7:]  # Remove the ```json prefix
    elif raw_output.startswith("```"):
        raw_output = raw_output[3:]  # Remove the ``` prefix
    elif raw_output.startswith("`"):
        raw_output = raw_output[1:]  # Remove the ` prefix
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]  # Remove the closing backticks
    elif raw_output.endswith("`"):
        raw_output = raw_output[:-1]  # Remove the closing backticks


    return raw_output

def structure_data_with_format(query_result, user_prompt):
    client = OpenAI()
    context_type = '''{
    "content": [
        {
            "type": "simple",
            "data": <simple_data_value-int,str,float,list-of(strings,ints,floats)>
        },
        {
            "type": "complex",
            "data": {
                <category_name_1>: <category_value_1-integeronly>,
                <category_name_2>: <category_value_2-integeronly>,
                ...
            }
        }
    ]
}
'''

    context = (
        "Given the following data, structure it according to the following format: {}. "
        "If the data is a single value (number, string, list of simple types, etc.), it should be considered as type 'simple' data."
        "If the data consists of categories or multiple values (such as a list of complex items or counts), it should be considered as 'complex' data with category counts. "
        "Return only the structured JSON object without any additional text, backticks, or formatting markers. Must keep the structure."
        "Absolutely make sure to follow predefined structure! Do not add new keys, that are not defined. No Null data!"
        "Structure data with attention to user prompt: {}"
    ).format(context_type, user_prompt)

    # Send the request to the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Context: {} \nData: {}".format(context,query_result)
            }
        ]
    )
    # print(response.choices[0].message.content)
    raw_output = response.choices[0].message.content
    # Remove unwanted backticks or "json" markers
    if raw_output.startswith("```json"):
        raw_output = raw_output[7:]  # Remove the ```json prefix
    elif raw_output.startswith("```"):
        raw_output = raw_output[3:]  # Remove the ``` prefix
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]  # Remove the closing backticks

    # Extract and return the formatted output
    return json.loads(raw_output)


def generate_additional_text(data, user_query):
    client = OpenAI()
    for idx, item in enumerate(data['content']):
        if item["type"] == "complex" and len(item["data"]) == 1:
            _, value = next(iter(item["data"].items())) 
            item["type"] = "simple"
            item["data"] = value

        if item['type'] == 'simple':
            # Extract the simple value
            simple_value = item['data']
            
            # Use the simple value in a prompt
            prompt = "You have previously done quering my dataset. Answer only in boundaries of my dataset! Given value from last query: {}, generate answer to asked question about dataset {}.".format(simple_value, user_query)
            
            response = client.chat.completions.create(
                model="o1-preview",
                messages=[
                    {
                    "role": "user", 
                    "content": "{}".format(prompt)
                    }
                ]
            )
            # Output the generated text
            generated_text = response.choices[0].message.content
            data['content'][idx]['data'] = generated_text
        


    return data


def get_documents():

    file_paths = [os.path.join(DATASETS_PATH, f) for f in os.listdir(DATASETS_PATH) if f.endswith(".csv")]

    documents = []
    for path in file_paths:
        loader = TextLoader(path)  # TextLoader loads the entire file as a single document
        documents.extend(loader.load())  # Combine all loaded documents

    documents = []
    for path in file_paths:
        loader = TextLoader(path)
        documents.extend(loader.load())

    print(f"Loaded {len(documents)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    return vectorstore

def create_llm(vectorstore):

    # Initialize the retriever and language model
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key)

    # Create a RetrievalQA chain
    rag_pipeline = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,  # Optional: Include source documents in output
    )
    return rag_pipeline


def get_document_paths_from_rag(rag_pipeline, query):
    # Run the query through the RAG pipeline
    response = rag_pipeline({"query": query})

    # Extract the source paths of the documents used
    documents = response["source_documents"]
    needed_documents = {doc.metadata['source'] for doc in documents}
    
    # Return the set of document paths
    return needed_documents


def load_and_concatenate_csvs(document_paths):
    """
    Loads multiple CSV files from a list of document paths and concatenates them into a single pandas DataFrame.

    Args:
        document_paths (list): A list of file paths to CSV files.

    Returns:
        pd.DataFrame: A concatenated DataFrame of all CSV files.
    """
    data_frames = []  # List to hold individual dataframes

    for path in document_paths:
        try:
            # Load the CSV into a DataFrame
            df = pd.read_csv(path)
            # Append the DataFrame to the list
            data_frames.append(df)
        except Exception as e:
            print(f"Error loading {path}: {e}")

    # Concatenate all DataFrames into one
    if data_frames:
        concatenated_df = pd.concat(data_frames, ignore_index=True)
        columns, description, unique_values = get_dataset_info(concatenated_df)
        return concatenated_df, columns, description, unique_values
    else:
        raise ValueError("No valid CSV files to concatenate.")
        
