# ui.py
import pygame

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 16)

# Options UI globales initiales
UI_OPTIONS = {
    "fractal_type": "Mandelbrot",
    "colormap": "plasma",
    "gamma": 0.5,
    "max_iter": 100,
    "custom_re": -0.7,       # Valeur par défaut pour Custom
    "custom_im": 0.27015,     # Valeur par défaut pour Custom
    "fixed_iter": False,      # Si True, le nombre d'itérations ne change pas avec le zoom
    "reset_zoom": False,      # Flag pour réinitialiser la vue
}

# Liste des palettes disponibles
PALETTE_LIST = ["viridis", "plasma", "magma", "cividis"]

# Boutons de sélection du type de fractale (en haut)
TOP_BUTTONS = [
    {"label": "Mandelbrot", "rect": pygame.Rect(10, 10, 100, 30)},
    {"label": "Julia", "rect": pygame.Rect(120, 10, 100, 30)},
    {"label": "Burning Ship", "rect": pygame.Rect(230, 10, 120, 30)},
    {"label": "Custom", "rect": pygame.Rect(360, 10, 100, 30)},
    {"label": "Tricorn", "rect": pygame.Rect(470, 10, 100, 30)},
    {"label": "Multibrot3", "rect": pygame.Rect(580, 10, 110, 30)},
    {"label": "Phoenix", "rect": pygame.Rect(700, 10, 100, 30)},
    {"label": "Perpendicular", "rect": pygame.Rect(810, 10, 120, 30)},
]

# Bouton pour reset zoom (en haut à droite)
RESET_BUTTON_RECT = pygame.Rect(950, 10, 100, 30)

# Case à cocher pour fixer le nombre d'itérations (au-dessous des boutons de fractale)
FIXED_ITER_CHECKBOX_RECT = pygame.Rect(10, 50, 20, 20)

# Curseur pour le nombre d'itérations (bas à gauche)
ITER_SLIDER_RECT = pygame.Rect(10, 560, 200, 20)

# Bouton pour changer de palette (bas à droite)
PALETTE_BUTTON_RECT = pygame.Rect(590, 560, 80, 30)

# Curseur pour gamma (bas à droite, en dessous du bouton de palette)
GAMMA_SLIDER_RECT = pygame.Rect(680, 565, 110, 10)

# Curseurs pour Custom (affichés seulement si le type est "Custom")
CUSTOM_RE_SLIDER_RECT = pygame.Rect(10, 80, 200, 20)
CUSTOM_IM_SLIDER_RECT = pygame.Rect(10, 110, 200, 20)

dragging_iter_slider = False
dragging_gamma_slider = False
dragging_custom_re_slider = False
dragging_custom_im_slider = False

