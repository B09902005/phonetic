import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request as req
import urllib

import bs4

import random

def makecontexthtml(url):
    request = req.Request(url, headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    context = bs4.BeautifulSoup(data,"html.parser")
    return context

def makelist():
    myfile = open('word.txt')
    chinese = [0 for i in range (10000)]
    while (True):
        a = myfile.readline().split(',')
        if (a[0] != '') and (a[0][0] in {'0','1','2','3','4','5','6','7','8','9'}):
            chinese[int(a[0])] = a[1]
            if (int(a[0]) == 9999):
                break
    return chinese

def findanswer(word):
    code = urllib.parse.quote(chinese[num])
    if (len(code) != 12):
        return 0
    url = "https://crptransfer.moe.gov.tw/index.jsp?SN=" + code[:9] + "&sound=1#res"
    context = makecontexthtml(url)
    data = context.find('tr').find_all('tr')
    if (len(data) <= 1):
        return 0
    answer = data[1].find_all('span')
    if (answer == []):
        return 0
    for i in range (len(answer)):
        answer[i] = answer[i].string
    return answer

if __name__ == '__main__':
    chinese = makelist()
    print('我是字音字形測驗機。等等程式會給你中文字，你必須回答他的注音，一字多音的字只要輸入一種讀音即可。\n'
          '(如，題目是「我」，你就要輸入ㄨㄛˇ。題目是「花」，你就要輸入ㄏㄨㄚ(一聲字不用加空白鍵)。'
          '題目是「的」，那麼輸入ㄉㄧˊ或˙ㄉㄜ都給對。(輕聲符號要在聲符跟韻母前面))\n'
          '輸入完按enter，程式就會跳出正確答案的列表，並告訴你你的答案是否正確。總共十題，一題十分。\n')
    temp = input('按enter以繼續\n')
    temp = 0
    score = 0
    while (temp < 10):
        num = random.randint(1,9999)
        correct = findanswer(chinese[num])
        if (correct == 0):
            continue
        print(chinese[num])
        answer = input('你的答案：')
        print('正確答案列表：',correct)
        if (answer in correct):
            print('正確，得到 10 分\n')
            score += 10
        else:
            print('錯誤，得到 0 分\n')
        temp += 1
    print('測驗結束，你的分數是', score ,'分')


