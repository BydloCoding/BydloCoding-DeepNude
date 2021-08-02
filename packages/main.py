from re import L

from vk_api import keyboard
from SDK.cmd import command, after_func
from Structs.user import User
from SDK.keyboard import Keyboard
from SDK.database import Struct, ProtectedProperty

menu_kb = Keyboard({"Раздеть девушку 👅": "green", "0": "line", "Баланс 💰": "blue", "Пополнить баланс 💶":
                    "white"})


@command("начать", aliases=["в меню"])
def start(self, args):
    User(self.db, user_id = self.user.id, balance = 0)
    self.reply("Привет! Наш бот поможет тебе раздеть любую девушку🔞", keyboard = menu_kb)

@command("раздеть девушку 👅")
def process(self, args):
    User(self.db, user_id = self.user.id, balance = 0)
    self.reply("Пришли мне фото девушки, которую хочешь раздеть 👸\n\nДля раздевания нужно:\n\n👉 Фотография в купальнике или нижнем белье\n👉 Чем меньше одежды, тем лучше эффект\n👉 Девушка должна быть по центру")

@command("баланс 💰")
def show_balance(self, args):
    user_profile = User(self.db, user_id = self.user.id, balance = 0)
    self.reply(f"💰 Ваш баланс: {user_profile.balance} руб.")

@command("пополнить баланс 💶")
def add_balance(self, args):
    User(self.db, user_id = self.user.id, balance = 0)
    k = Keyboard()
    k.add_openlink_button("50 ₽", f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={self.qiwi_wallet}&amountInteger=50&amountFraction=0&extra%5B%27comment%27%5D=deepnude:{self.user.id}&currency=643&blocked[0]=account&blocked[1]=comment")
    k.add_openlink_button("100 ₽", f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={self.qiwi_wallet}&amountInteger=100&amountFraction=0&extra%5B%27comment%27%5D=deepnude:{self.user.id}&currency=643&blocked[0]=account&blocked[1]=comment")
    k.add_line()
    k.add_openlink_button("200 ₽", f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={self.qiwi_wallet}&amountInteger=200&amountFraction=0&extra%5B%27comment%27%5D=deepnude:{self.user.id}&currency=643&blocked[0]=account&blocked[1]=comment")
    k.add_openlink_button("300 ₽", f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={self.qiwi_wallet}&amountInteger=300&amountFraction=0&extra%5B%27comment%27%5D=deepnude:{self.user.id}&currency=643&blocked[0]=account&blocked[1]=comment")
    k.add_line()
    k.add_openlink_button("400 ₽", f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={self.qiwi_wallet}&amountInteger=400&amountFraction=0&extra%5B%27comment%27%5D=deepnude:{self.user.id}&currency=643&blocked[0]=account&blocked[1]=comment")
    k.add_openlink_button("500 ₽", f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={self.qiwi_wallet}&amountInteger=500&amountFraction=0&extra%5B%27comment%27%5D=deepnude:{self.user.id}&currency=643&blocked[0]=account&blocked[1]=comment")
    k.add_line()
    k.add_button("В меню", color=Keyboard.colors["blue"])
    self.reply("Выберите сумму, на которую хотите поплнить баланс", keyboard=k)