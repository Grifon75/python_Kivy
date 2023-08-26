import io
import time
import asyncio

from kivy.app import async_runTouchApp
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Bezier, Line, RoundedRectangle, Triangle, SmoothLine, Canvas, Rectangle
from math import cos, sin, radians
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
# from kivy.uix.stencilview import StencilView
from kivy.config import Config

Config.set('graphics', 'shaped', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 512)
Config.set('graphics', 'height', 512)
Config.set('graphics', 'maxfps', 30)
Config.set('graphics', 'multisamples', 16)

# Config.set('graphics', 'position', 'custom')
# Config.set('graphics', 'left', 800)
# Config.set('graphics', 'top', 20)
from kivy.core.window import Window

Window.always_on_top = True
# WindowBase.Width = 600
# WindowBase.Height = 600
# m = Image.load('water.png', keep_data=True)
# Window.shape_mode = "reversebinalpha"

Window.shape_image = r'screenshots\fon001.png'
Window.set_system_cursor("size_all")
Window.shape_mode = "binalpha"

# Window.shape_color_key = [1,.5,.5,1
# Config.set('graphics', 'borderless', 1)
# Config.set('graphics', 'window_state', 'visible')
# Config.getint('kivy', 'show_fps')

# red background color
# Window.borderless = True
# Window.clearcolor = (.5, .5, .5, .5)

# from kivy.input.provider import MotionEventProvider
#
#
# class MousePro(MotionEventProvider):
#
#     def __init__(self, device, args):
#         super().__init__(device, args)
#         MotionEventProvider.start(self)


x, y = (256, 256)


class ColorManager:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


class ColorRGB:
    def __init__(self, value=1., value_step=None, limit_up=.7, limit_down=.3):
        self.value = value
        self.value_step = value_step
        self.limit_up = limit_up
        self.limit_down = limit_down


class FlashCircle:
    swing_count = 0
    negative_count_increase = 0
    negative_count_decrease = 0
    flash_color = (1, 1, 1)
    fade_color = (.1, .1, .1)
    fade_color_coefficient = (.1, .1, .1)
    fade_color_count = 1

    def __init__(self, itr_count=10):
        self.itr_count = itr_count
        self.COUNT = itr_count


class Arrow:
    points = []
    color = []

    def __init__(self, degrade, length_arrow, degrade_point, point_width):
        self.degrade = degrade
        self.length_arrow = length_arrow
        self.degrade_point = degrade_point
        self.point_width = point_width


class CirclePoint:
    pos = (x + 50, y + 50)
    color = [1, 1, 1]
    color_obj = None
    arrow_in = False
    touch_in = 360

    def __init__(self, size, radius):
        self.size = size
        self.radius = radius


class PeriodDelay:
    def __init__(self, anime_delay, float_frequency, constant_frequency):
        self.anime_delay = anime_delay
        self.float_frequency = float_frequency
        self.constant_frequency = constant_frequency


class EventBox:
    sec = None
    min = None
    hours = None


time_box = EventBox()


def screen_save(instance):
    Window.screenshot(r'screenshots\screen.png')


