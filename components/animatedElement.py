class AnimatedElement:
    def __init__(self, sprites, position):
        self.sprites = sprites
        self.current_frame = 0
        self.position = position
        self.animation_speed = 0.15  # Vitesse d'animation commune

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.sprites):
            self.current_frame = 0

    def draw(self, screen):
        frame_index = int(self.current_frame) % len(self.sprites)
        screen.blit(self.sprites[frame_index], self.position)