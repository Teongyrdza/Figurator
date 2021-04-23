from tkinter import *
from rect import *
from point import *
from math import sin, cos, pi
from utils import random_double
import logging
import random

# TODO: Transition Sprite.coords to use Canvas.bbox()
DEBUG = False


class Sprite:
    def __init__(self, canvas, id):
        self.canvas = canvas
        self.id = id
        if DEBUG:
            self.text_id = None
            self.draw_id()

        self.movement = self.minMovement = self.maxMovement = None
        self.rotation = self.minRotation = self.maxRotation = None

    def __del__(self):
        self.canvas.delete(self.id)
        if DEBUG:
            self.canvas.delete(self.text_id)

    def config(self, movement, minMovement, maxMovement, rotation, minRotation, maxRotation):
        self.movement = movement
        self.minMovement = minMovement
        self.maxMovement = maxMovement
        self.rotation = rotation
        self.minRotation = minRotation
        self.maxRotation = maxRotation

    def act(self, ratio: float):
        pass

    def move(self, x, y):
        logging.debug(f"Moving sprite {self.id} by x: {x:.2f}, y: {x:.2f} pixels")

        self.canvas.move(self.id, x, y)
        if DEBUG:
            self.canvas.move(self.text_id, x, y)

    def rotate(self, degrees):
        logging.debug(f"Rotating sprite {self.id} by {degrees:.2f} degrees")

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
    def screen(self) -> BoundingRect:
        return BoundingRect(0, 0, self.canvas.master.winfo_width(), self.canvas.master.winfo_height())

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

    @coords.setter
    def coords(self, new_coords):
        adj_x = new_coords.x1 - self.coords.x1
        adj_y = new_coords.y1 - self.coords.y1
        self.move(adj_x, adj_y)

    @property
    def points(self) -> list[Point]:
        points = self.canvas.coords(self.id)
        x_points = points[0::2]
        y_points = points[1::2]
        return list(map(lambda x, y: Point(x, y), x_points, y_points))


@collided.add
def collided(s1: Sprite, s2: Sprite) -> bool:
    return collided_left(s1, s2) or collided_right(s1, s2) or collided_top(s1, s2) or collided_bottom(s1, s2)


@collided_left.add
def collided_left(s1: Sprite, s2: Sprite) -> bool:
    if not collided_left(s1.coords, s2.coords):
        return False

    left_points = s2.points
    right_points = s1.points
    rightest = max(left_points, key=lambda p: p.x)  # Rightest point that collides with s1
    collided_points = [point for point in right_points if
                       point.x < rightest.x]  # Points that possibly collide with rightest

    if not collided_points:
        return False

    highest_collided = min(collided_points, key=lambda p: p.y)
    lowest_collided = max(collided_points, key=lambda p: p.y)

    if not highest_collided.y <= rightest.y <= lowest_collided.y:
        return False

    return True


@collided_right.add
def collided_right(s1: Sprite, s2: Sprite) -> bool:
    if not collided_right(s1.coords, s2.coords):
        return False

    left_points = s1.points
    right_points = s2.points
    rightest = max(left_points, key=lambda p: p.x)  # Rightest point that collides with s2
    collided_points = [point for point in right_points if
                       point.x < rightest.x]  # Points that possibly collide with rightest

    if not collided_points:
        return False

    highest_collided = min(collided_points, key=lambda p: p.y)
    lowest_collided = max(collided_points, key=lambda p: p.y)

    if not highest_collided.y <= rightest.y <= lowest_collided.y:
        return False

    return True


@collided_top.add
def collided_top(s1: Sprite, s2: Sprite) -> bool:
    if not collided_top(s1.coords, s2.coords):
        return False

    top_points = s2.points
    bottom_points = s1.points
    highest = max(bottom_points, key=lambda p: p.y)  # Highest point that collides with s2
    collided_points = [point for point in top_points if
                       point.y < highest.y]  # Points that possibly collide with highest

    if not collided_points:
        return False

    leftmost_collided = min(collided_points, key=lambda p: p.x)
    rightest_collided = max(collided_points, key=lambda p: p.x)

    if not leftmost_collided.x <= highest.x <= rightest_collided.x:
        return False

    return True