class BezierTest(FloatLayout):

    # texture = ObjectProperty()

    def __init__(self, arrow_sec, arrow_min, arrow_hours, arrow_sec_circle, *args, **kwargs):
        super(BezierTest, self).__init__(*args, **kwargs)
        # self.add_widget(Button(text='My first button', size_hint=(.1, .1), pos_hint={'x': 0}))
        with self.canvas:
            Color(.45, .35, 0.2)
            self.circle = RoundedRectangle(size=(514, 514), pos=(x - 257, y - 257), radius=(257, 257))
        with self.canvas:
            Color(.65, .55, 0.2)
            self.circle = RoundedRectangle(size=(500, 500), pos=(x - 250, y - 250), radius=(250, 250))
        with self.canvas:
            clock_face_color = Color(.5, .5, .5)
            self.circle = RoundedRectangle(size=(490, 490), pos=(x - 245, y - 245), radius=(245, 245))
        with self.canvas:
            Color(.65, .55, 0.2)
            self.circle = RoundedRectangle(size=(390, 390), pos=(x - 195, y - 195), radius=(195, 195))

        flash = FlashCircle()
        index_ = 0
        while index_ < 360:
            if not index_ % 30:
                radius_q = 15
                x_ = (x - radius_q) + (arrow_sec.length_arrow - 30) * cos(radians(index_))
                y_ = (y - radius_q) + (arrow_sec.length_arrow - 30) * sin(radians(index_))
                with self.canvas:
                    Color(.79, .85, .6)
                    self.circle_ = RoundedRectangle(size=(radius_q * 2, radius_q * 2), pos=(x_, y_),
                                                    radius=(radius_q, radius_q))
            else:
                radius_m = 7
                x_ = (x - radius_m) + (arrow_sec.length_arrow - 30) * cos(radians(index_))
                y_ = (y - radius_m) + (arrow_sec.length_arrow - 30) * sin(radians(index_))
                with self.canvas:
                    Color(.85, .79, .6)
                    self.circle_ = RoundedRectangle(size=(radius_m * 2, radius_m * 2), pos=(x_, y_),
                                                    radius=(radius_m, radius_m))
            index_ += 6

        map_circle = dict()
        map_numbers = dict()
        index = 0
        index_r = 360
        time_hours_index = 3
        while index < 360:
            if not index % 30:
                radius_q = 13
                x_ = (x - radius_q) + (arrow_sec.length_arrow - 30) * cos(radians(index))
                y_ = (y - radius_q) + (arrow_sec.length_arrow - 30) * sin(radians(index))
                with self.canvas:
                    clr = Color(flash.fade_color[0], flash.fade_color[1], flash.fade_color[2])
                    self.circle_ = RoundedRectangle(size=(radius_q * 2, radius_q * 2), pos=(x_, y_),
                                                    radius=(radius_q, radius_q))
                    color_numbers = (.8, .7, .3)
                    label_time_index = Label(text=str(time_hours_index), pos=(x_ - 37, y_ - 37), color=color_numbers,
                                             bold=BooleanProperty(True),
                                             font_size='20sp')
                    map_numbers[time_hours_index] = [label_time_index, color_numbers]
                    time_hours_index -= 1
                    if time_hours_index == 0:
                        time_hours_index = 12
                    map_circle[index_r] = clr
            else:
                radius_m = 5
                x_ = (x - radius_m) + (arrow_sec.length_arrow - 30) * cos(radians(index))
                y_ = (y - radius_m) + (arrow_sec.length_arrow - 30) * sin(radians(index))
                with self.canvas:
                    clr = Color(flash.fade_color[0], flash.fade_color[1], flash.fade_color[2])
                    self.circle_ = RoundedRectangle(size=(radius_m * 2, radius_m * 2), pos=(x_, y_),
                                                    radius=(radius_m, radius_m))
                    map_circle[index_r] = clr
            index += 6
            index_r -= 6

        with self.canvas:
            Color(.2, .2, .13)
            RoundedRectangle(size=(380, 380), pos=(x - 190, y - 190), radius=(190, 190))
            # d:\Ava\sexmachine999-2gnhz-5bb16a.gif image\Dali_open_window.jpg
        # image = Image(r'd:\Ava\sexmachine999-2gnhz-5bb16a.gif')
        # data = io.BytesIO(open(r'd:\Ava\sexmachine999-2gnhz-5bb16a.gif', "rb").read())
        # im_ = Image(data, ext="gif")
        texture = Image(source=r'image\in_clock_3.jpg').texture
        # texture.wrap = 'clamp_to_edge'
        # texture.uvpos = (0, 0)
        # texture.uvsize = (0, 0)
        # texture.get_region(0, 0, 64, 64)
        # Valid properties are['allow_stretch', 'anim_delay', 'anim_loop', 'center', 'center_x', 'center_y', 'children',
        # 'cls', 'color', 'disabled', 'fit_mode', 'height', 'ids', 'image_ratio', 'keep_data', 'keep_ratio', 'mipmap',
        # 'motion_filter', 'nocache', 'norm_image_size', 'opacity', 'parent', 'pos', 'pos_hint', 'right', 'size',
        # 'size_hint', 'size_hint_max', 'size_hint_max_x', 'size_hint_max_y', 'size_hint_min', 'size_hint_min_x',
        # 'size_hint_min_y', 'size_hint_x', 'size_hint_y', 'source', 'texture', 'texture_size', 'top', 'width',
        # 'x', 'y']
        # self.rpmBar = StencilView(size_hint=(None, None), size=(800, 154), pos=(0, 240))
        # self.rpmBarImage = Image(source='rpmBar.png', size=(800, 154), pos=(0, 240))
        # self.rpmBar.add_widget(self.rpmBarImage)
        # self.add_widget(self.rpmBar)
        with self.canvas:
            # Color(.75, .55, .15) #serpia
            Color(.79, .79, .7)
            RoundedRectangle(texture=texture, size=(370, 370), pos=(x - 185, y - 185), radius=(185, 185))
        with self.canvas:
            Color(arrow_hours.color[0], arrow_hours.color[1], arrow_hours.color[2])
            self.triangle_hours = Triangle(points=arrow_hours.points)
        with self.canvas:
            Color(arrow_min.color[0], arrow_min.color[1], arrow_min.color[2])
            self.triangle_min = Triangle(points=arrow_min.points)
        with self.canvas:
            Color(arrow_sec.color[0], arrow_sec.color[1], arrow_sec.color[2])
            self.triangle_sec = Triangle(points=arrow_sec.points)
        # texture_2 = Image(source=r'image\eclipsesun_2.gif').texture
        with self.canvas:
            # Color(.75, .55, .15) #serpia
            # Color(.79, .79, .7)
            # Button(texture=image_gif.anim_loop, size=(35, 35), pos=(x - 17.5, y - 17.5))
            Image(source=r'image\eclipsesun.gif', anim_delay=.1, anim_loop=0,
                  pos=(x - 30, y - 31), size=(60, 60))
            # self.add_widget(im)
        with self.canvas:
            arrow_color_circle = Color(arrow_sec_circle.color[0], arrow_sec_circle.color[1], arrow_sec_circle.color[2])
            self.triangle_sec_circle = RoundedRectangle(size=arrow_sec_circle.size, pos=arrow_sec_circle.pos,
                                                        radius=arrow_sec_circle.radius)
            arrow_sec_circle.color_obj = arrow_color_circle

        with self.canvas:
            Color(.1, .1, .1)
            r_bolt = max(arrow_hours.point_width, arrow_min.point_width, arrow_sec.point_width)
            self.circle_bolt = RoundedRectangle(size=(r_bolt, r_bolt), pos=(x - r_bolt / 2, y - r_bolt / 2),
                                                radius=(r_bolt / 2, r_bolt / 2))
        # with self.canvas:
        #     Color(1.0, 0.0, 1.0)
        #     self.line = Line(points=points)
        # Clock.schedule_interval(lambda yu: clock_arrow(self.line), 1)

        # Clock.schedule_interval(lambda sec_: clock_arrow_anime(arrow_sec, arrow_min, arrow_hours, self.triangle_sec,
        #                                                  self.triangle_min, self.triangle_hours, arrow_sec_circle,
        #                                                  self.triangle_sec_circle), 1 / 10.22)
        time_local_sec = time.localtime().tm_sec
        time_local_min = time.localtime().tm_min
        time_local_hours = time.localtime().tm_hour
        if time_local_hours >= 12:
            time_local_hours = time_local_hours - 12
        sec_period = PeriodDelay(time_local_sec * 6 / arrow_sec.degrade_point, 1 / 60,
                                 1 / (6 / arrow_sec.degrade_point))
        # print(sec_period.anime_delay, ' ', time_local_sec)
        min_period = PeriodDelay(
            time_local_min * 6 / arrow_min.degrade_point + time_local_sec * (6 / arrow_min.degrade_point) / 60, 1 / 60,
            60 / (6 / arrow_min.degrade_point))
        hours_period = PeriodDelay(time_local_hours * 5 * 6 / arrow_hours.degrade_point + time_local_min * (
                (6 / arrow_hours.degrade_point) * 5) / 60, 1 / 60,
                                   3600 / ((6 / arrow_hours.degrade_point) * 5))
        # anime_sec_delay = time.localtime().tm_sec * 6 / arrow_sec.degrade_point
        # anime_min_delay = time.localtime().tm_min * 6 / arrow_min.degrade_point
        # anime_hours_delay = time.localtime().tm_hour * 6 / arrow_hours.degrade_point
        # sec_period_start = 1/60
        # min_period_start = 1/60
        # hours_period_start = 1/60
        # sec_period = sec_period_start
        # min_period = min_period_start
        # hours_period = hours_period_start
        # global const_sec_period
        # global const_min_period
        # global const_hours_period
        # const_sec_period = 1 / ((6 / arrow_sec.degrade_point) + .22)
        # const_min_period = 60 / (6 / arrow_min.degrade_point)
        # const_hours_period = 3600 / ((6 / arrow_hours.degrade_point) * 5)
        event_sec = Clock.schedule_interval(
            lambda sec_: clock_arrow(arrow_sec, self.triangle_sec, 'sec', sec_period, arrow_sec_circle,
                                     self.triangle_sec_circle, map_circle, map_numbers), sec_period.float_frequency)
        event_min = Clock.schedule_interval(lambda min_: clock_arrow(arrow_min, self.triangle_min, 'min', min_period),
                                            min_period.float_frequency)
        event_hours = Clock.schedule_interval(
            lambda hours_: clock_arrow(arrow_hours, self.triangle_hours, 'hours', hours_period),
            hours_period.float_frequency)
        global time_box
        time_box.sec = event_sec
        time_box.min = event_min
        time_box.hours = event_hours
        color_manager = ColorManager(ColorRGB(.88, .005, .95, .84), ColorRGB(.88, .005, .95, .84),
                                     ColorRGB(.75, .005, .8, .7))

        Clock.schedule_interval(lambda uu: rainbow_color(clock_face_color, color_manager), .05)
        # time.struct_time(tm_year=2023, tm_mon=8, tm_mday=20, tm_hour=15, tm_min=50, tm_sec=46, tm_wday=6, tm_yday=232,
        #                  tm_isdst=0)

        # mp = MousePro("lan", 78)
        # print(mp.device)
        # from pywin.scintilla.keycodes import modifiers
        # dict_keys(['alt', 'lalt', 'ralt', 'ctrl', 'ctl', 'control', 'lctrl', 'lctl', 'rctrl', 'rctl', 'shift', 'key'])
        # Window.on_mouse_down(x, y, button, modifiers)
        # print(modifiers.keys())

    start_pos = (0, 0)
    # Window.on_mouse_down(x, y, 'Button1', 'ctr')

    def on_touch_down(self, touch):
        self.start_pos = touch.pos

    def on_touch_move(self, touch):
        Window.left = Window.left + (touch.pos[0] - self.start_pos[0])
        Window.top = Window.top + (self.start_pos[1] - touch.pos[1])

