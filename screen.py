import pygame, math

pygame.init()

screen_info = pygame.display.Info()
size = width, height = screen_info.current_w, screen_info.current_h
surface = pygame.display.set_mode(size)
center = width / 2, height / 2

font = "fonts/arcadepi.ttf"
unicode_font = "segoeuisymbol"

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "grey": (50, 50, 50),
    "lightgrey": (150, 150, 150),
    "red": (255, 0, 0),
    "orange": (255, 150, 0),
    "pink": (255, 0, 255),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "lightblue": (0, 255, 255),
    "yellow": (255, 255, 0)
}

def text(text, color, center, font, size):
    font_object = None
    if font == "segoeuisymbol":
        font_object = pygame.font.SysFont("segoeuisymbol", size)
    else:
        font_object = pygame.font.Font(font, size)
    text_surface = font_object.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = center
    surface.blit(text_surface, text_rect)

def hover_over(rectangle):
    x, y = pygame.mouse.get_pos()
    inside = (rectangle.left <= x <= rectangle.left + rectangle.width and rectangle.top <= y <= rectangle.top + rectangle.height)
    return inside

def click_inside(rectangle, events):
    x, y = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                inside = (rectangle.left <= x <= rectangle.left + rectangle.width and rectangle.top <= y <= rectangle.top + rectangle.height)
                return inside

def image(src, pos, scale=1, rotate=0):
    x, y = pos
    img = pygame.image.load(src)
    rotate *= 180 / math.pi
    img = pygame.transform.rotozoom(img, rotate, scale)
    rect = img.get_rect()
    rect.center = pos
    surface.blit(img, rect)