# -*- coding: utf-8 -*-

import time
import logging
import pigpio

import numpy as np
from typing import Callable

class RotaryEncoder:

    # use rotational encoding table for software debouncing
    # see https://www.best-microcontroller-projects.com/rotary-encoder.html
    rot_enc_table = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]

    def __init__(self,
                 push_cback: Callable,
                 cw_cback: Callable,
                 ccw_cback: Callable,
                 push_pin: int = 22,
                 clk_pin: int = 17,
                 dt_pin: int = 27,
                 push_time: float = 0.4,
                 ) -> None:

        self._logger = logging.getLogger(__name__)

        self.push_time = push_time
        self.push_called = time.time()

        # set pins
        self.push_pin = push_pin
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin

        # set callbacks
        self._push_cback = push_cback
        self._cw_cback = cw_cback
        self._ccw_cback = ccw_cback

        # GPIO
        self.gpio = pigpio.pi()
        # set all pins to input
        self.gpio.set_mode(self.push_pin, pigpio.INPUT)
        self.gpio.set_mode(self.clk_pin, pigpio.INPUT)
        self.gpio.set_mode(self.dt_pin, pigpio.INPUT)
        self._logger.debug(
            "pins %s, %s, %s set to GPIO input",
            self.push_pin, self.clk_pin, self.dt_pin)

        # activate internal pull-up resistor
        self.gpio.set_pull_up_down(self.push_pin, pigpio.PUD_UP)
        self.gpio.set_pull_up_down(self.clk_pin, pigpio.PUD_UP)
        self.gpio.set_pull_up_down(self.dt_pin, pigpio.PUD_UP)
        self._logger.debug(
            "pins %s, %s, %s pulled up",
            self.push_pin, self.clk_pin, self.dt_pin)

        # prep software debouncing
        self.prev_state = self.gpio.read(self.clk_pin)
        self.prev_next_code = np.uint8(0)
        self.store = np.uint16(0)

        # register callbacks
        self._push_cback_handle = self.gpio.callback(
            self.push_pin,
            pigpio.FALLING_EDGE,
            self._push_cback)

        self._cw_cback_handle = self.gpio.callback(
            self.clk_pin,
            pigpio.FALLING_EDGE,
            self._rotate_filter_cback)

        self._clk_cback_handle = self.gpio.callback(
            self.clk_pin,
            pigpio.EITHER_EDGE,
            self._rotate_filter_cback)

        self._dt_cback_handle = self.gpio.callback(
            self.dt_pin,
            pigpio.EITHER_EDGE,
            self._rotate_filter_cback)

        self._logger.debug(
            "registered callback on pin %s %s %s",
            self.push_pin, self.clk_pin, self.dt_pin)

        self._logger.debug("Instantiation successful")

    def _read_rotary(self):
        """
        Reads the rotary instruction(s)
        :return: boolean
        """
        # disabling rotary functions if push knob depressed
        if self.gpio.read(self.push_pin) == 0:
            self.push_called = time.time()
            self._logger.debug("debouncing from push button")
            return 0
        clk_state = self.gpio.read(self.clk_pin)
        dt_state = self.gpio.read(self.dt_pin)
        self._logger.debug("saved digital read states for pins %s and %s",
                           self.clk_pin, self.dt_pin)

        self.prev_next_code <<= np.uint8(2)
        self.prev_next_code &= np.uint8(0x0f)  # just hold to the 4 LSB
        if (clk_state):
            self.prev_next_code |= np.uint8(0x02)
        if (dt_state):
            self.prev_next_code |= np.uint8(0x01)
        self.prev_next_code &= np.uint8(0x0f)  # just hold to the 4 LSB

        # If valid then store as 16 bit data.
        if (self.rot_enc_table[self.prev_next_code]):
            self.store <<= np.uint16(4)
            self.store |= self.prev_next_code
            if (self.store & 0xff) == 0x2b:
                return 1
            if (self.store & 0xff) == 0x17:
                return -1
        return 0

    def _push_filter_callback(self):
        self._logger.debug("push callback triggered")
        push_state = self.gpio.read(self.push_pin)
        if time.time() - self.push_called > self.push_time:
            if push_state == 0:
                self._push_callback()
        self.push_called = time.time()

    def _rotate_filter_cback(self):
        self._logger.debug("rotate callback triggered")
        direction = self._read_rotary()
        if not direction == 0:
            if direction == 1:
                self._cw_cback()
            elif direction == -1:
                self._ccw_cback()
