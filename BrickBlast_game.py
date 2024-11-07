import tkinter as tk
import random

# Initialize main window
window = tk.Tk()
window.title("Brick Breaker")

# Canvas dimensions
canvas_width = 600
canvas_height = 400
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Paddle settings
paddle_width = 100
paddle_height = 10
paddle_x = (canvas_width // 2) - (paddle_width // 2)
paddle_y = canvas_height - 30
paddle_speed = 20
paddle = canvas.create_rectangle(paddle_x, paddle_y, paddle_x + paddle_width, paddle_y + paddle_height, fill="blue")

# Ball settings
ball_size = 20
ball_x_speed = 3
ball_y_speed = -3
ball = canvas.create_oval(paddle_x + paddle_width // 2 - ball_size // 2, paddle_y - ball_size, 
                          paddle_x + paddle_width // 2 + ball_size // 2, paddle_y, fill="white")

# Brick settings
brick_rows = 5
brick_cols = 8
brick_width = canvas_width // brick_cols
brick_height = 20
bricks = []

# Create bricks
for i in range(brick_rows):
    brick_row = []
    for j in range(brick_cols):
        brick_x = j * brick_width
        brick_y = i * brick_height + 30
        brick = canvas.create_rectangle(brick_x, brick_y, brick_x + brick_width, brick_y + brick_height, fill="green")
        brick_row.append(brick)
    bricks.append(brick_row)

# Game variables
lives = 3
score = 0
game_over = False

# Display score and lives
score_text = canvas.create_text(50, 10, text=f"Score: {score}", fill="white", font=("Arial", 14))
lives_text = canvas.create_text(canvas_width - 50, 10, text=f"Lives: {lives}", fill="white", font=("Arial", 14))

# Move paddle left or right
def move_paddle(event):
    global paddle_x
    if event.keysym == "Left" and paddle_x > 0:
        canvas.move(paddle, -paddle_speed, 0)
        paddle_x -= paddle_speed
    elif event.keysym == "Right" and paddle_x < canvas_width - paddle_width:
        canvas.move(paddle, paddle_speed, 0)
        paddle_x += paddle_speed

window.bind("<Left>", move_paddle)
window.bind("<Right>", move_paddle)

# Ball movement and collision
def move_ball():
    global ball_x_speed, ball_y_speed, ball, game_over, score, lives
    
    # Move the ball
    canvas.move(ball, ball_x_speed, ball_y_speed)
    ball_pos = canvas.coords(ball)
    
    # Ball collision with walls
    if ball_pos[0] <= 0 or ball_pos[2] >= canvas_width:  # Left or right wall
        ball_x_speed *= -1
    if ball_pos[1] <= 0:  # Top wall
        ball_y_speed *= -1

    # Ball collision with paddle
    paddle_pos = canvas.coords(paddle)
    if (paddle_pos[0] < ball_pos[0] < paddle_pos[2] or paddle_pos[0] < ball_pos[2] < paddle_pos[2]) \
            and ball_pos[3] >= paddle_pos[1]:
        ball_y_speed *= -1

    # Ball collision with bricks
    for row in bricks:
        for brick in row:
            if brick is not None:
                brick_pos = canvas.coords(brick)
                if (brick_pos[0] < ball_pos[0] < brick_pos[2] or brick_pos[0] < ball_pos[2] < brick_pos[2]) \
                        and (brick_pos[1] < ball_pos[1] < brick_pos[3] or brick_pos[1] < ball_pos[3] < brick_pos[3]):
                    canvas.delete(brick)
                    row[row.index(brick)] = None
                    ball_y_speed *= -1
                    score += 10
                    canvas.itemconfig(score_text, text=f"Score: {score}")

    # Check if ball hits the bottom (lose a life)
    if ball_pos[3] >= canvas_height:
        lives -= 1
        canvas.itemconfig(lives_text, text=f"Lives: {lives}")
        canvas.coords(ball, paddle_x + paddle_width // 2 - ball_size // 2, paddle_y - ball_size,
                      paddle_x + paddle_width // 2 + ball_size // 2, paddle_y)
        if lives == 0:
            canvas.create_text(canvas_width // 2, canvas_height // 2, text="Game Over", fill="red", font=("Arial", 24))
            game_over = True

    # Continue moving the ball if game is not over
    if not game_over:
        window.after(20, move_ball)

# Start the game
move_ball()

window.mainloop()
