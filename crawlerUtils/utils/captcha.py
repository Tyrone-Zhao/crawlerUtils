import base64
import os


__all__ = [
    "Base64",
]


class Base64():
    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def base64decode(self, b64data, filename_unextension="b64temp", dir_path=None):
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
    def base64encode(self, filepath):
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