# def on_mouse_down(x, y, button, modifiers):
#         print('wer')


def rainbow_color_(color):
    color.value += color.value_step
    if color.value > color.limit_up or color.value < color.limit_down:
        color.value_step = -1 * color.value_step
    return color.value


def rainbow_color(figure_color, manager):
    if manager.red.value_step is not None:
        red = rainbow_color_(manager.red)
    else:
        red = manager.red.value
    if manager.green.value_step is not None:
        green = rainbow_color_(manager.green)
    else:
        green = manager.green.value
    if manager.blue.value_step is not None:
        blue = rainbow_color_(manager.blue)
    else:
        blue = manager.blue.value
    figure_color.rgb = (red, green, blue)


def flash_number_create(map_numbers, indicator):
    if indicator <= 270:
        map_numbers[3 + indicator / 30][0].color = map_numbers[3 + indicator / 30][1]
    else:
        map_numbers[indicator / 30 - 9][0].color = map_numbers[indicator / 30 - 9][1]
    return False


def flash_circle(map_circle, map_numbers, flash, indicator):
    global light_line
    color_flash = []
    for color in flash.flash_color:
        color -= .09
        if color < 0:
            color = 0
        color_flash.append(color)
    flash.flash_color = color_flash
    if max(flash.flash_color) < .1:
        flash.flash_color = (.1, .1, .1)
    if flash.itr_count == flash.COUNT:
        map_circle[indicator].rgb = flash.flash_color
    elif flash.itr_count == 1:
        # map_circle[indicator].rgb = flash.fade_color
        pass
    elif flash.itr_count > flash.COUNT / 2:
        flash.swing_count += 6
        if indicator + flash.swing_count == 360:
            map_circle[360].rgb = flash.flash_color
        elif indicator + flash.swing_count > 360:
            # flash.swing_count -= 6
            flash.negative_count_increase += 6
            map_circle[0 + flash.negative_count_increase].rgb = flash.flash_color
        else:
            map_circle[indicator + flash.swing_count].rgb = flash.flash_color
        if indicator - flash.swing_count == 0:
            map_circle[360].rgb = flash.flash_color
        elif indicator - flash.swing_count < 0:
            flash.negative_count_decrease += 6
            map_circle[360 - flash.negative_count_decrease].rgb = flash.flash_color
        else:
            map_circle[indicator - flash.swing_count].rgb = flash.flash_color
    elif flash.itr_count > 0:
        if flash.negative_count_increase > 0:
            # flash.swing_count += 6
            map_circle[flash.negative_count_increase].rgb = flash.fade_color
            flash.negative_count_increase -= 6
        else:
            map_circle[indicator + flash.swing_count].rgb = flash.fade_color
        if flash.negative_count_decrease > 0:
            # flash.swing_count += 6
            map_circle[360 - flash.negative_count_decrease].rgb = flash.fade_color
            flash.negative_count_decrease -= 6
        elif indicator - flash.swing_count == 0:
            map_circle[360].rgb = flash.fade_color
        else:
            map_circle[indicator - flash.swing_count].rgb = flash.fade_color
        flash.swing_count -= 6
    else:
        flash = FlashCircle()
        flash.flash_color = (1, 1, .7)
        Clock.schedule_interval(
            lambda ffc: flash_figure_create(flash, map_circle[indicator], flash.fade_color, .05, .2),
            1 / 30)
        light_line = None
        Clock.schedule_once(lambda fnc: flash_number_create(map_numbers, indicator), 1 / 4)
        return False
    flash.itr_count -= 1


