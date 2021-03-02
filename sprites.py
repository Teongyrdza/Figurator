from tkinter import *
from PIL import Image, ImageTk
from rect import *
from math import sin, cos, pi
import logging

DEBUG = False


class Sprite:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = None
        if DEBUG:
            self.text_id = None

    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        if DEBUG:
            self.canvas.move(self.text_id, x, y)

    def rotate(self, degrees):
        radians = degrees / 180 * pi
        """
        hypot = self.coords.width / 2
        points = self.canvas.coords(self.id)
        x_points = points[0::2]
        y_points = points[1::2]
        adj_x = hypot * cos(radians)
        adj_y = hypot * sin(radians)

        # Adjust x points
        x_points = [xp + adj_x for xp in x_points]

        # Adjust y points
        y_points = [yp + adj_y for yp in y_points]

        new_points = []
        for i in range(len(x_points)):
            new_points.append(x_points[i])
            new_points.append(y_points[i])

        self.canvas.coords(self.id, new_points)
        """

        self.canvas.rotate(self.id, self.coords.cx, self.coords.cy, radians)

    def draw_id(self):
        if DEBUG:
            self.text_id = self.canvas.create_text(
                self.coords.cx,
                self.coords.cy,
                fill="white",
                font="System 20",
                text=f"{self.id}"
            )

    @property
    def coords(self) -> BoundingRect:
        xy = self.canvas.coords(self.id)
        return BoundingRect(xy[0], xy[1], xy[2], xy[3])

    @coords.setter
    def coords(self, new_coords):
        adj_x = new_coords.x1 - self.coords.x1
        adj_y = new_coords.y1 - self.coords.y1
        self.move(adj_x, adj_y)


class Polygon(Sprite):
    def __init__(self, canvas, *points, color="black"):
        super().__init__(canvas)
        self.num_sides = len(points) // 2
        self.id = canvas.create_polygon(points, fill=color)
        self.draw_id()

    @property
    def coords(self) -> BoundingRect:
        points = self.canvas.coords(self.id)
        x_points = points[0::2]
        y_points = points[1::2]
        x1 = min(x_points)
        y1 = min(y_points)
        x2 = max(x_points)
        y2 = max(y_points)
        return BoundingRect(x1, y1, x2, y2)


class Triangle(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, color=color)


class Rect(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x4, y4, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, x4, y4, color=color)


class Pentagon(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, color=color)


class Hexagon(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, color=color)


class Circle(Sprite):
    def __init__(self, canvas, x1, y1, x2, y2, color="black"):
        super().__init__(canvas)
        self.id = canvas.create_arc(x1, y1, x2, y2, extent=359.9, style=PIESLICE, fill=color, outline=color)
        self.draw_id()


class PlayerSprite(Sprite):
    move_amount = 20

    def __init__(self, canvas):
        super().__init__(canvas)
        # Star image creation
        self.image = ImageTk.PhotoImage(Image.open("./sprite.png"))
        self.id = canvas.create_image(720, 400, image=self.image)
        self.draw_id()

        # Motion bindings
        canvas.bind_all('<Key-Left>', self.move_left)
        canvas.bind_all('<Key-Right>', self.move_right)
        canvas.bind_all('<Key-Up>', self.move_up)
        canvas.bind_all('<Key-Down>', self.move_down)
        canvas.bind_all('<Return>', self.hide)

    @property
    def coords(self) -> BoundingRect:
        xy = self.canvas.coords(self.id)
        cx, cy = xy[0], xy[1]
        width, height = self.image.width(), self.image.height()
        return BoundingRect(cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2)

    def move_left(self, event):
        move_amount = self.__class__.move_amount
        self.move(-move_amount, 0)

    def move_right(self, event):
        move_amount = self.__class__.move_amount
        self.move(move_amount, 0)

    def move_up(self, event):
        move_amount = self.__class__.move_amount
        self.move(0, -move_amount)

    def move_down(self, event):
        move_amount = self.__class__.move_amount
        self.move(0, move_amount)

    def hide(self):
        """Hide the sprite underneath the screen."""

        logging.debug("Player Sprite is hiding")

        window_height = self.canvas.master.winfo_height()
        new_coords = BoundingRect(self.coords.x1, self.coords.y1 + window_height, self.coords.x2, self.coords.y2 + window_height)
        self.coords = new_coords


"""
tk = Tk()
canvas = Canvas(tk, width=1435, height=765)
canvas.pack()

circle = Circle(canvas, 10, 10, 200, 200, color="brown")
print(f"Circle's bounding rect is {circle.coords}")

triangle = Triangle(canvas, 300, 200, 300, 400, 500, 300, color="green")
print(f"Triangle's bounding rect is {triangle.coords}")

rect = Rect(canvas, 300, 500, 300, 600, 700, 600, 700, 500, color="yellow")
print(f"Rectangle's bounding rect is {rect.coords}")

pentagon = Pentagon(canvas, 900, 400, 750, 600, 850, 800, 950, 800, 1050, 600, color="purple")
print(f"Pentagon's bounding rect is  {pentagon.coords}")

hexagon = Hexagon(canvas, 1000, 20, 850, 220, 850, 420, 1000, 620, 1150, 420, 1150, 220,  color="pink")
print(f"Hexagon's bounding rect is  {hexagon.coords}")
"""
