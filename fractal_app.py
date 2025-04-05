# fractal_app.py
import pygame
import sys
from ui import draw_ui, handle_ui_event, UI_OPTIONS

try:
    from fractal_state_gpu import FractalStateGPU
    from renderer_incremental import display_fractal
    use_gpu = True
except ImportError:
    try:
        from fractal_state_cpu import FractalStateCPU
        from renderer_cpu import display_fractal as display_fractal
        use_gpu = False
    except ImportError:
        print("Aucune implémentation de fractale (GPU ou CPU) n'est disponible.")
        sys.exit(1)

# Configuration de base
WIDTH = 1100
HEIGHT = 600
INIT_MAX_ITER = 100
INIT_RE_START = -2.5
INIT_RE_END   = 1.5
INIT_IM_START = -1.2
INIT_IM_END   = 1.2
CONTINUOUS_ZOOM_FACTOR = 0.95

def run_app():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mandelbrot Interactive")
    clock = pygame.time.Clock()

    # Création de l'état initial de la fractale
    if use_gpu:
        state = FractalStateGPU(WIDTH, HEIGHT, INIT_MAX_ITER, INIT_RE_START, INIT_RE_END, INIT_IM_START, INIT_IM_END)
    else:
        state = FractalStateCPU(WIDTH, HEIGHT, INIT_MAX_ITER, INIT_RE_START, INIT_RE_END, INIT_IM_START, INIT_IM_END)

    display_fractal(screen, state, colormap_name=UI_OPTIONS["colormap"], gamma=UI_OPTIONS["gamma"])

    dragging = False
    continuous_zoom = False
    view_updated = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
            if handle_ui_event(event, state):
                view_updated = True

            # Gestion du zoom avec la molette
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom_factor = 0.9
                    new_max_iter = min(2000, int(state.max_iter+1)) if not UI_OPTIONS["fixed_iter"] else state.max_iter
                else:
                    zoom_factor = 1.1
                    new_max_iter = max(50, int(state.max_iter-1)) if not UI_OPTIONS["fixed_iter"] else state.max_iter
                center_re = (state.re_start + state.re_end) / 2
                center_im = (state.im_start + state.im_end) / 2
                width_range = (state.re_end - state.re_start) * zoom_factor
                height_range = (state.im_end - state.im_start) * zoom_factor
                new_re_start = center_re - width_range / 2
                new_re_end = center_re + width_range / 2
                new_im_start = center_im - height_range / 2
                new_im_end = center_im + height_range / 2
                state.update_zoom(new_re_start, new_re_end, new_im_start, new_im_end, new_max_iter)
                view_updated = True

            # Activation du déplacement et du zoom continu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                elif event.button == 3:
                    continuous_zoom = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                elif event.button == 3:
                    continuous_zoom = False

            if event.type == pygame.MOUSEMOTION and dragging:
                dx, dy = event.rel
                state.apply_translation(dx, dy)
                view_updated = True

        # Zoom continu
        if continuous_zoom:
            # Récupérer l'image actuelle
            current_surface = screen.copy()
            center_re = (state.re_start + state.re_end) / 2
            center_im = (state.im_start + state.im_end) / 2
            width_range = (state.re_end - state.re_start) * CONTINUOUS_ZOOM_FACTOR
            height_range = (state.im_end - state.im_start) * CONTINUOUS_ZOOM_FACTOR
            new_max_iter = min(2000, int(state.max_iter+1)) if not UI_OPTIONS["fixed_iter"] else state.max_iter
            new_re_start = center_re - width_range / 2
            new_re_end = center_re + width_range / 2
            new_im_start = center_im - height_range / 2
            new_im_end = center_im + height_range / 2
            state.update_zoom(new_re_start, new_re_end, new_im_start, new_im_end, new_max_iter)
            # Utiliser smoothscale pour interpoler entre l'image précédente et la nouvelle fractale
            interpolated = pygame.transform.smoothscale(current_surface, (WIDTH, HEIGHT))
            screen.blit(interpolated, (0, 0))
            view_updated = True

        # Si le bouton Reset Zoom a été cliqué, réinitialiser la vue
        if UI_OPTIONS.get("reset_zoom", False):
            state.reset_view()
            UI_OPTIONS["reset_zoom"] = False
            view_updated = True

        # Mettre à jour le nombre d'itérations affiché avec la valeur actuelle de state
        UI_OPTIONS["max_iter"] = state.max_iter

        if view_updated:
            display_fractal(screen, state, colormap_name=UI_OPTIONS["colormap"], gamma=UI_OPTIONS["gamma"])
            view_updated = False

        draw_ui(screen)
        pygame.display.update()
        clock.tick(60)

def run():
    run_app()

if __name__ == "__main__":
    run()
