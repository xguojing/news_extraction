# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:42:39 2019

@author: Yu-Yiyang
"""
import pickle
from functools import lru_cache

from pyhanlp import *


# pyhanlp: see https://github.com/hankcs/HanLP, need java and Jpype

def parse_sentence(sentence):
    return HanLP.parseDependency(sentence)


def search_dependency(sentence, related_words):
    '''
    input: Chinese text parsed by parse_sentence
    return: {speaker: point}
    '''
    parsed_sentence = HanLP.parseDependency(sentence)
    result = {}
    for word in parsed_sentence.iterator():
        if word.DEPREL == '主谓关系' and word.HEAD.LEMMA in related_words:
            # TODO: if word.LEMMA is 代词， 指代消解
            speaker_id = word.ID
            root_id = word.HEAD.ID
            result[word.LEMMA] = search(parsed_sentence, root_id, speaker_id)  # word.LEMMA为发表观点的人
    return result


def search(parsed_sentence, root_id, speaker_id):
    '''
    :root_id: id for "说"
    :speaker_id: speaker name word id
    :target_id: target word id, search whether it belong to "说"
    search the entire sentence, all tokens that belong to root and not belong to speaker is the result
    '''
    result = ''
    for word in parsed_sentence.iterator():
        if check_word(parsed_sentence, root_id, speaker_id, word):
            result += word.LEMMA
    return result


@lru_cache(maxsize=32)
def check_word(parsed_sentence, root_id, speaker_id, word):
    '''
    :root_id: id for "说"
    :speaker_id: id for speaker
    :word: check if word belong to root and not belong to speaker
    '''
    #状中结构：去除修饰说的成分; 主谓关系：去除说的主语
    except_relation = ['状中结构','主谓关系']
    if word.ID in [speaker_id, 0]: return False
    if word.HEAD.ID == root_id and word.DEPREL not in except_relation: 
        return True  # 找到
    return check_word(parsed_sentence, root_id, speaker_id, word.HEAD)


def load_related_words(file):
    '''
    :param file: pickle file of tuple list, eg: [('指出', 133), ('表示', 132), ('直言', 128), ...]
    :return: list of words related with '说'
    '''
    with open(file, 'rb') as f:
        tuple_list = pickle.load(f)
    related_words = [word for word, freq in tuple_list if freq > 5]
    return related_words

if __name__ == '__main__':
    sentence = '''热搜来得有些突然。8月1日，谷阿莫在微博上表示，并不清楚为什么“两年前发生的事今天才上热搜”，同时对事件进行了简单地说明。据了解，2017年，谷阿莫便因擅自取用电影片段进行创作违反著作权法而被迪士尼、车库娱乐、又水整合、KKTV影音平台及得利影视5家公司联合诉上法庭。法庭上，谷阿莫提出调解意向，此案至今仍在调解过程中。'''
    # parsed = parse_sentence(sentence)
    res = search_dependency(sentence, ['说', '表示'])
    print(res)
    print(type(res))
    import json
    print(json.dumps(res, ensure_ascii=False))
