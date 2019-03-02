# crawlerUtils
用requests和BeautifulSoup写爬虫时会用到的函数和类等

```shell
pip install crawlerUtils
```

## Examples

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
还未完成，因为采用了机器学习，所以需要大量训练数据。目前训练数据不足，导致验证码识别准确度不高45%左右
```python
from crawlerUtils import getElemeDishes


getElemeDishes()
```

识别成功如下显示:
![Image text](https://img-blog.csdnimg.cn/20190302190942567.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTg0NTUzMw==,size_16,color_FFFFFF,t_70)