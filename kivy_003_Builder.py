import kivy
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file('wid.kv')


class MyLabel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = 0
        Clock.schedule_once(self.schedule_label, 1)
        # Clock.schedule_interval(self.schedule_label, 1/2)

    def schedule_label(self, *args):
        print('123')
        Clock.schedule_once(self.schedule_label_2, 1)
        # self.ids.lbl_001.text = '{0}'.format(self.index)
        # self.index += 1

    def schedule_label_2(self, *args):
        print('321')
        trigger = Clock.create_trigger(self.trigger_func, 2)
        # later
        trigger()

    def trigger_func(self, *args):
        print('trigger work')



class MyApp(App):
    def build(self):
        self.screen_m = ScreenManager()
        self.mylabel = MyLabel()
        myscreen = Screen(name='scr_lbl')
        myscreen.add_widget(self.mylabel)
        self.screen_m.add_widget(myscreen)
        return self.screen_m


if __name__ == '__main__':
    myapp = MyApp()
    myapp.run()
