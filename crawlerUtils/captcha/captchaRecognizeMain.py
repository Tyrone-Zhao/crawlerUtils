from PIL import Image
import hashlib
import time
import os


__all__ = ["CAPTCHA_SET", "captchaRecognize",
           "longitudinalSplit", "captchaImageBinary"]


CAPTCHA_SET = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a',
    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]


def captchaImageBinary(pixel_min, pixel_max, image_object=None, image_path=None,
                       captcha_name="captcha", extension="jpeg"):
    """ 验证码图片二值化 """
    global CAPTCHA_SET_PATH

    if not image_object:
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

    binary_object.convert("RGB").save(
        os.path.dirname(__file__) + "/captcha_set" + "/" + captcha_name + "_binary." + extension)
    # binary_object.show()
    return binary_object


def longitudinalSplit(binary_object):
    """ 纵向扫描图片, 找出所有字符的起始和结束横坐标 """
    length = binary_object.size[0]
    block = length // 4
    letters = [(0, block), (block+1, block*2),
               (block*2+1, block*3), (block*3, length)]

    # print(f"\n分割后字符的横坐标范围：{letters}")
    return letters


def captchaRecognize(image_path, extension, pixel_min=0, pixel_max=188,
                     captcha_name="chaptcha"):
    """ 识别验证码 """
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
    print(temp)
    # 二值化
    binary_object = captchaImageBinary(
        image_object, pixel_min, pixel_max, captcha_name)

    # 纵向扫描图片
    letters = longitudinalSplit(binary_object)

    return binary_object, letters, extension


if __name__ == "__main__":
    filepath = "captcha.jpeg"
    (filepath, filename) = os.path.split(filepath)  # 获取文件路径，文件名
    (shotname, extension) = os.path.splitext(filename)  # 获取文件名称，文件后缀

    captchaRecognize(filepath, extension)
