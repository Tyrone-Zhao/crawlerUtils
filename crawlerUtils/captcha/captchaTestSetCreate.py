from .captchaRecognizeMain import CAPTCHA_SET, captchaRecognize
from ..utils import Post
import os
import random
import requests


__all__ = ["createTestSet", "cropImage", "CAPTCHA_SET_PATH",
           "CURRENT_DIR", "getRequsetCaptcha"]


CURRENT_DIR = os.path.dirname(__file__)
CAPTCHA_SET_PATH = CURRENT_DIR + "/captcha_set"


def getRequsetCaptcha(headers, telephone_number, dir_path=None, captcha_name="captcha"):
    ''' 获取验证码 '''
    captcha_params = {
        "captcha_str": telephone_number,
    }

    captcha_url = "https://h5.ele.me/restapi/eus/v3/captchas"

    captcha_json = Post(captcha_url, headers=headers, jsons=captcha_params).json
    captcha_hash = captcha_json["captcha_hash"]
    b64data = captcha_json['captcha_image']
    filepath, extension = Post.base64decode(b64data, captcha_name, dir_path)
    return filepath, extension, captcha_hash


def cropImage(binary_object, letters, extension, dir_path=".", captcha_name="captcha"):
    """ 分割图片，使用md5哈希命名 """
    image_objects = []
    count = 0
    for letter in letters:
        # 四元组，左、上、右、下
        temp_object = binary_object.crop(
            (letter[0], 0, letter[1], binary_object.size[1]))
        image_path = "%s/%s.%s" % (dir_path,
                                   captcha_name + f"___{count+1}", extension)
        temp_object.convert("RGB").save(image_path)
        image_objects.append(temp_object)
        count += 1

    return image_objects


def splitCaptcha(captcha_name="captcha"):
    ''' 请求并分割验证码, 将结果放入captcha_set目录，需要人工筛选放入对应的子目录 '''
    headers = {
        "referer": "https://h5.ele.me/login/"
    }
    telephone_numbers = [x for x in range(10)]
    telephone_heads = ["1581", "1861", "1355", "1760"]

    # 构造电话号码
    telephone_number = random.choice(telephone_heads)
    for i in range(7):
        telephone_number += str(random.choice(telephone_numbers))

    # 请求验证码
    filepath, extension, captcha_hash = getRequsetCaptcha(headers, telephone_number,
                                                          dir_path=CAPTCHA_SET_PATH, captcha_name=captcha_name)

    # 扫描验证码
    binary_object, letters, extension = captchaRecognize(
        filepath, extension, captcha_name=captcha_name)

    # 分割验证码字符
    cropImage(binary_object, letters, extension,
              CAPTCHA_SET_PATH, captcha_name=captcha_name)
    if len(letters) < 4:
        raise

    return captcha_hash


def createTestSet(captcha_set_path=None, captcha_set=None, captcha_numbers=1):
    ''' 创建训练数据集，目录为captcha_set_path, captcha_set为验证码可能包含的文字或者字母等的list '''
    global CAPTCHA_SET_PATH
    global CAPTCHA_SET

    if captcha_set_path:
        captcha_set_path = captcha_set_path
    else:
        captcha_set_path = CAPTCHA_SET_PATH

    if captcha_set:
        captcha_set = captcha_set
    else:
        captcha_set = CAPTCHA_SET

    print(captcha_set_path)
    # 创建captcha_set目录及其子目录
    if os.system(f"mkdir '{captcha_set_path}'"):
        for capt in captcha_set:
            dir_path = captcha_set_path + '/' + capt
            os.system(f"mkdir '{dir_path}'")

    # 请求验证码并分割，将结果放入captcha_set目录，人为放入其子目录
    # 请求100次
    for i in range(captcha_numbers):
        # 请求1次
        splitCaptcha(f"captcha__{str(i+1)}")
