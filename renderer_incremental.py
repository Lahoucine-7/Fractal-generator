# renderer_incremental.py
import pygame
import cupy as cp
import numpy as np
from coloration import map_smooth_to_color_fixed

def display_fractal(screen, state, colormap_name="viridis", gamma=0.5):
    """
    Affiche la fractale à partir de l'état GPU.
    Convertit le tableau 'result' du GPU en CPU, normalise, applique une correction gamma,
    puis applique le colormap pour obtenir une image RGB affichée via Pygame.
    """
    result_cpu = cp.asnumpy(state.result)
    normalized = result_cpu / (state.max_iter + 1)
    normalized = np.clip(normalized, 0, 1)
    normalized = np.power(normalized, gamma)
    color_array = map_smooth_to_color_fixed(normalized, colormap_name)
    # Pygame attend un tableau de forme (width, height, 3); on transpose car nos tableaux sont (hauteur, largeur, 3)
    surface = pygame.surfarray.make_surface(np.transpose(color_array, (1, 0, 2)))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
