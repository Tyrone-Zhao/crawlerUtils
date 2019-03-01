from .captchaTestSetCreate import createTestSet, cropImage, CAPTCHA_SET_PATH
from .captchaRecognizeMain import longitudinalSplit, CAPTCHA_SET, captchaImageBinary
import math
from PIL import Image
import os
import numpy as np


__all__ = ["recognizeCaptcha"]


class VectorCompare:
    # 计算矢量大小
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += np.dot(count, count)

        return math.sqrt(total)

    # 计算矢量之间的cos值
    def relation(self, concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word,  count in concordance1.items():
            if word in concordance2:
                topvalue += np.dot(count, concordance2[word])

        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


# 将图片转换为矢量
def buildvector(image_object):
    dict1 = dict(enumerate(image_object.getdata()))

    return dict1


def recognizeCaptcha(image_path=CAPTCHA_SET_PATH + "/captcha.jpeg", dir_path=CAPTCHA_SET_PATH, captcha_set=CAPTCHA_SET):
    dir_path = dir_path
    image_object = Image.open(image_path)
    binary_object = captchaImageBinary(pixel_min=0,
                                       pixel_max=188, image_path=image_path)
    v = VectorCompare()
    captcha_set = captcha_set

    # 加载训练集
    imageset = []
    for letter in captcha_set:
        for img in os.listdir(f'{dir_path}/%s/' % letter):
            temp = []
            if img != ".DS_Store":
                temp.append(buildvector(Image.open(
                    f"{dir_path}/%s/%s" % (letter, img))))

            imageset.append({letter: temp})

    letters = longitudinalSplit(binary_object)
    image_objects = cropImage(
        binary_object, letters, extension="jpeg", dir_path=dir_path, captcha_name="captcha_binary")

    count = 0
    result = []
    for test_object in image_objects:
        guess = []
        # 将切割得到的验证码小片段与每个训练片段进行比较
        for image in imageset:
            for x, y in image.items():
                if len(y) != 0:
                    guess.append(
                        (v.relation(y[0], buildvector(test_object))[0], x))

        guess.sort(reverse=True)
        print("", guess[0])
        count += 1
        result.append(guess[0][1])

    captcha_code = "".join(result)
    print(
        f"\n验证码识别结果：{captcha_code}, ", end="")
    return captcha_code
