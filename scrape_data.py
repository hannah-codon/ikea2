from openai import OpenAI
import pandas as pd
import json
import os 
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key= os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
input_path = "/mnt/data/projects/hackathons/mega-trend/data/html_dumps/"  
output_path = "/mnt/data/projects/hackathons/mega-trend/data/ikea_csv"
html_list = []

for filename in os.listdir(input_path):
    with open(f"{input_path}/{filename}", "r", encoding="utf-8") as f:
        html_content = f.read()
        html_list.append(html_content)

system_prompt_content = """ 
Take the list of htmls of several IKEA chairs and create a table in json format for each chair with following keys: 
id: a unique ID created by you (int) 
article_number: the article number of the given html (int) 
image_url: the image url of the given html (string) 
category: the category of the given html (string) 
description: the description of the given html (string) 
price: the price of the given html (float) 
weight: the weight of the given html (float) 
standards: A list of all standards that the chairs follows e.g. ["EN 16139-Level 1", "ANSI/BIFMA x5.4"]. If it does not follow any standards then leave it as an empty list (list[str])
material: A list of dictionaries of all matrials, where the key is the material name itself and the value is you estimating the percantage of how much the of the material the chair consists of in total of the given html (list[{material_name(str): percentage(int)}]) 

Return a list of json where for each json correspond to one html chair. 

"""

system_prompt = {
    "role": "system",
    "content": system_prompt_content
}

user_message = {
    "role": "user",
    "content":html_list
}

messages = [
    system_prompt,
    user_message
]

response = client.chat.completions.create(
    model="gpt-5",  
    messages=messages
)

raw_output = response.choices[0].message.content
data = json.loads(raw_output)
df = pd.DataFrame(data)

output_file = filename.replace(".html", ".csv")

df.to_csv(f"{output_path}/{output_file}", index=False, encoding="utf-8")
