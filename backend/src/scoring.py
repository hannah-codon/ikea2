import os

import pandas as pd
from openai import OpenAI

material_df_path = "data/materials_ranking.csv"
material_df = pd.read_csv(material_df_path)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)


def process_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.apply(process_item, axis=1)
    df = calc_rel_score(df)
    return df


def calc_rel_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    num_items = len(df)
    items_in_split = int(num_items / 3)
    sorted = df.sort_values(by="score", ascending=False).reset_index(drop=True)
    sorted["rel_score"] = 0
    sorted.loc[: items_in_split - 1, "rel_score"] = 1
    sorted.loc[items_in_split : num_items - 1, "rel_score"] = 2
    return sorted


def gen_description(item: pd.Series) -> str:
    system_prompt = """Given this description of a furniture item, give me a short description of it (2-3 sentences), 
    describing its sustainability. The item is scored either 0, 1 or 2, where 0 is the best and 2 is the worst. You will also get some sustainability attributes such as materials, weight and standards, which you should use in your description."""
    user_prompt = f"""
       Description: 

       score: {item['rel_score']}
         Materials: {item['Materials']}
            Weight: {item['weight']}
            Standards: {item['standards']}
         Score calculation: {item['calculation_string']}"""


def process_item(item: pd.Series) -> pd.Series:
    item["score"], item["calculation_string"] = score_item(item)
    return item


def score_item(item: pd.Series) -> tuple[float, str]:
    material_score = calc_material_score(item["Materials"], item["weight"])
    durability_score = material_score / item["durability"]
    weight_score = item["weight"]
    final_score = (material_score + durability_score + weight_score) / 3
    calculation_string = f"""Item final score: {final_score}. Materials and distribution in this item: {item['Materials']}. Durability: {item['durability']}. Weight: {item['weight']}. Material score: {material_score}. Durability score: {durability_score}. Weight score: {weight_score}. Material score is caluclated by multiplying material score with proportion of material in item and item weight. Durability score is material score divided by durability. Final score is average of material score, durability score and weight score."""
    return final_score, calculation_string


def calc_material_score(materials: dict, item_weight: float) -> float:
    total_score = 0.0
    for material, proportion in materials.items():
        material_score = get_material_score(material)
        total_score += material_score * (proportion * item_weight)
    return total_score


def get_material_score(material: str) -> float:
    material_row = material_df[material_df["Material"] == material]
    if material_row.empty:
        return 0.0
    return material_row["score"].values[0]
