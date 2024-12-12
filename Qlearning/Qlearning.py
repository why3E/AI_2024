import time
import numpy as np
import random
import tkinter as tk
from collections import defaultdict
from PIL import ImageTk, Image

UNIT = 100
HEIGHT, WIDTH = 5, 5

class Env(tk.Tk):
    def __init__(self):
        super().__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Q Learning')
        self.geometry(f'{HEIGHT * UNIT}x{WIDTH * UNIT}')
        self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        self.texts = []

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white', height=HEIGHT * UNIT, width=WIDTH * UNIT)
        [canvas.create_line(c, 0, c, HEIGHT * UNIT) for c in range(0, WIDTH * UNIT, UNIT)]
        [canvas.create_line(0, r, WIDTH * UNIT, r) for r in range(0, HEIGHT * UNIT, UNIT)]
        self.rectangle = canvas.create_image(50, 50, image=self.shapes[0])
        self.triangle1 = canvas.create_image(250, 150, image=self.shapes[1])
        self.triangle2 = canvas.create_image(150, 250, image=self.shapes[1])
        self.circle = canvas.create_image(250, 250, image=self.shapes[2])
        canvas.pack()
        return canvas

    def load_images(self):
        return tuple(ImageTk.PhotoImage(Image.open(f"img/{name}.png").resize((65, 65))) for name in ["rectangle", "triangle", "circle"])

    def text_value(self, row, col, contents, action, font='Helvetica', size=10, style='normal', anchor="center"):
        if action == 0:  # Up
            origin_x, origin_y = UNIT // 2, UNIT // 5
        elif action == 1:  # Down
            origin_x, origin_y = UNIT // 2, UNIT - UNIT // 5
        elif action == 2:  # Left
            origin_x, origin_y = UNIT // 5, UNIT // 2
        elif action == 3:  # Right
            origin_x, origin_y = UNIT - UNIT // 5, UNIT // 2

        x, y = col * UNIT + origin_x, row * UNIT + origin_y
        font = (font, str(size), style)
        text = self.canvas.create_text(x, y, fill="black", text=contents, font=font, anchor=anchor)
        self.texts.append(text)

    def print_value_all(self, q_table):
        [self.canvas.delete(text) for text in self.texts]
        self.texts.clear()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                state = str([i, j])
                if state in q_table:
                    for action, value in enumerate(q_table[state]):
                        self.text_value(i, j, f"{value:.2f}", action)

    def coords_to_state(self, coords):
        x = int((coords[0] - 50) / UNIT)
        y = int((coords[1] - 50) / UNIT)
        return [x, y]

    def state_to_coords(self, state):
        x = int(state[0] * UNIT + 50)
        y = int(state[1] * UNIT + 50)
        return [x, y]

    def reset(self):
        self.canvas.coords(self.rectangle, 50, 50)
        self.render()
        return [0, 0]

    def step(self, action):
        moves = [np.array([0, -UNIT]), np.array([0, UNIT]), np.array([-UNIT, 0]), np.array([UNIT, 0])]
        current = np.array(self.canvas.coords(self.rectangle))
        next_coords = current + moves[action]
        if 0 <= next_coords[0] < WIDTH * UNIT and 0 <= next_coords[1] < HEIGHT * UNIT:
            self.canvas.coords(self.rectangle, *next_coords)
        self.canvas.tag_raise(self.rectangle)
        self.render()
        next_coords = self.canvas.coords(self.rectangle)
        if next_coords == self.canvas.coords(self.circle):
            return [2, 2], 100, True
        elif next_coords in [self.canvas.coords(self.triangle1), self.canvas.coords(self.triangle2)]:
            return [1, 1], -100, True
        return [int(next_coords[1] // UNIT), int(next_coords[0] // UNIT)], 0, False

    def render(self):
        time.sleep(0.01)
        self.update()

class QLearning:
    def __init__(self, actions):
        self.actions = actions
        self.q_table = defaultdict(lambda: [0.0] * len(actions))
        self.step_size, self.discount_factor, self.epsilon = 0.01, 0.9, 0.9

    def learn(self, state, action, reward, next_state):
        q_1 = self.q_table[state][action]
        q_2 = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.step_size * (q_2 - q_1)

    def get_action(self, state):
        if np.random.rand() > self.epsilon:
            return np.random.choice(self.actions)
        return random.choice([i for i, q in enumerate(self.q_table[state]) if q == max(self.q_table[state])])

if __name__ == "__main__":
    env = Env()
    agent = QLearning(actions=list(range(env.n_actions)))

    for episode in range(50):
        state = env.reset()
        while True:
            action = agent.get_action(str(state))
            next_state, reward, done = env.step(action)
            agent.learn(str(state), action, reward, str(next_state))
            env.print_value_all(agent.q_table)
            state = next_state
            if done:
                break
    env.mainloop()
