from pathlib import Path
from kivy.config import Config
from kivy.resources import resource_add_path
from kivy.app import App
from . import widgets

resource_add_path(str(Path(widgets.__file__).resolve().parent / "data"))
Config.set("graphics", "width", 1365)
Config.set("graphics", "height", 768)


class OwareClientApp(App):
    pass


if __name__ == "__main__":
    OwareClientApp().run()
