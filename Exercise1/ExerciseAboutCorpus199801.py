"""
Class: 软件工程1803班
Author: 王俊朗
ID: 20181003043
"""

import pandas
from collections import Counter

# 导入语料库（以行为单位）
with open('199801.txt', 'r', encoding="utf-8") as file:
    corpus = file.readlines()

# 1. 统计文章数
passageNum = 0
for line in corpus:
    if line == "\n":
        passageNum += 1

print("语料库中文章数为： ", passageNum)

# 2. 统计语料库的词数（含重复）
wordNum = 0
wordList = []
for line in corpus:
    # 获得每行句子（非空行）的词数组
    if line != "\n":
        words = line.strip().split("  ")

        for item in words:
            word = item.split('/')[0]
            if word != "":
                wordList.append(word.strip())
                # 由于每个数组的长度为词数，因此每次循环加上该长度即可
                wordNum += 1

print("语料库中词数为（包含重复词）： ", wordNum)

# 3. 统计语料库的词数（去重）
wordDataFrame = pandas.DataFrame({'word': wordList})
# 导入去重函数
result = wordDataFrame.drop_duplicates()
distinctWordNum = len(result)
print("语料库中词数为（不包含重复词）： ", distinctWordNum)


# 4. 统计语料库的字数（含重复）
characterNum = 0
allWordString = ""
for singleWord in wordList:
    allWordString += singleWord
    characterNum += len(singleWord)

print("语料库中字数为（包含重复字）： ", characterNum)

# 5. 统计语料库的字数（去重）
# 先将所有词语连接而成的字符串转化为字列表
charList = [char for char in allWordString]

# 再构造DataFrame类型并导入去重函数
charDataFrame = pandas.DataFrame({'char': charList})
# 导入去重函数
charResult = charDataFrame.drop_duplicates()
distinctCharNum = len(charResult)
print("语料库中字数为（不包含重复字）： ", distinctCharNum)

# 6. 统计高频词和低频词
cnt = Counter(wordList)
wordDict = {key:value for key, value in cnt.items() if value >= 1}

# 按value进行字典排序
resultList = sorted(wordDict.items(), key = lambda kv:(kv[1], kv[0]))

lowFrequencyWordList = []
loopNum = 0

for i in range(50):
    lowFrequencyWordList.append(resultList[i][0])

# 低频词为前50个元素
print("前五十个低频词依次为： ", lowFrequencyWordList)

# 高频词
frequentWordsGroup = cnt.most_common(50)
frequentWordsList = []

for item in frequentWordsGroup:
    frequentWordsList.append(item[0])

print("前五十个高频词依次为： ", frequentWordsList)