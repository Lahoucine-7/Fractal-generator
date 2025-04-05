# coloration.py
import numpy as np
import matplotlib.pyplot as plt

def map_smooth_to_color_fixed(normalized_array, colormap_name="viridis"):
    """
    Applique un colormap à un tableau 2D de valeurs normalisées (dans [0,1]).
    On suppose que 0 correspond à du noir.
    
    Retourne un tableau 3D (hauteur, largeur, 3) en uint8.
    """
    cmap = plt.get_cmap(colormap_name)
    colored = cmap(normalized_array)  # Tableau de forme (H, W, 4) avec des valeurs dans [0,1]
    image_rgb = (colored[:, :, :3] * 255).astype(np.uint8)
    return image_rgb
