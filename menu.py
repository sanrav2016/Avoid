import pygame, screen, levels

music = pygame.mixer.music
music_playing = False
menu_open = True
menu_options = []
for level in levels.levels:
    menu_options.append(level.name)
selected_menu_option = 0

def menu_loop(time, events):
    global selected_menu_option, menu_open, music_playing
    if not music_playing:
        music.load("audio/L6.mp3")
        music.play()
        music_playing = True
    screen.surface.fill(screen.colors["black"])
    screen.image("images/title.png", (screen.width / 2, screen.height / 2 - 100), scale=0.5)
    screen.text(menu_options[selected_menu_option], screen.colors["white"], (screen.width / 2, screen.height / 2 + 50), screen.font, 30)
    rect_left = None
    rect_right = None
    if selected_menu_option > 0:
        screen.text(menu_options[selected_menu_option - 1], screen.colors["grey"], (screen.width / 2 - 200, screen.height / 2 + 50), screen.font, 30)
        screen.text("⏴", screen.colors["yellow"], (screen.width / 2 - 350, screen.height / 2 + 50), screen.unicode_font, 30)
        rect_left = pygame.Rect(screen.width / 2 - 450, screen.height / 2 - 50, 200, 200)
    if selected_menu_option < len(menu_options) - 1:
        screen.text(menu_options[selected_menu_option + 1], screen.colors["grey"], (screen.width / 2 + 200, screen.height / 2 + 50), screen.font, 30)
        screen.text("⏵", screen.colors["yellow"], (screen.width / 2 + 350, screen.height / 2 + 50), screen.unicode_font,
                    30)
        rect_right = pygame.Rect(screen.width / 2 + 250, screen.height / 2 - 50, 200, 200)
    start_rect = pygame.Rect(screen.width / 2 - 100, screen.height / 2 + 125, 200, 100)
    start_color = screen.colors["pink"] if int(time) % 2 == 0 else screen.colors["yellow"]
    if screen.hover_over(start_rect):
        start_color = screen.colors["red"]
    screen.text("START", start_color, (screen.width / 2, screen.height / 2 + 175), screen.font, 30)
    pygame.draw.rect(screen.surface, start_color, start_rect, 5)
    if screen.click_inside(start_rect, events):
        menu_open = False
        music_playing = False
    if rect_left != None:
        if screen.click_inside(rect_left, events):
            selected_menu_option -= 1
    if rect_right != None:
        if screen.click_inside(rect_right, events):
            selected_menu_option += 1
    levels.level = selected_menu_option