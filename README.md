# IMDB 评论爬虫

这个 Python 脚本用于从 IMDb 上抓取指定电影的用户评论，并将其保存为 CSV 文件。

## 特性

- 最多抓取 300 条用户评论。
- 自动处理分页。
- 将评论以结构化的 CSV 格式保存。

## 需求

- Python 3.x
- `requests` 库
- `beautifulsoup4` 库

## 使用方法

- 克隆仓库或下载脚本。
- 编辑电影 ID：打开脚本，将 movie_id 变量替换为你想要抓取的电影的 IMDb ID。例如，要抓取《盗梦空间》，可以使用 "tt1375666"。
- 输出：评论将保存到与脚本同一目录下的 imdb_comments.csv 文件中。

## 代码说明

- 导入：脚本使用 requests 进行 HTTP 请求，使用 BeautifulSoup 解析 HTML。
- 函数：scrape_imdb_comments(movie_id, max_comments, output_file)：
- 参数：
movie_id：电影的 IMDb ID。
max_comments：要抓取的最大评论数（默认值为 300）。
output_file：输出 CSV 文件的名称（默认值为 imdb_comments.csv）。
- 处理过程：
构建 IMDb 评论页面的 URL。
抓取评论，直到达到最大数量或没有更多评论。
将评论保存到 CSV 文件中。

## 注意事项
脚本在请求之间包括 1 秒的延迟，以避免对 IMDb 服务器造成过大压力。
确保遵守 IMDb 的服务条款。


# IMDB 评论处理与词云生成工具

这个 Python 脚本用于处理多个 IMDb 评论 CSV 文件，利用 OpenAI API 生成评论摘要，并生成词云图。

## 特性

- 从多个 CSV 文件中读取 IMDb 评论。
- 使用 OpenAI API 对评论进行摘要处理。
- 生成词云图以可视化评论摘要的关键词。

## 需求

- Python 3.x
- `pandas` 库
- `openai` 库
- `wordcloud` 库
- `matplotlib` 库
- `collections` 库

## 使用方法

- 设置 API 密钥：在代码中将 api_key="api" 替换为你的 OpenAI API 密钥。
- 指定输入文件：在 input_files 列表中，添加你想要处理的 IMDb 评论 CSV 文件的路径。
- 输出：处理后的评论将保存到以 _output 结尾的新 CSV 文件中。
生成的词云图将保存为 wordcloud.png。

## 代码说明
- 导入模块：代码导入所需的库，并设置 OpenAI API 客户端。
- 函数 process_prompt(prompt)：调用 OpenAI API 生成评论摘要。
- 并发处理：使用线程池并发处理评论以提高效率。
- 词频统计：通过 Counter 统计所有生成摘要的词频。
- 生成词云：使用 WordCloud 生成词云图并显示。

# IMDB 评论词频分析与词云生成工具

这个 Python 脚本用于分析 IMDb 评论生成的 CSV 文件，提取评论中的词汇并生成词频表及词云图。

## 特性

- 从指定的 CSV 文件中读取生成的评论。
- 清洗文本数据，去除特殊字符和数字。
- 统计词频并输出为 CSV 文件。
- 生成词云图以可视化词频。

## 需求

- Python 3.x
- `pandas` 库
- `re` 库（内置）
- `collections` 库（内置）
- `wordcloud` 库
- `matplotlib` 库

## 使用方法

- 设置文件路径：在代码中将 file_path 变量设置为包含你的 IMDb 评论输出文件的目录路径。
- 指定文件名：在 file_names 列表中添加你想要分析的 CSV 文件名。
- 输出：词频数据将保存到 word_frequency.csv 文件中。
生成的词云图将保存为 wordcloud.png。

## 代码说明
- 导入模块：代码导入所需的库，设置文件路径和文件名。
- 数据读取：使用 pandas 读取 CSV 文件并提取 Generated 列。
- 数据清洗：将评论转换为小写，并使用正则表达式去除特殊字符和数字。
- 词频统计：使用 Counter 统计词频，并将结果保存为 CSV 文件。
- 生成词云：使用 WordCloud 生成词云图并保存。
