from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty

Config.set("graphics", "width", 1365)
Config.set("graphics", "height", 768)


class Events2App(App):
    targeted = BooleanProperty(False)

    def do_something(self, button):
        print(button)

    def touched(self, button, touch):
        if button.collide_point(touch.x, touch.y):
            self.targeted = True
            return True

    def moved(self, button, touch):
        if self.targeted:
            button.x += touch.dx / 2
            button.y += touch.dy / 2

    def untouched(self, button, touch):
        self.targeted = False


if __name__ == "__main__":
    Events2App().run()
