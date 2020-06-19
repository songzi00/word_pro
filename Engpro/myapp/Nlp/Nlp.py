# -*- coding: utf-8 -*-
from gensim.models import word2vec
import logging

# 训练模型，仅第一次运行，生成文件即可。之后不需要运行
def train_save_model():
    # 主程序

    word2vec.Text8Corpus('text8')
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus('text8')
    model = word2vec.Word2Vec(sentences, size=200)  # 训练skip-gram模型; 默认window=5
    # 保存模型，以便重用
    model.save("text8.model")


# 接收词
def load_model(keyword):

    model = word2vec.Word2Vec.load('text8.model')
    result = model.most_similar(keyword)
    # 返回相似列表中第一个单词
    return result[0][0]

if __name__ == '__main__':
    try:
        result = load_model('good')
        print(result)
    except:
        print('暂无此单词语料')



