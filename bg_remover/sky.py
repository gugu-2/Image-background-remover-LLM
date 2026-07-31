import cv2
import numpy as np
from PIL import Image

def remove_sky(input_data: bytes) -> bytes:
    """
    Removes sky from landscape images preserving 100% of mountains, trees, and ground.
    Accepts image bytes and returns PNG bytes with transparent sky.
    """
    # Convert bytes to cv2 image
    nparr = np.frombuffer(input_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image bytes.")
        
    h, w, c = img.shape
    
    # Convert to HSV color space for accurate sky detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # FloodFill mask initialized (2 pixels wider/higher than image for cv2.floodFill)
    mask = np.zeros((h + 2, w + 2), np.uint8)
    
    # Seeds along the top edge
    num_seeds = 40
    seed_points = [(int(x), 0) for x in np.linspace(0, w - 1, num_seeds)]
    
    # Perform flood fill from top edge seeds
    fill_img = img.copy()
    lo_diff = (25, 30, 40)
    up_diff = (25, 30, 40)
    
    for seed in seed_points:
        cv2.floodFill(fill_img, mask, seed, (0, 0, 0), lo_diff, up_diff, cv2.FLOODFILL_FIXED_RANGE)
        
    # Extracted sky mask (1 where filled, 0 elsewhere)
    sky_mask = (mask[1:-1, 1:-1] == 1).astype(np.uint8) * 255
    
    # Include bright / low-saturation top areas (white clouds / bright sky)
    bright_sky = ((hsv[:, :, 2] > 190) & (hsv[:, :, 1] < 70)).astype(np.uint8) * 255
    
    top_half_mask = np.zeros((h, w), np.uint8)
    top_half_mask[0:int(h * 0.65), :] = 255
    
    combined_sky = cv2.bitwise_or(sky_mask, cv2.bitwise_and(bright_sky, top_half_mask))
    
    # Morphological cleaning (smoothing edges, closing holes)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    combined_sky = cv2.morphologyEx(combined_sky, cv2.MORPH_CLOSE, kernel)
    combined_sky = cv2.GaussianBlur(combined_sky, (5, 5), 0)
    
    # Invert to get foreground mask (255 = keep mountain/ground, 0 = transparent sky)
    fg_mask = cv2.bitwise_not(combined_sky)
    
    # Convert BGR image to BGRA (RGBA)
    b, g, r = cv2.split(img)
    rgba = cv2.merge([r, g, b, fg_mask])
    
    # Encode as PNG bytes
    success, encoded_img = cv2.imencode('.png', rgba)
    if not success:
        raise ValueError("Failed to encode image to PNG.")
        
    return encoded_img.tobytes()

def process_sky_file(input_path: str, output_path: str):
    """Processes a single file to remove sky."""
    with open(input_path, 'rb') as i:
        input_data = i.read()
    output_data = remove_sky(input_data)
    with open(output_path, 'wb') as o:
        o.write(output_data)
    print(f"Saved sky-removed image to {output_path}")
