# Main.py
# Main script

# Import all libraries
import sys, menu, math, obstacles, pygame, player, screen, void, levels, random

# Initialize PyGame
pygame.init()

music = pygame.mixer.music

# Frame rate is set to 60
frames = 0
FRAME_RATE = 60

# Global variables to keep track of game stage
game_playing = False
game_lost = False
game_lost_delay_finished = False
game_won = False
game_lost_delay_finished = False

intro_run = False

# Pygame clock - runs the game at the desired frame rate
# It compensates for lag and makes sure the game will run at the same speed on
# lower-performance devices as it would on higher-performance ones
clock = pygame.time.Clock()

# Instantiate player
player = player.Player(rect=pygame.Rect(0, 0, 30, 30))
player.motion.change_motion(time=0,
                     origin=screen.center,
                     radius=200)

# Instantiate void
void = void.Void(rect=pygame.Rect(0, 0, 10, 10))
void.motion.change_motion(time=0,
                     origin=screen.center,
                     radius=math.sqrt(screen.width ** 2 + screen.height ** 2),
                     start_angle=0.5 * math.pi)

# Beginning of render loop
# Basic processes to run each time a frame is drawn
#  - Tick the clock
#  - Program "esc" to quit
#  - Erase the previous frame

pressed_keys = []

# Fun Easter egg/advanced feature - the Konami code
# Was used in many 80s games like Frogger
# If the code is pressed quickly, the secret level will begin!
konami = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]

current_konami_index = 0

def render_loop_start(events):
    global frames, current_konami_index, pressed_keys
    time = frames / FRAME_RATE
    clock.tick(FRAME_RATE)
    for event in events:
        if event.type == pygame.KEYDOWN:
            if menu.menu_open:
                pressed_keys.append([event.key, time])
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.QUIT:
            sys.exit()
    screen.surface.fill(screen.colors["black"])
    if menu.menu_open:
        for key_arr in pressed_keys:
            key = key_arr[0]
            if current_konami_index == len(konami):
                secret_level()
                current_konami_index = 0
                pressed_keys.clear()
            if key == konami[current_konami_index]:
                current_konami_index += 1
            else:
                current_konami_index = 0
    return time

# End of frame
# Draw "quit" button and "menu" if playing game
def render_loop_end(events):
    global frames
    quit_rect = pygame.Rect(10, 10, 60, 40)
    quit_color = screen.colors["lightgrey"]
    if screen.hover_over(quit_rect):
        quit_color = screen.colors["yellow"]
    screen.text("QUIT", quit_color, (41, 30), screen.font, 15)
    pygame.draw.rect(screen.surface, quit_color, quit_rect, 3)
    if screen.click_inside(quit_rect, events):
        sys.exit()
    if game_playing:
        menu_rect = pygame.Rect(10, 60, 60, 40)
        menu_color = screen.colors["lightgrey"]
        if screen.hover_over(menu_rect):
            menu_color = screen.colors["yellow"]
        screen.text("MENU", menu_color, (41, 80), screen.font, 15)
        pygame.draw.rect(screen.surface, menu_color, menu_rect, 3)
        if screen.click_inside(menu_rect, events):
            menu.menu_open = True
    pygame.display.flip()
    frames += 1

# Run when a level starts
# Controls the level's music and player and void motion settings
# Also causes the 1 second delay following the press of the Start button on the title screen
def init_game():
    global intro_run
    intro_run = True
    level = levels.levels[levels.level]
    level.played += 1
    if level.name != "Demo":
        level.celebration = None
        level.consolation = None
    music.pause()
    screen.surface.fill(screen.colors["black"])
    screen.text(level.name, screen.colors["green"], (screen.width / 2, screen.height / 2 + 50),
                screen.font, 30)
    pygame.display.flip()
    music.load("audio/SELECT.mp3")
    music.play()
    pygame.time.wait(1000)
    music.load("audio/" + level.music)
    music.play()
    global game_playing, game_lost, game_lost_delay_finished, game_won, game_won_delay_finished, frames
    game_playing = True
    game_lost = False
    game_lost_delay_finished = False
    game_won = False
    game_won_delay_finished = False
    frames = 0
    levels.current_timer = level.time
    void.origin = screen.center
    void.color = level.void_color
    void.hover_color = level.void_hover_color
    void.reflect = []
    void.angle_offset = math.pi / 20
    void.curve_offset = 100000
    obstacles.generate_obstacles()
    player.health = 100
    player.motion.change_motion(time=0,
                                init_velocity=0,
                                acceleration=0,
                                start_angle=0)
    void.motion.change_motion(time=0,
                              init_velocity=0,
                              acceleration=0,
                              start_angle=0.5 * math.pi)

