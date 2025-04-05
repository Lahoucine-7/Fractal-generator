# renderer_cpu.py
import pygame
import numpy as np
from coloration import map_smooth_to_color_fixed

def display_fractal(screen, state, colormap_name="viridis", gamma=0.5):
    """
    Affiche la fractale à partir de l'état CPU.
    Normalise le tableau 'result' obtenu par NumPy, applique une correction gamma,
    puis utilise un colormap pour obtenir l'image finale en RGB affichée via Pygame.
    
    Paramètres :
      - screen : Surface Pygame où afficher l'image.
      - state : Instance de FractalStateCPU contenant 'result', 'max_iter', etc.
      - colormap_name : Nom du colormap à appliquer (défaut "viridis").
      - gamma : Valeur de correction gamma à appliquer (défaut 0.5).
    """
    # Normalisation de la fractale en fonction du nombre maximal d'itérations
    normalized = state.result / (state.max_iter + 1)
    normalized = np.clip(normalized, 0, 1)
    normalized = np.power(normalized, gamma)
    
    # Application du colormap pour obtenir une image RGB
    color_array = map_smooth_to_color_fixed(normalized, colormap_name)
    
    # Pygame attend une surface avec un tableau de forme (width, height, 3),
    # donc on transpose le tableau (qui est initialement de forme (hauteur, largeur, 3))
    surface = pygame.surfarray.make_surface(np.transpose(color_array, (1, 0, 2)))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
