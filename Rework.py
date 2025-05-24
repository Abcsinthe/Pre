import pandas as pd
from openai import OpenAI
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# 设置API的URL和密钥
client = OpenAI(api_key="api",
                base_url="https://api.chatanywhere.tech/v1")

# 文件路径和名称
input_files = [
    "C:\\Users\\Lenovo\\Desktop\\BigDataPre\\Pre\\imdb_comments-202405.csv"
]

# 存储所有生成的文本
all_generated_texts = []


def process_prompt(prompt):
    try:
        outputs = client.chat.completions.create(
            model="deepseek-v3",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": "请帮我用一到三个单词总结评论的主要内容，要求能表达电影的核心或者观影人的强烈感情。切记不要有其余多余的词汇等内容，只需要输出一到三个单词的总结！：," + prompt}
            ],
            max_tokens=50,
            temperature=0,
        )
        generated_text = outputs.choices[0].message.content.replace('*', '')
        return generated_text
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return "Error"


# 遍历每个输入文件
for input_file in input_files:
    output_file = input_file.replace('.csv', '_output.csv')

    data = pd.read_csv(input_file, encoding='utf-8')
    results = []

    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_prompt, prompt): prompt for prompt in data['content']}
        for future in futures:
            generated_text = future.result()
            results.append(generated_text)
            all_generated_texts.append(generated_text)

    # 将结果保存为新的CSV文件
    data['Generated'] = results
    data.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"生成的结果已保存到 {output_file}")

# 统计词频
word_list = ' '.join(all_generated_texts).split()
word_counts = Counter(word_list)

# 生成词云
wordcloud = WordCloud(font_path='msyh.ttc', width=800, height=400, background_color='white').generate_from_frequencies(
    word_counts)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 保存词云图
wordcloud.to_file("wordcloud.png")
print("词云图已保存为 wordcloud.png")