def flash_figure_create(flash, indicator, final_color=(.1, .1, .1), count_step=.05, count_limit=.5):
    global light_circle
    color_flash = []
    for color in flash.flash_color:
        color -= count_step
        if color < min(final_color):
            color = min(final_color)
        color_flash.append(color)
    flash.flash_color = color_flash
    if max(flash.flash_color) < count_limit:
        # print('Good')
        indicator.rgb = final_color
        light_circle = None
        return False
    indicator.rgb = flash.flash_color


def clock_arrow_local(arrow, triangle, mark, anime_period, arrow_circle, triangle_circle, map_circle, map_numbers):
    global time_box
    if mark == 'sec':
        Clock.unschedule(time_box.sec)
        arrow.degrade_point = 6 / 10
        anime_period.constant_frequency = 1 / (6 / arrow.degrade_point)
        Clock.schedule_interval(lambda sec: clock_arrow(arrow, triangle, mark, None, arrow_circle,
                                                        triangle_circle, map_circle, map_numbers),
                                anime_period.constant_frequency)
    elif mark == 'min':
        Clock.unschedule(time_box.min)
        arrow.degrade_point = 6 / 20
        anime_period.constant_frequency = 60 / (6 / arrow.degrade_point)
        Clock.schedule_interval(lambda min: clock_arrow(arrow, triangle, mark, None, arrow_circle,
                                                        triangle_circle, map_circle, map_numbers),
                                anime_period.constant_frequency)
    elif mark == 'hours':
        Clock.unschedule(time_box.hours)
        arrow.degrade_point = 6 / 20
        anime_period.constant_frequency = 3600 / ((6 / arrow.degrade_point) * 5)
        Clock.schedule_interval(lambda hours: clock_arrow(arrow, triangle, mark, None, arrow_circle,
                                                          triangle_circle, map_circle, map_numbers),
                                anime_period.constant_frequency)


