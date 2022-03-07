import screen, math, random

level = 0

current_timer = 0

local_player = None
local_void = None
local_time = 0

bpm = 120
bps = bpm / 60

class Level():
    def __init__(self, name, time, penalty, gain, v, a, void_color, void_hover_color, music, events=[], consolation = None, celebration = None):
        self.name = name
        self.time = time
        self.penalty = penalty
        self.gain = gain
        self.v = v
        self.a = a
        self.void_color = void_color
        self.void_hover_color = void_hover_color
        self.events = events
        self.music = music
        self.played = 0
        self.consolation = consolation
        self.celebration = celebration

    def run_events(self, player, void, time):
        global local_player, local_void, local_time
        local_player = player
        local_void = void
        local_time = time
        for event in self.events:
            if event.start <= time <= event.end:
                event.function()

class Event():
    def __init__(self, start, end, function):
        self.start = start
        self.end = end
        self.function = function

levels = [
    Level(name="Demo",
          time=30,
          penalty=1,
          gain=1,
          v=[1, 3],
          a=[1, 3],
          void_color=screen.colors["white"],
          void_hover_color=screen.colors["lightblue"],
          events=[
                    Event(start=1,
                          end=30,
                          function=lambda: screen.text("Welcome to AVOID", screen.colors["lightblue"], (screen.width / 2, 60), screen.font, 30)),
                    Event(start=3,
                          end=30,
                          function=lambda: screen.text("Press/hold SPACE to move", screen.colors["green"], (screen.width / 2, 120), screen.font, 30)),
                    Event(start=5,
                          end=30,
                          function=lambda: screen.text("Avoid the spinning laser", screen.colors["yellow"], (screen.width/2, 180), screen.font, 30)),
                    Event(start=7,
                          end=30,
                          function=lambda: screen.text("Hit the dots to gain health", screen.colors["white"], (screen.width / 2, 240), screen.font, 30)),
                    Event(start=9,
                          end=30,
                          function=lambda: screen.text("Survive until the timer runs out", screen.colors["pink"], (screen.width / 2, 300), screen.font, 30))
        ],
        music="L0.mp3",
        consolation="Press MENU to go back",
        celebration="Press MENU to go back"
    ),
    Level(name="Level 1",
          time=30,
          penalty=5,
          gain=1,
          v=[3, 5],
          a=[1, 3],
          void_color=screen.colors["blue"],
          void_hover_color=screen.colors["lightblue"],
          events = [
              Event(start=0,
                    end=0,
                    function=lambda: (True)
              ),
              Event(start=0,
                    end=3,
                    function=lambda: screen.text("Level 1: Jumps", screen.colors["lightblue"], (screen.width / 2, 60), screen.font, 30)
              ),
              Event(start=5,
                    end=5,
                    function=lambda: local_void.change_motion(local_time, angle=local_player.motion.angle(local_time) - 0.25 * math.pi)
              ),
              Event(start=10,
                    end=10,
                    function=lambda: local_void.change_motion(local_time, angle=local_player.motion.angle(local_time) - 0.25 * math.pi)
              ),
              Event(start=15,
                    end=15,
                    function=lambda: local_void.change_motion(local_time, angle=local_player.motion.angle(local_time) - 0.25 * math.pi)
              ),
              Event(start=20,
                    end=20,
                    function=lambda: local_void.change_motion(local_time, angle=local_player.motion.angle(local_time) - 0.25 * math.pi)
              ),
              Event(start=25,
                    end=25,
                    function=lambda: local_void.change_motion(local_time, angle=local_player.motion.angle(local_time) - 0.25 * math.pi)
              )
          ],
        music="L1.mp3"
    ),
    Level(name="Level 2",
          time=30,
          penalty=3,
          gain=3,
          v=[7, 10],
          a=[1, 5],
          void_color=screen.colors["pink"],
          void_hover_color=screen.colors["orange"],
          events=[
              Event(start=0,
                    end=3,
                    function=lambda: (screen.text("Level 2: Spirals", screen.colors["orange"], (screen.width / 2, 60), screen.font, 30), screen.text("WARNING: FLASHING LIGHTS, DIZZYING EFFECTS", screen.colors["red"], (screen.width / 2, 120), screen.font, 40))
              ),
              Event(start=5,
                    end=5,
                    function=lambda: local_void.change_curve_offset(-95000, goal=5000)
              ),
              Event(start=5,
                    end=10,
                    function=lambda: local_void.change_curve_offset(-50, goal=500)
              ),
              Event(start=10,
                    end=15,
                    function=lambda: local_void.change_curve_offset(-3, goal=-500)
              ),
              Event(start=15,
                    end=20,
                    function=lambda: local_void.change_curve_offset(3, goal=500)
              ),
              Event(start=20,
                    end=25,
                    function=lambda: local_void.change_curve_offset(-3, goal=-500)
              )
          ],
        music="L2.mp3"
    ),
    Level(name="Level 3",
          time=30,
          penalty=6,
          gain=3,
          v=[4, 6],
          a=[1, 3],
          void_color=screen.colors["blue"],
          void_hover_color=screen.colors["green"],
          events=[
                    Event(start=0,
                    end=3,
                    function=lambda: screen.text("Level 3: Widening", screen.colors["green"], (screen.width / 2, 60), screen.font, 30)
                    ),
                    Event(start=10,
                          end=15,
                          function=lambda: local_void.change_size(1/225)
                    ),
                    Event(start=26,
                          end=30,
                          function=lambda: local_void.change_size(1/225)
                    )
          ],
        music="L3.mp3"
    ),
    Level(name="Level 4",
          time=30,
          penalty=3,
          gain=3,
          v=[10, 15],
          a=[20, 21],
          void_color=screen.colors["white"],
          void_hover_color=screen.colors["red"],
          events=[
                    Event(start=0,
                          end=3,
                          function=lambda: screen.text("Level 4: Invisibility", screen.colors["white"], (screen.width / 2, 60), screen.font, 30)
                    ),
                    Event(start=5,
                          end=10,
                          function=lambda: local_void.change_color(screen.colors["black"], -5)
                    ),
                    Event(start=10,
                          end=15,
                          function=lambda: local_void.change_color(screen.colors["white"], 5)
                    ),
                    Event(start=15,
                          end=20,
                          function=lambda: local_void.change_color(screen.colors["black"], -5)
                    ),
                    Event(start=20,
                          end=25,
                          function=lambda: local_void.change_color(screen.colors["white"], 5)
                    ),
                    Event(start=25,
                          end=30,
                          function=lambda: local_void.change_color(screen.colors["black"], -5)
                    )
          ],
        music="L4.mp3"
    ),
    Level(name="Level 5",
          time=30,
          penalty=3,
          gain=6,
          v=[3, 5],
          a=[1, 3],
          void_color=screen.colors["pink"],
          void_hover_color=screen.colors["lightblue"],
          events=[
                    Event(start=0,
                          end=3,
                          function=lambda: (screen.text("Level 5: Mirror", screen.colors["pink"], (screen.width / 2, 60), screen.font, 30), screen.text("WARNING: FLASHING LIGHTS, DIZZYING EFFECTS", screen.colors["red"], (screen.width / 2, 120), screen.font, 40))
                    ),
                    Event(start=7,
                          end=7,
                          function=lambda: (local_void.set_reflect([math.pi]), local_void.motion.change_motion(time=local_time, init_velocity=7, acceleration=0))
                    ),
                    Event(start=8,
                          end=8,
                          function=lambda: (local_void.set_reflect([]), local_void.motion.change_motion(time=local_time, init_velocity=3, acceleration=-1))
                    ),
                    Event(start=12.5,
                          end=12.5,
                          function=lambda: (local_void.set_reflect([2 * math.pi / 3, 4 * math.pi / 3]), local_void.motion.change_motion(time=local_time, init_velocity=8, acceleration=0))
                    ),
                    Event(start=13.5,
                          end=13.5,
                          function=lambda: (local_void.set_reflect([]), local_void.motion.change_motion(time=local_time, init_velocity=3, acceleration=-1))
                    ),
                    Event(start=18,
                          end=18,
                          function=lambda: (local_void.set_reflect([2 * math.pi / 3, 4 * math.pi / 3]), local_void.motion.change_motion(time=local_time, init_velocity=8, acceleration=0))
                    ),
                    Event(start=19,
                          end=19,
                          function=lambda: (local_void.set_reflect([]), local_void.motion.change_motion(time=local_time, init_velocity=3, acceleration=-1))
                    ),
                    Event(start=21,
                          end=21,
                          function=lambda: (local_void.set_reflect([0.5 * math.pi, math.pi, 1.5 * math.pi]), local_void.motion.change_motion(time=local_time, init_velocity=10, acceleration=0))
                    ),
                    Event(start=22,
                          end=22,
                          function=lambda: local_void.motion.change_motion(time=local_time, init_velocity=15, acceleration=0)
                    ),
                    Event(start=23,
                          end=23,
                          function=lambda: (local_void.set_reflect([]), local_void.motion.change_motion(time=local_time, init_velocity=3, acceleration=-1))
                    ),
                    Event(start=26,
                          end=26,
                          function=lambda: (local_void.set_reflect([0.5 * math.pi, math.pi, 1.5 * math.pi]), local_void.motion.change_motion(time=local_time, acceleration=4))
                    )
          ],
        music="L5.mp3"
    )
]

def str_time(t):
    t = math.ceil(t)
    m = str(int(t / 60))
    s = str(t % 60)
    if len(m) == 1:
        m = "0" + m
    if len(s) == 1:
        s = "0" + s
    return m + ":" + s