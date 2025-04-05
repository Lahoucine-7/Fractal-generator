# fractal_state_cpu.py
import numpy as np

class FractalStateCPU:
    """
    Cette classe gère l'état du calcul de la fractale Mandelbrot sur le CPU à l'aide de NumPy.
    Elle calcule la grille complexe correspondant au domaine d'affichage et réalise le calcul
    de la fractale de manière complète ou incrémentale pour ajouter des itérations.
    Elle permet également de traduire (déplacer) la vue.
    """
    
    def __init__(self, width, height, max_iter, re_start, re_end, im_start, im_end):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.re_start = re_start
        self.re_end = re_end
        self.im_start = im_start
        self.im_end = im_end
        self.compute_grid()
        self.full_recompute()
    
    def compute_grid(self):
        """
        Crée la grille de nombres complexes correspondant au domaine courant, sur le CPU.
        """
        re = np.linspace(self.re_start, self.re_end, self.width)
        im = np.linspace(self.im_start, self.im_end, self.height)
        self.c = re[np.newaxis, :] + 1j * im[:, np.newaxis]
    
    def full_recompute(self):
        """
        Recalcule entièrement la fractale pour le domaine courant et le nombre d'itérations défini.
        Initialise les tableaux 'z' (pour le calcul de z = z^2 + c),
        'result' (pour stocker la valeur smooth finale de chaque pixel) et 'mask' (pour suivre les pixels actifs).
        """
        self.z = np.zeros((self.height, self.width), dtype=np.complex128)
        self.result = np.full((self.height, self.width), self.max_iter, dtype=np.float64)
        self.mask = np.ones((self.height, self.width), dtype=bool)
        for i in range(self.max_iter):
            self.z[self.mask] = self.z[self.mask]**2 + self.c[self.mask]
            diverged = np.abs(self.z) > 2
            new_diverged = diverged & self.mask
            if np.any(new_diverged):
                self.result[new_diverged] = i + 1 - np.log(np.log(np.abs(self.z[new_diverged])))/np.log(2)
                self.mask[new_diverged] = False
    
    def update_add_iterations(self, new_max_iter):
        """
        Ajoute des itérations supplémentaires si le domaine reste identique.
        
        Pour chaque itération additionnelle (de self.max_iter à new_max_iter), met à jour
        les tableaux 'z', 'result' et 'mask' pour traiter uniquement les pixels encore actifs.
        """
        for i in range(self.max_iter, new_max_iter):
            self.z[self.mask] = self.z[self.mask]**2 + self.c[self.mask]
            diverged = np.abs(self.z) > 2
            new_diverged = diverged & self.mask
            if np.any(new_diverged):
                self.result[new_diverged] = i + 1 - np.log(np.log(np.abs(self.z[new_diverged])))/np.log(2)
                self.mask[new_diverged] = False
        self.max_iter = new_max_iter
    
    def apply_translation(self, dx, dy):
        """
        Applique une translation (déplacement) aux tableaux en utilisant np.roll et met à jour le domaine.
        """
        self.z = np.roll(self.z, shift=(dy, dx), axis=(0, 1))
        self.result = np.roll(self.result, shift=(dy, dx), axis=(0, 1))
        self.mask = np.roll(self.mask, shift=(dy, dx), axis=(0, 1))
        scale_re = (self.re_end - self.re_start) / self.width
        scale_im = (self.im_end - self.im_start) / self.height
        self.re_start -= dx * scale_re
        self.re_end   -= dx * scale_re
        self.im_start -= dy * scale_im
        self.im_end   -= dy * scale_im
        self.compute_grid()
    
    def update_zoom(self, new_re_start, new_re_end, new_im_start, new_im_end, new_max_iter):
        """
        Met à jour le domaine et le nombre d'itérations.
        
        Si le domaine reste identique (à un epsilon près) et que new_max_iter est supérieur,
        effectue seulement les itérations supplémentaires (update incrémental). Sinon, refait un recalcul complet.
        """
        if (abs(new_re_start - self.re_start) < 1e-9 and abs(new_re_end - self.re_end) < 1e-9 and
            abs(new_im_start - self.im_start) < 1e-9 and abs(new_im_end - self.im_end) < 1e-9 and
            new_max_iter > self.max_iter):
            self.update_add_iterations(new_max_iter)
        else:
            self.re_start = new_re_start
            self.re_end = new_re_end
            self.im_start = new_im_start
            self.im_end = new_im_end
            self.max_iter = new_max_iter
            self.compute_grid()
            self.full_recompute()
