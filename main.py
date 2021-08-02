from vk_api import keyboard, utils
from SDK.keyboard import Keyboard
from SDK.listExtension import ListExtension
import re
import os
import random
import requests
from datetime import date, datetime
from Structs.user import User
import main_deepnude
import pyqiwi

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from SDK.stringExtension import StringExtension
from SDK import (database, jsonExtension, user, imports, cmd, thread)

config = jsonExtension.load("config.json")


class LongPoll(VkLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except:
                # we shall participate in large amount of tomfoolery
                pass
class A:
    amount = 1456

class TestPayment:
    type = "IN"
    txn_id = random.randint(0, 900000000)
    sum = A
    comment = "deepnude:295770555"

class Main(object):
    def __init__(self):
        self.attachments = ListExtension()
        self.config = config
        self.clear_tasks = []
        main_deepnude.test_fn()
        imports.ImportTools(["packages", "Structs"])
        self.database = database.Database(config["db_file"], config["db_backups_folder"], self)
        self.db = self.database
        self.all_payments_list = jsonExtension.load("data/all_payments.json")
        database.db = self.database
        self.qiwi_wallet = self.config["qiwi_wallet"]
        self.qiwi_token = self.config["qiwi_api_key"]
        self.wallet = pyqiwi.Wallet(token=self.qiwi_token, number=self.qiwi_wallet)
        self.vk_session = vk_api.VkApi(token=self.config["vk_api_key"])
        self.longpoll = LongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()
        self.group_id = "-" + re.findall(r'\d+', self.longpoll.server)[0]
        thread.every(300, name="Qiwi-Payments")(self.qiwi_payments)
        print("Bot started!")
        self.poll()

    def check_clear_tasks(self):
        while self.clear_tasks:
            os.remove(self.clear_tasks.pop())

    def parse_attachments(self):
        for attachmentList in self.attachments_last_message:
            attachment_type = attachmentList['type']
            attachment = attachmentList[attachment_type]
            access_key = attachment.get("access_key")
            
            self.attachments.append(
                f"{attachment_type}{attachment['owner_id']}_{attachment['id']}") if access_key is None \
                else self.attachments.append(
                f"{attachment_type}{attachment['owner_id']}_{attachment['id']}_{access_key}")

    def reply(self, *args, **kwargs):
        return self.user.write(*args, **kwargs)

    def wait(self, x, y):
        return cmd.set_after(x, self.user.id, y)

    def set_after(self, x, y=None):
        if y is None:
            y = []
        cmd.set_after(x, self.user.id, y)

    def handle_attachments(self):
        attachment = self.attachments_last_message.find(lambda it: it["type"] == "photo")
        r = requests.get(attachment["photo"]["sizes"][-1]["url"])
        file = datetime.now().strftime("%m-%d-%Y-%H-%M-%S-%f")
        with open(f"images/input/{file}", "wb") as f:
            f.write(r.content)
        thread.threading.Thread(target = main_deepnude.bound_deepnude_process, args = (self, self.user.id, file)).start()

    def qiwi_payments(self):
        db = database.ThreadedDatabse()
        transactions = self.wallet.history(rows=50)["transactions"]
        #transactions.append(TestPayment)
        for payment in transactions:
            if payment.type == "IN" and payment.txn_id not in self.all_payments_list and payment.comment is not None and payment.comment.startswith("deepnude:"):
                found = re.findall(r'\d+', payment.comment)
                self.all_payments_list.append(payment.txn_id)
                if found:
                    user_id = found[0]
                    user_profile = db.select_one("select * from users where user_id = ?", [user_id])
                    if user_profile is not None:
                        db.execute("update users set balance = ? where user_id = ?", [user_profile["balance"] + payment.sum.amount, user_profile["user_id"]])
                        user.User(self.vk, user_profile["user_id"]).write(f"Оплата прошла успешно! На ваш счет зачислено {payment.sum.amount} ₽\n\n")
        db.close()

    def poll(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.db.check_tasks()
                self.check_clear_tasks()
                self.user = user.User(self.vk, event.user_id)
                self.raw_text = StringExtension(event.message.strip())
                self.event = event
                self.text = StringExtension(self.raw_text.lower().strip())
                self.txtSplit = self.text.split()
                self.command = self.txtSplit[0] if len(self.txtSplit) > 0 else ""
                self.args = self.txtSplit[1:]
                self.messages = self.user.messages.getHistory(count=3, photo_sizes=0)["items"]
                self.last_message = self.messages[0]
                self.attachments_last_message = ListExtension(self.last_message["attachments"])
                self.parse_attachments()
                if self.attachments.find(lambda it: it.startswith("photo")) is not None:
                    user_profile = User(self.db, user_id = self.user.id, balance = 0)
                    if user_profile.balance >= 50:
                        user_profile.balance -= 50
                        self.reply("Фото отправлено на обработку...")
                        self.handle_attachments()
                    else:
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
                        self.reply("Пополните баланс, чтобы продолжить!\n\n💰 Баланс: 0р\n💶 Цена обработки: 50р.\n", keyboard = k)

                else:
                    cmd.execute_command(self)


Main()
