from kivy.clock import Clock
import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import time as tm
import threading as thr


class LoginScreen(GridLayout):
    lb_1 = Label()
    index = 0

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.lb_1 = Label(text='Hello\nWorld!!', font_size='20sp')
        self.add_widget(self.lb_1)
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        Clock.schedule_interval(self.mmm, 2)

    def mmm(self, *args):
        self.index += 1
        self.lb_1.text = 'Hello\nWorld!! char = {0} unicode = {1}'.format(chr(self.index), self.index)


class MyApp(App):
    def build(self):
        lg = LoginScreen()
        return lg


if __name__ == '__main__':
    MyApp().run()
