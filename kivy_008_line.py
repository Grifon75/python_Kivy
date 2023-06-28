from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Bezier, Line, RoundedRectangle, Triangle, SmoothLine
from math import cos, sin, radians
from kivy.uix.label import Label
from kivy.uix.button import Button

x, y = (360, 300)


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
    color_red = 0.5
    color_red_delta = 0.01
    points = []
    color = []

    def __init__(self, degrade, length_arrow, degrade_point):
        self.degrade = degrade
        self.length_arrow = length_arrow
        self.degrade_point = degrade_point


class CirclePoint:
    pos = (x + 50, y + 50)
    color = [1, 1, 1]
    color_obj = None
    arrow_in = False
    touch_in = 360

    def __init__(self, size, radius):
        self.size = size
        self.radius = radius


class BezierTest(FloatLayout):
    def __init__(self, arrow_sec, arrow_min, arrow_hours, arrow_sec_circle, *args, **kwargs):
        super(BezierTest, self).__init__(*args, **kwargs)
        label_ = Label(text='0', size_hint=(.1, .1), pos_hint={'x': .1}, color=(1, 1, 1), font_size=20)
        self.add_widget(label_)
        # self.add_widget(Button(text='My first button', size_hint=(.1, .1), pos_hint={'x': 0}))
        with self.canvas:
            circle_color = Color(.5, .5, .6)
            self.circle = RoundedRectangle(size=(500, 500), pos=(x - 250, y - 250), radius=(250, 250))
        map_circle = dict()
        index = 0
        index_r = 360
        flash = FlashCircle()
        while index < 360:
            if not index % 30:
                x_ = (x - 9) + 240 * cos(radians(index))
                y_ = (y - 9) + 240 * sin(radians(index))
                with self.canvas:
                    clr = Color(flash.fade_color[0], flash.fade_color[1], flash.fade_color[2])
                    self.circle_ = RoundedRectangle(size=(18, 18), pos=(x_, y_), radius=(9, 9))
                    map_circle[index_r] = clr
            else:
                x_ = (x - 5) + 240 * cos(radians(index))
                y_ = (y - 5) + 240 * sin(radians(index))
                with self.canvas:
                    clr = Color(flash.fade_color[0], flash.fade_color[1], flash.fade_color[2])
                    self.circle_ = RoundedRectangle(size=(10, 10), pos=(x_, y_), radius=(5, 5))
                    map_circle[index_r] = clr
            index += 6
            index_r -= 6
        print(map_circle)
        with self.canvas:
            Color(arrow_hours.color[0], arrow_hours.color[1], arrow_hours.color[2])
            self.triangle_hours = Triangle(points=arrow_hours.points)
        with self.canvas:
            Color(arrow_min.color[0], arrow_min.color[1], arrow_min.color[2])
            self.triangle_min = Triangle(points=arrow_min.points)
        with self.canvas:
            Color(arrow_sec.color[0], arrow_sec.color[1], arrow_sec.color[2])
            self.triangle_sec = Triangle(points=arrow_sec.points)
        with self.canvas:
            arrow_color_circle = Color(arrow_sec_circle.color[0], arrow_sec_circle.color[1], arrow_sec_circle.color[2])
            self.triangle_sec_circle = RoundedRectangle(size=arrow_sec_circle.size, pos=arrow_sec_circle.pos,
                                                        radius=arrow_sec_circle.radius)
            arrow_sec_circle.color_obj = arrow_color_circle
        with self.canvas:
            Color(.1, .1, .1)
            r_bolt = 20
            self.circle_bolt = RoundedRectangle(size=(r_bolt, r_bolt), pos=(x - r_bolt / 2, y - r_bolt / 2),
                                                radius=(r_bolt / 2, r_bolt / 2))
        # with self.canvas:
        #     Color(1.0, 0.0, 1.0)
        #     self.line = Line(points=points)
        # Clock.schedule_interval(lambda yu: clock_arrow(self.line), 1)
        Clock.schedule_interval(lambda sec_: clock_arrow(arrow_sec, self.triangle_sec, label_, arrow_sec_circle,
                                                         self.triangle_sec_circle, map_circle), 1 / 10.3)
        Clock.schedule_interval(lambda min_: clock_arrow(arrow_min, self.triangle_min), 60 / 20)
        Clock.schedule_interval(lambda hours_: clock_arrow(arrow_hours, self.triangle_hours), 3600 /
                                (360 / 12 / arrow_hours.degrade_point))
        # Clock.schedule_interval(lambda uu: clock_color(circle_color), .02)


# def clock_color(circle_color):
#     color_red += color_red_delta
#     if color_red > .7:
#         color_red_delta = -1 * color_red_delta
#     if color_red < .3:
#         color_red_delta = -1 * color_red_delta
#     circle_color.rgb = (color_red, .5, .6)
count = -1


