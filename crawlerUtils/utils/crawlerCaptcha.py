import base64
import os
import math
import time
import hashlib
import psutil
import numpy as np
from PIL import Image

__all__ = [
    "Base64", "VectorCompare", "Captcha"
]


class VectorCompare:
    # 计算矢量大小
    @staticmethod
    def magnitude(concordance):
        total = 0
        for word, count in concordance.items():
            total += np.dot(count, count)

        return math.sqrt(total)

    # 计算矢量之间的cos值
    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += np.dot(count, concordance2[word])

        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


class Base64:
    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def base64decode(cls, b64data, filename_unextension="captcha", dir_path=None):
        """ base64文本解码成文件, 返回文件路径 """
        head_and_content = b64data.split(",")
        extension = head_and_content[0].rsplit("/")[1].split(";")[0]
        filename = filename_unextension + "." + extension
        if dir_path:
            filepath = dir_path + "/" + filename
        else:
            filepath = os.path.dirname(os.path.dirname(__file__)) + \
                       "/captcha/captcha_set/" + filename
        with open(filepath, 'wb') as f:
            content_decode = base64.b64decode(head_and_content[1])
            f.write(content_decode)
        # print(f"验证码获取成功，保存路径为：{filepath}")
        return filepath, extension

    @classmethod
    def base64encode(cls, filepath):
        """ 文件编码成base64, 返回base64数据列表
            [data不含头，head头，extension文件扩展名，file_size文件大小, alldata头加数据]
        """
        (dirname, allname) = os.path.split(filepath)
        (filename, extension) = os.path.splitext(allname)
        # 判断是图片还是视频
        images = [".png", "gif", "jpeg", "jpg", "bmp", "ico", "GIF", "JPG", "PNG"]
        videos = ["mp4", "rmvb", "avi", "ts"]
        extension = extension[1:]
        if extension in images:
            filetype = "image"
        elif extension in videos:
            filetype = "video"
        else:
            filetype = ""
        file_size = os.path.getsize(filepath)
        with open(filepath, 'rb') as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            head = "data:" + filetype + "/" + extension + ";base64"
            alldata = head + "," + data
        return data, head, extension, file_size, alldata