# Draw loop
# Checks to see if the game is won or lost. If so, run processes as needed (show messages)
# If the game is still playing, update the motion of all objects and draw them to the screen
def draw_loop(time):
    global game_playing, game_lost, game_lost_delay_finished, game_won, game_won_delay_finished
    level = levels.levels[levels.level]
    if game_lost:
        if not game_lost_delay_finished:
            music.pause()
            pygame.time.wait(1000)
            music.load("audio/LOSE.mp3")
            music.play()
            game_lost_delay_finished = True
        screen.text("Game over", screen.colors["red"], screen.center, screen.font, 60)
        consolation = ["The void compels you.", "Mastery requires patience.", "Do not fret, not just yet.", "You were supposed to avoid it.",
                       "Click Menu to play again. You know you want to.", "Keep calm and carry on.", "So close, yet so far.", "*generic consolation message*"]
        if not level.consolation:
            level.consolation = random.choice(consolation)
        l = list(screen.center)
        l[1] += 60
        l = tuple(l)
        screen.text(level.consolation, screen.colors["white"], l, screen.font, 30)
        return
    if game_won:
        if not game_won_delay_finished:
            music.pause()
            pygame.time.wait(1000)
            music.load("audio/WIN.mp3")
            music.play()
            game_won_delay_finished = True
        screen.text("You win!", screen.colors["yellow"], screen.center, screen.font, 60)
        celebration = ["The void compels you.", "Might it have been a pyrrhic victory?", "A well deserved victory.",
                       "Nice job, you avoided it.",
                       "Click Menu to play again. You know you want to.", "Don't let it get to your head.", "*generic celebratory message*"]
        if not level.celebration:
            level.celebration = random.choice(celebration)
        l = list(screen.center)
        l[1] += 60
        l = tuple(l)
        screen.text(level.celebration, screen.colors["white"], l, screen.font, 30)
        return
    void.draw(time)
    if levels.level != 6 or levels.level == 6 and time >= 4:
        obstacles.draw_obstacles(time)
        obstacles.check_collide(player)
    player.draw(time)
    void.change_motion(time)
    void.check_collide(time, player)
    if void.collide:
        player.health -= level.penalty
        player.health = int(player.health)
        if player.health < 0: player.health = 0
    player.control(time)
    player.change_motion(time)
    levels.current_timer = levels.levels[levels.level].time - time
    if player.health <= 0:
        game_lost = True
    if levels.current_timer <= 0:
        game_won = True
    # Timer and health
    screen.text("❤", screen.colors["pink"], (screen.width - 135, 45), screen.unicode_font, 40)
    screen.text(str(player.health), screen.colors["pink"], (screen.width - 60, 50), screen.font, 40)
    screen.text("🕑", screen.colors["lightblue"], (screen.width - 180, 100), screen.unicode_font, 40)
    screen.text(levels.str_time(levels.current_timer), screen.colors["lightblue"], (screen.width - 80, 105), screen.font, 40)
    level.run_events(player, void, time)

# Intro story: runs at the very beginning
def intro(time):
    global intro_run
    if time < 5:
        screen.image("images/intro/1.png", screen.center)
    elif time < 10:
        screen.image("images/intro/2.png", screen.center)
    elif time < 15:
        screen.image("images/intro/3.png", screen.center)
    elif time < 25:
        screen.image("images/intro/4.png", screen.center)

# Secret level runs when the Konami code is pressed
def secret_level():
    levels.level = 6
    menu.menu_open = False

# Main loop, takes care of the above functions and runs them as necessary
# Is controlled by the global variables from earlier
while 1:
    events = pygame.event.get()
    time = render_loop_start(events)
    if menu.menu_open:
        if game_playing:
            game_playing = False
            music.pause()
            menu.music_playing = False
        menu.menu_loop(time, events)
    else:
        if not game_playing:
            init_game()
        if frames > 0:
            draw_loop(time)
    if not intro_run:
        intro(time)
    render_loop_end(events)