def correction_sec(arrow):
    time_s = time.localtime().tm_sec * (6 / arrow.degrade_point)
    quarter_t = 15 * (6 / arrow.degrade_point)
    if time_s < quarter_t:
        arrow.degrade_point -= .01
        print('correction = -')
    elif time_s > quarter_t:
        arrow.degrade_point += .01
        print('correction = +')
    arrow.degrade = round(arrow.degrade, 2)
    print('correction = ', arrow.degrade)


light_circle = None
light_line = None


def clock_arrow(arrow, triangle=None, mark='', anime_period=None, arrow_circle=None, triangle_circle=None,
                map_circle=None, map_numbers=None):
    global x, y
    # if mark == 'min':
    #     print(arrow.degrade_point)
    if anime_period is not None:
        if anime_period.anime_delay > 0:
            anime_period.anime_delay -= 1
        else:
            # anime_period.anime_delay = 100
            # print(tyz)
            clock_arrow_local(arrow, triangle, mark, anime_period, arrow_circle, triangle_circle, map_circle,
                              map_numbers)
            return False
    # x_ = x
    # y_ = y
    # index = 0
    # points = []
    # while index <= length_arrow:
    #     x_ += cos(radians(degrade))
    #     y_ -= sin(radians(degrade))
    #     points.extend([x_, y_])
    #     index += 1
    # print('cos = ', cos(degrade), 'sin = ', sin(degrade))
    x_end = x + arrow.length_arrow * cos(radians(arrow.degrade))
    y_end = y - arrow.length_arrow * sin(radians(arrow.degrade))
    # print('x_end = ', x_end, 'y_end = ', y_end)
    first_point_base_triangle_x = x + arrow.point_width / 2 * cos(radians(arrow.degrade - 90))
    first_point_base_triangle_y = y - arrow.point_width / 2 * sin(radians(arrow.degrade - 90))
    second_point_base_triangle_x = x + arrow.point_width / 2 * cos(radians(arrow.degrade + 90))
    second_point_base_triangle_y = y - arrow.point_width / 2 * sin(radians(arrow.degrade + 90))
    arrow.points = [first_point_base_triangle_x, first_point_base_triangle_y, second_point_base_triangle_x,
                    second_point_base_triangle_y, x_end, y_end]
    if arrow_circle is not None:
        x_circle = x + (arrow.length_arrow - 30) * cos(radians(arrow.degrade)) - (arrow_circle.size[0] / 2)
        y_circle = y - (arrow.length_arrow - 30) * sin(radians(arrow.degrade)) - (arrow_circle.size[1] / 2)
        arrow_circle.pos = (x_circle, y_circle)
    global light_circle
    global light_line
    if triangle_circle is not None:
        triangle_circle.pos = arrow_circle.pos
        if not int(arrow.degrade) % 30 and anime_period is None and light_circle is None and light_line is None:
            # arrow_circle.color_obj.rgb = [1, 1, 1]
            # arrow_circle.arrow_in = True
            arrow_circle.touch_in = int(arrow.degrade)
            # elif arrow_circle.arrow_in:
            flash_arrow_crl = FlashCircle()
            flash_arrow_crl.flash_color = (1, 1, .7)
            # if anime_period is None and light_circle is None:
            light_circle = Clock.schedule_interval(
                lambda ui: flash_figure_create(flash_arrow_crl, arrow_circle.color_obj,
                                               arrow_circle.color, .03, .5), 1 / 10)
            # arrow_circle.arrow_in = False
            arrow_circle.color_obj.rgb = arrow_circle.color
            if not arrow_circle.touch_in:
                arrow_circle.touch_in = 360
            flash_ani_scale = FlashCircle(20)
            flash_ani_scale.flash_color = (1, 1, .7)
            # if anime_period is None and light_line is None:
            light_line = Clock.schedule_interval(
                lambda ui: flash_circle(map_circle, map_numbers, flash_ani_scale, arrow_circle.touch_in),
                1 / 30)
            if arrow_circle.touch_in <= 270:
                map_numbers[3 + arrow_circle.touch_in / 30][0].color = (.2, .2, .2)
            else:
                map_numbers[arrow_circle.touch_in / 30 - 9][0].color = (.2, .2, .2)
            # if arrow_circle.touch_in == 270:
            #     count += 1
            # label.text = str(count)
    arrow.degrade += arrow.degrade_point
    # if mark == 'sec':
    #     print(arrow.degrade)
    # if mark == 'min':
    #     print(arrow.degrade)
    arrow.degrade = round(arrow.degrade, 2)
    # if 270 + arrow.degrade_point > arrow.degrade >= 270:
    #     count += 1
    #     label.text = str(count)
    if arrow.degrade == 360:
        arrow.degrade = 0
        if mark == 'sec' and arrow.degrade_point < 1:
            correction_sec(arrow)
        print('=360', arrow.degrade)
    elif arrow.degrade > 360:
        print('>360', arrow.degrade)
        arrow.degrade = arrow.degrade - 360
        if mark == 'sec' and arrow.degrade_point < 1:
            correction_sec(arrow)
    if triangle is not None:
        triangle.points = arrow.points
    # def _set_bezier_dash_offset(self, instance, value):
    #     # effect to reduce length while increase offset
    #     self.bezier.dash_length = 100 - value
    #     self.bezier.dash_offset = value
    #
    # def _set_line_dash_offset(self, instance, value):
    #     # effect to reduce length while increase offset
    #     self.line.dash_length = 100 - value
    #     self.line.dash_offset = value
    #
    # def on_touch_down(self, touch):
    #     if self.collide_point(touch.pos[0], touch.pos[1]):
    #         for i, p in enumerate(list(zip(self.points[::2],
    #                                        self.points[1::2]))):
    #             if (abs(touch.pos[0] - self.pos[0] - p[0]) < self.d and
    #                     abs(touch.pos[1] - self.pos[1] - p[1]) < self.d):
    #                 self.current_point = i + 1
    #                 return True
    #         return super(BezierTest, self).on_touch_down(touch)
    #
    # def on_touch_up(self, touch):
    #     if self.collide_point(touch.pos[0], touch.pos[1]):
    #         if self.current_point:
    #             self.current_point = None
    #             return True
    #         return super(BezierTest, self).on_touch_up(touch)
    #
    # def on_touch_move(self, touch):
    #     if self.collide_point(touch.pos[0], touch.pos[1]):
    #         c = self.current_point
    #         if c:
    #             self.points[(c - 1) * 2] = touch.pos[0] - self.pos[0]
    #             self.points[(c - 1) * 2 + 1] = touch.pos[1] - self.pos[1]
    #             self.bezier.points = self.points
    #             self.line.points = self.points + self.points[:2]
    #             return True
    #         return super(BezierTest, self).on_touch_move(touch)


