from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, AliasProperty
import ctypes as ct


class RootWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.add_widget(Button(text='btn 1', size=(self.width * .2, self.height * .1), font_size=self.height * .25))
        cb = CustomBtn(text='btn test', font_size=50, color=(2, 2, 2, 1), background_color=(1, 1, 1, 1),
                       font_name='Mistral',
                       italic=True, border=(29, 29, 29, 29))
        cb.bind(on_pressed=self.btn_pressed)
        self.add_widget(cb)
        self.add_widget(Button(text='btn 2'))

    def btn_pressed(self, *args):
        ins, x, y = args
        print('button pressed', x, y)


# class MyAliasProperty(AliasProperty):
#     def __init__(self, **kwargs):
#         super(MyAliasProperty, self).__init__(**kwargs)
#
#     def _get_cursor_pos(self, *args):
#         print(args)

class CustomBtn(Button):

    def __init__(self, **kwargs):
        super(CustomBtn, self).__init__(**kwargs)
        self.register_event_type('on_pressed')
        self.register_event_type('on_released')
        pass

    def bg_color(self, event):
        self.background_color = '#7777ee'

    def _get_pos(self):
        print('getter work')
        # Clock.schedule_once(self.bg_color, .2)
        return self.x, self.y

    # cursor_pos = AliasProperty(_get_pos, None,
    #                            bind=('cursor', 'size',
    #                                  'focus', 'scroll_x', 'scroll_y',
    #                                  'line_height', 'line_spacing'),
    #                            cache=True)
    cursor_pos = AliasProperty(_get_pos, None, bind=('size', 'line_height', 'background_color'), cache=True)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # print(self._get_pos())
            # print(self.cursor_pos)
            # self.pressed = touch.pos
            qw, wq = self.cursor_pos
            print('x = ', qw, 'y = ', wq)
            self.dispatch('on_pressed', *touch.pos)
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.dispatch('on_released', *touch.pos)
        return super(CustomBtn, self).on_touch_up(touch)

    def on_pressed(self, *args):
        self.background_color = (2.55, 2, 2.55, 1)
        self.color = (.3, .3, .3, 1)
        print(*args)

    def on_released(self, *args):
        self.background_color = (1, 1, 1, 1)
        self.color = (2, 2, 2, 1)

    # def _get_cursor_pos(self, *args):
    #     print(args)


class TestApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()
