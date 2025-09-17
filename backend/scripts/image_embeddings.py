import torch
from transformers import AutoImageProcessor, AutoModel
from transformers.image_utils import load_image
import csv
from typing import List, Dict
import db.crud as crud

def process_images_from_csv(csv_path: str, url_column: str = 'url') -> List[Dict]:
    """
    Read CSV with image URLs and return CLS tokens for each image.
    
    Args:
        csv_path: Path to CSV file
        url_column: Name of column containing image URLs
    
    Returns:
        List of dictionaries with original row data + cls_token
    """
    processor = AutoImageProcessor.from_pretrained("facebook/dinov3-vits16-pretrain-lvd1689m")
    model = AutoModel.from_pretrained("facebook/dinov3-vits16-pretrain-lvd1689m")
    
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    results = []
    
    for i, row in enumerate(rows):
        try:
            image_url = row[url_column]
            print(f"Processing image {i+1}/{len(rows)}: {image_url}")
            
            image = load_image(image_url)
            inputs = processor(images=image, return_tensors="pt")
            
            with torch.inference_mode():
                outputs = model(**inputs)
            last_hidden_states = outputs.last_hidden_state
            cls_token = last_hidden_states[:, 0, :].squeeze().numpy()
            
            result = row.copy()
            result['cls_token'] = cls_token
            results.append(result)
            
        except Exception as e:
            print(f"Error processing image {i+1}: {e}")
    
    return results

if __name__ == "__main__":
    csv_file = "/mnt/data/projects/hackathons/mega-trend/data/extra.csv" 
    results = process_images_from_csv(csv_file, url_column='image_url')
    for i, result in enumerate(results):
        if result['cls_token'] is not None:
            if crud.get_item(result['article_number']) is not None:
                print(f"Item {result['article_number']} already exists")
                continue
            else:
                crud.write_item(result['article_number'], result['cls_token'])
            print(f"Image {i+1}: CLS token shape {result['cls_token'].shape}")
        else:
            print(f"Image {i+1}: Failed to process")
