from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import NumericProperty

Config.set("graphics", "width", 1365)
Config.set("graphics", "height", 768)


class PropButton(Button):
    count = NumericProperty(0)

    def on_press(self):
        super().on_press()
        self.count += 1

    def on_count(self, instance, value):
        print(f"Clicked {value} times")


class PropObserveApp(App):
    def changed(self, instance, value):
        print(f"Woo! {value}")

    def build(self):
        self.root.bind(count=self.changed)


if __name__ == "__main__":
    PropObserveApp().run()
