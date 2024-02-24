from tkinter import *
import random
import time

# Define colors for the game
bgc = 'black'
grid_col = 'black'
food_col = '#F12A00'

# Define game parameters
grid_size = (20, 20)
sq_size = 20
game_speed = 5
time_int = 100

grad_start_col = "#1134A6"
grad_end_color = "#74E72B"

# Create the main Tkinter window
window = Tk()
window.title('Snake Game')
window.resizable(True, True)

# Initialize variables for high score, current score, and timer
high_score = 0
score = 0
timer_seconds = 0

# Create labels for high score, current score, and timer
label_high_score = Label(window, text="High Score: {}".format(high_score), font=('sans-serif', 20), fg="white", bg=bgc)
label_high_score.grid(row=0, column=0, pady=10, padx=10)

label_score = Label(window, text="Score: {}".format(score), font=('sans-serif', 20), fg="white", bg=bgc)
label_score.grid(row=0, column=1, pady=10, padx=10)

label_timer = Label(window, text="Time: {}s".format(timer_seconds), font=('sans-serif', 20), fg="white", bg=bgc)
label_timer.grid(row=0, column=2, pady=10, padx=10)

# Create the canvas for the game grid
canvas = Canvas(window, bg=bgc, width=grid_size[0] * sq_size, height=grid_size[1] * sq_size)
canvas.grid(row=1, column=0, columnspan=3)

# Initialize variables for snake and game state
snake_cord = []
curr_dir = "down"
next_dir = "down"

food_pos = (0, 0)

is_game_running = False

# Function to start the game
def start_game():
    global is_game_running, score, timer_seconds, start_time, snake_cord
    is_game_running = True
    score = 0
    timer_seconds = 0
    start_time = time.time()
    label_score.config(text="Score: {}".format(score))
    label_timer.config(text="Time: {}s".format(timer_seconds))
    initialize_game()

