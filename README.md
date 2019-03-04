# crawlerUtils
爬虫专用框架，对requests、BeautifulSoup进行了再封装，并加入了一些常用模块

## Installation
```shell
pip install crawlerUtils
```

## Examples

### 以下所有例子的源代码都在crawlerUtils/examples里

### 查看所有可用变量和函数
```python
import crawlerUtils

print(crawlerUtils.__all__)
```

### 获取QQ音乐某个歌手的歌曲信息和评论
结果会保存为Excel, 请在运行目录内查找
```python
from crawlerUtils import getQQSinger

getQQSinger()
```

### 获取知乎某个作者的所有文章
结果会保存为Excel, 请在运行目录内查找
```python
from crawlerUtils import getZhiHuArticle

getZhiHuArticle()
```

### 登陆饿了么并获取附近餐厅
使用了向量空间，验证码识别准确度目前48%左右。每次使用自动在本地进行训练，越用越强！一次识别验证码成功后，自动保存crawlerUtilsCookies.txt到本地，下次直接登录，不用再进行验证码识别。
```python
from crawlerUtils import getElemeDishes

getElemeDishes()
```

识别成功如下显示:
![Image text](https://img-blog.csdnimg.cn/2019030221472810.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTg0NTUzMw==,size_16,color_FFFFFF,t_70)


### 使用requests+正则表达式获取豆瓣top250电影信息
这个程序是用requests+正则表达式写的，并没有使用BeautifulSoup
```python
from crawlerUtils import getDoubanTop250UseRegexExpression

getDoubanTop250UseRegexExpression()
```

### Selenium实现登录并用BeatifulSoup解析文本打印Python之禅
这个程序是使用crawlerUtils里封装的getMCFunc、getBSText、loginNoCaptcha写的
```python
from crawlerUtils import loginAndPrintZens

loginAndPrintZens()
```

### 每天定时发送天气信息邮件
这个程序是使用crawlerUtils里封装的每天定时发送邮件函数及urlOpen等函数写的
```python
from crawlerUtils import sendCityWeatherEveryDay

sendCityWeatherEveryDay("广州")
```

## 更新记录
V1.4.1 更新内容: 封装了一些BeautifulSoup和Selenium函数、增加打印python之禅的例子