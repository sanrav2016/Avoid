import sys, menu, math, obstacles, pygame, player, screen, void, levels

pygame.init()

frames = 0
FRAME_RATE = 60

game_playing = False
game_lost = False
game_lost_delay_finished = False
game_won = False
game_lost_delay_finished = False

clock = pygame.time.Clock()

player = player.Player(rect=pygame.Rect(0, 0, 30, 30))
player.motion.change_motion(time=0,
                     origin=screen.center,
                     radius=200)

void = void.Void(rect=pygame.Rect(0, 0, 10, 10))
void.motion.change_motion(time=0,
                     origin=screen.center,
                     radius=math.sqrt(screen.width ** 2 + screen.height ** 2),
                     start_angle=0.5 * math.pi)

def render_loop_start(events):
    global frames
    time = frames / FRAME_RATE
    clock.tick(FRAME_RATE)
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.QUIT:
            sys.exit()
    screen.surface.fill(screen.colors["black"])
    return time

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

def init_game():
    global game_playing, game_lost, game_lost_delay_finished, game_won, game_won_delay_finished, frames
    game_playing = True
    game_lost = False
    game_lost_delay_finished = False
    game_won = False
    game_won_delay_finished = False
    frames = 0
    level = levels.levels[levels.level]
    levels.current_timer = level.time
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

def draw_loop(time):
    global game_playing, game_lost, game_lost_delay_finished, game_won, game_won_delay_finished
    level = levels.levels[levels.level]
    if game_lost:
        if not game_lost_delay_finished:
            pygame.time.wait(1000)
            game_lost_delay_finished = True
        screen.text("Game over", screen.colors["red"], screen.center, screen.font, 60)
        return
    if game_won:
        if not game_won_delay_finished:
            pygame.time.wait(1000)
            game_won_delay_finished = True
        screen.text("You win!", screen.colors["yellow"], screen.center, screen.font, 60)
        return
    void.draw(time)
    obstacles.draw_obstacles(time)
    player.draw(time)
    void.change_motion(time)
    void.check_collide(time, player)
    if void.collide:
        player.health -= level.penalty
        player.health = int(player.health)
        if player.health < 0: player.health = 0
    obstacles.check_collide(player)
    player.control(time)
    player.change_motion(time)
    levels.current_timer = levels.levels[levels.level].time - time
    if player.health <= 0:
        game_lost = True
    if levels.current_timer <= 0:
        game_won = True
    screen.text("❤", screen.colors["pink"], (screen.width - 135, 45), screen.unicode_font, 40)
    screen.text(str(player.health), screen.colors["pink"], (screen.width - 60, 50), screen.font, 40)
    screen.text("🕑", screen.colors["lightblue"], (screen.width - 180, 100), screen.unicode_font, 40)
    screen.text(levels.str_time(levels.current_timer), screen.colors["lightblue"], (screen.width - 80, 105), screen.font, 40)
    level.run_events(player, void, time)

while 1:
    events = pygame.event.get()
    time = render_loop_start(events)
    if menu.menu_open:
        if game_playing:
            game_playing = False
        menu.menu_loop(events)
    else:
        if not game_playing:
            init_game()
        if frames > 0:
            draw_loop(time)
    render_loop_end(events)