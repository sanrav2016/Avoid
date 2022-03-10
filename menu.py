# Menu.py
# Handles the menu/title screen

import pygame, screen, levels

# Music
music = pygame.mixer.music
music_playing = False
menu_open = True
leaderboard_clicked = False
menu_options = []
for level in levels.levels:
    if level.name != "Secret Level":
        menu_options.append(level.name)
selected_menu_option = 0

# menu loop, runs while the menu is open
def menu_loop(time, events):
    global selected_menu_option, menu_open, music_playing, leaderboard_clicked
    if not music_playing:
        music.load("audio/LOBBY.mp3")
        music.play()
        music_playing = True
    screen.surface.fill(screen.colors["black"])
    # Title image
    screen.image("images/title.png", (screen.width / 2, screen.height / 2 - 100), scale=0.5)
    # Scrollable menu
    screen.text(menu_options[selected_menu_option], screen.colors["white"], (screen.width / 2, screen.height / 2 + 50), screen.font, 30)
    rect_left = None
    rect_right = None
    # Makes the left and right arrows disappear if the user is on the first or last option, respectively
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
    # Blinking start button
    start_color = screen.colors["pink"] if int(time) % 2 == 0 else screen.colors["yellow"]
    # Hover behavior
    # Modelled after CSS
    if screen.hover_over(start_rect):
        start_color = screen.colors["red"]
    screen.text("START", start_color, (screen.width / 2, screen.height / 2 + 175), screen.font, 30)
    pygame.draw.rect(screen.surface, start_color, start_rect, 5)
    # Responding to clicks
    # Touch input will also work
    # This is defined in Screen.py
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
    # Leaderboard
    all_played = True
    for level in levels.levels:
        if level.name != "Secret Level" and level.played == 0: all_played = False
    if all_played:
        screen.image("images/end.png", screen.center)
        leaderboard_rect = pygame.Rect(screen.width / 2 - 150, screen.height / 2 + 125, 300, 100)
        screen.text("LEADERBOARD", screen.colors["lightblue"], (screen.width / 2, screen.height / 2 + 175), screen.font,
                    30)
        pygame.draw.rect(screen.surface, screen.colors["lightblue"], leaderboard_rect, 5)
        if screen.click_inside(start_rect, events):
            menu_open = True
            music_playing = True
        if leaderboard_clicked:
            screen.text("Check console", screen.colors["orange"], (screen.width / 2, screen.height),
                        screen.font,
                        30)
            name = input("What is your name? ")
            open("data.txt", "a").write(name + "\n")
            print(name + ", you have been added to the leaderboard! Here is the whole thing:")
            print(open("data.txt", "r").read())
            leaderboard_clicked = False
            for level in levels.levels:
                level.played = 0
        if not leaderboard_clicked and screen.click_inside(leaderboard_rect, events):
            leaderboard_clicked = True
            screen.text("Check console", screen.colors["orange"], (screen.width / 2, screen.height - 60), screen.font, 30)