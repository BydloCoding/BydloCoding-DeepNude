import random

from vk_api import keyboard

from SDK.jsonExtension import StructByAction


class Keyboard(keyboard.VkKeyboard):
    colors = {"blue": "primary", "white": "default", "red": "negative", "green": "positive"}

    def __init__(self, buttons=None, strategy="default", one_time=False, inline=False):
        if buttons is None:
            buttons = []
        self.strategy = strategy
        super().__init__(one_time=one_time, inline=inline)
        self.button_index = 0
        if type(buttons) is list:
            self.add_from_list(buttons)
        elif type(buttons) is dict:
            self.add_from_dict(buttons)
        elif type(buttons) is str:
            self.add_button(buttons, color=Keyboard.colors["green"])
        elif isinstance(buttons, StructByAction):
            self.add_from_list(buttons.dictionary)

    @classmethod
    def byKeyboard(cls, newKb):
        if isinstance(newKb, cls):
            return newKb
        else:
            return cls(newKb)

    def get_keyboard(self):
        self.cleanup_empty()
        return super().get_keyboard()

    @classmethod
    def get_empty_keyboard(cls):
        return cls()

    def add_button(self, *args, **kwargs):
        if getattr(Strategies, self.strategy)(self):
            self.add_line()
        super().add_button(*args, **kwargs)
        self.button_index += 1

    def cleanup_empty(self):
        for i, line in enumerate(self.lines):
            if not line:
                del self.lines[i]

    def add_line(self):
        self.cleanup_empty()
        self.button_index = 0
        super().add_line()

    def add_from_list(self, arr):
        for j in arr:
            if j != "locationButton":
                self.add_button(j, color=self.get_random_color())
            else:
                self.add_location_button()
                self.add_line()

    def add_from_dict(self, d):
        for k, v in d.items():
            if v == "line":
                self.add_line()
            else:
                self.add_button(k, self.parse_color(v))

    def get_random_color(self):
        return random.choice(list(self.colors.values()))

    def __repr__(self):
        return self.get_keyboard()

    # += operator
    def __iadd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, dict):
            self.add_from_dict(other)
        elif isinstance(other, list):
            self.add_from_list(other)
        else:
            self.add_button(other, color = self.get_random_color())
        return self

    def parse_color(self, str1):
        return self.colors[str1]


class Strategies(object):
    @staticmethod
    def default(keyboard: Keyboard):
        return keyboard.button_index % 4 == 0

    @staticmethod
    def insert_lines(_):
        return True
