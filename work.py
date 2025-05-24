import os
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk

# 确保 NLTK 数据已下载
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# 文件路径
folder_path = r"C:\Users\Lenovo\Desktop\BigDataPre\Pre"
file_names = [
    "imdb_comments-202201.csv",
    "imdb_comments-202202.csv",
    "imdb_comments-202203.csv",
    "imdb_comments-202204.csv",
    "imdb_comments-202205.csv",
]

# 数据处理类
class DataProcessor:
    def __init__(self):
        self.stop_words = self.get_custom_stopwords()
        self.lemmatizer = WordNetLemmatizer()

    def get_custom_stopwords(self):
        """获取自定义停用词列表"""
        custom_stop_words = set(stopwords.words('english'))  # 默认的停用词
        additional_stopwords = {
            "movie", "film", "like", "story", "character", "characters", "plot",
            "scene", "scenes", "good", "bad", "really", "one", "two", "would", "time", "people", "even", "just", "also"
        }
        custom_stop_words.update(additional_stopwords)
        return list(custom_stop_words)  # 转为列表

    def clean_text(self, text):
        """清洗文本，包括小写、去标点、去数字、词形还原等"""
        # 转小写
        text = text.lower()
        # 去掉标点符号
        text = re.sub(r'[^\w\s]', '', text)
        # 去掉数字
        text = re.sub(r'\d+', '', text)
        # 分词
        words = word_tokenize(text)
        # 去停用词并进行词形还原
        words = [
            self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words
        ]
        return " ".join(words)  # 返回清洗后的字符串

    def transform(self, comments):
        """对评论数据进行清洗"""
        return comments.apply(self.clean_text)

# TF-IDF 处理类
class TfidfProcessor:
    def __init__(self, max_features=1000, max_df=0.9, min_df=5):
        self.vectorizer = TfidfVectorizer(
            stop_words=None,  # 自定义停用词已在清洗阶段处理
            max_features=max_features,
            max_df=max_df,
            min_df=min_df
        )

    def fit_transform(self, comments):
        """对清洗后的评论数据进行 TF-IDF 计算"""
        tfidf_matrix = self.vectorizer.fit_transform(comments)
        feature_names = self.vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.sum(axis=0).A1
        return dict(zip(feature_names, tfidf_scores))  # 返回词汇及其权重

# 主代码
if __name__ == "__main__":
    # 加载数据
    all_files = [os.path.join(folder_path, file) for file in file_names]
    df = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)

    # 假设评论列是 'content'，请根据实际列名修改
    if 'content' not in df.columns:
        raise ValueError("请检查 CSV 文件，确保评论列名为 'content'")
    comments = df['content'].dropna()  # 去掉空值

    # 数据清洗
    processor = DataProcessor()
    cleaned_comments = processor.transform(comments)

    # TF-IDF 计算
    tfidf_processor = TfidfProcessor()
    word_scores = tfidf_processor.fit_transform(cleaned_comments)

    # 按权重排序
    sorted_word_scores = dict(sorted(word_scores.items(), key=lambda item: item[1], reverse=True))

    # 输出词汇频率表
    freq_table = pd.DataFrame(list(sorted_word_scores.items()), columns=['Word', 'Score'])
    freq_table.to_csv(r"C:\Users\Lenovo\Desktop\word_frequency_filtered.csv", index=False)
    print("词汇频率表已保存为 C:\\Users\\Lenovo\\Desktop\\word_frequency_filtered.csv")

    # 生成词云图
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white'
    ).generate_from_frequencies(sorted_word_scores)

    # 显示词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Word Cloud of IMDB Comments (Filtered)", fontsize=16)
    plt.show()