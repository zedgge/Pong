import turtle
import random

def update_score(l_score, r_score, player, score_board):
    if player == 'l':
        l_score += 1
    else:
        r_score += 1

    score_board.clear()
    score_board.write('Left Player: {} -- Right Player: {}'.format(
        l_score, r_score), align='center', font=('Arial', 24, 'normal'))
    return l_score, r_score, score_board


def setup_game():
    screen = turtle.Screen()
    screen.title('Pong Arcade Game')
    screen.bgcolor('white')
    screen.setup(width=1000, height=600)
    screen.tracer(0)

    l_paddle = turtle.Turtle()
    l_paddle.speed(0)
    l_paddle.shape('square')
    l_paddle.color('red')
    l_paddle.shapesize(stretch_wid=6, stretch_len=2)
    l_paddle.penup()
    l_paddle.goto(-400, 0)

    r_paddle = turtle.Turtle()
    r_paddle.speed(0)
    r_paddle.shape('square')
    r_paddle.color('black')
    r_paddle.shapesize(stretch_wid=6, stretch_len=2)
    r_paddle.penup()
    r_paddle.goto(400, 0)

    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape('circle')
    ball.color('blue')
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 3
    ball.dy = -3

    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.color('blue')
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, 260)
    score_board.write('Left Player: 0 -- Right Player: 0',
                      align='center', font=('Arial', 24, 'normal'))

    return screen, ball, l_paddle, r_paddle, score_board


def pong_game():
    # Ask user for player mode
    mode = turtle.textinput("Game Mode", "Enter 1 for single player, 2 for two players:")
    single_player = (mode == '1')

    screen, ball, l_paddle, r_paddle, score_board = setup_game()
    l_score = 0
    r_score = 0
    max_speed = 10
    paddle_height = 120

    def l_paddle_up():
        if l_paddle.ycor() < 250:
            l_paddle.sety(l_paddle.ycor() + 20)

    def l_paddle_down():
        if l_paddle.ycor() > -250:
            l_paddle.sety(l_paddle.ycor() - 20)

    def r_paddle_up():
        if r_paddle.ycor() < 250:
            r_paddle.sety(r_paddle.ycor() + 20)

    def r_paddle_down():
        if r_paddle.ycor() > -250:
            r_paddle.sety(r_paddle.ycor() - 20)

    screen.listen()
    screen.onkeypress(l_paddle_up, 'e')
    screen.onkeypress(l_paddle_down, 'x')

    if not single_player:
        screen.onkeypress(r_paddle_up, 'Up')
        screen.onkeypress(r_paddle_down, 'Down')

    def game_loop():
        nonlocal l_score, r_score

        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Top/bottom walls
        if ball.ycor() > 280 or ball.ycor() < -280:
            ball.sety(min(max(ball.ycor(), -280), 280))
            ball.dy *= -1

        # Score handling
        if ball.xcor() > 490:
            ball.goto(0, 0)
            ball.dx = -3
            ball.dy = -3
            l_score, r_score, _ = update_score(l_score, r_score, 'l', score_board)

        elif ball.xcor() < -490:
            ball.goto(0, 0)
            ball.dx = 3
            ball.dy = 3
            l_score, r_score, _ = update_score(l_score, r_score, 'r', score_board)

        # Paddle collisions
        if (350 < ball.xcor() < 370) and (r_paddle.ycor() - paddle_height / 2 < ball.ycor() < r_paddle.ycor() + paddle_height / 2):
            ball.setx(350)
            ball.dx *= -1.05
            ball.dy *= 1.05

        if (-370 < ball.xcor() < -350) and (l_paddle.ycor() - paddle_height / 2 < ball.ycor() < l_paddle.ycor() + paddle_height / 2):
            ball.setx(-350)
            ball.dx *= -1.05
            ball.dy *= 1.05

        # Clamp speed
        ball.dx = max(min(ball.dx, max_speed), -max_speed)
        ball.dy = max(min(ball.dy, max_speed), -max_speed)

        # AI behavior
        if single_player:
            if ball.dx > 0:
                target_y = ball.ycor() + random.randint(-20, 20)
                if abs(r_paddle.ycor() - target_y) > 10:
                    if r_paddle.ycor() < target_y:
                        r_paddle.sety(r_paddle.ycor() + random.randint(6, 10))
                    elif r_paddle.ycor() > target_y:
                        r_paddle.sety(r_paddle.ycor() - random.randint(6, 10))

        screen.update()
        screen.ontimer(game_loop, 16)  # 60 FPS

    game_loop()
    screen.mainloop()


if __name__ == '__main__':
    pong_game()