def draw_ui(screen):
    """
    Dessine l'interface utilisateur par-dessus l'affichage de la fractale.
    """
    # Boutons de sélection du type de fractale
    for button in TOP_BUTTONS:
        rect = button["rect"]
        color = (0, 200, 0) if button["label"] == UI_OPTIONS["fractal_type"] else (200, 200, 200)
        pygame.draw.rect(screen, color, rect)
        text_surface = FONT.render(button["label"], True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    # Bouton Reset Zoom
    pygame.draw.rect(screen, (200, 100, 100), RESET_BUTTON_RECT)
    reset_text = FONT.render("Reset Zoom", True, (0, 0, 0))
    reset_text_rect = reset_text.get_rect(center=RESET_BUTTON_RECT.center)
    screen.blit(reset_text, reset_text_rect)
    
    # Case à cocher pour fixer le nombre d'itérations
    pygame.draw.rect(screen, (200, 200, 200), FIXED_ITER_CHECKBOX_RECT)
    if UI_OPTIONS["fixed_iter"]:
        pygame.draw.line(screen, (0,0,0), (FIXED_ITER_CHECKBOX_RECT.left, FIXED_ITER_CHECKBOX_RECT.top),
                         (FIXED_ITER_CHECKBOX_RECT.right, FIXED_ITER_CHECKBOX_RECT.bottom), 2)
        pygame.draw.line(screen, (0,0,0), (FIXED_ITER_CHECKBOX_RECT.left, FIXED_ITER_CHECKBOX_RECT.bottom),
                         (FIXED_ITER_CHECKBOX_RECT.right, FIXED_ITER_CHECKBOX_RECT.top), 2)
    fixed_text = FONT.render("Fixer itérations", True, (255, 255, 255))
    screen.blit(fixed_text, (FIXED_ITER_CHECKBOX_RECT.right + 5, FIXED_ITER_CHECKBOX_RECT.top))
    
    # Curseur pour le nombre d'itérations
    pygame.draw.rect(screen, (180, 180, 180), ITER_SLIDER_RECT)
    slider_pos = int((UI_OPTIONS["max_iter"] - 50) / (2000 - 50) * ITER_SLIDER_RECT.width) + ITER_SLIDER_RECT.x
    iter_handle_rect = pygame.Rect(slider_pos - 5, ITER_SLIDER_RECT.y - 5, 10, ITER_SLIDER_RECT.height + 10)
    pygame.draw.rect(screen, (100, 100, 250), iter_handle_rect)
    iter_text = FONT.render(f"Iter: {UI_OPTIONS['max_iter']}", True, (255, 255, 255))
    screen.blit(iter_text, (ITER_SLIDER_RECT.x, ITER_SLIDER_RECT.y - 20))
    
    # Bouton pour changer de palette
    pygame.draw.rect(screen, (180, 180, 180), PALETTE_BUTTON_RECT)
    palette_text = FONT.render(UI_OPTIONS["colormap"], True, (0, 0, 0))
    palette_text_rect = palette_text.get_rect(center=PALETTE_BUTTON_RECT.center)
    screen.blit(palette_text, palette_text_rect)
    
    # Curseur pour gamma
    pygame.draw.rect(screen, (180, 180, 180), GAMMA_SLIDER_RECT)
    gamma_range = 2.0 - 0.1
    gamma_pos = int((UI_OPTIONS["gamma"] - 0.1) / gamma_range * GAMMA_SLIDER_RECT.width) + GAMMA_SLIDER_RECT.x
    gamma_handle_rect = pygame.Rect(gamma_pos - 5, GAMMA_SLIDER_RECT.y - 5, 10, GAMMA_SLIDER_RECT.height + 10)
    pygame.draw.rect(screen, (100, 250, 100), gamma_handle_rect)
    gamma_text = FONT.render(f"Gamma: {UI_OPTIONS['gamma']:.2f}", True, (255, 255, 255))
    screen.blit(gamma_text, (GAMMA_SLIDER_RECT.x, GAMMA_SLIDER_RECT.y - 20))
    
    # Curseurs Custom (affichés uniquement en mode Custom)
    if UI_OPTIONS["fractal_type"] == "Custom":
        pygame.draw.rect(screen, (180, 180, 180), CUSTOM_RE_SLIDER_RECT)
        re_pos = int((UI_OPTIONS["custom_re"] + 2.0) / 4.0 * CUSTOM_RE_SLIDER_RECT.width) + CUSTOM_RE_SLIDER_RECT.x
        custom_re_handle = pygame.Rect(re_pos - 5, CUSTOM_RE_SLIDER_RECT.y - 5, 10, CUSTOM_RE_SLIDER_RECT.height + 10)
        pygame.draw.rect(screen, (250, 100, 100), custom_re_handle)
        re_text = FONT.render(f"Re: {UI_OPTIONS['custom_re']:.2f}", True, (255, 255, 255))
        screen.blit(re_text, (CUSTOM_RE_SLIDER_RECT.x, CUSTOM_RE_SLIDER_RECT.y - 20))
        
        pygame.draw.rect(screen, (180, 180, 180), CUSTOM_IM_SLIDER_RECT)
        im_pos = int((UI_OPTIONS["custom_im"] + 2.0) / 4.0 * CUSTOM_IM_SLIDER_RECT.width) + CUSTOM_IM_SLIDER_RECT.x
        custom_im_handle = pygame.Rect(im_pos - 5, CUSTOM_IM_SLIDER_RECT.y - 5, 10, CUSTOM_IM_SLIDER_RECT.height + 10)
        pygame.draw.rect(screen, (250, 100, 100), custom_im_handle)
        im_text = FONT.render(f"Im: {UI_OPTIONS['custom_im']:.2f}", True, (255, 255, 255))
        screen.blit(im_text, (CUSTOM_IM_SLIDER_RECT.x, CUSTOM_IM_SLIDER_RECT.y - 20))

def handle_ui_event(event, state):
    """
    Gère les événements liés à l'UI et retourne True si l'affichage doit être rafraîchi.
    """
    global dragging_iter_slider, dragging_gamma_slider, dragging_custom_re_slider, dragging_custom_im_slider
    updated = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        # Boutons de type fractale
        for button in TOP_BUTTONS:
            if button["rect"].collidepoint(pos):
                if UI_OPTIONS["fractal_type"] != button["label"]:
                    UI_OPTIONS["fractal_type"] = button["label"]
                    state.fractal_type = button["label"]
                    state.full_recompute()
                    updated = True
                break
        # Bouton Reset Zoom
        if RESET_BUTTON_RECT.collidepoint(pos):
            UI_OPTIONS["reset_zoom"] = True
            updated = True
        # Bouton de palette
        if PALETTE_BUTTON_RECT.collidepoint(pos):
            current_index = PALETTE_LIST.index(UI_OPTIONS["colormap"])
            new_index = (current_index + 1) % len(PALETTE_LIST)
            UI_OPTIONS["colormap"] = PALETTE_LIST[new_index]
            updated = True
        # Case à cocher fixed_iter
        if FIXED_ITER_CHECKBOX_RECT.collidepoint(pos):
            UI_OPTIONS["fixed_iter"] = not UI_OPTIONS["fixed_iter"]
            updated = True

        # Curseur itérations (si la case n'est pas fixée)
        if not UI_OPTIONS["fixed_iter"] and ITER_SLIDER_RECT.collidepoint(pos):
            dragging_iter_slider = True
            relative_x = pos[0] - ITER_SLIDER_RECT.x
            new_iter = int(relative_x / ITER_SLIDER_RECT.width * (2000 - 50)) + 50
            UI_OPTIONS["max_iter"] = new_iter
            state.update_zoom(state.re_start, state.re_end, state.im_start, state.im_end, new_iter)
            updated = True

        # Curseur gamma
        if GAMMA_SLIDER_RECT.collidepoint(pos):
            dragging_gamma_slider = True
            relative_x = pos[0] - GAMMA_SLIDER_RECT.x
            new_gamma = relative_x / GAMMA_SLIDER_RECT.width * (2.0 - 0.1) + 0.1
            UI_OPTIONS["gamma"] = round(new_gamma, 2)
            updated = True

        # Curseurs Custom si en mode Custom
        if UI_OPTIONS["fractal_type"] == "Custom":
            if CUSTOM_RE_SLIDER_RECT.collidepoint(pos):
                dragging_custom_re_slider = True
                relative_x = pos[0] - CUSTOM_RE_SLIDER_RECT.x
                new_custom_re = (relative_x / CUSTOM_RE_SLIDER_RECT.width) * 4.0 - 2.0
                UI_OPTIONS["custom_re"] = round(new_custom_re, 2)
                state.full_recompute()
                updated = True
            if CUSTOM_IM_SLIDER_RECT.collidepoint(pos):
                dragging_custom_im_slider = True
                relative_x = pos[0] - CUSTOM_IM_SLIDER_RECT.x
                new_custom_im = (relative_x / CUSTOM_IM_SLIDER_RECT.width) * 4.0 - 2.0
                UI_OPTIONS["custom_im"] = round(new_custom_im, 2)
                state.full_recompute()
                updated = True

    elif event.type == pygame.MOUSEBUTTONUP:
        dragging_iter_slider = dragging_gamma_slider = dragging_custom_re_slider = dragging_custom_im_slider = False

    elif event.type == pygame.MOUSEMOTION:
        if dragging_iter_slider and not UI_OPTIONS["fixed_iter"]:
            pos = event.pos
            relative_x = pos[0] - ITER_SLIDER_RECT.x
            new_iter = int(relative_x / ITER_SLIDER_RECT.width * (2000 - 50)) + 50
            UI_OPTIONS["max_iter"] = new_iter
            state.update_zoom(state.re_start, state.re_end, state.im_start, state.im_end, new_iter)
            updated = True
        if dragging_gamma_slider:
            pos = event.pos
            relative_x = pos[0] - GAMMA_SLIDER_RECT.x
            new_gamma = relative_x / GAMMA_SLIDER_RECT.width * (2.0 - 0.1) + 0.1
            UI_OPTIONS["gamma"] = round(new_gamma, 2)
            updated = True
        if dragging_custom_re_slider and UI_OPTIONS["fractal_type"] == "Custom":
            pos = event.pos
            relative_x = pos[0] - CUSTOM_RE_SLIDER_RECT.x
            new_custom_re = (relative_x / CUSTOM_RE_SLIDER_RECT.width) * 4.0 - 2.0
            UI_OPTIONS["custom_re"] = round(new_custom_re, 2)
            state.full_recompute()
            updated = True
        if dragging_custom_im_slider and UI_OPTIONS["fractal_type"] == "Custom":
            pos = event.pos
            relative_x = pos[0] - CUSTOM_IM_SLIDER_RECT.x
            new_custom_im = (relative_x / CUSTOM_IM_SLIDER_RECT.width) * 4.0 - 2.0
            UI_OPTIONS["custom_im"] = round(new_custom_im, 2)
            state.full_recompute()
            updated = True

    return updated
