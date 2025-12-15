import pygame
import random
import math
from collections import namedtuple

pygame.init()
Vec = pygame.math.Vector2

SCREEN_W, SCREEN_H = 900, 600
FPS = 60

# --- Particle definition ---
Particle = namedtuple("Particle", ["pos", "vel", "r", "col", "mass"])

class Liquid:
    def __init__(self, n_particles, screen_size, lowres_scale=0.5):
        self.screen_w, self.screen_h = screen_size
        self.lowres_scale = lowres_scale  # drawing scale to produce blur
        self.particles = []
        self.viscosity = 0.05      # damping of velocity; lower -> splashier
        self.attract_strength = 5000.0
        self.interaction_radius = 60.0
        self.trails = True
        self._init_particles(n_particles)

    def _init_particles(self, n):
        for _ in range(n):
            self.spawn_random()

    def spawn_random(self, x=None, y=None, r=None, color=None):
        x = self.screen_w * 0.5 if x is None else x
        y = self.screen_h * 0.5 if y is None else y
        pos = Vec(
            random.uniform(0, self.screen_w) if x is None else x,
            random.uniform(0, self.screen_h) if y is None else y
        )
        vel = Vec(random.uniform(-30, 30), random.uniform(-30, 30))
        r = random.uniform(6, 22) if r is None else r
        # soft pastel-ish colors; can be customized
        palette = [
            (90, 200, 255),
            (255, 140, 200),
            (170, 255, 150),
            (255, 200, 110)
        ]
        col = random.choice(palette) if color is None else color
        mass = max(0.5, r / 10.0)
        self.particles.append(Particle(pos, vel, r, col, mass))

    def spawn_drop(self, x, y, r=36, color=None):
        # spawn a cluster of small particles for a nice drop
        base_color = color or (255, 150, 200)
        for i in range(6):
            jitter = Vec(random.uniform(-r*0.2, r*0.2), random.uniform(-r*0.2, r*0.2))
            p_pos = Vec(x, y) + jitter
            p_vel = Vec(random.uniform(-40, 40), random.uniform(-40, 40))
            p_r = max(6, r * random.uniform(0.25, 0.7))
            self.particles.append(Particle(p_pos, p_vel, p_r, base_color, max(0.5, p_r/10)))

    def update(self, dt, attractor_pos=None, attract_on=False):
        # Update particle positions using simple physics + rudimentary particle repulsion
        new_particles = []
        for p in self.particles:
            pos = Vec(p.pos)
            vel = Vec(p.vel)
            # attraction to cursor if enabled
            if attract_on and attractor_pos is not None:
                dir_to_cursor = Vec(attractor_pos) - pos
                dist = dir_to_cursor.length() + 1e-6
                if dist < self.interaction_radius * 5:
                    # inverse-square-ish attraction
                    force = dir_to_cursor.normalize() * (self.attract_strength / (dist * dist))
                    vel += force * (dt / max(0.5, p.mass))
            # simple inter-particle soft repulsion to keep blobs from collapsing
            # perform cheap local repulsion (O(n^2) is fine for small n)
            for q in self.particles:
                if q is p:
                    continue
                v = Vec(pos) - Vec(q.pos)
                d = v.length()
                if d == 0:
                    continue
                # if very close, push apart
                min_dist = (p.r + q.r) * 0.6
                if d < min_dist:
                    push = v.normalize() * (min_dist - d) * 0.1
                    vel += push / p.mass
            # viscosity / damping
            vel *= (1.0 - self.viscosity)
            # integrate
            pos += vel * dt
            # wrap-around edges for continuous flow; clamp optionally
            if pos.x < -50: pos.x = self.screen_w + 50
            if pos.x > self.screen_w + 50: pos.x = -50
            if pos.y < -50: pos.y = self.screen_h + 50
            if pos.y > self.screen_h + 50: pos.y = -50
            new_particles.append(Particle(pos, vel, p.r, p.col, p.mass))
        self.particles = new_particles

    def draw(self, screen):
        # create a low-res surface, draw additive, then smoothscale up to blur/glow effect
        lw = max(1, int(self.screen_w * self.lowres_scale))
        lh = max(1, int(self.screen_h * self.lowres_scale))
        lowres = pygame.Surface((lw, lh), flags=pygame.SRCALPHA).convert_alpha()
        lowres.fill((0, 0, 0, 0) if self.trails else (10, 10, 12, 0))

        # draw additive circles on lowres
        for p in self.particles:
            # scaled positions & radius
            sp = (int(p.pos.x * self.lowres_scale), int(p.pos.y * self.lowres_scale))
            sr = max(1, int(p.r * self.lowres_scale))
            # semi-transparent circle - alpha scales with radius so big drops glow more
            alpha = int(min(180, 30 + sr * 6))
            col = (*p.col, alpha)
            # draw multiple concentric circles for a soft falloff
            for i in range(3):
                rr = int(sr * (1.0 + 0.25 * i))
                a = max(8, alpha - i * 40)
                pygame.draw.circle(lowres, (*p.col, a), sp, rr, 0,)

        # upscale to screen size using smoothscale (soft blur)
        scaled = pygame.transform.smoothscale(lowres, (self.screen_w, self.screen_h))
        # colorize: draw scaled onto screen with additive blending for neon liquid look
        screen.blit(scaled, (0, 0), special_flags=pygame.BLEND_ADD)

        # optional soft colored overlay / vignette for aesthetics
        # (draw subtle radial gradient using circles)
        overlay = pygame.Surface((self.screen_w, self.screen_h), flags=pygame.SRCALPHA).convert_alpha()
        # draw a faint gradient center
        for i, a in enumerate([18, 12, 8]):
            rr = int(max(self.screen_w, self.screen_h) * (0.5 + i * 0.15))
            pygame.draw.circle(overlay, (10, 8, 20, a), (self.screen_w//2, self.screen_h//2), rr)
        screen.blit(overlay, (0, 0), special_flags=pygame.BLEND_ADD)

    # convenience: tweak parameters
    def add_particles(self, k=5):
        for _ in range(k):
            self.spawn_random()

    def remove_particles(self, k=1):
        for _ in range(k):
            if self.particles:
                self.particles.pop()

# ---------------------------
# Main program
# ---------------------------
def main():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Liquid Aesthetic — Pygame")
    clock = pygame.time.Clock()
    liquid = Liquid(n_particles=40, screen_size=(SCREEN_W, SCREEN_H), lowres_scale=0.45)

    running = True
    attract = False
    attract_pos = (SCREEN_W//2, SCREEN_H//2)

    font = pygame.font.SysFont(None, 18)
    show_help = True

    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # spawn random drop near center
                    liquid.spawn_drop(random.uniform(0.2*SCREEN_W, 0.8*SCREEN_W),
                                       random.uniform(0.2*SCREEN_H, 0.8*SCREEN_H),
                                       r=random.uniform(20, 48))
                elif event.key == pygame.K_t:
                    liquid.trails = not liquid.trails
                elif event.key == pygame.K_UP:
                    liquid.viscosity = max(0.0, liquid.viscosity - 0.01)
                elif event.key == pygame.K_DOWN:
                    liquid.viscosity = min(0.3, liquid.viscosity + 0.01)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    liquid.add_particles(5)
                elif event.key == pygame.K_MINUS:
                    liquid.remove_particles(5)
                elif event.key == pygame.K_h:
                    show_help = not show_help
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    attract = True
                    attract_pos = event.pos
                elif event.button == 3:
                    liquid.spawn_drop(*event.pos, r=48)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    attract = False
            elif event.type == pygame.MOUSEMOTION:
                attract_pos = event.pos

        # background (dark)
        if liquid.trails:
            # leave a faint dark rectangle to create motion trails
            dark = pygame.Surface((SCREEN_W, SCREEN_H))
            dark.fill((8, 8, 12))
            dark.set_alpha(60)
            screen.blit(dark, (0, 0))
        else:
            screen.fill((8, 8, 12))

        # update & draw liquid
        liquid.update(dt, attractor_pos=attract_pos, attract_on=attract)
        liquid.draw(screen)

        # UI overlay (small)
        info_lines = [
            f"Particles: {len(liquid.particles)}  |  Viscosity: {liquid.viscosity:.3f}  |  Trails: {'On' if liquid.trails else 'Off'}",
            "Left-click+drag: attract | Right-click: big drop | Space: spawn drop",
            "Up/Down: viscosity | +/-: add/remove particles | T: toggle trails | H: toggle help"
        ]
        if show_help:
            for i, line in enumerate(info_lines):
                txt = font.render(line, True, (200, 200, 210))
                screen.blit(txt, (10, 10 + i * 18))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()