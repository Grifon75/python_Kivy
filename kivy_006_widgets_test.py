from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import time as tm
import threading as thr
from kivy.graphics.instructions import Canvas
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget


class MyWidget(Widget):

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        # print(self.height, self.width, self.size)
        canvas_1 = Canvas(color=(1.5, 1.5, 1), size=(500, 500))
        # canvas_1.add(Rectangle(size=(50, 50)))
        layout_float = FloatLayout(size=(500, 500))
        # listen to size and position changes
        layout_float.bind(pos=self.update_rect, size=self.update_rect)
        layout_box = BoxLayout(size=(500, 500), x=500)
        layout_box.bind(pos=self.update_rect, size=self.update_rect)
        with layout_float.canvas.before:
            Color(.2, .2, .2, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect_float = Rectangle(size=layout_float.size,
                                  pos=layout_float.pos)
        with layout_box.canvas.before:
            Color(.3, .3, .1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect_box = Rectangle(size=layout_box.size,
                                  pos=layout_box.pos)
        # Valid properties
        # are['center', 'center_x', 'center_y', 'children', 'cls', 'disabled', 'height', 'ids', 'minimum_height',
        # 'minimum_size', 'minimum_width', 'motion_filter', 'opacity', 'orientation', 'padding', 'parent', 'pos',
        # 'pos_hint', 'right', 'size', 'size_hint', 'size_hint_max', 'size_hint_max_x', 'size_hint_max_y',
        # 'size_hint_min', 'size_hint_min_x', 'size_hint_min_y', 'size_hint_x', 'size_hint_y', 'spacing', 'top',
        # 'width', 'x', 'y']
        hint_max = .3
        button_1 = Button(text='My first button', size_hint=(.25, .15), pos_hint={'x': 0})
        button_2 = Button(text='My second button', size_hint=(.25, .15), pos_hint={'right': 1})
        button_3 = Button(text='My third button', size_hint=(.25, .15), pos_hint={'center_x': .5})
        button_4 = Button(text='My 4 button', size_hint=(.25, .15), pos_hint={'top': .8})
        button_5 = Button(text='My 5 button', size_hint=(.25, .15), pos_hint={'top': .9})
        button_6 = Button(text='My 6 button', size_hint=(.25, .15), pos_hint={'top': 1})
        # Valid properties
        # are['always_release', 'anchors', 'background_color', 'background_disabled_down', 'background_disabled_normal',
        # 'background_down', 'background_normal', 'base_direction', 'bold', 'border', 'center', 'center_x', 'center_y',
        # 'children', 'cls', 'color', 'disabled', 'disabled_color', 'disabled_outline_color', 'ellipsis_options',
        # 'font_blended', 'font_context', 'font_direction', 'font_family', 'font_features', 'font_hinting',
        # 'font_kerning', 'font_name', 'font_script_name', 'font_size', 'halign', 'height', 'ids', 'is_shortened',
        # 'italic', 'last_touch', 'line_height', 'markup', 'max_lines', 'min_state_time', 'mipmap', 'motion_filter',
        # 'opacity', 'outline_color', 'outline_width', 'padding', 'padding_x', 'padding_y', 'parent', 'pos', 'pos_hint',
        # 'refs', 'right', 'shorten', 'shorten_from', 'size', 'size_hint', 'size_hint_max', 'size_hint_max_x',
        # 'size_hint_max_y', 'size_hint_min', 'size_hint_min_x', 'size_hint_min_y', 'size_hint_x', 'size_hint_y',
        # 'split_str', 'state', 'strikethrough', 'strip', 'text', 'text_language', 'text_size', 'texture',
        # 'texture_size', 'top', 'underline', 'unicode_errors', 'valign', 'width', 'x', 'y']
        layout_float.add_widget(button_1)
        layout_float.add_widget(button_2)
        layout_float.add_widget(button_3)
        layout_box.add_widget(button_4)
        layout_box.add_widget(button_5)
        layout_box.add_widget(button_6)
        # print(layout.children)
        self.add_widget(layout_float)
        self.add_widget(layout_box)
    def update_rect(instance, value):
        if instance is FloatLayout:
            instance.rect_float.pos = instance.pos
            instance.rect_float.size = instance.size
        elif instance is BoxLayout:
            instance.rect_box.pos = instance.pos
            instance.rect_box.size = instance.size

class MyApp(App):

    def build(self):
        self.root = root = MyWidget()
        self.title = 'test Canvas what background'
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, .22, 0.2, 1)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    MyApp().run()
