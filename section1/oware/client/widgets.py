from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from random import choice, random

SEEDS = ["seed0.png", "seed1.png", "seed2.png"]


class GameBoard(Widget):
    grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        houses = []

        for i in range(12):
            house = House()
            house.index = i
            houses.append(house)

        for i in range(11, 5, -1):
            self.grid.add_widget(houses[i])

        for i in range(6):
            self.grid.add_widget(houses[i])

        self.houses = houses


class House(Widget):
    index = NumericProperty(-1)
    seeds = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.seed_widgets = [Seed() for i in range(self.seeds)]

    def on_seeds(self, instance, value):
        delta = value - len(self.seed_widgets)

        if delta < 0:
            for i in range(-delta):
                self.remove_widget(self.seed_widgets.pop())

        elif delta > 0:
            for i in range(delta):
                self.seed_widgets.append(Seed())
                self.seed_widgets[-1].sow(self)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.seeds:
                self.seeds -= 1
            else:
                self.seeds += 1


class Seed(Widget):
    image = StringProperty(SEEDS[0])
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = choice(SEEDS)
        self.angle = random() * 360

    def sow(self, house):
        house.add_widget(self)

        x_off = (random() - 0.5) * (house.width / 2.25)
        y_off = (random() - 0.5) * (house.height / 2.25)

        self.center_x = house.center_x + x_off
        self.center_y = house.center_y + y_off
