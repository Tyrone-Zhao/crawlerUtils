import base64
import os


__all__ = [
    "captchaB64decode",
]


def captchaB64decode(b64data, filename_unextension="b64temp", dir_path=None):
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