class Main(App):

    def build(self):
        self.title = 'Clock'
        self.use_kivy_settings = True
        arrow_sec = Arrow(270, 250, 6 / 3, 16)
        arrow_sec.color = [.72, .15, .1]
        arrow_min = Arrow(270, 250, 6 / 4, 24)
        arrow_min.color = [.2, .15, .5]
        arrow_hours = Arrow(270, 150, 6 / 5, 26)
        arrow_hours.color = [.3, .1, .3]
        arrow_sec_circle = CirclePoint((20, 20), (10, 10))
        arrow_sec_circle.color = arrow_sec.color
        # clock_arrow(arrow_sec, None, '', None, arrow_sec_circle)
        # clock_arrow(arrow_min)
        # clock_arrow(arrow_hours)
        from kivy.uix.widget import Widget
        parent = Widget()
        # parent.opacity = .5
        clock = BezierTest(arrow_sec, arrow_min, arrow_hours, arrow_sec_circle)
        parent.add_widget(clock)
        parent.add_widget(Button(text='screen', size=(100, 50), pos=(0, 0), on_press=screen_save))
        return parent


if __name__ == '__main__':
    main = Main()
    # main.run()
    # from kivy.base import runTouchApp
    # runTouchApp(Main())
    asyncio.run(main.async_run())
