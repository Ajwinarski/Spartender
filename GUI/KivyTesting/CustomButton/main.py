from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class ImageButton(ButtonBehavior, Image):
    pass

class MyApp(App):
    def build(self):
        return ImageButton(source="../../Kivy/assets/design/ConfigBtn.png", on_press=lambda *args: print("press"),
            background_normal = '../../Kivy/assets/design/ConfigBtn.png',
            background_down = '../../Kivy/assets/design/ConfigBtnPressed.png')

if __name__ == "__main__":
    MyApp().run()
