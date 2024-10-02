import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chasers, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chasers = chasers
        self.catch_radius2 = catch_radius**2
        self.score = 0
        self.start_time = time.time()  # 게임 시작 시간
        self.items = []
        self.game_over_flag = False

        # Initialize 'runner' and 'chasers'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        for chaser in self.chasers:
            chaser.shape('turtle')
            chaser.color('red')
            chaser.penup()

        # Instantiate another turtle for drawing text
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        for chaser in self.chasers:
            p = self.runner.pos()
            q = chaser.pos()
            dx, dy = p[0] - q[0], p[1] - q[1]
            if dx**2 + dy**2 < self.catch_radius2:
                return True
        return False

    def check_item_collision(self):
        # 아이템과 충돌 여부 확인
        for item in self.items:
            if self.runner.distance(item) < 20:
                item.hideturtle()
                self.items.remove(item)
                self.score += 10
                self.create_random_item()  # 아이템을 먹으면 즉시 새로운 아이템 생성

    def create_random_item(self):
        # 무작위 위치에 아이템 생성
        item = turtle.RawTurtle(self.canvas)
        item.shape('circle')
        item.color('green')
        item.penup()
        item.setpos(random.randint(-300, 300), random.randint(-300, 300))
        self.items.append(item)

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        
        for i, chaser in enumerate(self.chasers):
            chaser.setpos((+init_dist / 2 - i * 50, 0))
            chaser.setheading(180)

        self.start_time = time.time()  # 게임 시작 시간 초기화

        # 처음 시작 시 아이템 생성
        self.create_random_item()

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def game_over(self, message):
        self.drawer.clear()
        self.drawer.setpos(0, 0)  # 중앙으로 설정
        self.drawer.write(message, align="center", font=("Arial", 24, "bold"))  # 중앙 정렬
        self.game_over_flag = True

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)  # 시작 시간부터 경과한 시간 계산
        return elapsed_time

    def step(self):
        if not self.game_over_flag:
            self.runner.run_ai(None, None)
            for chaser in self.chasers:
                chaser.run_ai(self.runner.pos(), self.runner.heading())

            is_catched = self.is_catched()

            self.check_item_collision()

            self.drawer.clear()  # 이전 글씨를 모두 지웁니다.
            self.drawer.penup()
            self.drawer.setpos(-300, 300)
            self.drawer.write(f'Score: {self.score}', font=("Arial", 16, "normal"))  # 점수 출력
            self.drawer.setpos(-300, 250)  # 타이머 위치
            
            # 타이머 업데이트
            timer = self.update_timer()
            self.drawer.write(f'Time: {timer} sec', font=("Arial", 16, "normal"))  # 타이머 출력

            # 게임 오버 조건
            if is_catched:
                self.game_over('Game Over! You were caught!')
            elif timer >= 60:  # 60초가 지났는지 확인
                if self.score < 50:
                    self.game_over('Game Over! You didn\'t reach 50 points!')
                else:
                    self.game_over('Congratulations! You reached 50 points!')

            else:
                self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class Chaser(turtle.RawTurtle):
    def __init__(self, canvas, step_move=15, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, runner_pos, runner_heading):
        if runner_pos is not None:
            self.setheading(self.towards(runner_pos))
            self.forward(self.step_move)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Turtle Runaway')
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    runner = ManualMover(screen)
    chasers = [Chaser(screen) for _ in range(3)]  # 여러 마리의 chaser

    game = RunawayGame(screen, runner, chasers)
    game.start()
    screen.mainloop()
