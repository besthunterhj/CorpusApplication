import requests
import re
import json

"""
常用变量定义部分
"""
# 定义一个变量存主域名，方便之后的请求
domain = "https://news.gdufs.edu.cn/"
# 定义一个变量存新闻网html文件数量，方便之后的下一页请求（截止到2021.3.9共有1189页）
pageNum = 1189
# 定义一个变量存校园新闻的域名
schoolNewsDomain = "https://news.gdufs.edu.cn/xyxw/"

# 抓取校园新闻网首页
firstUrl = "https://news.gdufs.edu.cn/xyxw.htm"

allDateList = []
allTitleList = []
allContentList = []

# 尝试一次性抓3个校园新闻页的所有新闻内容
for i in range(42):
    if i == 0:
        res = requests.get(firstUrl)
    else:
        testUrl = schoolNewsDomain + str(pageNum - 1) + ".htm"
        res = requests.get(testUrl)

    # 更改编码为 utf-8 并抓取内容
    res.encoding = 'utf-8'
    htmlText = res.text

    # 抓取当前网页的所有新闻的正文url
    # 创建一个正则表达式
    urlRe = r'<span class=\"date\">[\s\S]*?<a href=\"(.*?)\" target=\"_blank\"'
    urls = re.findall(urlRe, htmlText, re.I | re.M)

    # 定义存放新闻时间、新闻标题、新闻正文的列表
    dateList = []
    titleList = []
    contentList = []

    # 遍历当前页的所有新闻正文子网页
    for url in urls:
        # 如果i > 0，需要处理一下url
        if i > 0:
            url = url.lstrip("../")

        currentPageUrl = domain + url
        mainTextRes = requests.get(currentPageUrl)
        mainTextRes.encoding = "utf-8"

        # 循环中的当前页内容
        currentPageText = mainTextRes.text

        # 定义获取新闻时间标签的正则表达式
        dateRe = r'<span>发布时间：(.*?)</span>'
        date = re.findall(dateRe, currentPageText, re.I | re.M)
        # 将获取到的时间信息添加到列表中
        dateList.append(date[0])

        # 定义获取新闻标题标签的正则表达式
        titleRe = r'<h2 class=\"title\">(.*?)</h2>'
        title = re.findall(titleRe, currentPageText, re.I | re.M)
        # 将获取到的标题信息添加到列表中
        titleList.append(title[0])

        # 定义获取新闻正文标签的正则表达式
        contentRe = r'<div class=\"v_news_content\">([\s\S]*?)</div>'
        rawContent = re.findall(contentRe, currentPageText, re.I | re.M)
        rawContentText = rawContent[0]

        # 清洗获取到的含标签的字符串
        # 获取开头段内容
        startTextRe = re.compile('<p class=\"vsbcontent_start\">(.*)<')
        startText = startTextRe.findall(rawContentText)[0]

        # 获取中间段内容
        mainTextRe = re.compile('<p>(.*)<')
        textInSimplePList = mainTextRe.findall(rawContentText)
        textInSimpleP = ""

        # <p>标签有可能是小标题，要判断是否为小标题，若是则去掉
        for sentence in textInSimplePList:
            if not "<strong>" in sentence:
                textInSimpleP += sentence

        # 获取结尾段内容（有些文章没有，因此需要做判断）
        endTextRe = re.compile('<p class=\"vsbcontent_end\">(.*)<')
        if len(endTextRe.findall(rawContentText)) != 0:
            endText = endTextRe.findall(rawContentText)[0]
        else:
            endText = ""

        # 拼接文本内容并删去<strong>和空格
        unfinishedText = ""
        if endText != "":
            unfinishedText = startText + textInSimpleP + endText
        else:
            unfinishedText = startText + textInSimpleP

        # 处理<span>等杂标签
        pattern = re.compile(r'<[^>]+>', re.S)
        clearText = pattern.sub("", unfinishedText)
        clearContent = ""

        # 处理html中的空格字符：&nbsp; 或 &nbsp;&nbsp;
        if "&nbsp;&nbsp;" in clearText:
            clearContentList = clearText.strip().split("&nbsp;&nbsp;")
            clearContent = clearContentList[0] + clearContentList[1]

        elif "&nbsp;" in clearText:
            clearContentList = clearText.strip().split("&nbsp;")
            clearContent = clearContentList[0] + clearContentList[1]

        else:
            clearContent = clearText

        contentList.append(clearContent)

    allDateList += dateList
    allTitleList += titleList
    allContentList += contentList


# 构建新闻的发布时间、标题、正文构成的字典及其列表
newsDictList = []
for i in range(500):
    newsDict = {"date": allDateList[i], "title": allTitleList[i], "content": allContentList[i]}
    newsDictList.append(newsDict)

# 将字典列表转换为JSON格式（不转换为ASCII码）并输出
jsonNews = json.dumps(newsDictList, ensure_ascii=False)

with open('./test.json', 'w', encoding='utf-8') as file:
    file.write(jsonNews)

