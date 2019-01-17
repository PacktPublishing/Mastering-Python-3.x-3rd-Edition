from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App


Config.set("graphics", "width", 1365)
Config.set("graphics", "height", 768)


class MinimalApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", spacing=10)
        layout.add_widget(Button(text="Hello"))
        layout.add_widget(Button(text="World"))
        return layout


if __name__ == "__main__":
    MinimalApp().run()