class Captcha:
    CAPTCHA_SET = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
        'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

    CURRENT_DIR = os.path.dirname(os.path.dirname(__file__)) + "/captcha"
    CAPTCHA_SET_PATH = CURRENT_DIR + "/captcha_set"

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def captchaCreateTestSet(cls, captcha_set_path=None, captcha_set=None):
        """ 创建训练数据集，目录为captcha_set_path, captcha_set为验证码可能包含的文字或者字母等的list """
        if captcha_set_path:
            captcha_set_path = captcha_set_path
        else:
            captcha_set_path = cls.CAPTCHA_SET_PATH

        if captcha_set:
            captcha_set = captcha_set
        else:
            captcha_set = cls.CAPTCHA_SET

        # print(captcha_set_path)
        # 创建captcha_set目录及其子目录
        cmd_line = f"mkdir '{captcha_set_path}' && "
        for capt in captcha_set:
            dir_path = captcha_set_path + '/' + capt
            cmd_line += f" mkdir '{dir_path}' && "

        os.system(cmd_line.rstrip(" && "))

    @classmethod
    def inputRightCaptchaCode(cls):
        """ 把正确的验证码添加到训练集 """
        captcha_image = Image.open(cls.CAPTCHA_SET_PATH + "/captcha.jpeg")
        captcha_image.show()
        right_captcha_code = input(
            f"\n\n请输入图片中的验证码以提高下次识别的准确性, 不认识的验证码字符请以*代替：")
        letters = [x for x in range(1, 5)]
        for i in range(len(letters)):
            letter_path = cls.CAPTCHA_SET_PATH + \
                          f"/captcha_binary___{str(letters[i])}.jpeg"
            m = hashlib.md5()
            m.update(("%s%s" % (time.time(), i)).encode("utf-8"))
            if right_captcha_code[i] != "*":
                new_path = cls.CAPTCHA_SET_PATH + \
                           f"/{right_captcha_code[i]}/" + m.hexdigest() + ".jpeg"
                os.system(f"mv '{letter_path}' '{new_path}'")
            else:
                os.system(f"rm -f '{letter_path}'")
        binary_path = cls.CAPTCHA_SET_PATH + '/captcha_binary.jpeg'
        os.system(f"rm -f '{binary_path}'")
        image_path = cls.CAPTCHA_SET_PATH + '/captcha.jpeg'
        os.system(f"rm -f '{image_path}'")

    @classmethod
    def captchaImageBinary(cls, pixel_min, pixel_max, image_object=None, image_path=None):
        """ 验证码图片二值化 """
        (filepath, tempfilename) = os.path.split(image_path)
        (filename, extension) = os.path.splitext(tempfilename)
        if image_object is None:
            image_object = Image.open(image_path)
            image_object = image_object.convert("P")
        else:
            image_object = image_object
        binary_object = Image.new("P", image_object.size, 255)

        for x in range(image_object.size[0]):
            for y in range(image_object.size[1]):
                pix = image_object.getpixel((x, y))
                if pixel_min <= pix <= pixel_max:
                    binary_object.putpixel((x, y), 0)

        binary_object.convert("RGB").save(cls.CAPTCHA_SET_PATH + "/" + filename + "_binary" + extension)
        # binary_object.show()
        return binary_object

    @classmethod
    def longitudinalSplit(cls, binary_object):
        """ 分割图片，返回所有字符的起始和结束横坐标 """
        length = binary_object.size[0]
        block = length // 4
        letters = [(0, block), (block + 1, block * 2),
                   (block * 2 + 1, block * 3), (block * 3, length)]

        # print(f"\n分割后字符的横坐标范围：{letters}")
        return letters

    @classmethod
    def splitCaptcha(cls, filepath, extension, captcha_name="captcha"):
        """ 分割验证码, 需要人工筛选放入将结果放入captcha_set目录 """

        # 扫描验证码
        binary_object, letters, extension = cls.captchaRecognize(
            filepath, extension, captcha_name=captcha_name)

        # 分割验证码字符
        cls.cropImage(binary_object, letters, extension,
                      cls.CAPTCHA_SET_PATH, captcha_name=captcha_name)
        if len(letters) < 4:
            raise ValueError("分割后的字符数小于4！")

    @classmethod
    def recognizeCaptcha(cls, image_path, extension, pixel_min=0, captcha_name="chaptcha"):
        """ 识别验证码， 返回二值化验证码和字符分割横坐标，以及图片扩展名 """
        from PIL import Image

        image_object = Image.open(image_path)
        # 将图片转换为8位像素模式
        image_object = image_object.convert("P")
        # 颜色直方图, 代表0~255的色值元素数量, 从黑到白
        d_histogram = image_object.histogram()

        # 转换为索引序列
        values = dict(enumerate(d_histogram, 0))

        # 按照像素值数量最多的降序
        # print("像素的值和数量从大到小前10个为：")
        temp = sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]
        # 去掉三个最大值，最亮的三个点
        temp = sorted(temp, key=lambda x: x[0], reverse=True)[3:]
        pixel_max = temp[0][0]
        # print(temp)
        # 二值化
        binary_object = cls.captchaImageBinary(pixel_min, pixel_max, image_object=image_object, image_path=image_path)

        # 切割函数
        letters = cls.longitudinalSplit(binary_object)

        return binary_object, letters, extension

    @classmethod
    def captchaTrain(cls, func, times=10):
        """ 进行验证码训练 """
        for i in range(times):
            filepath, extension, *_ = func()
            new_filepath = cls.CAPTCHA_SET_PATH + "/captcha." + extension
            os.system(f"mv '{filepath}' '{new_filepath}'")
            binary_object, letters, extension = cls.recognizeCaptcha(filepath, extension, pixel_min=0,
                                                                     captcha_name="chaptcha")
            cls.cropImage(binary_object, letters, extension, dir_path=cls.CAPTCHA_SET_PATH, captcha_name="captcha_binary")
            cls.inputRightCaptchaCode()

    @classmethod
    def cropImage(cls, binary_object, letters, extension, dir_path=".", captcha_name="captcha"):
        """ 切割二值化后的验证码图片，返回切割后的图片对象列表 """
        image_objects = []
        count = 0
        for letter in letters:
            # 四元组，左、上、右、下
            temp_object = binary_object.crop(
                (letter[0], 0, letter[1], binary_object.size[1]))
            image_path = "%s/%s.%s" % (dir_path,
                                       captcha_name + f"___{count + 1}", extension)
            temp_object.convert("RGB").save(image_path)
            image_objects.append(temp_object)
            count += 1

        return image_objects

    @classmethod
    def buildvector(cls, image_object):
        """ 将图片转换为矢量 """
        dict1 = dict(enumerate(image_object.getdata()))

        return dict1

    @classmethod
    def captchaRecognize(cls, func):
        """ 识别验证码 """
        captcha_set = cls.CAPTCHA_SET
        dir_path = cls.CAPTCHA_SET_PATH
        filepath, extension, *_ = func()
        new_filepath = cls.CAPTCHA_SET_PATH + "/captcha." + extension
        os.system(f"mv '{filepath}' '{new_filepath}'")
        binary_object, letters, extension = cls.recognizeCaptcha(filepath, extension, pixel_min=0,
                                                                 captcha_name="chaptcha")
        v = VectorCompare()
        captcha_set = captcha_set

        # 加载训练集
        imageset = []
        for letter in captcha_set:
            for img in os.listdir(f'{dir_path}/%s/' % letter):
                temp = []
                if img != ".DS_Store":
                    temp.append(cls.buildvector(Image.open(
                        f"{dir_path}/%s/%s" % (letter, img))))

                imageset.append({letter: temp})

        image_objects = cls.cropImage(
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
                            (v.relation(y[0], cls.buildvector(test_object))[0], x))

            guess.sort(reverse=True)
            print("", guess[0])
            count += 1
            result.append(guess[0][1])

        captcha_code = "".join(result)
        # print(
        #     f"\n验证码识别结果：{captcha_code}, ", end="")
        return captcha_code
