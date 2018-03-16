import sys

import math
import toga
from toga.style import Pack


class TimeInput(toga.Box):
    def __init__(self,
            initial=None, prefix=None, suffix=None, readonly=False, on_change=None,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.parent_on_change = on_change
        self._value=None

        if initial is not None:
            assert isinstance(initial, int), "initial must be a Integer!"

        time_box = toga.Box(style=Pack(direction=toga.ROW, padding=5))

        if prefix is not None:
            time_label_right = toga.Label(prefix, style=Pack(text_align=toga.RIGHT))
            time_box.add(time_label_right)

        self.time_input_hh = toga.NumberInput(
            min_value=0, max_value=99, on_change=self.on_change_handler
        )
        time_box.add(self.time_input_hh)

        time_label_hh_mm = toga.Label(":", style=Pack(text_align=toga.CENTER))
        time_box.add(time_label_hh_mm)

        self.time_input_mm = toga.NumberInput(
            min_value=0, max_value=99, on_change=self.on_change_handler
        )
        time_box.add(self.time_input_mm)

        time_label_mm_ss = toga.Label(":", style=Pack(text_align=toga.CENTER))
        time_box.add(time_label_mm_ss)

        self.time_input_ss = toga.NumberInput(
            min_value=0, max_value=99, on_change=self.on_change_handler
        )
        time_box.add(self.time_input_ss)

        if suffix is not None:
            time_label_left = toga.Label(suffix, style=Pack(text_align=toga.LEFT))
            time_box.add(time_label_left)

        self.add(time_box)

        self.value = initial

    def on_change_handler(self, widget):
        seconds = self.time_input_ss.value
        seconds += self.time_input_mm.value * 60
        seconds += self.time_input_hh.value * 60 * 60
        self.value = seconds
        self.parent_on_change(widget)

    @property
    def value(self):
        """Current value contained by the widget

        Returns:
            The current value(int) of the widget. Returns None
            if the field has no value set.
        """
        return self._value

    @value.setter
    def value(self, value):
        try:
            seconds = int(value)
        except ValueError:
            raise ValueError("value must be an integer")

        self._value = seconds

        hours = math.floor(seconds / 60 / 60)
        self.time_input_hh.value = hours
        if hours>0:
            seconds -= (hours * 60 * 60)

        minutes = math.floor(seconds / 60)
        self.time_input_mm.value = minutes
        seconds -= minutes * 60

        self.time_input_ss.value = seconds



