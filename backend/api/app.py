import pandas as pd
import json
from openai import OpenAI, embeddings, completions
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables from .env file
load_dotenv(".env")
api_key=os.getenv("OPENAI_API_KEY")
user_query = "How many genders are depressed."

def get_dataset():
    df = pd.read_csv('../data/dataset.csv')
    columns = df.columns.tolist()
    description = df.describe()

    non_numeric_columns = df.select_dtypes(exclude=['number'])
    unique_values = {col: non_numeric_columns[col].unique().tolist() for col in non_numeric_columns.columns}
    return df, columns, description, unique_values

def generate_pandas_query(columns, description, unique_values, user_query):
    client = OpenAI()
    context = "You are writting pandas query from dataset df. Columns list: {}. Here is short statistics of dataframe {}.  Here is information about unique values in non-numeric columns: {} Convert natural language query into a raw runnable pandas query string without any formatting. Returned output should be able to run in eval function in python.".format(columns, description,unique_values)

    response = client.chat.completions.create(
        model="o1-preview",
        messages=[
            {
                "role": "user", 
                "content": "Context: {} \nUser query: {}".format(context,user_query)
            }
        ]
    )

    # Extract and return the generated query
    query = response.choices[0].message.content.strip('"')
    return query

def structure_data_with_format(query_result):
    client = OpenAI()
    context_type = '''{
    "data": [
        {
        "type": "simple",
        "value": <simple_data_value>
        },
        {
        "type": "complex",
        "data": {
            <category_name_1>: <category_value_1>,
            <category_name_2>: <category_value_2>,
            ...
        }
        }
    ]
    }
    '''

    context = "Given the following data, structure it according to the following format: {}. If the data is a single value (number, string, list of simple types, etc.), it should be considered as 'simple' data. If the data consists of categories or multiple values (such as a list of complex items or counts), it should be considered as 'complex' data with category counts. Raw formatting is must".format(context_type)

    # Send the request to the OpenAI API
    response = client.chat.completions.create(
        model="o1-preview",
        messages=[
            {
                "role": "user",
                "content": f"Context: {context} \nData: {query_result}"
            }
        ]
    )
    
    # Extract and return the formatted output
    return json.loads(response.choices[0].message.content)
