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
output_path = "/mnt/data/projects/hackathons/mega-trend/data/"

system_prompt_content = """ 
Take the given html of an IKEA chair and create a table 
in json format for each chair with following keys: 

    id:the article number of the given html (int) 
    article_number: the article number of the given html (int) 
    image_url: the image url of the given html (string) 
    category: the category of the given html (string) 
    description: the description of the given html (string) 
    price: the price of the given html (float) 
    weight: the weight of the given html (float) 
    standards:  A list of all standards that the chairs follows 
                e.g. ["EN 16139-Level 1", "ANSI/BIFMA x5.4"]. 
                If it does not follow any standards then leave it 
                as an empty list (list[str])
    material:   First fit all the materials of given HTML to the 
                closest material_category of the list: 
                [Steel, Wood (Solid), Engineered Wood (Composite/Veneer), Recycled Polyester, New Polyester & Polyester Blends, Plastics (Polypropylene), Plastics (Polyethylene), Plastics (Mixed/Other), Polyurethane Foam, Natural Fibers (Cotton), Natural Fibers (Leather), Natural Fibers (Other), Paper, Paints & Stains (Acrylic), Clear Finishes (Lacquer), Epoxy & Powder Coatings, Chemicals & Adhesives, Rubber & Synthetic Rubber, Mixed Materials, Polymer Blends (Other)]
                If it does match to any material_category, discard the material. 
                After that create list of dictionaries of all material_categories, where the key is 
                the material_category itself and the value is you estimating the 
                percantage of how much the of the material_category the chair 
                consists of in total of the given html 
                (list[{material_category(str): percentage(float)}]). 

"""

system_prompt = {
    "role": "system",
    "content": system_prompt_content
}

json_list = []
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
    json_list.append(data[0])

df = pd.DataFrame(json_list)