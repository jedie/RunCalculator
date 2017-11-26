
"""
    https://yourpart.eu/p/PyDDF-Sprint-2017-kivy
"""

from __future__ import print_function, absolute_import, unicode_literals

import math
from functools import partial

from kivy.config import Config

from kivy.properties import OptionProperty

Config.set("kivy", "log_level", "debug")


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.core.window import Window


class IntegerInput(TextInput):
    input_type = OptionProperty( # kivy.uix.behaviors.FocusBehavior
        'number',
        # 'datetime',
        # 'text', 'number', 'url', 'mail', 'datetime', 'tel', 'address'
    )

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.input_filter = "int" # kivy.uix.textinput.TextInput#insert_text

        self.str2number_func = int
        self.min_value=min_value
        self.max_value=max_value
        self.value = None
        super(IntegerInput, self).__init__(**kwargs)

    def is_valid(self, substring):
        try:
            value = self.str2number_func(substring)
        except ValueError as err:
            Logger.debug("insert_text(): %s", err)
            return False

        if self.min_value is not None and value<self.min_value:
            Logger.debug("Validation error min value")
            return False

        if self.max_value is not None and value>self.max_value:
            Logger.debug("Validation error max value")
            return False

        return True

    def insert_text(self, substring, from_undo=False):
        if not self.is_valid(self.text + substring):
            return # Ignore not valid values

        Logger.debug("insert_text(): %r" % substring)
        super(IntegerInput, self).insert_text(substring, from_undo=from_undo)
        self.value = int(self.text)



class FloatInput(TextInput):
    input_type = OptionProperty( # kivy.uix.behaviors.FocusBehavior
        'number',
        # 'text', 'number', 'url', 'mail', 'datetime', 'tel', 'address'
    )
    def __init__(self, **kwargs):
        self.input_filter = "float" # kivy.uix.textinput.TextInput#insert_text
        super(FloatInput, self).__init__(**kwargs)


class TimeTextInput(BoxLayout):
    def __init__(self, hours=True, **kwargs):
        self.hours = hours

        self.register_event_type('on_time')
        super(TimeTextInput, self).__init__(**kwargs)

        self.seconds = 0

        if self.hours:
            self.text_hh = IntegerInput(
                multiline=False,
                min_value=0, max_value=None,
            )
            self.text_hh.bind(text=partial(self.on_value, key="hour"))
            self.add_widget(self.text_hh)

            self.add_widget(Label(text=":"))

        self.text_mm = IntegerInput(
            multiline=False,
            min_value=0,
            max_value=None,
        )
        self.text_mm.bind(text=partial(self.on_value, key="minute"))
        self.add_widget(self.text_mm)

        self.add_widget(Label(text=":"))

        self.text_ss = IntegerInput(
            multiline=False,
            min_value=0,
            max_value=None,
        )
        self.text_ss.bind(text=partial(self.on_value, key="second"))
        self.add_widget(self.text_ss)

    def update_seconds(self):
        minutes = self.text_mm.value or 0
        seconds = self.text_ss.value or 0
        self.seconds = (minutes*60) +  seconds

        if self.hours:
            hours = self.text_hh.value or 0
            self.seconds += hours*60*60

        Logger.debug("update_seconds(): seconds: %i" % self.seconds)

        self.dispatch('on_time', self.seconds)

    def set_seconds(self, seconds):
        Logger.debug("set_seconds(): %r" % seconds)
        if self.hours:
            hours = math.floor(seconds / 60.0 / 60.0)
            Logger.debug("set_seconds() hours: %i" % hours)
            self.text_hh.text = "%i" % hours
            if hours>0:
                seconds -= hours * 60

        minutes = math.floor(seconds / 60.0)
        Logger.debug("set_seconds() minutes: %i" % minutes)
        self.text_mm.text = "%i" % minutes
        seconds -= minutes * 60

        Logger.debug("set_seconds() seconds: %i" % seconds)
        self.text_ss.text = "%i" % seconds

    def on_value(self, instance, value, key):
        if value:
            instance.text = value
            self.update_seconds()

    def on_time(self, time):
        pass



class RunCalcApp(App):
    def __init__(self, *args, **kwargs):
        super(RunCalcApp, self).__init__(*args, **kwargs)
        self.distance = None
        self.time_seconds = None
        self.pace = None
        
    def build(self):
        root = BoxLayout(orientation='vertical')

        #---------------------------------------------------------------------

        root.add_widget(Label(text='Distance [km]'))
        text_distance = FloatInput(multiline=False)
        text_distance.bind(text=self.on_distance)
        root.add_widget(text_distance)

        #---------------------------------------------------------------------

        root.add_widget(Label(text='Time [hh:mm:ss]'))
        text_time = TimeTextInput(hours=True)
        text_time.bind(on_time=self.on_time)
        root.add_widget(text_time)

        #---------------------------------------------------------------------

        root.add_widget(Label(text='Pace [mm:ss]'))
        self.text_pace = TimeTextInput(hours=False)
        self.text_pace.bind(on_time=self.on_pace)
        root.add_widget(self.text_pace)

        #---------------------------------------------------------------------

        root.add_widget(Label(text='info:'))
        self.textbox_info = TextInput(multiline=False)
        root.add_widget(self.textbox_info)

        return root

    def calculate_pace(self):
        Logger.info("calculate_pace(): distance %r time %r", self.distance, self.time_seconds)

        if self.distance is None:
            Logger.info("Distance emtpy")
            return

        if self.time_seconds is None:
            Logger.info("Time emtpy")
            return

        self.pace = calc_pace(
            distance=self.distance,
            seconds=self.time_seconds
        )
        self.textbox_info.text = "%.2f min/km." % self.pace
        self.text_pace.set_seconds(self.pace * 60.0)

    def on_distance(self, instance, value):
        print("on_distance():", repr(value))
        if value:
            try:
                self.distance = float(value)
            except ValueError as err:
                Logger.error("on_distance(): %s", err)
                self.textbox_info.text = "Distance value error %s" % err
            else:
                self.textbox_info.text = "Set distance to: %s" % instance.text
                self.calculate_pace()
            instance.text = "%.4f" % self.distance

    def on_time(self, instance, time):
        Logger.debug("RunCalcApp().on_time(): %r", time)
        self.time_seconds = time
        self.calculate_pace()
        return True # ignore other binds

    def on_pace(self, instance, time):
        Logger.debug("RunCalcApp().on_pace(): %r", time)
        return True # ignore other binds


def calc_pace(distance, seconds):
    """
    >>> calc_pace(distance=10, seconds=1*60*60)
    6.0
    """
    Logger.info("calculate_pace(): distance %r time %r", distance, seconds)
    pace = (seconds/60.0) / distance
    return pace



if __name__ == '__main__':
    assert calc_pace(distance=10, seconds=1*60*60) == 6.0

    Window.clearcolor = (0.5, 0.5, 0.5, 1)
    RunCalcApp().run()
