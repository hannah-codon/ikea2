import ast
import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

material_df_path = "/mnt/data/projects/hackathons/mega-trend/data/materials.csv"
material_df = pd.read_csv(material_df_path)


def process_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.apply(process_item, axis=1)
    df = calc_rel_score(df)
    df["gen_description"] = df.apply(gen_description, axis=1)
    return df


def calc_rel_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rel_score"] = 0
    df.loc[df["score"] <= 395, "rel_score"] = 0
    df.loc[(df["score"] > 395) & (df["score"] <= 905), "rel_score"] = 1
    df.loc[df["score"] > 905, "rel_score"] = 2
    return df


def gen_description(item: pd.Series) -> str:

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
    )
    system_prompt_content = """Given this description of a furniture item, give me a short description of it (1 short sentence.), 
    describing its sustainability. The item is scored either 0, 1 or 2, where 0 is the best and 2 is the worst. You will also get some sustainability attributes such as materials, weight and standards, which you should use in your description. You should not be too technical, but rather user friendly."""
    user_prompt = f"""
       Description: 

       score: {item['rel_score']}
         Materials: {item['material']}
            Weight: {item['weight']}
            Standards: {item['standards']}
         Score calculation: {item['calculation_string']}"""
    system_prompt = {"role": "system", "content": system_prompt_content}

    user_message = {"role": "user", "content": user_prompt}

    messages = [system_prompt, user_message]

    response = client.chat.completions.create(model="gpt-5", messages=messages)
    return response.choices[0].message.content


def process_item(item: pd.Series) -> pd.Series:
    item["score"], item["calculation_string"] = score_item(item)
    return item


def score_item(item: pd.Series) -> tuple[float, str]:
    material_score = calc_material_score(item["material"], item["weight"])
    durability_score = (
        material_score / len(item["standards"]) if len(item["standards"]) > 0 else 0.5
    )
    weight_score = item["weight"]
    final_score = (material_score + durability_score + weight_score) / 3
    calculation_string = f"""Item final score: {final_score}. Materials and distribution in this item: {item['material']}. Standards: {item['standards']}. Weight: {item['weight']}. Material score: {material_score}. Durability score: {durability_score}. Weight score: {weight_score}. Material score is caluclated by multiplying material score with proportion of material in item and item weight. Durability score is material score divided by durability. Final score is average of material score, durability score and weight score."""
    return final_score, calculation_string


def calc_material_score(materials: str, item_weight: float) -> float:
    total_score = 0.0
    materials_list = ast.literal_eval(materials)
    for material in materials_list:
        for material, proportion in material.items():
            material_score = get_material_score(material)
            total_score += material_score * (proportion * item_weight)
    return total_score


def get_material_score(material: str) -> float:
    material_row = material_df[material_df["material"] == material]
    if material_row.empty:
        return 0.0
    return material_row["score"].values[0]