# Function to initialize the game state
def initialize_game():
    global snake_cord
    snake_cord = [(grid_size[0] // 2, grid_size[1] // 2)]
    move_food()

# Function to update the game state
def update():
    snakestep()

# Function to check collisions in the game
def check_coll():
    snake_coll()
    food_coll()

# Function to draw game elements on the canvas
def elem():
    canvas.delete("all")
    grid()
    drsnake()
    drfood()

# Function to handle game over
def game_over():
    global is_game_running, high_score
    is_game_running = False
    canvas.delete("all")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    font_size = min(canvas_width // 18, canvas_height // 8)

    canvas.create_text(
        canvas_width / 2.0,
        canvas_height / 2.0,
        text="Game Over\nPress Space to Restart",
        font=("consolas", font_size),
        fill="#F12A00")

    if score > high_score:
        high_score = score
        label_high_score.config(text="High Score: {}".format(high_score))

    window.bind("<space>", restart_game)

# Function to restart the game
def restart_game(event):
    global is_game_running, score, timer_seconds, start_time, snake_cord, curr_dir, next_dir
    is_game_running = True
    score = 0
    timer_seconds = 0
    start_time = time.time()
    label_score.config(text="Score: {}".format(score))
    label_timer.config(text="Time: {}s".format(timer_seconds))
    initialize_game()
    curr_dir = "down"
    next_dir = "down"
    window.unbind("<space>")
    game_loop()

# Function to run the game loop
def game_loop():
    global is_game_running, timer_seconds, start_time
    if is_game_running == True:
        update()
        check_coll()
        elem()

        update_time = int(900 / game_speed)
        window.after(update_time, game_loop)

        elapsed_time = time.time() - start_time
        timer_seconds = int(elapsed_time)
        label_timer.config(text="Time: {}s".format(timer_seconds))

    else:
        game_over()

# Function to draw the game grid
def grid():
    canvas_width = grid_size[0] * sq_size
    canvas_height = grid_size[1] * sq_size

    for ix in range(grid_size[0] + 1):
        xpos = ix * sq_size
        canvas.create_line(xpos, 0, xpos, canvas_height, width=1, fill=grid_col)

    for iy in range(grid_size[1] + 1):
        ypos = iy * sq_size
        canvas.create_line(0, ypos, canvas_width, ypos, width=1, fill=grid_col)

# Function to update the snake's position
def snakestep():
    global snake_cord, curr_dir, is_game_running

    head = snake_cord[0]
    snake_cord = snake_cord[:-1]

    newhead = None
    if next_dir == "down":
        newhead = (head[0], head[1] + 1)
    elif next_dir == "up":
        newhead = (head[0], head[1] - 1)
    elif next_dir == "left":
        newhead = (head[0] - 1, head[1])
    elif next_dir == "right":
        newhead = (head[0] + 1, head[1])

    headx, heady = newhead

    if headx < 0 or headx >= grid_size[0] or heady < 0 or heady >= grid_size[1]:
        is_game_running = False

    snake_cord.insert(0, newhead)
    curr_dir = next_dir

# Function to draw the snake on the canvas
def drsnake():
    for i, (x, y) in enumerate(snake_cord):
        x1 = x * sq_size
        y1 = y * sq_size

        x2 = (x + 1) * sq_size
        y2 = (y + 1) * sq_size

        gradient_color = blend_colors(grad_start_col, grad_end_color, i / len(snake_cord))
        canvas.create_rectangle(x1, y1, x2, y2, fill=gradient_color)

# Function to blend colors for gradient effect
def blend_colors(color1, color2, ratio):
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = int(r1 * (1 - ratio) + r2 * ratio)
    g = int(g1 * (1 - ratio) + g2 * ratio)
    b = int(b1 * (1 - ratio) + b2 * ratio)
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

# Function to check snake collisions
def snake_coll():
    global is_game_running
    head = snake_cord[0]
    headx, heady = head

    if headx < 0 or headx >= grid_size[0] or heady < 0 or heady >= grid_size[1]:
        is_game_running = False

    if head in snake_cord[1:]:
        is_game_running = False

# Function to handle directional changes
def change_dir(new_dir):
    global next_dir

    if (new_dir == "up" and curr_dir == "down") or (new_dir == "down" and curr_dir == "up") or \
            (new_dir == "left" and curr_dir == "right") or (new_dir == "right" and curr_dir == "left"):
        return
    next_dir = new_dir

# Bind arrow keys to change snake direction
window.bind("<Left>", lambda event: change_dir("left"))
window.bind("<Right>", lambda event: change_dir("right"))
window.bind("<Up>", lambda event: change_dir("up"))
window.bind("<Down>", lambda event: change_dir("down"))

# Function to move the food to a random position
def move_food():
    global food_pos

    newx = random.randint(0, grid_size[0] - 1)
    newy = random.randint(0, grid_size[1] - 1)

    food_pos = (newx, newy)
    if food_pos in snake_cord:
        move_food()

# Initialize food position
move_food()

# Function to handle food collisions
def food_coll():
    global score
    head = snake_cord[0]

    if head == food_pos:
        move_food()
        increase_score()

        snake_cord.append(snake_cord[-1])

# Function to draw the food on the canvas
def drfood():
    x1 = food_pos[0] * sq_size
    y1 = food_pos[1] * sq_size
    x2 = (food_pos[0] + 1) * sq_size
    y2 = (food_pos[1] + 1) * sq_size

    canvas.create_oval(x1, y1, x2, y2, fill=food_col)

# Function to increase the score
def increase_score():
    global score
    score = score + 1
    label_score.config(text="Score: {}".format(score))

# Function to start the game on pressing the space bar
def on_space_bar(event):
    if not is_game_running:
        start_game()

# Bind space bar to start the game
window.bind("<space>", on_space_bar)

# Start the game loop
if __name__ == '__main__':
    window.after(time_int, game_loop)
    window.mainloop()
