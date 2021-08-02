from SDK.keyboard import Keyboard

import re

import vk_api

import traceback


class User(object):
    # method to insert keyword map
    user_id_methods = {"messages.getHistory": "user_id", "users.get": "user_ids"}

    def __init__(self, vk, user_id, method=None):
        self._vk = vk
        self._method = method
        self.id = user_id

    def write(self, message, keyboard=None, **kwargs):
        if keyboard is not None:
            kwargs["keyboard"] = Keyboard.byKeyboard(keyboard)
        try:
            return self._vk.messages.send(user_id=self.id, message=message, random_id=vk_api.utils.get_random_id(),
                                      **kwargs)
        except:
            traceback.print_exc()
            return

    @property
    def user_name(self):
        if re.match(r"-?\d+$", self.id):
            fetched = self._vk.users.get(user_ids=self.id)[0]
            try:
                return f"{fetched['first_name']} {fetched['last_name']}"
            except:
                return self.id
        else:
            return self.id

    def __getattr__(self, method):  # str8 up
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])
        return User(
            self._vk,
            self.id,
            (self._method + '.' if self._method else '') + method
        )

    def __call__(self, **kwargs):
        if self._method in User.user_id_methods:
            kwargs[User.user_id_methods[self._method]] = self.id
        self._vk._method = self._method
        tmpReturn = self._vk.__call__(**kwargs)
        # set to null
        self._vk._method = None
        self._method = None
        return tmpReturn
