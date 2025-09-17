import pandas as pd

material_df_path = "data/materials_ranking.csv"
material_df = pd.read_csv(material_df_path)


def process_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.apply(process_item, axis=1)
    return df


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
