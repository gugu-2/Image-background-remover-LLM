import os
import cv2
import numpy as np
from rembg import remove, new_session
from bg_remover.sky import remove_sky
from bg_remover.matting import refine_alpha_matting

def remove_background_bytes(input_data: bytes, model_name: str = "birefnet-general") -> bytes:
    """
    Removes the background from image bytes using a specified SOTA model.
    Supported models:
      - 'birefnet-general' (SOTA BiRefNet - Best for General & High Res)
      - 'birefnet-hrs' (High-Resolution Segmentation)
      - 'birefnet-portrait' (SOTA Portrait)
      - 'sky-remover' (Custom Sky/Landscape Filter)
      - 'u2net' (Legacy)
      - 'isnet-general-use' (Legacy)
    """
    if model_name == "sky-remover":
        return remove_sky(input_data)
        
    session = new_session(model_name)
    # Enable post_process_mask for smooth alpha boundaries
    output_bytes = remove(input_data, session=session, post_process_mask=True)
    return output_bytes

def process_file(input_path: str, output_path: str, model_name: str = "birefnet-general"):
    """Removes background from a single file and saves it."""
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove_background_bytes(input_data, model_name=model_name)
            with open(output_path, 'wb') as o:
                o.write(output_data)
        print(f"Saved to {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_folder(input_folder: str, output_folder: str, model_name: str = "birefnet-general"):
    """Processes all images in a folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    images_processed = False
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            images_processed = True
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '_nobg.png'
            output_path = os.path.join(output_folder, output_filename)
            
            print(f"Processing {filename} with model '{model_name}'...")
            if os.path.exists(output_path):
                print(f"Skipping {filename}: {output_filename} already exists.")
            else:
                process_file(input_path, output_path, model_name=model_name)
            
    if not images_processed:
        print(f"No images found in '{input_folder}'.")
