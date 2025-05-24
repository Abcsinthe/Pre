import pandas as pd
import os
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 文件路径
file_path = r'C:\Users\Lenovo\Desktop\BigDataPre\Pre'
file_names = [
    'imdb_comments-202301_output.csv'
]

# 初始化一个空的列表，用于存储所有的词汇
all_words = []

# 读取每个文件
for file_name in file_names:
    file_full_path = os.path.join(file_path, file_name)
    df = pd.read_csv(file_full_path)

    # 提取“Generated”列
    generated_comments = df['Generated']

    # 清洗数据
    for comment in generated_comments:
        # 转换为小写，并使用正则表达式去除数字和特殊符号
        clean_comment = re.sub(r'[^a-zA-Z\s]', '', comment.lower())
        # 分词
        words = clean_comment.split()
        all_words.extend(words)

# 计算词频
word_counts = Counter(all_words)

# 输出词频表
word_freq_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])
word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)
word_freq_df.to_csv(os.path.join(file_path, 'word_frequency.csv'), index=False)

# 生成词云图
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig(os.path.join(file_path, 'wordcloud.png'))
plt.show()