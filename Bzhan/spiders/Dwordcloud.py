#-*- coding:utf-8 -*-
#导入词云的包
from wordcloud import WordCloud,ImageColorGenerator
from scipy.misc import imread
import io
import sys
import jieba

#导入matplotlib作图的包
import matplotlib.pyplot as plt
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码

#分词
my_cut_words=["大门"]
#截词
stopwords_path="E:/Pythonwork/source/chineseStopWords.txt"
f=open(stopwords_path,"r")
stopwords={}.fromkeys(f.read().split("\n"))
f.close()
#读取图片
back_coloring=imread("E:/Pythonwork/source/t22.jpg")
back_co=imread("E:/Pythonwork/source/t3.jpg")
#读取文件,返回一个字符串，使用utf-8编码方式读取，该文档位于此python同以及目录下
# f = open(u'E:/Pythonwork/source/te.txt','rb').read()

# text=f.decode("utf-8")
#生成一个词云对象
wordcloud = WordCloud(
        background_color="white", #设置背景为白色，默认为黑色
        width=1500,              #设置图片的宽度
        height=800,              #设置图片的高度
        margin=2,              #设置图片的边缘
        font_path='C:/Windows/Fonts/STFANGSO.ttf',
        mask=back_coloring #设置显示背景图片
        )

#添加自己的词库分词
def add_word(list):
    for items in list:
        jieba.add_word(items)

add_word(my_cut_words)
#打开文件
ff = open(u'E:/Pythonwork/source/te.txt','rb').read()
f_Text=ff.decode("utf-8")

jieba.load_userdict("E:/Pythonwork/source/utf-8-dict.txt")
cut_words=jieba.cut(f_Text)
cut_text_Arr=[]
for ite in cut_words:
        if ite not in stopwords and ite !=' ' and len(ite)!=1:
                te=ite.replace("姓名：","")
                cut_text_Arr.append(te.replace("rpid：",""))
cut_text_t=','.join(cut_text_Arr)
wordcloud.generate(cut_text_t)

image_color=ImageColorGenerator(back_coloring)


# 绘制图片
plt.imshow(wordcloud)
# 消除坐标轴
plt.axis("off")
# 展示图片
plt.show()
# 保存图片
wordcloud.to_file('DX4.png')
#
image_colors =ImageColorGenerator(back_coloring)
plt.imshow(wordcloud.recolor(color_func=image_colors))
plt.axis("off")
# 绘制背景图片为颜色的图片
plt.figure()
plt.imshow(back_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
# 保存图片
wordcloud.to_file("dx.png")
