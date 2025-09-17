import os
import pandas as pd

input_dir = "/mnt/data/projects/hackathons/mega-trend/data/ikea_csv"

# Load all csvs in ths directory to one big csv
all_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
df_list = [pd.read_csv(os.path.join(input_dir, f)) for f in all_files]
df = pd.concat(df_list, ignore_index=True)

print(df.columns)
print("DF SIZE", df.shape)

materials_and_count = {}

def extract_materials(x):
    if isinstance(x, str):
        try:
            val = eval(x)
            if isinstance(val, dict):
                return list(val.keys())
            elif isinstance(val, list):
                return val
        except Exception:
            return [x]
    elif isinstance(x, list):
        return x
    return []

for entry in df['material'].dropna().values:
    for material in extract_materials(entry):
        # If material is a dict, use its keys
        if isinstance(material, dict):
            for key in material.keys():
                key_clean = str(key).strip().lower()
                if key_clean in materials_and_count:
                    materials_and_count[key_clean] += 1
                else:
                    materials_and_count[key_clean] = 1
        else:
            material_clean = str(material).strip().lower()
            if material_clean in materials_and_count:
                materials_and_count[material_clean] += 1
            else:
                materials_and_count[material_clean] = 1

print(materials_and_count)