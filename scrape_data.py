from openai import OpenAI
import pandas as pd
import json
import os 

system_prompt_content = """ 
Take the given html of an IKEA chair and create a table in json format with following keys: 
id: a unique ID created by you (int) 
article_number: the article number of the given html (int) 
image_url: the image url of the given html (string) 
category: the category of the given html (string) 
description: the description of the given html (string) 
price: the price of the given html (float) 
weight: the weight of the given html (float) 
material: a list of dictionaries of all matrials, where the key is the material name itself and the value is you estimating the percantage of how much the of the material the chair consists of in total of the given html (list[{material_name(str): percentage(int)}]) """


system_prompt = {
    "role": "system",
    "content": system_prompt_content
}

input_path = "/mnt/data/projects/hackathons/mega-trend/data/html_dumps/"  
output_path = "/mnt/data/projects/hackathons/mega-trend/data/ikea_csv"

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

for filename in os.listdir(input_path):
    with open(f"{input_path}/{filename}", "r", encoding="utf-8") as f:
        html_content = f.read()

    user_message = {
        "role": "user",
        "content":html_content
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
