import hashlib
import os
from PIL import Image


def analyze_skin(image_path):
    """Mock AI skin analysis engine.

    Uses image properties to generate consistent, realistic-looking results.
    Designed to be replaced with a real ML model (TensorFlow/PyTorch) later.
    """
    conditions = [
        {'name': 'Acne', 'weight': 0},
        {'name': 'Dryness', 'weight': 0},
        {'name': 'Oiliness', 'weight': 0},
        {'name': 'Hyperpigmentation', 'weight': 0},
        {'name': 'Normal', 'weight': 0},
    ]

    try:
        img = Image.open(image_path)
        width, height = img.size
        img_rgb = img.convert('RGB')

        # Sample pixels to derive mock analysis
        pixels = []
        step = max(width, height) // 10
        for x in range(0, width, max(step, 1)):
            for y in range(0, height, max(step, 1)):
                pixels.append(img_rgb.getpixel((x, y)))

        avg_r = sum(p[0] for p in pixels) / len(pixels)
        avg_g = sum(p[1] for p in pixels) / len(pixels)
        avg_b = sum(p[2] for p in pixels) / len(pixels)

        # Use filename hash for consistent results per image
        file_hash = hashlib.md5(os.path.basename(image_path).encode()).hexdigest()
        seed_val = int(file_hash[:8], 16)

        # Generate condition weights based on image properties
        if avg_r > 160 and avg_g < 140:
            conditions[0]['weight'] = 75 + (seed_val % 25)  # Acne
        elif avg_b > avg_r and avg_b > avg_g:
            conditions[1]['weight'] = 65 + (seed_val % 30)  # Dryness
        elif avg_g > avg_r:
            conditions[2]['weight'] = 70 + (seed_val % 25)  # Oiliness
        elif avg_r > 170 and avg_g > 150:
            conditions[3]['weight'] = 60 + (seed_val % 35)  # Hyperpigmentation
        else:
            conditions[4]['weight'] = 80 + (seed_val % 20)  # Normal

        # Ensure at least one condition has a weight
        if all(c['weight'] == 0 for c in conditions):
            conditions[seed_val % len(conditions)]['weight'] = 70 + (seed_val % 30)

    except Exception:
        # Fallback if image can't be processed
        conditions[0]['weight'] = 85

    # Sort by weight descending
    conditions.sort(key=lambda c: c['weight'], reverse=True)
    top_condition = conditions[0]

    return {
        'condition': top_condition['name'],
        'confidence': min(top_condition['weight'], 100),
        'all_conditions': [
            {'name': c['name'], 'confidence': min(c['weight'], 100)}
            for c in conditions if c['weight'] > 0
        ]
    }