@collided_bottom.add
def collided_bottom(s1: Sprite, s2: Sprite) -> bool:
    if not collided_bottom(s1.coords, s2.coords):
        return False

    top_points = s1.points
    bottom_points = s2.points
    highest = max(bottom_points, key=lambda p: p.y)  # Highest point that collides with s1
    collided_points = [point for point in top_points if
                       point.y < highest.y]  # Points that possibly collide with highest

    if not collided_points:
        return False

    leftmost_collided = min(collided_points, key=lambda p: p.x)
    rightest_collided = max(collided_points, key=lambda p: p.x)

    if not leftmost_collided.x <= highest.x <= rightest_collided.x:
        return False

    return True


class Polygon(Sprite):
    def __init__(self, canvas, *points, color="black"):
        self.num_sides = len(points) // 2

        logging.debug(f"Creating a polygon with {self.num_sides} sides")
        assert len(points) % 2 == 0

        super().__init__(
            canvas,
            canvas.create_polygon(points, fill=color)
        )

    def act(self, ratio: float):
        if self.movement and self.minMovement and self.maxMovement:
            movement = self.movement * random_double(self.minMovement, self.maxMovement) * ratio
            self.move(0, movement)

        if self.rotation and self.minRotation and self.maxRotation:
            # Only small polygons should rotate
            if self.coords.width < self.screen.width and self.coords.height < self.screen.height:
                rotation = self.rotation * random_double(self.minRotation, self.maxRotation) * ratio
                self.rotate(rotation)


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


class Star(Polygon):
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10,
                 color="black"):
        super().__init__(canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10,
                         color=color)


class Circle(Sprite):
    def __init__(self, canvas, x1, y1, x2, y2, color="black"):
        super().__init__(
            canvas,
            canvas.create_arc(x1, y1, x2, y2, extent=359.9, style=PIESLICE, fill=color, outline=color)
        )

    def act(self, ratio: float):
        if self.movement and self.minMovement and self.maxMovement:
            movement = self.movement * random_double(self.minMovement, self.maxMovement) * ratio
            self.move(0, movement)

        if self.rotation and self.minRotation and self.maxRotation:
            if self.coords.width == self.coords.height: # Ellipses don`t rotate
                rotation = self.rotation * random_double(self.minRotation, self.maxRotation) * ratio
                self.rotate(rotation)


class PlayerSprite(Star):
    move_amount = 20

    def __init__(self, canvas):
        cx, cy = 720, 400
        radius = 300
        offset = radius / 4
        super().__init__(
            canvas,
            cx, cy - radius,
                cx - offset, cy - offset,
                cx - radius, cy - offset,
                cx - offset, cy,
                cx - offset * 2, cy + radius,
            cx, cy + offset,
                cx + offset * 2, cy + radius,
                cx + offset, cy,
                cx + radius, cy - offset,
                cx + offset, cy - offset,
            color="#fb0"
        )

        self.mouse_x = None
        self.mouse_y = None

        # Motion bindings
        canvas.bind_all('<Key-Left>', self.move_left)
        canvas.bind_all('<Key-Right>', self.move_right)
        canvas.bind_all('<Key-Up>', self.move_up)
        canvas.bind_all('<Key-Down>', self.move_down)
        canvas.bind_all('<Return>', self.hide)
        canvas.bind_all('<Button-2>', self.hide)
        canvas.bind_all('<B1-Motion>', self.follow_mouse)

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

    def hide(self, event):
        """Hide the sprite underneath the screen."""

        logging.debug("Player Sprite is hiding")

        window_height = self.screen.height
        new_coords = BoundingRect(self.coords.x1, self.coords.y1 + window_height, self.coords.x2,
                                  self.coords.y2 + window_height)
        self.coords = new_coords

    def follow_mouse(self, event):
        if self.mouse_x and self.mouse_y:
            ratio = 1
            adj_x = event.x - self.mouse_x
            adj_y = event.y - self.mouse_y
            self.move(adj_x * ratio, adj_y * ratio)
        self.mouse_x, self.mouse_y = event.x, event.y


if __name__ == "__main__":
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

    hexagon = Hexagon(canvas, 1000, 20, 850, 220, 850, 420, 1000, 620, 1150, 420, 1150, 220, color="pink")
    print(f"Hexagon's bounding rect is  {hexagon.coords}")
