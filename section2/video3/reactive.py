from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import NumericProperty

Config.set("graphics", "width", 1365)
Config.set("graphics", "height", 768)


class PropButton(Button):
    count = NumericProperty(0)
    doubled = NumericProperty(0)

    def on_press(self):
        super().on_press()
        self.count += 1


class ReactiveApp(App):
    pass


if __name__ == "__main__":
    ReactiveApp().run()
