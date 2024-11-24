import pandas as pd
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")


# user_query = "How many genders are depressed."

def get_dataset(dataset_name):
    df = pd.read_csv(dataset_name)
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
    "content": [
        {
        "type": "simple",
        "data": <simple_data_value>
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

    context = (
        "Given the following data, structure it according to the following format: {}. "
        "If the data is a single value (number, string, list of simple types, etc.), it should be considered as 'simple' data. "
        "If the data consists of categories or multiple values (such as a list of complex items or counts), it should be considered as 'complex' data with category counts. "
        "Return only the structured JSON object without any additional text, backticks, or formatting markers."
    ).format(context_type)

    # Send the request to the OpenAI API
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Context: {context} \nData: {query_result}"
            }
        ]
    )
    print(response.choices[0].message.content)
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
        if item['type'] == 'simple':
            # Extract the simple value
            simple_value = item['data']
            
            # Use the simple value in a prompt
            prompt = "You have previously done quering dataset. Given value from last query: {}, generate answer to asked question about dataset {}.".format(simple_value, user_query)
            
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