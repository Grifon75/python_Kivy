from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty


class RootWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.add_widget(Button(text='btn 1', size=(self.width * .2, self.height * .1), font_size=self.height * .25))
        cb = CustomBtn(text='btn test', font_size=50, color='#aaffdd', background_color='#999999', font_name='Mistral',
                       italic=True, border=(29, 29, 29, 29))
        cb.bind(on_pressed=self.btn_pressed)
        self.add_widget(cb)
        self.add_widget(Button(text='btn 2'))

    def btn_pressed(self, *args):
        ins, x, y = args
        print(x, y)


class CustomBtn(Button):
    pressed = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(CustomBtn, self).__init__(**kwargs)
        self.register_event_type('on_pressed')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # self.pressed = touch.pos
            self.dispatch('on_pressed', *touch.pos)
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_down(touch)

    def on_pressed(self, *args):
        print(*args)


class TestApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()
