# fractal_state_gpu.py
import cupy as cp
import ui  # Pour accéder à UI_OPTIONS

class FractalStateGPU:
    """
    Calcule la fractale sur le GPU avec CuPy et supporte plusieurs formules :
      - Mandelbrot, Julia, Burning Ship, Custom,
      - Tricorn, Multibrot3, Phoenix et Perpendicular.
    """
    
    def __init__(self, width, height, max_iter, re_start, re_end, im_start, im_end, fractal_type="Mandelbrot"):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.re_start = re_start
        self.re_end = re_end
        self.im_start = im_start
        self.im_end = im_end
        self.fractal_type = fractal_type
        # Sauvegarde des paramètres initiaux pour le Reset Zoom
        self.init_params = (re_start, re_end, im_start, im_end, max_iter)
        self.compute_grid()
        self.full_recompute()
    
    def compute_grid(self):
        re = cp.linspace(self.re_start, self.re_end, self.width)
        im = cp.linspace(self.im_start, self.im_end, self.height)
        self.c = re[cp.newaxis, :] + 1j * im[:, cp.newaxis]
    
    def full_recompute(self):
        # Initialisation de z selon la formule
        if self.fractal_type in ["Julia", "Custom"]:
            self.z = self.c.copy()
        else:
            self.z = cp.zeros((self.height, self.width), dtype=cp.complex128)
        # Variables pour le calcul itératif
        self.result = cp.full((self.height, self.width), self.max_iter, dtype=cp.float64)
        self.mask = cp.ones((self.height, self.width), dtype=bool)
        # Pour Phoenix, on garde z_prev (initialisé à 0)
        self.z_prev = cp.zeros_like(self.z)
        for i in range(self.max_iter):
            self.iterate(i)
    
    def iterate(self, i):
        if self.fractal_type == "Mandelbrot":
            self.z[self.mask] = self.z[self.mask]**2 + self.c[self.mask]
        elif self.fractal_type == "Julia":
            self.z[self.mask] = self.z[self.mask]**2 + (-0.7 + 0.27015j)
        elif self.fractal_type == "Burning Ship":
            z = self.z[self.mask]
            z = cp.abs(z.real) + 1j * cp.abs(z.imag)
            self.z[self.mask] = z**2 + self.c[self.mask]
        elif self.fractal_type == "Custom":
            custom_c = ui.UI_OPTIONS["custom_re"] + 1j * ui.UI_OPTIONS["custom_im"]
            self.z[self.mask] = self.z[self.mask]**2 + custom_c
        elif self.fractal_type == "Tricorn":
            # Utilise le conjugué : z = conj(z)^2 + c
            self.z[self.mask] = cp.conj(self.z[self.mask])**2 + self.c[self.mask]
        elif self.fractal_type == "Multibrot3":
            self.z[self.mask] = self.z[self.mask]**3 + self.c[self.mask]
        elif self.fractal_type == "Phoenix":
            # p constant, par exemple -0.5
            p = -0.5
            temp = self.z[self.mask]
            self.z[self.mask] = self.z[self.mask]**2 + p * self.z_prev[self.mask] + self.c[self.mask]
            self.z_prev[self.mask] = temp
        elif self.fractal_type == "Perpendicular":
            # Variation : inverser le signe de la partie imaginaire après avoir pris l'absolu
            z = self.z[self.mask]
            self.z[self.mask] = (cp.abs(z.real) + 1j * -cp.abs(z.imag))**2 + self.c[self.mask]
        
        diverged = cp.abs(self.z) > 2
        new_diverged = diverged & self.mask
        if cp.any(new_diverged):
            self.result[new_diverged] = i + 1 - cp.log(cp.log(cp.abs(self.z[new_diverged])))/cp.log(2)
            self.mask[new_diverged] = False

    def update_add_iterations(self, new_max_iter):
        for i in range(self.max_iter, new_max_iter):
            self.iterate(i)
        self.max_iter = new_max_iter
    
    def apply_translation(self, dx, dy):
        self.z = cp.roll(self.z, shift=(dy, dx), axis=(0, 1))
        self.result = cp.roll(self.result, shift=(dy, dx), axis=(0, 1))
        self.mask = cp.roll(self.mask, shift=(dy, dx), axis=(0, 1))
        scale_re = (self.re_end - self.re_start) / self.width
        scale_im = (self.im_end - self.im_start) / self.height
        self.re_start -= dx * scale_re
        self.re_end   -= dx * scale_re
        self.im_start -= dy * scale_im
        self.im_end   -= dy * scale_im
        self.compute_grid()
    
    def update_zoom(self, new_re_start, new_re_end, new_im_start, new_im_end, new_max_iter):
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
    
    def reset_view(self):
        """
        Réinitialise la vue aux paramètres initiaux.
        """
        self.re_start, self.re_end, self.im_start, self.im_end, self.max_iter = self.init_params
        self.compute_grid()
        self.full_recompute()
