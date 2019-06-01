"""
Colored by Group Example(字体颜色案例)

Generating a word cloud that assigns colors to words based on
a predefined mapping from colors to words
(生成一个单词云，该云根据从颜色到单词的预定义映射为单词分配颜色)
"""
 
from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt
 
 
class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping
       Parameters
       ----------（创造一个颜色函数：能给特定的单词分配确切的颜色）
       color_to_words : dict(str -> list(str))（创造一个字符串字典）
         A dictionary that maps a color to the list of words.
       default_color : str（这个字典可以将颜色映射到单词列表）
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.（颜色会分配给特定单词，而不是任意单词）
    """
 
    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}
 
        self.default_color = default_color
 
    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)
 
 
class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.
       Uses wordcloud.get_single_color_func
       Parameters
       
       ----------(创建一个颜色函数对象，
       该对象根据颜色到单词的映射将指定颜色的不同色调分配给特定的单词。
       使用WordCloudget_单色_func参数)
       
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.
       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """
 
    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]
 
        self.default_color_func = get_single_color_func(default_color)
 
    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func
 
        return color_func
 
    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)
 
 
text = """The Zen of Python, by Tim Peters
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""
 
# Since the text is small collocations are turned off and text is lower-cased
("""文本很小，关闭词组搭配，获取小写文本""")
wc = WordCloud(collocations=False).generate(text.lower())
 
color_to_words = {
    # words below will be colored with a green single color function("""以下单词会进行绿色处理""")
    'green' : ['beautiful', 'explicit', 'simple', 'sparse',
                'readability', 'rules', 'practicality',
                'explicitly', 'one', 'now', 'easy', 'obvious', 'better'],
    # will be colored with a red single color function("""以下单词会进行红色处理""")
    'red' : ['ugly', 'implicit', 'complex', 'complicated', 'nested',
            'dense', 'special', 'errors', 'silently', 'ambiguity',
            'guess', 'hard']
}
 
# Words that are not in any of the color_to_words values
# will be colored with a grey single color function
default_color = 'grey'
 
# Create a color function with single tone
# grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)
 
# Create a color function with multiple tones(其余的是单词进行灰色处理)
grouped_color_func = GroupedColorFunc(color_to_words, default_color)
 
# Apply our color function
wc.recolor(color_func=grouped_color_func)
wc.to_file('word.png')

plt.figure()
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
