"""
Turtle Runaway

Controls (Runner):
    - W/S: forward/backward
    - A/D: turn left/right
    - Q/E: quick turn left/right

Rules:
    - Survive until the countdown timer reaches 0 to win.
    - If the chaser catches you (within the catch radius), you lose.
    - Score increases with time survived (10 points per second).

Note: In some IDEs like Spyder, launch via the console using a python command.
"""
import tkinter as tk
import turtle, random, time, math

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        
        # Game state: timer and scoring
        self.total_time = 30.0  # seconds (countdown)
        self.elapsed_time = 0.0
        self.remaining_time = self.total_time
        self.score = 0
        self.game_over = False
        self.last_tick = None

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

    # HUD drawer turtle (for timer/score/messages)
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.last_tick = time.perf_counter()
        self._draw_hud()  # initial HUD
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        if self.game_over:
            return

        # Timekeeping
        now = time.perf_counter()
        dt = now - (self.last_tick or now)
        self.last_tick = now
        self.elapsed_time += dt
        self.remaining_time = max(0.0, self.total_time - self.elapsed_time)

        # Scoring: 1 point per 0.1 sec survived
        self.score = int(self.elapsed_time * 10)

        # Update entities
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # Check win/lose conditions
        if self.is_catched():
            self._end_game(message="Caught! Game Over")
            return
        if self.remaining_time <= 0:
            self._end_game(message="Time's up! You win")
            return

        # Update HUD
        self._draw_hud()

        # Keep the game running
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def _time_str(self, seconds: float) -> str:
        s = max(0, int(seconds))
        ms = int((seconds - int(seconds)) * 10)  # tenths
        m, s = divmod(s, 60)
        return f"{m:02d}:{s:02d}.{ms}"

    def _draw_hud(self):
        # Clear and draw timer and score at top-left
        self.drawer.clear()
        self.drawer.penup()
        self.drawer.setpos(-330, 310)
        hud = (
            f"Time: {self._time_str(self.remaining_time)}  "
            f"Score: {self.score}"
        )
        self.drawer.write(hud, align='left', font=('Arial', 14, 'bold'))

    def _end_game(self, message: str):
        self.game_over = True
        # Final HUD update
        self._draw_hud()
        # Show centered end message
        self.drawer.penup()
        self.drawer.setpos(0, 0)
        self.drawer.write(
            f"{message}\nFinal Score: {self.score}",
            align='center', font=('Arial', 18, 'bold')
        )

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self._bound = 340  # keep within ~700x700 canvas

        # Register event handlers
        # WASD controls (runner)
        canvas.onkeypress(lambda: self._move_forward(self.step_move), 'w')
        canvas.onkeypress(lambda: self._move_forward(self.step_move), 'W')
        canvas.onkeypress(lambda: self._move_backward(self.step_move), 's')
        canvas.onkeypress(lambda: self._move_backward(self.step_move), 'S')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'a')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'A')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'd')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'D')
        # Optional: quick turn with QE
        canvas.onkeypress(lambda: self.left(self.step_turn * 2), 'q')
        canvas.onkeypress(lambda: self.right(self.step_turn * 2), 'e')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

    # Helpers to keep within bounds
    def _clamp_to_bounds(self):
        x, y = self.pos()
        x = max(-self._bound, min(self._bound, x))
        y = max(-self._bound, min(self._bound, y))
        if (x, y) != self.pos():
            self.setpos(x, y)

    def _move_forward(self, step):
        super().forward(step)
        self._clamp_to_bounds()

    def _move_backward(self, step):
        super().backward(step)
        self._clamp_to_bounds()

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

class ChaserAI(turtle.RawTurtle):
    """A simple chasing AI that steers towards the opponent and moves forward."""
    def __init__(self, canvas, step_move=8, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self._bound = 340

    def _bearing_to(self, target_pos):
        x, y = self.pos()
        tx, ty = target_pos
        ang = math.degrees(math.atan2(ty - y, tx - x))
        return ang % 360

    def _angle_diff(self, a, b):
        # Smallest difference from heading a to b in [-180, 180]
        d = (b - a + 540) % 360 - 180
        return d

    def run_ai(self, opp_pos, opp_heading):
        desired = self._bearing_to(opp_pos)
        current = self.heading()
        diff = self._angle_diff(current, desired)
        # Turn toward target but clamp by step_turn
        turn = max(-self.step_turn, min(self.step_turn, diff))
        if turn > 0:
            self.left(turn)
        elif turn < 0:
            self.right(-turn)
        # Move forward
        self.forward(self.step_move)
        # clamp
        x, y = self.pos()
        x = max(-self._bound, min(self._bound, x))
        y = max(-self._bound, min(self._bound, y))
        if (x, y) != self.pos():
            self.setpos(x, y)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # Roles: runner = player (WASD), chaser = AI
    runner = ManualMover(screen, step_move=12, step_turn=15)
    runner.color('blue')
    chaser = ChaserAI(screen, step_move=10, step_turn=10)
    chaser.color('red')

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
