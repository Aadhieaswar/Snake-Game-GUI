# built-in modules
from random import randint

# installed modules
import tkinter as tk
from PIL import Image, ImageTk

# constants
APP_NAME = "Snacking Snake"
SIZE = 700  # set dimensions of the screen
STARTED = False  # determines whether the game has started or not
MOVE_INC = 20
GAME_SPEED = 75

# class Snake_App start
class SnakeApp(tk.Canvas):

    def __init__(self):
        # creates the canvas
        super().__init__(width=SIZE, height=SIZE, background="#1d2124")

        # show the end of space for the snake to move
        self.create_rectangle(10, 10, 693, 693, outline="lightblue")

        # score
        self.score = 0
        self.create_text(65, 25, text=f"Score: {self.score}", tag="score", fill="#fff", font=("Fira Code", 14))

        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        # positions of the snake and food to be used later
        self.snake_pos = [(100, 300), (80, 300), (60, 300)]
        self.food_pos = self.change_food_pos()

        self.bind_all("<space>", self.start_game)

        # loads the game graphics (the snake and food)
        self.load_assets()
        self.create_obj()

        # creates welcome text before starting the game
        self.create_text(
            350, 350,
            text="Press <space> to start the Game",
            fill="lightblue",
            font=("Fira Code", 24),
            tag="welcome_msg"
        )

    def start_game(self, event):
        print(event)
        msg = self.find_withtag("welcome_msg")
        self.delete(msg)
        self.after(GAME_SPEED,self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_img = Image.open("./assets/Snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_img)

            self.food_img = Image.open("./assets/Food.png")
            self.food = ImageTk.PhotoImage(self.food_img)
        except IOError as error:
            print(error)
            screen.destroy()

    def create_obj(self):
        for x, y in self.snake_pos:
            self.create_image(x, y, image=self.snake_body, tag="snake")

        self.create_image(*self.food_pos, image=self.food, tag="food")

    def move_snake(self):
        x_pos, y_pos = self.snake_pos[0]

        if self.direction == "Left":
            new_head_pos = (x_pos - MOVE_INC, y_pos)
        if self.direction == "Right":
            new_head_pos = (x_pos + MOVE_INC, y_pos)
        if self.direction == "Up":
            new_head_pos = (x_pos, y_pos - MOVE_INC)
        if self.direction == "Down":
            new_head_pos = (x_pos, y_pos + MOVE_INC)

        self.snake_pos = [new_head_pos] + self.snake_pos[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_pos):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return

        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        x_pos, y_pos = self.snake_pos[0]

        return (
            x_pos in (0, 700)
            or y_pos in (700, 0)
            or (x_pos, y_pos) in self.snake_pos[1:]
        )

    def on_key_press(self, event):
        new_direction = event.keysym
        all_directions = ("Left", "Right", "Up", "Down")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_pos[0] == self.food_pos:
            self.score += 1
            self.snake_pos.append(self.snake_pos[-1])

            self.create_image(*self.snake_pos[-1], image=self.snake_body, tag="snake")

            self.food_pos = self.change_food_pos()
            self.coords(self.find_withtag("food"), self.food_pos)

        score = self.find_withtag("score")
        self.itemconfigure(score, text=f"score: {self.score}", tag="score")

    def change_food_pos(self):
        while True:
            x_pos = randint(1, 29) * MOVE_INC
            y_pos = randint(2, 31) * MOVE_INC
            new_food_pos = (x_pos, y_pos)

            if new_food_pos not in self.snake_pos:
                return new_food_pos

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"GAME OVER! Your Score is {self.score}",
            fill="#fff",
            font=("Fira Code", 24)
        )

# class Snake_App end
screen = tk.Tk()
screen.title(APP_NAME)  # set name of the application
screen.resizable(False, False)

field = SnakeApp()
field.pack()

screen.mainloop()
