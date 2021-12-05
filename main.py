# File name: DropPiUI.py
import DropPiUI_Dropper
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.uix.screenmanager import (ScreenManager, Screen)
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from DropPi_lib import *

kivy.require('1.9.0')

version = '1.06'

root_folder = ''

template_file = ''


def format_number(value):
    if "." in value:
        value = str("{:.1f}".format(float(value)))
    else:
        value = str("{:.0f}".format(float(value)))
    if ".0" in value:
        value = str("{:.0f}".format(float(value)))
    return value


class LongpressButton(Factory.Button):
    __events__ = ('on_long_press',)

    long_press_time = Factory.NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_interval(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass


class NumKeyboardPopup(Popup):

    def press_read(self):
        app = App.get_running_app()
        self.ids.popup_label.text = str(app.instance_selected)
        print(app.instance_selected)

    def press_0(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '0')

    def press_1(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '1')

    def press_2(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '2')

    def press_3(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '3')

    def press_4(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '4')

    def press_5(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '5')

    def press_6(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '6')

    def press_7(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '7')

    def press_8(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '8')

    def press_9(self):
        self.ids.popup_number_screen.text = format_number(self.ids.popup_number_screen.text + '9')

    def press_dot(self):
        if "." not in self.ids.popup_number_screen.text:
            self.ids.popup_number_screen.text = self.ids.popup_number_screen.text + '.'

    def press_enter(self):
        app = App.get_running_app()
        app.instance_selected.text = self.ids.popup_number_screen.text
        self.dismiss()

    def press_backspace(self):
        self.ids.popup_number_screen.text = self.ids.popup_number_screen.text[:-1]
        if self.ids.popup_number_screen.text == '':
            self.ids.popup_number_screen.text = '0'

    def press_clear(self):
        self.ids.popup_number_screen.text = '0'


class LoadingScreen(Screen):
    pass


class MainScreen(Screen):
    global version
    droppiversion = f'DropPi v.{version} - A droplet photography controller'

    def text_focused(self, instance, value):
        # TODO: Fix a custom numeric keyboard so that we can place
        #   it wherever we want on the screen. The Kivy 2.0 vKeyboard
        #   is not easy to place
        if value:
            print(str(instance))
            print(instance.text)
            print(self.get_id(instance))
            app = App.get_running_app()
            app.num_value = instance.text
            app.instance_selected = instance
            app.instance_selected_string = self.get_id(instance)
            mypopup = NumKeyboardPopup()
            mypopup.open()


    def get_id(self, instance):
        # for id, widget in instance.parent.ids.items():
        for id, widget in self.ids.items():
            if widget.__self__ == instance:
                return id

    def get_instance(self, id):
        # for id, widget in instance.parent.ids.items():
        for instance, widget in self.ids.items():
            if widget.__self__ == instance:
                return instance

    # VALVE TOGGLES (ROW TOGGLES)
    def press_valvetoggle1callback(self):
        if self.ids.valvetoggle1.color == [1, 1, 1, 1]:
            self.ids.valvetoggle1.color = (.1, .1, .8, 1)
            self.ids.v1d2toggle.color = (.5, .5, 1, 1)
            self.ids.v1d3toggle.color = (.5, .5, 1, 1)
            self.ids.v1d4toggle.color = (.5, .5, 1, 1)
            self.ids.v1d1on.disabled = True
            self.ids.v1d1off.disabled = True
            self.ids.v1d2toggle.disabled = True
            self.ids.v1d3toggle.disabled = True
            self.ids.v1d4toggle.disabled = True
            self.ids.v1d1on.opacity = 0
            self.ids.v1d1off.opacity = 0
            self.ids.v1d2on.opacity = 0
            self.ids.v1d2off.opacity = 0
            self.ids.v1d3on.opacity = 0
            self.ids.v1d3off.opacity = 0
            self.ids.v1d4on.opacity = 0
            self.ids.v1d4off.opacity = 0
        else:
            self.ids.valvetoggle1.color = (1, 1, 1, 1)
            self.ids.v1d1on.disabled = False
            self.ids.v1d1off.disabled = False
            self.ids.v1d2toggle.disabled = False
            self.ids.v1d3toggle.disabled = True
            self.ids.v1d4toggle.disabled = True
            self.ids.v1d1on.opacity = 1
            self.ids.v1d1off.opacity = 1

    def press_valvetoggle2callback(self):
        if self.ids.valvetoggle2.color == [1, 1, 1, 1]:
            self.ids.valvetoggle2.color = (.1, .1, .8, 1)
            self.ids.v2d2toggle.color = (.5, .5, 1, 1)
            self.ids.v2d3toggle.color = (.5, .5, 1, 1)
            self.ids.v2d4toggle.color = (.5, .5, 1, 1)
            self.ids.v2d1on.disabled = True
            self.ids.v2d1off.disabled = True
            self.ids.v2d2toggle.disabled = True
            self.ids.v2d3toggle.disabled = True
            self.ids.v2d4toggle.disabled = True
            self.ids.v2d1on.opacity = 0
            self.ids.v2d1off.opacity = 0
            self.ids.v2d2on.opacity = 0
            self.ids.v2d2off.opacity = 0
            self.ids.v2d3on.opacity = 0
            self.ids.v2d3off.opacity = 0
            self.ids.v2d4on.opacity = 0
            self.ids.v2d4off.opacity = 0
        else:
            self.ids.valvetoggle2.color = (1, 1, 1, 1)
            self.ids.v2d1on.disabled = False
            self.ids.v2d1off.disabled = False
            self.ids.v2d2toggle.disabled = False
            self.ids.v2d3toggle.disabled = True
            self.ids.v2d4toggle.disabled = True
            self.ids.v2d1on.opacity = 1
            self.ids.v2d1off.opacity = 1

    def press_valvetoggle3callback(self):
        if self.ids.valvetoggle3.color == [1, 1, 1, 1]:
            self.ids.valvetoggle3.color = (.1, .1, .8, 1)
            self.ids.v3d2toggle.color = (.5, .5, 1, 1)
            self.ids.v3d3toggle.color = (.5, .5, 1, 1)
            self.ids.v3d4toggle.color = (.5, .5, 1, 1)
            self.ids.v3d1on.disabled = True
            self.ids.v3d1off.disabled = True
            self.ids.v3d2toggle.disabled = True
            self.ids.v3d3toggle.disabled = True
            self.ids.v3d4toggle.disabled = True
            self.ids.v3d1on.opacity = 0
            self.ids.v3d1off.opacity = 0
            self.ids.v3d2on.opacity = 0
            self.ids.v3d2off.opacity = 0
            self.ids.v3d3on.opacity = 0
            self.ids.v3d3off.opacity = 0
            self.ids.v3d4on.opacity = 0
            self.ids.v3d4off.opacity = 0
        else:
            self.ids.valvetoggle3.color = (1, 1, 1, 1)
            self.ids.v3d1on.disabled = False
            self.ids.v3d1off.disabled = False
            self.ids.v3d2toggle.disabled = False
            self.ids.v3d3toggle.disabled = True
            self.ids.v3d4toggle.disabled = True
            self.ids.v3d1on.opacity = 1
            self.ids.v3d1off.opacity = 1

    def press_valvetoggle4callback(self):
        if self.ids.valvetoggle4.color == [1, 1, 1, 1]:
            self.ids.valvetoggle4.color = (.1, .1, .8, 1)
            self.ids.v4d2toggle.color = (.5, .5, 1, 1)
            self.ids.v4d3toggle.color = (.5, .5, 1, 1)
            self.ids.v4d4toggle.color = (.5, .5, 1, 1)
            self.ids.v4d1on.disabled = True
            self.ids.v4d1off.disabled = True
            self.ids.v4d2toggle.disabled = True
            self.ids.v4d3toggle.disabled = True
            self.ids.v4d4toggle.disabled = True
            self.ids.v4d1on.opacity = 0
            self.ids.v4d1off.opacity = 0
            self.ids.v4d2on.opacity = 0
            self.ids.v4d2off.opacity = 0
            self.ids.v4d3on.opacity = 0
            self.ids.v4d3off.opacity = 0
            self.ids.v4d4on.opacity = 0
            self.ids.v4d4off.opacity = 0
        else:
            self.ids.valvetoggle4.color = (1, 1, 1, 1)
            self.ids.v4d1on.disabled = False
            self.ids.v4d1off.disabled = False
            self.ids.v4d2toggle.disabled = False
            self.ids.v4d3toggle.disabled = True
            self.ids.v4d4toggle.disabled = True
            self.ids.v4d1on.opacity = 1
            self.ids.v4d1off.opacity = 1

    # VALVE 1 (ROW 1) TOGGLE BUTTONS
    def press_v1d2togglecallback(self):
        if self.ids.v1d2toggle.color == [1, 1, 1, 1]:
            self.ids.v1d2toggle.color = (.5, .5, 1, 1)
            self.ids.v1d3toggle.color = (.5, .5, 1, 1)
            self.ids.v1d4toggle.color = (.5, .5, 1, 1)
            self.ids.v1d3toggle.disabled = True
            self.ids.v1d4toggle.disabled = True
            self.ids.v1d2on.opacity = 0
            self.ids.v1d2on.disabled = True
            self.ids.v1d2off.opacity = 0
            self.ids.v1d2off.disabled = True
            self.ids.v1d3on.opacity = 0
            self.ids.v1d3on.disabled = True
            self.ids.v1d3off.opacity = 0
            self.ids.v1d3off.disabled = True
            self.ids.v1d4on.opacity = 0
            self.ids.v1d4on.disabled = True
            self.ids.v1d4off.opacity = 0
            self.ids.v1d4off.disabled = True
        else:
            self.ids.v1d2toggle.color = (1, 1, 1, 1)
            self.ids.v1d3toggle.disabled = False
            self.ids.v1d2on.opacity = 1
            self.ids.v1d2on.disabled = False
            self.ids.v1d2off.opacity = 1
            self.ids.v1d2off.disabled = False

    def press_v1d3togglecallback(self):
        if self.ids.v1d3toggle.color == [1, 1, 1, 1]:
            self.ids.v1d3toggle.color = (.5, .5, 1, 1)
            self.ids.v1d4toggle.color = (.5, .5, 1, 1)
            self.ids.v1d4toggle.disabled = True
            self.ids.v1d3on.opacity = 0
            self.ids.v1d3on.disabled = True
            self.ids.v1d3off.opacity = 0
            self.ids.v1d3off.disabled = True
            self.ids.v1d4on.opacity = 0
            self.ids.v1d4on.disabled = True
            self.ids.v1d4off.opacity = 0
            self.ids.v1d4off.disabled = True
        else:
            self.ids.v1d3toggle.color = (1, 1, 1, 1)
            self.ids.v1d4toggle.disabled = False
            self.ids.v1d3on.opacity = 1
            self.ids.v1d3on.disabled = False
            self.ids.v1d3off.opacity = 1
            self.ids.v1d3off.disabled = False

    def press_v1d4togglecallback(self):
        if self.ids.v1d4toggle.color == [1, 1, 1, 1]:
            self.ids.v1d4toggle.color = (.5, .5, 1, 1)
            self.ids.v1d4on.opacity = 0
            self.ids.v1d4on.disabled = True
            self.ids.v1d4off.opacity = 0
            self.ids.v1d4off.disabled = True
        else:
            self.ids.v1d4toggle.color = (1, 1, 1, 1)
            self.ids.v1d4on.opacity = 1
            self.ids.v1d4on.disabled = False
            self.ids.v1d4off.opacity = 1
            self.ids.v1d4off.disabled = False

    # VALVE 2 (ROW 2) TOGGLE BUTTONS
    def press_v2d2togglecallback(self):
        if self.ids.v2d2toggle.color == [1, 1, 1, 1]:
            self.ids.v2d2toggle.color = (.5, .5, 1, 1)
            self.ids.v2d3toggle.color = (.5, .5, 1, 1)
            self.ids.v2d4toggle.color = (.5, .5, 1, 1)
            self.ids.v2d3toggle.disabled = True
            self.ids.v2d4toggle.disabled = True
            self.ids.v2d2on.opacity = 0
            self.ids.v2d2on.disabled = True
            self.ids.v2d2off.opacity = 0
            self.ids.v2d2off.disabled = True
            self.ids.v2d3on.opacity = 0
            self.ids.v2d3on.disabled = True
            self.ids.v2d3off.opacity = 0
            self.ids.v2d3off.disabled = True
            self.ids.v2d4on.opacity = 0
            self.ids.v2d4on.disabled = True
            self.ids.v2d4off.opacity = 0
            self.ids.v2d4off.disabled = True
        else:
            self.ids.v2d2toggle.color = (1, 1, 1, 1)
            self.ids.v2d3toggle.disabled = False
            self.ids.v2d2on.opacity = 1
            self.ids.v2d2on.disabled = False
            self.ids.v2d2off.opacity = 1
            self.ids.v2d2off.disabled = False

    def press_v2d3togglecallback(self):
        if self.ids.v2d3toggle.color == [1, 1, 1, 1]:
            self.ids.v2d3toggle.color = (.5, .5, 1, 1)
            self.ids.v2d4toggle.color = (.5, .5, 1, 1)
            self.ids.v2d4toggle.disabled = True
            self.ids.v2d3on.opacity = 0
            self.ids.v2d3on.disabled = True
            self.ids.v2d3off.opacity = 0
            self.ids.v2d3off.disabled = True
            self.ids.v2d4on.opacity = 0
            self.ids.v2d4on.disabled = True
            self.ids.v2d4off.opacity = 0
            self.ids.v2d4off.disabled = True
        else:
            self.ids.v2d3toggle.color = (1, 1, 1, 1)
            self.ids.v2d4toggle.disabled = False
            self.ids.v2d3on.opacity = 1
            self.ids.v2d3on.disabled = False
            self.ids.v2d3off.opacity = 1
            self.ids.v2d3off.disabled = False

    def press_v2d4togglecallback(self):
        if self.ids.v2d4toggle.color == [1, 1, 1, 1]:
            self.ids.v2d4toggle.color = (.5, .5, 1, 1)
            self.ids.v2d4on.opacity = 0
            self.ids.v2d4on.disabled = True
            self.ids.v2d4off.opacity = 0
            self.ids.v2d4off.disabled = True
        else:
            self.ids.v2d4toggle.color = (1, 1, 1, 1)
            self.ids.v2d4on.opacity = 1
            self.ids.v2d4on.disabled = False
            self.ids.v2d4off.opacity = 1
            self.ids.v2d4off.disabled = False

    # VALVE 3 (ROW 3) TOGGLE BUTTONS
    def press_v3d2togglecallback(self):
        if self.ids.v3d2toggle.color == [1, 1, 1, 1]:
            self.ids.v3d2toggle.color = (.5, .5, 1, 1)
            self.ids.v3d3toggle.color = (.5, .5, 1, 1)
            self.ids.v3d4toggle.color = (.5, .5, 1, 1)
            self.ids.v3d3toggle.disabled = True
            self.ids.v3d4toggle.disabled = True
            self.ids.v3d2on.opacity = 0
            self.ids.v3d2on.disabled = True
            self.ids.v3d2off.opacity = 0
            self.ids.v3d2off.disabled = True
            self.ids.v3d3on.opacity = 0
            self.ids.v3d3on.disabled = True
            self.ids.v3d3off.opacity = 0
            self.ids.v3d3off.disabled = True
            self.ids.v3d4on.opacity = 0
            self.ids.v3d4on.disabled = True
            self.ids.v3d4off.opacity = 0
            self.ids.v3d4off.disabled = True
        else:
            self.ids.v3d2toggle.color = (1, 1, 1, 1)
            self.ids.v3d3toggle.disabled = False
            self.ids.v3d2on.opacity = 1
            self.ids.v3d2on.disabled = False
            self.ids.v3d2off.opacity = 1
            self.ids.v3d2off.disabled = False

    def press_v3d3togglecallback(self):
        if self.ids.v3d3toggle.color == [1, 1, 1, 1]:
            self.ids.v3d3toggle.color = (.5, .5, 1, 1)
            self.ids.v3d4toggle.color = (.5, .5, 1, 1)
            self.ids.v3d4toggle.disabled = True
            self.ids.v3d3on.opacity = 0
            self.ids.v3d3on.disabled = True
            self.ids.v3d3off.opacity = 0
            self.ids.v3d3off.disabled = True
            self.ids.v3d4on.opacity = 0
            self.ids.v3d4on.disabled = True
            self.ids.v3d4off.opacity = 0
            self.ids.v3d4off.disabled = True
        else:
            self.ids.v3d3toggle.color = (1, 1, 1, 1)
            self.ids.v3d4toggle.disabled = False
            self.ids.v3d3on.opacity = 1
            self.ids.v3d3on.disabled = False
            self.ids.v3d3off.opacity = 1
            self.ids.v3d3off.disabled = False

    def press_v3d4togglecallback(self):
        if self.ids.v3d4toggle.color == [1, 1, 1, 1]:
            self.ids.v3d4toggle.color = (.5, .5, 1, 1)
            self.ids.v3d4on.opacity = 0
            self.ids.v3d4on.disabled = True
            self.ids.v3d4off.opacity = 0
            self.ids.v3d4off.disabled = True
        else:
            self.ids.v3d4toggle.color = (1, 1, 1, 1)
            self.ids.v3d4on.opacity = 1
            self.ids.v3d4on.disabled = False
            self.ids.v3d4off.opacity = 1
            self.ids.v3d4off.disabled = False

    # VALVE 4 (ROW 4) TOGGLE BUTTONS
    def press_v4d2togglecallback(self):
        if self.ids.v4d2toggle.color == [1, 1, 1, 1]:
            self.ids.v4d2toggle.color = (.5, .5, 1, 1)
            self.ids.v4d3toggle.color = (.5, .5, 1, 1)
            self.ids.v4d4toggle.color = (.5, .5, 1, 1)
            self.ids.v4d3toggle.disabled = True
            self.ids.v4d4toggle.disabled = True
            self.ids.v4d2on.opacity = 0
            self.ids.v4d2on.disabled = True
            self.ids.v4d2off.opacity = 0
            self.ids.v4d2off.disabled = True
            self.ids.v4d3on.opacity = 0
            self.ids.v4d3on.disabled = True
            self.ids.v4d3off.opacity = 0
            self.ids.v4d3off.disabled = True
            self.ids.v4d4on.opacity = 0
            self.ids.v4d4on.disabled = True
            self.ids.v4d4off.opacity = 0
            self.ids.v4d4off.disabled = True
        else:
            self.ids.v4d2toggle.color = (1, 1, 1, 1)
            self.ids.v4d3toggle.disabled = False
            self.ids.v4d2on.opacity = 1
            self.ids.v4d2on.disabled = False
            self.ids.v4d2off.opacity = 1
            self.ids.v4d2off.disabled = False

    def press_v4d3togglecallback(self):
        if self.ids.v4d3toggle.color == [1, 1, 1, 1]:
            self.ids.v4d3toggle.color = (.5, .5, 1, 1)
            self.ids.v4d4toggle.color = (.5, .5, 1, 1)
            self.ids.v4d4toggle.disabled = True
            self.ids.v4d3on.opacity = 0
            self.ids.v4d3on.disabled = True
            self.ids.v4d3off.opacity = 0
            self.ids.v4d3off.disabled = True
            self.ids.v4d4on.opacity = 0
            self.ids.v4d4on.disabled = True
            self.ids.v4d4off.opacity = 0
            self.ids.v4d4off.disabled = True
        else:
            self.ids.v4d3toggle.color = (1, 1, 1, 1)
            self.ids.v4d4toggle.disabled = False
            self.ids.v4d3on.opacity = 1
            self.ids.v4d3on.disabled = False
            self.ids.v4d3off.opacity = 1
            self.ids.v4d3off.disabled = False

    def press_v4d4togglecallback(self):
        if self.ids.v4d4toggle.color == [1, 1, 1, 1]:
            self.ids.v4d4toggle.color = (.5, .5, 1, 1)
            self.ids.v4d4on.opacity = 0
            self.ids.v4d4on.disabled = True
            self.ids.v4d4off.opacity = 0
            self.ids.v4d4off.disabled = True
        else:
            self.ids.v4d4toggle.color = (1, 1, 1, 1)
            self.ids.v4d4on.opacity = 1
            self.ids.v4d4on.disabled = False
            self.ids.v4d4off.opacity = 1
            self.ids.v4d4off.disabled = False

    # flash toggle button callbacks
    def press_f1togglecallback(self):
        if self.ids.f1toggle.color == [1, 1, 1, 1]:
            self.ids.f1toggle.color = (.5, .5, 1, 1)
        else:
            self.ids.f1toggle.color = (1, 1, 1, 1)

    def press_f2togglecallback(self):
        if self.ids.f2toggle.color == [1, 1, 1, 1]:
            self.ids.f2toggle.color = (.5, .5, 1, 1)
        else:
            self.ids.f2toggle.color = (1, 1, 1, 1)

    def press_f3togglecallback(self):
        if self.ids.f3toggle.color == [1, 1, 1, 1]:
            self.ids.f3toggle.color = (.5, .5, 1, 1)
        else:
            self.ids.f3toggle.color = (1, 1, 1, 1)

    # PLUS AND MINUS BUTTONS

    # ROW 1 MINUS BUTTONS
    def press_v1d1on_min(self, longpress):
        if not longpress:
            self.ids.v1d1on_val.text = format_number(str(float(self.ids.v1d1on_val.text) - 1))
        else:
            self.ids.v1d1on_val.text = format_number(str(float(self.ids.v1d1on_val.text) - 10))

    def press_v1d2on_min(self, longpress):
        if not longpress:
            self.ids.v1d2on_val.text = format_number(str(float(self.ids.v1d2on_val.text) - 1))
        else:
            self.ids.v1d2on_val.text = format_number(str(float(self.ids.v1d2on_val.text) - 10))

    def press_v1d3on_min(self, longpress):
        if not longpress:
            self.ids.v1d3on_val.text = format_number(str(float(self.ids.v1d3on_val.text) - 1))
        else:
            self.ids.v1d3on_val.text = format_number(str(float(self.ids.v1d3on_val.text) - 10))

    def press_v1d4on_min(self, longpress):
        if not longpress:
            self.ids.v1d4on_val.text = format_number(str(float(self.ids.v1d4on_val.text) - 1))
        else:
            self.ids.v1d4on_val.text = format_number(str(float(self.ids.v1d4on_val.text) - 10))

    def press_v1d1off_min(self, longpress):
        if not longpress:
            self.ids.v1d1off_val.text = format_number(str(float(self.ids.v1d1off_val.text) - 1))
        else:
            self.ids.v1d1off_val.text = format_number(str(float(self.ids.v1d1off_val.text) - 10))

    def press_v1d2off_min(self, longpress):
        if not longpress:
            self.ids.v1d2off_val.text = format_number(str(float(self.ids.v1d2off_val.text) - 1))
        else:
            self.ids.v1d2off_val.text = format_number(str(float(self.ids.v1d2off_val.text) - 10))

    def press_v1d3off_min(self, longpress):
        if not longpress:
            self.ids.v1d3off_val.text = format_number(str(float(self.ids.v1d3off_val.text) - 1))
        else:
            self.ids.v1d3off_val.text = format_number(str(float(self.ids.v1d3off_val.text) - 10))

    def press_v1d4off_min(self, longpress):
        if not longpress:
            self.ids.v1d4off_val.text = format_number(str(float(self.ids.v1d4off_val.text) - 1))
        else:
            self.ids.v1d4off_val.text = format_number(str(float(self.ids.v1d4off_val.text) - 10))

    # ROW 2 MINUS BUTTONS
    def press_v2d1on_min(self, longpress):
        if not longpress:
            self.ids.v2d1on_val.text = format_number(str(float(self.ids.v2d1on_val.text) - 1))
        else:
            self.ids.v2d1on_val.text = format_number(str(float(self.ids.v2d1on_val.text) - 10))

    def press_v2d2on_min(self, longpress):
        if not longpress:
            self.ids.v2d2on_val.text = format_number(str(float(self.ids.v2d2on_val.text) - 1))
        else:
            self.ids.v2d2on_val.text = format_number(str(float(self.ids.v2d2on_val.text) - 10))

    def press_v2d3on_min(self, longpress):
        if not longpress:
            self.ids.v2d3on_val.text = format_number(str(float(self.ids.v2d3on_val.text) - 1))
        else:
            self.ids.v2d3on_val.text = format_number(str(float(self.ids.v2d3on_val.text) - 10))

    def press_v2d4on_min(self, longpress):
        if not longpress:
            self.ids.v2d4on_val.text = format_number(str(float(self.ids.v2d4on_val.text) - 1))
        else:
            self.ids.v2d4on_val.text = format_number(str(float(self.ids.v2d4on_val.text) - 10))

    def press_v2d1off_min(self, longpress):
        if not longpress:
            self.ids.v2d1off_val.text = format_number(str(float(self.ids.v2d1off_val.text) - 1))
        else:
            self.ids.v2d1off_val.text = format_number(str(float(self.ids.v2d1off_val.text) - 10))

    def press_v2d2off_min(self, longpress):
        if not longpress:
            self.ids.v2d2off_val.text = format_number(str(float(self.ids.v2d2off_val.text) - 1))
        else:
            self.ids.v2d2off_val.text = format_number(str(float(self.ids.v2d2off_val.text) - 10))

    def press_v2d3off_min(self, longpress):
        if not longpress:
            self.ids.v2d3off_val.text = format_number(str(float(self.ids.v2d3off_val.text) - 1))
        else:
            self.ids.v2d3off_val.text = format_number(str(float(self.ids.v2d3off_val.text) - 10))

    def press_v2d4off_min(self, longpress):
        if not longpress:
            self.ids.v2d4off_val.text = format_number(str(float(self.ids.v2d4off_val.text) - 1))
        else:
            self.ids.v2d4off_val.text = format_number(str(float(self.ids.v2d4off_val.text) - 10))

    # ROW 3 MINUS BUTTONS
    def press_v3d1on_min(self, longpress):
        if not longpress:
            self.ids.v3d1on_val.text = format_number(str(float(self.ids.v3d1on_val.text) - 1))
        else:
            self.ids.v3d1on_val.text = format_number(str(float(self.ids.v3d1on_val.text) - 10))

    def press_v3d2on_min(self, longpress):
        if not longpress:
            self.ids.v3d2on_val.text = format_number(str(float(self.ids.v3d2on_val.text) - 1))
        else:
            self.ids.v3d2on_val.text = format_number(str(float(self.ids.v3d2on_val.text) - 10))

    def press_v3d3on_min(self, longpress):
        if not longpress:
            self.ids.v3d3on_val.text = format_number(str(float(self.ids.v3d3on_val.text) - 1))
        else:
            self.ids.v3d3on_val.text = format_number(str(float(self.ids.v3d3on_val.text) - 10))

    def press_v3d4on_min(self, longpress):
        if not longpress:
            self.ids.v3d4on_val.text = format_number(str(float(self.ids.v3d4on_val.text) - 1))
        else:
            self.ids.v3d4on_val.text = format_number(str(float(self.ids.v3d4on_val.text) - 10))

    def press_v3d1off_min(self, longpress):
        if not longpress:
            self.ids.v3d1off_val.text = format_number(str(float(self.ids.v3d1off_val.text) - 1))
        else:
            self.ids.v3d1off_val.text = format_number(str(float(self.ids.v3d1off_val.text) - 10))

    def press_v3d2off_min(self, longpress):
        if not longpress:
            self.ids.v3d2off_val.text = format_number(str(float(self.ids.v3d2off_val.text) - 1))
        else:
            self.ids.v3d2off_val.text = format_number(str(float(self.ids.v3d2off_val.text) - 10))

    def press_v3d3off_min(self, longpress):
        if not longpress:
            self.ids.v3d3off_val.text = format_number(str(float(self.ids.v3d3off_val.text) - 1))
        else:
            self.ids.v3d3off_val.text = format_number(str(float(self.ids.v3d3off_val.text) - 10))

    def press_v3d4off_min(self, longpress):
        if not longpress:
            self.ids.v3d4off_val.text = format_number(str(float(self.ids.v3d4off_val.text) - 1))
        else:
            self.ids.v3d4off_val.text = format_number(str(float(self.ids.v3d4off_val.text) - 10))

    # ROW 4 MINUS BUTTONS
    def press_v4d1on_min(self, longpress):
        if not longpress:
            self.ids.v4d1on_val.text = format_number(str(float(self.ids.v4d1on_val.text) - 1))
        else:
            self.ids.v4d1on_val.text = format_number(str(float(self.ids.v4d1on_val.text) - 10))

    def press_v4d2on_min(self, longpress):
        if not longpress:
            self.ids.v4d2on_val.text = format_number(str(float(self.ids.v4d2on_val.text) - 1))
        else:
            self.ids.v4d2on_val.text = format_number(str(float(self.ids.v4d2on_val.text) - 10))

    def press_v4d3on_min(self, longpress):
        if not longpress:
            self.ids.v4d3on_val.text = format_number(str(float(self.ids.v4d3on_val.text) - 1))
        else:
            self.ids.v4d3on_val.text = format_number(str(float(self.ids.v4d3on_val.text) - 10))

    def press_v4d4on_min(self, longpress):
        if not longpress:
            self.ids.v4d4on_val.text = format_number(str(float(self.ids.v4d4on_val.text) - 1))
        else:
            self.ids.v4d4on_val.text = format_number(str(float(self.ids.v4d4on_val.text) - 10))

    def press_v4d1off_min(self, longpress):
        if not longpress:
            self.ids.v4d1off_val.text = format_number(str(float(self.ids.v4d1off_val.text) - 1))
        else:
            self.ids.v4d1off_val.text = format_number(str(float(self.ids.v4d1off_val.text) - 10))

    def press_v4d2off_min(self, longpress):
        if not longpress:
            self.ids.v4d2off_val.text = format_number(str(float(self.ids.v4d2off_val.text) - 1))
        else:
            self.ids.v4d2off_val.text = format_number(str(float(self.ids.v4d2off_val.text) - 10))

    def press_v4d3off_min(self, longpress):
        if not longpress:
            self.ids.v4d3off_val.text = format_number(str(float(self.ids.v4d3off_val.text) - 1))
        else:
            self.ids.v4d3off_val.text = format_number(str(float(self.ids.v4d3off_val.text) - 10))

    def press_v4d4off_min(self, longpress):
        if not longpress:
            self.ids.v4d4off_val.text = format_number(str(float(self.ids.v4d4off_val.text) - 1))
        else:
            self.ids.v4d4off_val.text = format_number(str(float(self.ids.v4d4off_val.text) - 10))

    # CAMERA MINUS BUTTONS
    def press_camon_min(self, longpress):
        if not longpress:
            self.ids.camon_val.text = format_number(str(float(self.ids.camon_val.text) - 1))
        else:
            self.ids.camon_val.text = format_number(str(float(self.ids.camon_val.text) - 10))

    def press_camoff_min(self, longpress):
        if not longpress:
            self.ids.camoff_val.text = format_number(str(float(self.ids.camoff_val.text) - 1))
        else:
            self.ids.camoff_val.text = format_number(str(float(self.ids.camoff_val.text) - 10))

    # FLASH MINUS BUTTONS
    def press_flashon_min(self, longpress):
        if not longpress:
            self.ids.flashon_val.text = format_number(str(float(self.ids.flashon_val.text) - 1))
        else:
            self.ids.flashon_val.text = format_number(str(float(self.ids.flashon_val.text) - 10))

    def press_flashoff_min(self, longpress):
        if not longpress:
            self.ids.flashoff_val.text = format_number(str(float(self.ids.flashoff_val.text) - 1))
        else:
            self.ids.flashoff_val.text = format_number(str(float(self.ids.flashoff_val.text) - 10))

    # ROW 1 PLUS BUTTONS
    def press_v1d1on_plus(self, longpress):
        if not longpress:
            self.ids.v1d1on_val.text = format_number(str(float(self.ids.v1d1on_val.text) + 1))
        else:
            self.ids.v1d1on_val.text = format_number(str(float(self.ids.v1d1on_val.text) + 10))

    def press_v1d2on_plus(self, longpress):
        if not longpress:
            self.ids.v1d2on_val.text = format_number(str(float(self.ids.v1d2on_val.text) + 1))
        else:
            self.ids.v1d2on_val.text = format_number(str(float(self.ids.v1d2on_val.text) + 10))

    def press_v1d3on_plus(self, longpress):
        if not longpress:
            self.ids.v1d3on_val.text = format_number(str(float(self.ids.v1d3on_val.text) + 1))
        else:
            self.ids.v1d3on_val.text = format_number(str(float(self.ids.v1d3on_val.text) + 10))

    def press_v1d4on_plus(self, longpress):
        if not longpress:
            self.ids.v1d4on_val.text = format_number(str(float(self.ids.v1d4on_val.text) + 1))
        else:
            self.ids.v1d4on_val.text = format_number(str(float(self.ids.v1d4on_val.text) + 10))

    def press_v1d1off_plus(self, longpress):
        if not longpress:
            self.ids.v1d1off_val.text = format_number(str(float(self.ids.v1d1off_val.text) + 1))
        else:
            self.ids.v1d1off_val.text = format_number(str(float(self.ids.v1d1off_val.text) + 10))

    def press_v1d2off_plus(self, longpress):
        if not longpress:
            self.ids.v1d2off_val.text = format_number(str(float(self.ids.v1d2off_val.text) + 1))
        else:
            self.ids.v1d2off_val.text = format_number(str(float(self.ids.v1d2off_val.text) + 10))

    def press_v1d3off_plus(self, longpress):
        if not longpress:
            self.ids.v1d3off_val.text = format_number(str(float(self.ids.v1d3off_val.text) + 1))
        else:
            self.ids.v1d3off_val.text = format_number(str(float(self.ids.v1d3off_val.text) + 10))

    def press_v1d4off_plus(self, longpress):
        if not longpress:
            self.ids.v1d4off_val.text = format_number(str(float(self.ids.v1d4off_val.text) + 1))
        else:
            self.ids.v1d4off_val.text = format_number(str(float(self.ids.v1d4off_val.text) + 10))

    # ROW 2 PLUS BUTTONS
    def press_v2d1on_plus(self, longpress):
        if not longpress:
            self.ids.v2d1on_val.text = format_number(str(float(self.ids.v2d1on_val.text) + 1))
        else:
            self.ids.v2d1on_val.text = format_number(str(float(self.ids.v2d1on_val.text) + 10))

    def press_v2d2on_plus(self, longpress):
        if not longpress:
            self.ids.v2d2on_val.text = format_number(str(float(self.ids.v2d2on_val.text) + 1))
        else:
            self.ids.v2d2on_val.text = format_number(str(float(self.ids.v2d2on_val.text) + 10))

    def press_v2d3on_plus(self, longpress):
        if not longpress:
            self.ids.v2d3on_val.text = format_number(str(float(self.ids.v2d3on_val.text) + 1))
        else:
            self.ids.v2d3on_val.text = format_number(str(float(self.ids.v2d3on_val.text) + 10))

    def press_v2d4on_plus(self, longpress):
        if not longpress:
            self.ids.v2d4on_val.text = format_number(str(float(self.ids.v2d4on_val.text) + 1))
        else:
            self.ids.v2d4on_val.text = format_number(str(float(self.ids.v2d4on_val.text) + 10))

    def press_v2d1off_plus(self, longpress):
        if not longpress:
            self.ids.v2d1off_val.text = format_number(str(float(self.ids.v2d1off_val.text) + 1))
        else:
            self.ids.v2d1off_val.text = format_number(str(float(self.ids.v2d1off_val.text) + 10))

    def press_v2d2off_plus(self, longpress):
        if not longpress:
            self.ids.v2d2off_val.text = format_number(str(float(self.ids.v2d2off_val.text) + 1))
        else:
            self.ids.v2d2off_val.text = format_number(str(float(self.ids.v2d2off_val.text) + 10))

    def press_v2d3off_plus(self, longpress):
        if not longpress:
            self.ids.v2d3off_val.text = format_number(str(float(self.ids.v2d3off_val.text) + 1))
        else:
            self.ids.v2d3off_val.text = format_number(str(float(self.ids.v2d3off_val.text) + 10))

    def press_v2d4off_plus(self, longpress):
        if not longpress:
            self.ids.v2d4off_val.text = format_number(str(float(self.ids.v2d4off_val.text) + 1))
        else:
            self.ids.v2d4off_val.text = format_number(str(float(self.ids.v2d4off_val.text) + 10))

    # ROW 3 PLUS BUTTONS
    def press_v3d1on_plus(self, longpress):
        if not longpress:
            self.ids.v3d1on_val.text = format_number(str(float(self.ids.v3d1on_val.text) + 1))
        else:
            self.ids.v3d1on_val.text = format_number(str(float(self.ids.v3d1on_val.text) + 10))

    def press_v3d2on_plus(self, longpress):
        if not longpress:
            self.ids.v3d2on_val.text = format_number(str(float(self.ids.v3d2on_val.text) + 1))
        else:
            self.ids.v3d2on_val.text = format_number(str(float(self.ids.v3d2on_val.text) + 10))

    def press_v3d3on_plus(self, longpress):
        if not longpress:
            self.ids.v3d3on_val.text = format_number(str(float(self.ids.v3d3on_val.text) + 1))
        else:
            self.ids.v3d3on_val.text = format_number(str(float(self.ids.v3d3on_val.text) + 10))

    def press_v3d4on_plus(self, longpress):
        if not longpress:
            self.ids.v3d4on_val.text = format_number(str(float(self.ids.v3d4on_val.text) + 1))
        else:
            self.ids.v3d4on_val.text = format_number(str(float(self.ids.v3d4on_val.text) + 10))

    def press_v3d1off_plus(self, longpress):
        if not longpress:
            self.ids.v3d1off_val.text = format_number(str(float(self.ids.v3d1off_val.text) + 1))
        else:
            self.ids.v3d1off_val.text = format_number(str(float(self.ids.v3d1off_val.text) + 10))

    def press_v3d2off_plus(self, longpress):
        if not longpress:
            self.ids.v3d2off_val.text = format_number(str(float(self.ids.v3d2off_val.text) + 1))
        else:
            self.ids.v3d2off_val.text = format_number(str(float(self.ids.v3d2off_val.text) + 10))

    def press_v3d3off_plus(self, longpress):
        if not longpress:
            self.ids.v3d3off_val.text = format_number(str(float(self.ids.v3d3off_val.text) + 1))
        else:
            self.ids.v3d3off_val.text = format_number(str(float(self.ids.v3d3off_val.text) + 10))

    def press_v3d4off_plus(self, longpress):
        if not longpress:
            self.ids.v3d4off_val.text = format_number(str(float(self.ids.v3d4off_val.text) + 1))
        else:
            self.ids.v3d4off_val.text = format_number(str(float(self.ids.v3d4off_val.text) + 10))

    # ROW 4 PLUS BUTTONS
    def press_v4d1on_plus(self, longpress):
        if not longpress:
            self.ids.v4d1on_val.text = format_number(str(float(self.ids.v4d1on_val.text) + 1))
        else:
            self.ids.v4d1on_val.text = format_number(str(float(self.ids.v4d1on_val.text) + 10))

    def press_v4d2on_plus(self, longpress):
        if not longpress:
            self.ids.v4d2on_val.text = format_number(str(float(self.ids.v4d2on_val.text) + 1))
        else:
            self.ids.v4d2on_val.text = format_number(str(float(self.ids.v4d2on_val.text) + 10))

    def press_v4d3on_plus(self, longpress):
        if not longpress:
            self.ids.v4d3on_val.text = format_number(str(float(self.ids.v4d3on_val.text) + 1))
        else:
            self.ids.v4d3on_val.text = format_number(str(float(self.ids.v4d3on_val.text) + 10))

    def press_v4d4on_plus(self, longpress):
        if not longpress:
            self.ids.v4d4on_val.text = format_number(str(float(self.ids.v4d4on_val.text) + 1))
        else:
            self.ids.v4d4on_val.text = format_number(str(float(self.ids.v4d4on_val.text) + 10))

    def press_v4d1off_plus(self, longpress):
        if not longpress:
            self.ids.v4d1off_val.text = format_number(str(float(self.ids.v4d1off_val.text) + 1))
        else:
            self.ids.v4d1off_val.text = format_number(str(float(self.ids.v4d1off_val.text) + 10))

    def press_v4d2off_plus(self, longpress):
        if not longpress:
            self.ids.v4d2off_val.text = format_number(str(float(self.ids.v4d2off_val.text) + 1))
        else:
            self.ids.v4d2off_val.text = format_number(str(float(self.ids.v4d2off_val.text) + 10))

    def press_v4d3off_plus(self, longpress):
        if not longpress:
            self.ids.v4d3off_val.text = format_number(str(float(self.ids.v4d3off_val.text) + 1))
        else:
            self.ids.v4d3off_val.text = format_number(str(float(self.ids.v4d3off_val.text) + 10))

    def press_v4d4off_plus(self, longpress):
        if not longpress:
            self.ids.v4d4off_val.text = format_number(str(float(self.ids.v4d4off_val.text) + 1))
        else:
            self.ids.v4d4off_val.text = format_number(str(float(self.ids.v4d4off_val.text) + 10))

    # CAMERA PLUS BUTTONS
    def press_camon_plus(self, longpress):
        if not longpress:
            self.ids.camon_val.text = format_number(str(float(self.ids.camon_val.text) + 1))
        else:
            self.ids.camon_val.text = format_number(str(float(self.ids.camon_val.text) + 10))

    def press_camoff_plus(self, longpress):
        if not longpress:
            self.ids.camoff_val.text = format_number(str(float(self.ids.camoff_val.text) + 1))
        else:
            self.ids.camoff_val.text = format_number(str(float(self.ids.camoff_val.text) + 10))

    # FLASH PLUS BUTTONS
    def press_flashon_plus(self, longpress):
        if not longpress:
            self.ids.flashon_val.text = format_number(str(float(self.ids.flashon_val.text) + 1))
        else:
            self.ids.flashon_val.text = format_number(str(float(self.ids.flashon_val.text) + 10))

    def press_flashoff_plus(self, longpress):
        if not longpress:
            self.ids.flashoff_val.text = format_number(str(float(self.ids.flashoff_val.text) + 1))
        else:
            self.ids.flashoff_val.text = format_number(str(float(self.ids.flashoff_val.text) + 10))

    # FIRE BUTTON CALLBACK
    def execute_sequence_callback(self):
        # self.ids.filestatus.text = ''
        # Verify which fields in the GUI are off. If a dropfield is off, then it is not to be passed towards the valve.
        v1 = list()
        if not self.ids.v1d1on.disabled:
            v1.append([self.ids.v1d1on_val.text, self.ids.v1d1off_val.text])
        if not self.ids.v1d2on.disabled:
            v1.append([self.ids.v1d2on_val.text, self.ids.v1d2off_val.text])
        if not self.ids.v1d3on.disabled:
            v1.append([self.ids.v1d3on_val.text, self.ids.v1d3off_val.text])
        if not self.ids.v1d4on.disabled:
            v1.append([self.ids.v1d4on_val.text, self.ids.v1d4off_val.text])
        v2 = list()
        if not self.ids.v2d1on.disabled:
            v2.append([self.ids.v2d1on_val.text, self.ids.v2d1off_val.text])
        if not self.ids.v2d2on.disabled:
            v2.append([self.ids.v2d2on_val.text, self.ids.v2d2off_val.text])
        if not self.ids.v2d3on.disabled:
            v2.append([self.ids.v2d3on_val.text, self.ids.v2d3off_val.text])
        if not self.ids.v2d4on.disabled:
            v2.append([self.ids.v2d4on_val.text, self.ids.v2d4off_val.text])
        v3 = list()
        if not self.ids.v3d1on.disabled:
            v3.append([self.ids.v3d1on_val.text, self.ids.v3d1off_val.text])
        if not self.ids.v3d2on.disabled:
            v3.append([self.ids.v3d2on_val.text, self.ids.v3d2off_val.text])
        if not self.ids.v3d3on.disabled:
            v3.append([self.ids.v3d3on_val.text, self.ids.v3d3off_val.text])
        if not self.ids.v3d4on.disabled:
            v3.append([self.ids.v3d4on_val.text, self.ids.v3d4off_val.text])
        v4 = list()
        if not self.ids.v4d1on.disabled:
            v4.append([self.ids.v4d1on_val.text, self.ids.v4d1off_val.text])
        if not self.ids.v4d2on.disabled:
            v4.append([self.ids.v4d2on_val.text, self.ids.v4d2off_val.text])
        if not self.ids.v4d3on.disabled:
            v4.append([self.ids.v4d3on_val.text, self.ids.v4d3off_val.text])
        if not self.ids.v4d4on.disabled:
            v4.append([self.ids.v4d4on_val.text, self.ids.v4d4off_val.text])
        flashon = self.ids.flashon_val.text
        if self.ids.f1toggle.color == [1, 1, 1, 1]:
            flash1on = True
        else:
            flash1on = False
        if self.ids.f2toggle.color == [1, 1, 1, 1]:
            flash2on = True
        else:
            flash2on = False
        if self.ids.f3toggle.color == [1, 1, 1, 1]:
            flash3on = True
        else:
            flash3on = False
        if self.ids.mirrorlockup_on.active:
            mirrorlockup = True
        else:
            mirrorlockup = False
        DropPiUI_Dropper.main(flash_def=self.ids.flashoff_val.text, cam_def=self.ids.camoff_val.text,
                              cam_on=self.ids.camon_val.text, flash_on=flashon, flash1_on=flash1on,
                              flash2_on=flash2on, flash3_on=flash3on,
                              v1times=v1, v2times=v2, v3times=v3, v4times=v4, mirror=mirrorlockup)

    # PURGE BUTTONS, PRESS AND RELEASE
    def press_purgev1(self):
        relay_on(VALVE_1)

    def release_purgev1(self):
        relay_off(VALVE_1)

    def press_purgev2(self):
        relay_on(VALVE_2)

    def release_purgev2(self):
        relay_off(VALVE_2)

    def press_purgev3(self):
        relay_on(VALVE_3)

    def release_purgev3(self):
        relay_off(VALVE_3)

    def press_purgev4(self):
        relay_on(VALVE_4)

    def release_purgev4(self):
        relay_off(VALVE_4)

    # EXIT BUTTON CALLBACK
    def execute_exit_callback(self):
        App.get_running_app().stop()


class FileScreen(Screen):

    def on_enter(self, *args):
        self.manager.get_screen("filescreen").ids.filescreen_status.text = ''
        pass

    def on_leave(self, *args):
        self.manager.get_screen("filescreen").ids.filescreen_status.text = ''
        pass

    def select(self, filename):
        global template_file
        try:
            self.manager.get_screen("filescreen").ids.filename_val.text = filename[0]
            template_file = filename[0]
        except:
            pass

    # LOAD BUTTON CALLBACK
    def execute_load_callback(self):
        global template_file
        self.manager.get_screen(
            "filescreen").ids.filescreen_status.text = ''
        if template_file == '':
            self.manager.get_screen(
                "filescreen").ids.filescreen_status.text = 'Please select a file first or enter a valid filename'
        else:
            template_file = self.manager.get_screen("filescreen").ids.filename_val.text
            store = JsonStore(template_file)
            # We need to start reading all settings from the file.
            if store.get('defaults')['flash1_on'] != '':
                self.manager.get_screen("mainscreen").ids.flashon_val.text = store.get('defaults')['flash1_on']
                self.manager.get_screen("mainscreen").ids.f1toggle.color = (1, 1, 1, 1)
            else:
                self.manager.get_screen("mainscreen").ids.f1toggle.color = (.5, .5, 1, 1)
            if store.get('defaults')['flash2_on'] != '':
                self.manager.get_screen("mainscreen").ids.flashon_val.text = store.get('defaults')['flash2_on']
                self.manager.get_screen("mainscreen").ids.f2toggle.color = (1, 1, 1, 1)
            else:
                self.manager.get_screen("mainscreen").ids.f2toggle.color = (.5, .5, 1, 1)
            if store.get('defaults')['flash3_on'] != '':
                self.manager.get_screen("mainscreen").ids.flashon_val.text = store.get('defaults')['flash3_on']
                self.manager.get_screen("mainscreen").ids.f3toggle.color = (1, 1, 1, 1)
            else:
                self.manager.get_screen("mainscreen").ids.f3toggle.color = (.5, .5, 1, 1)
            self.manager.get_screen("mainscreen").ids.flashoff_val.text = store.get('defaults')['flash_def']
            self.manager.get_screen("mainscreen").ids.camoff_val.text = store.get('defaults')['cam_def']
            self.manager.get_screen("mainscreen").ids.camon_val.text = store.get('defaults')['cam_on']
            self.manager.get_screen("mainscreen").ids.mirrorlockup_on.active = store.get('defaults')['mirror_lock']

            # If read values are non-empty, we need to enable the controls in the GUI
            vtimes = list()
            # VALVE 1 TIMES, ALL OF THEM
            vtimes = store.get('defaults')['v1times']
            if len(vtimes) >= 1:
                self.manager.get_screen("mainscreen").ids.valvetoggle1.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d2toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d1on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d1on.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d1off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d1off.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d1on_val.text = vtimes[0][0]
                self.manager.get_screen("mainscreen").ids.v1d1off_val.text = vtimes[0][1]
            else:
                self.manager.get_screen("mainscreen").ids.valvetoggle1.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d2toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v1d1on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d1on.disabled = True
                self.manager.get_screen("mainscreen").ids.v1d1off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d1off.disabled = True
            if len(vtimes) >= 2:
                self.manager.get_screen("mainscreen").ids.v1d2toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d3toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d2on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d2on.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d2off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d2off.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d2on_val.text = vtimes[1][0]
                self.manager.get_screen("mainscreen").ids.v1d2off_val.text = vtimes[1][1]
            else:
                self.manager.get_screen("mainscreen").ids.v1d2toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d3toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v1d2on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d2on.disabled = True
                self.manager.get_screen("mainscreen").ids.v1d2off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d2off.disabled = True
            if len(vtimes) >= 3:
                self.manager.get_screen("mainscreen").ids.v1d3toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d4toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d3on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d3on.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d3off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d3off.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d3on_val.text = vtimes[2][0]
                self.manager.get_screen("mainscreen").ids.v1d3off_val.text = vtimes[2][1]
            else:
                self.manager.get_screen("mainscreen").ids.v1d3toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d4toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v1d3on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d3on.disabled = True
                self.manager.get_screen("mainscreen").ids.v1d3off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d3off.disabled = True
            if len(vtimes) >= 4:
                self.manager.get_screen("mainscreen").ids.v1d4toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d4on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d4on.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d4off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v1d4off.disabled = False
                self.manager.get_screen("mainscreen").ids.v1d4on_val.text = vtimes[3][0]
                self.manager.get_screen("mainscreen").ids.v1d4off_val.text = vtimes[3][1]
            else:
                self.manager.get_screen("mainscreen").ids.v1d4toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v1d4on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d4on.disabled = True
                self.manager.get_screen("mainscreen").ids.v1d4off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v1d4off.disabled = True

            # VALVE 2 TIMES, ALL OF THEM
            vtimes = store.get('defaults')['v2times']
            if len(vtimes) >= 1:
                self.manager.get_screen("mainscreen").ids.valvetoggle2.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d2toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d1on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d1on.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d1off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d1off.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d1on_val.text = vtimes[0][0]
                self.manager.get_screen("mainscreen").ids.v2d1off_val.text = vtimes[0][1]
            else:
                self.manager.get_screen("mainscreen").ids.valvetoggle2.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d2toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v2d1on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d1on.disabled = True
                self.manager.get_screen("mainscreen").ids.v2d1off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d1off.disabled = True
            if len(vtimes) >= 2:
                self.manager.get_screen("mainscreen").ids.v2d2toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d3toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d2on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d2on.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d2off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d2off.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d2on_val.text = vtimes[1][0]
                self.manager.get_screen("mainscreen").ids.v2d2off_val.text = vtimes[1][1]
            else:
                self.manager.get_screen("mainscreen").ids.v2d2toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d3toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v2d2on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d2on.disabled = True
                self.manager.get_screen("mainscreen").ids.v2d2off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d2off.disabled = True
            if len(vtimes) >= 3:
                self.manager.get_screen("mainscreen").ids.v2d3toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d4toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d3on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d3on.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d3off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d3off.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d3on_val.text = vtimes[2][0]
                self.manager.get_screen("mainscreen").ids.v2d3off_val.text = vtimes[2][1]
            else:
                self.manager.get_screen("mainscreen").ids.v2d3toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d4toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v2d3on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d3on.disabled = True
                self.manager.get_screen("mainscreen").ids.v2d3off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d3off.disabled = True
            if len(vtimes) >= 4:
                self.manager.get_screen("mainscreen").ids.v2d4toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d4on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d4on.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d4off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v2d4off.disabled = False
                self.manager.get_screen("mainscreen").ids.v2d4on_val.text = vtimes[3][0]
                self.manager.get_screen("mainscreen").ids.v2d4off_val.text = vtimes[3][1]
            else:
                self.manager.get_screen("mainscreen").ids.v2d4toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v2d4on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d4on.disabled = True
                self.manager.get_screen("mainscreen").ids.v2d4off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v2d4off.disabled = True

            # VALVE 3 TIMES, ALL OF THEM
            vtimes = store.get('defaults')['v3times']
            if len(vtimes) >= 1:
                self.manager.get_screen("mainscreen").ids.valvetoggle3.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d2toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d1on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d1on.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d1off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d1off.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d1on_val.text = vtimes[0][0]
                self.manager.get_screen("mainscreen").ids.v3d1off_val.text = vtimes[0][1]
            else:
                self.manager.get_screen("mainscreen").ids.valvetoggle3.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d2toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v3d1on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d1on.disabled = True
                self.manager.get_screen("mainscreen").ids.v3d1off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d1off.disabled = True
            if len(vtimes) >= 2:
                self.manager.get_screen("mainscreen").ids.v3d2toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d3toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d2on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d2on.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d2off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d2off.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d2on_val.text = vtimes[1][0]
                self.manager.get_screen("mainscreen").ids.v3d2off_val.text = vtimes[1][1]
            else:
                self.manager.get_screen("mainscreen").ids.v3d2toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d3toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v3d2on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d2on.disabled = True
                self.manager.get_screen("mainscreen").ids.v3d2off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d2off.disabled = True
            if len(vtimes) >= 3:
                self.manager.get_screen("mainscreen").ids.v3d3toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d4toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d3on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d3on.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d3off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d3off.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d3on_val.text = vtimes[2][0]
                self.manager.get_screen("mainscreen").ids.v3d3off_val.text = vtimes[2][1]
            else:
                self.manager.get_screen("mainscreen").ids.v3d3toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d4toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v3d3on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d3on.disabled = True
                self.manager.get_screen("mainscreen").ids.v3d3off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d3off.disabled = True
            if len(vtimes) >= 4:
                self.manager.get_screen("mainscreen").ids.v3d4toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d4on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d4on.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d4off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v3d4off.disabled = False
                self.manager.get_screen("mainscreen").ids.v3d4on_val.text = vtimes[3][0]
                self.manager.get_screen("mainscreen").ids.v3d4off_val.text = vtimes[3][1]
            else:
                self.manager.get_screen("mainscreen").ids.v3d4toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v3d4on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d4on.disabled = True
                self.manager.get_screen("mainscreen").ids.v3d4off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v3d4off.disabled = True

            # VALVE 4 TIMES, ALL OF THEM
            vtimes = store.get('defaults')['v4times']
            if len(vtimes) >= 1:
                self.manager.get_screen("mainscreen").ids.valvetoggle4.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d2toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d1on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d1on.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d1off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d1off.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d1on_val.text = vtimes[0][0]
                self.manager.get_screen("mainscreen").ids.v4d1off_val.text = vtimes[0][1]
            else:
                self.manager.get_screen("mainscreen").ids.valvetoggle4.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d2toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v4d1on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d1on.disabled = True
                self.manager.get_screen("mainscreen").ids.v4d1off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d1off.disabled = True
            if len(vtimes) >= 2:
                self.manager.get_screen("mainscreen").ids.v4d2toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d3toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d2on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d2on.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d2off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d2off.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d2on_val.text = vtimes[1][0]
                self.manager.get_screen("mainscreen").ids.v4d2off_val.text = vtimes[1][1]
            else:
                self.manager.get_screen("mainscreen").ids.v4d2toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d3toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v4d2on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d2on.disabled = True
                self.manager.get_screen("mainscreen").ids.v4d2off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d2off.disabled = True
            if len(vtimes) >= 3:
                self.manager.get_screen("mainscreen").ids.v4d3toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d4toggle.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d3on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d3on.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d3off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d3off.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d3on_val.text = vtimes[2][0]
                self.manager.get_screen("mainscreen").ids.v4d3off_val.text = vtimes[2][1]
            else:
                self.manager.get_screen("mainscreen").ids.v4d3toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d4toggle.disabled = True
                self.manager.get_screen("mainscreen").ids.v4d3on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d3on.disabled = True
                self.manager.get_screen("mainscreen").ids.v4d3off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d3off.disabled = True
            if len(vtimes) >= 4:
                self.manager.get_screen("mainscreen").ids.v4d4toggle.color = (1, 1, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d4on.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d4on.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d4off.opacity = 1
                self.manager.get_screen("mainscreen").ids.v4d4off.disabled = False
                self.manager.get_screen("mainscreen").ids.v4d4on_val.text = vtimes[3][0]
                self.manager.get_screen("mainscreen").ids.v4d4off_val.text = vtimes[3][1]
            else:
                self.manager.get_screen("mainscreen").ids.v4d4toggle.color = (.5, .5, 1, 1)
                self.manager.get_screen("mainscreen").ids.v4d4on.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d4on.disabled = True
                self.manager.get_screen("mainscreen").ids.v4d4off.opacity = 0
                self.manager.get_screen("mainscreen").ids.v4d4off.disabled = True

            self.manager.get_screen("filescreen").ids.filescreen_status.text = 'Loaded from {} succesfully.'.format(
                template_file)

    # SAVE BUTTON CALLBACK
    def execute_save_callback(self):
        global template_file
        self.manager.get_screen(
            "filescreen").ids.filescreen_status.text = ''
        if template_file == '':
            self.manager.get_screen(
                "filescreen").ids.filescreen_status.text = 'Please select a file first or enter a valid filename'
        else:
            template_file = self.manager.get_screen("filescreen").ids.filename_val.text
            store = JsonStore(template_file)
            # Verify which fields in the GUI are off. If a dropfield is off, then it is not to be passed towards the valve.
            v1 = list()
            if not self.manager.get_screen("mainscreen").ids.v1d1on.disabled:
                v1.append([self.manager.get_screen("mainscreen").ids.v1d1on_val.text,
                           self.manager.get_screen("mainscreen").ids.v1d1off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v1d2on.disabled:
                v1.append([self.manager.get_screen("mainscreen").ids.v1d2on_val.text,
                           self.manager.get_screen("mainscreen").ids.v1d2off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v1d3on.disabled:
                v1.append([self.manager.get_screen("mainscreen").ids.v1d3on_val.text,
                           self.manager.get_screen("mainscreen").ids.v1d3off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v1d4on.disabled:
                v1.append([self.manager.get_screen("mainscreen").ids.v1d4on_val.text,
                           self.manager.get_screen("mainscreen").ids.v1d4off_val.text])
            v2 = list()
            if not self.manager.get_screen("mainscreen").ids.v2d1on.disabled:
                v2.append([self.manager.get_screen("mainscreen").ids.v2d1on_val.text,
                           self.manager.get_screen("mainscreen").ids.v2d1off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v2d2on.disabled:
                v2.append([self.manager.get_screen("mainscreen").ids.v2d2on_val.text,
                           self.manager.get_screen("mainscreen").ids.v2d2off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v2d3on.disabled:
                v2.append([self.manager.get_screen("mainscreen").ids.v2d3on_val.text,
                           self.manager.get_screen("mainscreen").ids.v2d3off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v2d4on.disabled:
                v2.append([self.manager.get_screen("mainscreen").ids.v2d4on_val.text,
                           self.manager.get_screen("mainscreen").ids.v2d4off_val.text])
            v3 = list()
            if not self.manager.get_screen("mainscreen").ids.v3d1on.disabled:
                v3.append([self.manager.get_screen("mainscreen").ids.v3d1on_val.text,
                           self.manager.get_screen("mainscreen").ids.v3d1off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v3d2on.disabled:
                v3.append([self.manager.get_screen("mainscreen").ids.v3d2on_val.text,
                           self.manager.get_screen("mainscreen").ids.v3d2off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v3d3on.disabled:
                v3.append([self.manager.get_screen("mainscreen").ids.v3d3on_val.text,
                           self.manager.get_screen("mainscreen").ids.v3d3off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v3d4on.disabled:
                v3.append([self.manager.get_screen("mainscreen").ids.v3d4on_val.text,
                           self.manager.get_screen("mainscreen").ids.v3d4off_val.text])
            v4 = list()
            if not self.manager.get_screen("mainscreen").ids.v4d1on.disabled:
                v4.append([self.manager.get_screen("mainscreen").ids.v4d1on_val.text,
                           self.manager.get_screen("mainscreen").ids.v4d1off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v4d2on.disabled:
                v4.append([self.manager.get_screen("mainscreen").ids.v4d2on_val.text,
                           self.manager.get_screen("mainscreen").ids.v4d2off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v4d3on.disabled:
                v4.append([self.manager.get_screen("mainscreen").ids.v4d3on_val.text,
                           self.manager.get_screen("mainscreen").ids.v4d3off_val.text])
            if not self.manager.get_screen("mainscreen").ids.v4d4on.disabled:
                v4.append([self.manager.get_screen("mainscreen").ids.v4d4on_val.text,
                           self.manager.get_screen("mainscreen").ids.v4d4off_val.text])
            flash1 = ''
            flash2 = ''
            flash3 = ''
            if self.manager.get_screen("mainscreen").ids.f1toggle.color == [1, 1, 1, 1]:
                flash1 = self.manager.get_screen("mainscreen").ids.flashon_val.text
            else:
                flash1 = ''
            if self.manager.get_screen("mainscreen").ids.f2toggle.color == [1, 1, 1, 1]:
                flash2 = self.manager.get_screen("mainscreen").ids.flashon_val.text
            else:
                flash2 = ''
            if self.manager.get_screen("mainscreen").ids.f3toggle.color == [1, 1, 1, 1]:
                flash3 = self.manager.get_screen("mainscreen").ids.flashon_val.text
            else:
                flash3 = ''
            # put some values
            store.put('defaults', mirror_lock=self.manager.get_screen("mainscreen").ids.mirrorlockup_on.active,
                      flash_def=self.manager.get_screen("mainscreen").ids.flashoff_val.text,
                      cam_def=self.manager.get_screen("mainscreen").ids.camoff_val.text,
                      cam_on=self.manager.get_screen("mainscreen").ids.camon_val.text, flash1_on=flash1,
                      flash2_on=flash2, flash3_on=flash3,
                      v1times=v1, v2times=v2, v3times=v3, v4times=v4)
            self.manager.get_screen("filescreen").ids.filescreen_status.text = 'Saved to {} succesfully.'.format(
                template_file)


# The ScreenManager controls moving between screens
class ScreenManagement(ScreenManager):
    pass


class DropPiUIApp(App):
    instance_selected_string = ''
    instance_selected = None
    num_value = 0

    def build(self):
        #Window.bind(on_request_close=self.on_request_close)
        self.initialize_global_vars()
        return ScreenManagement()

    def initialize_global_vars(self):
        global root_folder
        root_folder = App.user_data_dir

    def exit(self):
        App.get_running_app().stop()

    ##def on_request_close(self):
        # self.textpopup(title='Exit', text='Are you sure?')
      #  return True


if __name__ == "__main__":
    Window.borderless = True
    Window.maximize()
    DropPiUIApp().run()
