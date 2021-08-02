# coding=utf-8
import cv2
from SDK import user
import sys
import vk_api

from run import process

"""
main.py

 How to run:
 python main.py

"""


def bound_deepnude_process(bot_class, user_id, file_name):
	
	nude = deep_nude_process(f"images/input/{file_name}")
	upload_session = vk_api.VkUpload(bot_class.vk_session)
	path = f"images/output/{file_name}.png"
	cv2.imwrite(path, nude)
	uploaded = upload_session.photo_messages(path)[0]
	bot_class.clear_tasks.append(f"images/input/{file_name}")
	bot_class.clear_tasks.append(path)
	user.User(bot_class.vk, user_id).write("Вот результат обработки фото", attachment=f'photo{uploaded["owner_id"]}_{uploaded["id"]}_{uploaded["access_key"]}')

def deep_nude_process(item):
    print('Processing {}'.format(item))
    dress = cv2.imread(item)
    h = dress.shape[0]
    w = dress.shape[1]
    dress = cv2.resize(dress, (512,512), interpolation=cv2.INTER_CUBIC)
    watermark = process(dress)
    watermark = cv2.resize(watermark, (w,h), interpolation=cv2.INTER_CUBIC)
    return watermark