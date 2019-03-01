import io
import shutil
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import base64


__all__ = ["runDecodeTool"]


class MainWidgetUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 200)  # PyQT禁止调整窗口大小
        self.setWindowTitle('文件base64编码互转')
        self.setWindowIcon(QtGui.QIcon("favicon.ico"))

        Layout = QVBoxLayout()
        self.pushButton1 = QPushButton("To base64")
        self.pushButton2 = QPushButton("To file")
        Layout.addWidget(self.pushButton1)  # addWidget 添加一个挂件
        Layout.addSpacing(100)  # 添加一个100px的空间距离 且不带弹性
        Layout.addWidget(self.pushButton2)
        # setLayout设置 QVBoxLayout()垂直 与QHBoxLayout() 水平布局, 查看布局请移步CURL-api.py
        self.setLayout(Layout)
        # pushButton1点击按钮
        self.pushButton1.clicked.connect(self.Tobase64)
        # pushButton2点击按钮
        self.pushButton2.clicked.connect(self.Tofile)

    def Tobase64(self):
        fileDict = self.selectFile()
        if fileDict:
            GlobalToBase64(
                fileDict['file'], fileDict['filepath'] + "/" + fileDict['shotname'] + ".txt")
            QMessageBox.information(self, '提示！', "转换成功", QMessageBox.Yes)

    def Tofile(self):
        fileDict = self.selectFile()
        if fileDict:
            # 简单判断文件是否自带Mime 文件扩展 data:audio/mp3;base64,
            fobj = open(fileDict['file'])
            contents = fobj.read()
            extensions = contents.split(',')[0].rsplit('/')[1].split(';')
            if len(extensions) == 2:  # ['mp3', 'base64'] 格式为两个
                # 生成临时文件保存base64
                tmpFile = fileDict['filepath'] + \
                    "/" + fileDict['shotname'] + ".tmp"
                tmpFileObj = open(tmpFile, 'w')
                tmpFileObj.write(contents.split(',')[1])
                tmpFileObj.close()
                GlobalToFile(
                    tmpFile, fileDict['filepath'] + "/" + fileDict['shotname'] + "." + extensions[0])
                QMessageBox.information(self, '提示！', "转换成功", QMessageBox.Yes)
                os.remove(tmpFile)  # 删除临时文件

            else:  # 无mime
                mine, okPressed = QInputDialog.getText(self, "文件格式类型", "请输入文件格式类型:", QLineEdit.Normal,
                                                       "mp3")  # 获取输入对话框内容
                if okPressed and mine:  # 选择确认且输入文本
                    GlobalToFile(
                        fileDict['file'], fileDict['filepath'] + "/" + fileDict['shotname'] + "." + mine)
                    QMessageBox.information(
                        self, '提示！', "转换成功", QMessageBox.Yes)
                else:
                    return False

    def selectFile(self):
        '''
        选择文件
        '''
        # getOpenFileName  只能选择一个    getOpenFileNames  可多个选择
        file = QFileDialog.getOpenFileName(self, "请选择文件", '', "*.*")
        if file[0] == '':
            QMessageBox.warning(self, '错误提示！', "请选择文件", QMessageBox.Yes)
        else:
            (filepath, filename) = os.path.split(file[0])  # 获取文件路径，文件名
            (shotname, extension) = os.path.splitext(filename)  # 获取文件名称，文件后缀
            return {"file": file[0], "filepath": filepath, "shotname": shotname}


def GlobalToBase64(file, txt):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        fout = open(txt, 'w')
        fout.write(base64_data.decode())
        fout.close()


def GlobalToFile(txt, file):
    with open(txt, 'r') as fileObj:
        base64_data = fileObj.read()
        ori_image_data = base64.b64decode(base64_data)
        fout = open(file, 'wb')
        fout.write(ori_image_data)
        fout.close()


def runDecodeTool():
    app = QApplication(sys.argv)
    main_widget = MainWidgetUI()
    main_widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    runDecodeTool()
