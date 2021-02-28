from tkinter import *
from PIL import Image, ImageTk
from rect import *


class Sprite:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = None

    def move(self, x, y):
        self.canvas.move(self.id, x, y)

    def rotate(self, angle):
        self.canvas.rotate(self.id, angle)

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


class Triangle(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, color=color)

    @property
    def coords(self):
        xy = self.canvas.coords(self.id)
        return BoundingRect(xy[0], xy[1], xy[4], xy[3])


class Rect(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x4, y4, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, x4, y4, color=color)

    @property
    def coords(self):
        xy = self.canvas.coords(self.id)
        return BoundingRect(xy[0], xy[1], xy[4], xy[5])


class Pentagon(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, color=color)

    @property
    def coords(self):
        xy = self.canvas.coords(self.id)
        return BoundingRect(xy[2], xy[1], xy[8], xy[5])


class Hexagon(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, color=color)

    @property
    def coords(self):
        xy = self.canvas.coords(self.id)
        return BoundingRect(xy[2], xy[1], xy[10], xy[7])


class Circle(Sprite):
    def __init__(self, canvas, x1, y1, x2, y2, color="black"):
        super().__init__(canvas)
        self.id = canvas.create_arc(x1, y1, x2, y2, extent=359.9, style=PIESLICE, fill=color, outline=color)

    @property
    def coords(self):
        xy = self.canvas.coords(self.id)
        return BoundingRect(xy[0], xy[1], xy[2], xy[3])


class PlayerSprite(Sprite):
    def __init__(self, canvas):
        super().__init__(canvas)
        # Star image creation
        self.image = ImageTk.PhotoImage(Image.open("./sprite.png"))
        self.id = canvas.create_image(720, 400, image=self.image)

        # Motion bindings
        canvas.bind_all('<Key-Left>', self.move_left)
        canvas.bind_all('<Key-Right>', self.move_right)

    def move_left(self, event):
        self.canvas.move(self.id, -10, 0)

    def move_right(self, event):
        self.canvas.move(self.id, 10, 0)


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
