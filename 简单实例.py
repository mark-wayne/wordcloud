from wordcloud import WordCloud
import matplotlib.pyplot as plt
 
f = open('word.txt', 'r').read()#读取文件内容

wordcloud = WordCloud(background_color="white",width=1000,height=860, margin=2).generate(f)
#设置格式（背景 = “黑色或者白色”， 宽=1000（400）， 高=860（200），边缘=2）形成图片（f）

plt.imshow(wordcloud)#绘制图片
plt.axis("off")#不调整坐标轴
plt.show()#生成图片
wordcloud.to_file('example1.png')#保存图片为.png