def flash_circle(map_circle, flash, indicator):
    color_flash = []
    for color in flash.flash_color:
        color = round(color * flash.fade_color_count, 2)
        color_flash.append(color)
    flash.fade_color_count -= .1
    flash.fade_color_count = round(flash.fade_color_count, 2)
    if flash.fade_color_count < 0:
        flash.fade_color_count = 0
    if flash.itr_count == flash.COUNT:
        map_circle[indicator].rgb = color_flash
    elif flash.itr_count == 1:
        map_circle[indicator].rgb = flash.fade_color
    elif flash.itr_count > flash.COUNT/2:
        flash.swing_count += 6
        if indicator + flash.swing_count == 360:
            map_circle[360].rgb = color_flash
        elif indicator + flash.swing_count > 360:
            # flash.swing_count -= 6
            flash.negative_count_increase += 6
            map_circle[0 + flash.negative_count_increase].rgb = color_flash
        else:
            map_circle[indicator + flash.swing_count].rgb = color_flash
        if indicator - flash.swing_count == 0:
            map_circle[360].rgb = color_flash
        elif indicator - flash.swing_count < 0:
            flash.negative_count_decrease += 6
            map_circle[360 - flash.negative_count_decrease].rgb = color_flash
        else:
            map_circle[indicator - flash.swing_count].rgb = color_flash
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
        return False
    flash.itr_count -= 1


def flash_arrow_circle(arrow_circle, flash):
    color_flash = []
    for color in flash.flash_color:
        color = round(color * flash.fade_color_count, 2)
        color_flash.append(color)
    flash.fade_color_count -= .05
    flash.fade_color_count = round(flash.fade_color_count, 2)
    if flash.fade_color_count < .5:
        # print('Good')
        arrow_circle.color_obj.rgb = arrow_circle.color
        return False
    arrow_circle.color_obj.rgb = color_flash


def clock_arrow(arrow, triangle=None, label=None, arrow_circle=None, triangle_circle=None, map_circle=None):
    global x, y, count
    x_ = x
    y_ = y
    index = 0
    points = []
    # while index <= length_arrow:
    #     x_ += cos(radians(degrade))
    #     y_ -= sin(radians(degrade))
    #     points.extend([x_, y_])
    #     index += 1
    # print('cos = ', cos(degrade), 'sin = ', sin(degrade))
    x_end = x + arrow.length_arrow * cos(radians(arrow.degrade))
    y_end = y - arrow.length_arrow * sin(radians(arrow.degrade))
    # print('x_end = ', x_end, 'y_end = ', y_end)
    first_point_base_triangle_x = x + 10 * cos(radians(arrow.degrade - 90))
    first_point_base_triangle_y = y - 10 * sin(radians(arrow.degrade - 90))
    second_point_base_triangle_x = x + 10 * cos(radians(arrow.degrade + 90))
    second_point_base_triangle_y = y - 10 * sin(radians(arrow.degrade + 90))
    arrow.points = [first_point_base_triangle_x, first_point_base_triangle_y, second_point_base_triangle_x,
                    second_point_base_triangle_y, x_end, y_end]
    if arrow_circle is not None:
        x_circle = x + (arrow.length_arrow - 30) * cos(radians(arrow.degrade)) - (arrow_circle.size[0] / 2)
        y_circle = y - (arrow.length_arrow - 30) * sin(radians(arrow.degrade)) - (arrow_circle.size[0] / 2)
        arrow_circle.pos = (x_circle, y_circle)
    if triangle_circle is not None:
        triangle_circle.pos = arrow_circle.pos
        if not int(arrow.degrade) % 30:
            flash = FlashCircle()
            Clock.schedule_interval(lambda ui: flash_arrow_circle(arrow_circle, flash), 1 / 5)
            # arrow_circle.color_obj.rgb = [1, 1, 1]
            arrow_circle.arrow_in = True
            arrow_circle.touch_in = int(arrow.degrade)
        elif arrow_circle.arrow_in:
            arrow_circle.arrow_in = False
            arrow_circle.color_obj.rgb = arrow_circle.color
            if not arrow_circle.touch_in:
                arrow_circle.touch_in = 360
            flash = FlashCircle(20)
            Clock.schedule_interval(lambda ui: flash_circle(map_circle, flash, arrow_circle.touch_in), 1/10)
            if arrow_circle.touch_in == 270:
                count += 1
                label.text = str(count)
    arrow.degrade += arrow.degrade_point
    arrow.degrade = round(arrow.degrade, 1)
    # if 270 + arrow.degrade_point > arrow.degrade >= 270:
    #     count += 1
    #     label.text = str(count)
    if arrow.degrade > 360:
        arrow.degrade = arrow.degrade_point
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
        arrow_sec = Arrow(270, 250, 6 / 10)
        arrow_sec.color = [.7, .15, .15]
        arrow_min = Arrow(270, 250, 6 / 20)
        arrow_min.color = [.15, .15, .7]
        arrow_hours = Arrow(270, 150, 6 / 20)
        arrow_hours.color = [.15, .15, .15]
        arrow_sec_circle = CirclePoint((20, 20), (10, 10))
        arrow_sec_circle.color = arrow_sec.color
        clock_arrow(arrow_sec, None, arrow_sec_circle)
        clock_arrow(arrow_min)
        clock_arrow(arrow_hours)
        return BezierTest(arrow_sec, arrow_min, arrow_hours, arrow_sec_circle)


if __name__ == '__main__':
    Main().run()
