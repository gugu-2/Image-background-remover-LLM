import cv2
import numpy as np
from PIL import Image

def guided_filter(I, p, r, eps):
    """
    Guided filter for edge-preserving alpha mask refinement.
    I: guidance image (grayscale/color normalized [0, 1])
    p: filtering input (mask normalized [0, 1])
    r: radius
    eps: regularization parameter
    """
    h, w = p.shape
    N = cv2.boxFilter(np.ones((h, w), np.float32), -1, (r, r))
    
    mean_I = cv2.boxFilter(I, -1, (r, r)) / N
    mean_p = cv2.boxFilter(p, -1, (r, r)) / N
    mean_Ip = cv2.boxFilter(I * p, -1, (r, r)) / N
    cov_Ip = mean_Ip - mean_I * mean_p
    
    mean_II = cv2.boxFilter(I * I, -1, (r, r)) / N
    var_I = mean_II - mean_I * mean_I
    
    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I
    
    mean_a = cv2.boxFilter(a, -1, (r, r)) / N
    mean_b = cv2.boxFilter(b, -1, (r, r)) / N
    
    q = mean_a * I + mean_b
    return q

def refine_alpha_matting(image_bgr: np.ndarray, raw_mask: np.ndarray) -> np.ndarray:
    """
    Refines raw binary/probabilistic mask using Guided Filter to preserve fine details
    like mountain ridges, tree leaves, and grass blades.
    """
    # Normalize image and mask to [0, 1]
    gray_I = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    p = (raw_mask.astype(np.float32) / 255.0)
    
    # Apply guided filter
    r = 8
    eps = 1e-3
    refined_mask = guided_filter(gray_I, p, r, eps)
    
    # Clip and scale back to uint8 [0, 255]
    refined_mask = np.clip(refined_mask * 255.0, 0, 255).astype(np.uint8)
    return refined_mask
