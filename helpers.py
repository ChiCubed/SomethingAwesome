import pygame

def load_image(name):
    return pygame.image.load(name)

def fade(screen, image, rect, fps):
    for i in range(128):
        image.set_alpha(i)
        screen.blit(image, rect)

        pygame.display.flip()

        pygame.time.Clock().tick(fps)