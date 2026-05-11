from collections import Counter
from pathlib import Path
from typing import Dict, List

import numpy as np
from PIL import Image


FASHION_KEYWORDS = [
    'jeans', 'tshirt', 'shirt', 'jacket', 'dress', 'sneakers', 'shoes', 'hoodie', 'watch', 'bag',
]


def analyze_image(image_path: str) -> Dict[str, object]:
    img = Image.open(image_path).convert('RGB')
    # Resize for faster processing
    small = img.resize((128, 128))
    arr = np.array(small)
    # Get dominant colors via simple kmeans-like binning
    pixels = arr.reshape(-1, 3)
    # Quantize to 16 levels per channel
    quantized = (pixels // 32) * 32
    colors, counts = np.unique(quantized, axis=0, return_counts=True)
    top_indices = np.argsort(-counts)[:5]
    top_colors = [colors[i].tolist() for i in top_indices]

    # Convert to human-readable color names (rough mapping)
    def rgb_to_name(rgb):
        r, g, b = rgb
        if r < 60 and g < 60 and b < 60:
            return 'black'
        if r > 200 and g > 200 and b > 200:
            return 'white'
        # Maroon detection (dark red)
        if r > 100 and r < 150 and g < 60 and b < 60:
            return 'maroon'
        # Cream/beige detection (light yellow-tan)
        if r > 180 and g > 180 and b > 140 and r < 220 and g < 220:
            return 'beige'
        if b > r and b > g:
            return 'blue'
        if r > g and r > b:
            return 'red'
        if g > r and g > b:
            return 'green'
        return 'beige'

    color_names = list(dict.fromkeys([rgb_to_name(c) for c in top_colors]))[:3]

    # Very lightweight clothing item guess based on aspect ratio and color blocks
    height, width = arr.shape[:2]
    top_half = arr[: height // 2, :, :]
    bottom_half = arr[height // 2 :, :, :]
    def dominant_name(a):
        px = a.reshape(-1, 3)
        q = (px // 32) * 32
        cs, cnt = np.unique(q, axis=0, return_counts=True)
        idx = np.argmax(cnt)
        return rgb_to_name(cs[idx])

    top_color = dominant_name(top_half)
    bottom_color = dominant_name(bottom_half)

    guessed_items: List[str] = ['top', 'bottom']

    synthesized_text = (
        f"top color {top_color} bottom color {bottom_color} "
        f"overall palette {' '.join(color_names)} minimal pattern"
    )

    return {
        'colors': color_names,
        'items': guessed_items,
        'top_color': top_color,
        'bottom_color': bottom_color,
        'synthesized_text': synthesized_text,
    }



