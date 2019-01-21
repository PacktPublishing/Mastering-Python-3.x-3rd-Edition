from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

Config.set("graphics", "width", 1365)
Config.set("graphics", "height", 768)


class HandledButton(Button):
    def on_press(self):
        super().on_press()
        print("Python bound by name", self)


class Events1App(App):
    def do_something(self, button):
        print("KV bound by name", button)

    def do_the_other_thing(self, button):
        print("Python bound using bind()", button)

    def build(self):
        self.root.third_button.bind(on_press=self.do_the_other_thing)


if __name__ == "__main__":
    Events1App().run()
