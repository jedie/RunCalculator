
"""
    https://github.com/pybee/toga/
    https://toga.readthedocs.io/en/latest/reference/index.html
"""

import decimal
import gettext
import logging
import sys

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from run_calculator.utils import calc_pace, human_distance, human_duration
from run_calculator.widgets.time_input import TimeInput

log = logging.getLogger(__name__)


_ = gettext.gettext


BASE_DISTANCES = (
    0.4,
    0.8,
    1,
    5,
    10,
    21.0975,
    42.195,
    100
)


class RunCalculator(toga.App):
    def startup(self):
        # Create the main window
        self.main_window = toga.MainWindow(self.name)

        main_box = toga.Box(style=Pack(direction=COLUMN, padding_top=10))

        #
        #_____________________________________________________________________
        # Distance __ km
        #
        distance_box = toga.Box(style=Pack(direction=ROW, padding=5))

        distance_label_right = toga.Label("Distance", style=Pack(text_align=toga.RIGHT))
        distance_box.add(distance_label_right)

        self.distance_input = toga.NumberInput(
            min_value=0, max_value=99,
            on_change=self.button_handler,
        )
        self.distance_input.value = 10
        distance_box.add(self.distance_input)

        distance_label_left = toga.Label("km", style=Pack(text_align=toga.LEFT))
        distance_box.add(distance_label_left)

        main_box.add(distance_box)

        #
        #_____________________________________________________________________
        # Time __:__:__ hh:mm:ss
        #
        self.time_input = TimeInput(
            # initial=(12*60*60) + (34*60) + 56, # 12:34:56
            initial=1*60*60, # 1:00:00
            prefix="Time", suffix="hh:mm:ss",
            style=Pack(direction=ROW, padding=5),
            on_change=self.button_handler,
        )

        main_box.add(self.time_input)

        #
        #_____________________________________________________________________
        # Calculate button
        #
        calc_box = toga.Box(style=Pack(direction=ROW, padding=5))
        calc_button = toga.Button("Calculate", on_press=self.button_handler)
        calc_button.style.padding = 50
        calc_button.style.flex = 1
        calc_box.add(calc_button)
        main_box.add(calc_box)

        #
        #
        # left_container = toga.OptionContainer()
        #
        table_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.table = toga.Table(
            headings=["Distance", "Time", "Pace"],
            style=Pack(flex=1)
        )
        table_box.add(self.table)
        main_box.add(table_box)

        # update table with initial values:
        self.button_handler(widget=None)

        self.main_window.content = main_box
        self.main_window.show()

    def button_handler(self, widget):
        try:
            distance=self.distance_input.value
            seconds=self.time_input.value
        except AttributeError:
            # FIXME: fired from:
            # run_calculator.widgets.time_input.TimeInput#on_change_handler
            log.exception("FIXME! handler is fired in init phase:")
            return

        pace = calc_pace(distance, seconds)

        distances = set(BASE_DISTANCES)
        distances.add(self.distance_input.value)

        data = []
        for no, distance in enumerate(sorted(distances)):
            distance = decimal.Decimal(distance)
            duration = distance * pace * decimal.Decimal(60)

            distance_txt = human_distance(distance)
            duration_txt = human_duration(duration)
            pace_txt = "{:.2f} Min/km".format(pace)

            data.append(
                (distance_txt, duration_txt, pace_txt)
            )
        self.table.data = data


def main():
    return RunCalculator("Run Calculator", "org.pybee.jensdiemer.run_calculator")
