import json
import time
import threading
import requests
import selenium.webdriver
from bs4 import BeautifulSoup
import difflib
import os
import shutil
from googletrans import Translator


# url = 'https://www.javnow.com/doll/page/'

# index = 1
listurl = []
errorlistpage = []
def getpageurls(urlpage,pagenum):
    index = 1
    while index <= pagenum:
        tempurl = urlpage + str(index)
        headers = {

            'path': '/pantyhose/page/',

            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.36 Safari/537.36'
        }
        temppath = headers['path']
        temp = temppath + str(index) + '/'
        headers['path'] = temp
        tempheader = headers
        tempdic = {tempurl: headers}
        listurl.append(tempdic)
        index += 1
    # print({tempurl:headers})
# https://www.javnow.com/petite/page/48/
url = 'https://www.javnow.com/doll/page/'
getpageurls(url,6)
urlse='https://www.javnow.com/petite/page/'
getpageurls(urlse,48)


def getRespone(urls, header):
    tempure = urls
    temphe = header

    try:
        sessions = requests.session()
        try:
            respone = sessions.get(urls, headers=header, allow_redirects=True, timeout=4)
            respone.encoding = 'UTF-8'
        except Exception as e:
            respone=None

        # respone.encoding = respone.apparent_encoding
        if (respone.status_code == 200 or respone != None):

            bs = BeautifulSoup(respone.content, 'lxml')

            return bs
        else:
            while respone == None:
                try:
                    respone = sessions.get(url, headers=header, allow_redirects=True, timeout=4)
                    time.sleep(1)
                except Exception as e:
                    respone = None
            if (respone.status_code == 200 or respone != None):
                bs = BeautifulSoup(respone.content, 'lxml')
                return bs
    except Exception as e:
        print('错误')
        print(e)
        print('错误网址' + url)

        errorlistpage.append(urls)
againurllist=[]
def pagegetRespone(urls, header):
    tempure = urls
    temphe = header

    try:
        sessions = requests.session()
        try:
            respone = sessions.get(urls, headers=header, allow_redirects=True, timeout=4)
            respone.encoding = 'UTF-8'
        except Exception as e:
            respone=None

        # respone.encoding = respone.apparent_encoding
        if (respone.status_code == 200 or respone != None):

            bs = BeautifulSoup(respone.content, 'lxml')

            return bs
        else:
            while respone == None:
                try:
                    respone = sessions.get(url, headers=header, allow_redirects=True, timeout=4)
                    time.sleep(1)
                except Exception as e:
                    respone = None
            if (respone.status_code == 200 or respone != None):
                bs = BeautifulSoup(respone.content, 'lxml')
                return bs
    except Exception as e:
        print('错误')
        print(e)
        print('错误网址' + url)
        againurllist.append({tempure:temphe})


listresp = []
for item in listurl:
    for key in item.keys():
        temprespone = pagegetRespone(key, item[key])
        if temprespone:
            print(key)
            listresp.append(temprespone)
        # time.sleep(1)
while len(againurllist)>0:
    tenmlistpage=againurllist.copy()
    againurllist.clear()
    for item in tenmlistpage:
        for key in item.keys():
            temprespone = pagegetRespone(key, item[key])
            if temprespone:
                print(key)
                listresp.append(temprespone)
    print(len(againurllist))
            # time.sleep(1)
print('listresp长度')
print(len(listresp))
lisinforurl = []


def getinformation(respone):
    # listpage =[]
    # div = respone.find('div', class_='generate-columns-container ')

    try:
        div = respone.find('div', class_='generate-columns-container ')
        for dininfo in div.find_all('div', class_='inside-article'):
           try:
               divimg = dininfo.find('div', class_='post-image')
               imghref = divimg.find('img').attrs['src']
               numdiv = dininfo.find('div', class_='entry-summary')
               spanlist = numdiv.find_all('span')

               num = numdiv.find('span', class_='jdvdid')
               English = spanlist[3].attrs['title']

               name = num.find('a').text
               tempdic = {name: {imghref: English}}
               lisinforurl.append(tempdic)
           except Exception as e :
               print(e)
    except Exception as e:
        print(e)


for infor in listresp:
    if infor:
        tempinfor = getinformation(infor)


def get_IformationUrl(name):
    # name = name.strip()
    informationUrl = 'http://www.clb.biz/s/' + name + '.html'
    # print(informationUrl)
    return informationUrl


newUrlList = []
for tempdict in lisinforurl:
    for key in tempdict.keys():
        tempkey = key.strip()
        linkurl = get_IformationUrl(tempkey)
        tempurl = {tempkey: {linkurl: tempdict[key]}}

        newUrlList.append(tempurl)


def getMaxSimilarityUrl(urllist):
    try:
        temp = []
        for item in urllist:
            for key in item.keys():
                temp.append(key)
        maxtemp = max(temp)
        for item in urllist:
            for key in item.keys():
                if (maxtemp == key):
                    return item[key]
    except Exception as e:
        return None


notFoundList = []
errorlist = []


def getnewInformation(name, respone, kind):
    cxname = name
    cxre = respone
    cxkind = kind
    try:

        tempname = name + "（" +str(kind)  + ")"
        div = respone.find('div', id='wall')
        templist = []
        name = name
        print('tempname')
        print(tempname)
        print('name')
        print(name)
        for divitem in div.find_all('div', class_="search-item"):

            if (divitem):
                dinscre = divitem.find('div', class_='item-title')
                h3 = dinscre.find('h3')
                title = h3.text.lower()
                a = h3.find('a').attrs['href']
                aUrl = 'http://www.clb.biz' + a
                sq = difflib.SequenceMatcher(None, name, title)
                ratio = sq.ratio()
                tempdic = {ratio: {name: {aUrl: kind}}}
                templist.append(tempdic)
        tempurl = getMaxSimilarityUrl(templist)
        if tempurl != None:
            return tempurl
        else:
            notFoundList.append(tempname)
            return None



    except Exception as e:
        print(e)
        print(name)
        print('getnewInformation方法报错')
        errorlist.append({name: kind})


linkList = []
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.36 Safari/537.36',
    'Connection': 'close'}


def geturlMethod(url, name, kind):
    tempmethod = url
    tempname = name
    tempkind = kind
    newResponeinformation = getRespone(url, head)
    while (newResponeinformation == None):
        print('对象为空重新请求')
        time.sleep(1)
        newResponeinformation = getRespone(url, head)
    if (newResponeinformation):
        temp = getnewInformation(name, newResponeinformation, kind)
        print(url)
        if (temp):
            linkList.append(temp)
    else:
        print('while失效重新调用geturlMethod')
        time.sleep(1)
        geturlMethod(tempmethod, tempname, tempkind)


newUrlListnums = 0
lsiththread = []
for getUrl in newUrlList:
    for key in getUrl.keys():
        urls = ''
        kind = ''
        for name in getUrl[key].keys():
            urls = name
            item = getUrl[key]
            kind = item[name]
            print('urls')
            print(urls)
            print('key')
            print(key)
            print('kind')
            print(kind)
            if (newUrlListnums < 30):
                threads = threading.Thread(target=geturlMethod, args=(urls, key, kind,))
                threads.start()
                print(threads.name + '开始')
                lsiththread.append(threads)
                time.sleep(1)
            else:
                newUrlListnums = 0
                print('开始等待一部分线程结束')
                for tr in lsiththread:
                    tr.join()
                    print(tr.name + '结束')
                print('等待结束')

for listtr in lsiththread:
    listtr.join()
    print(listtr.name + '结束')
print('找到的连接')
print(linkList)
print(str(len(linkList)) + '长度')
print('未找到的连番号')
print(notFoundList)
print(str(len(notFoundList)) + '长度')


def get_link(item):
    tempitem = item

    try:
        respone = getRespone(item, head)
        if respone:
            divwall = respone.find('div', id="wall")
            divfil = divwall.find('div', class_='fileDetail')
            pList = divfil.find_all('p')
            goalP = pList[len(pList) - 2]
            if (goalP):
                a = goalP.find('a', id="down-url").attrs['href']
                return a

        else:
            time.sleep(1)
            print('get_link里面请求网页为空，正在重新请求')
            get_link(tempitem)



    except Exception as e:
        time.sleep(1)
        get_link(tempitem)
        print('判断失效重新调用get_link')


endDic = {}
errorlink = []
fenzhulis = []

for links in linkList:
    # print('links')
    # print(links)
    try:
        for key in links.keys():
            tempkey = links[key]
            for urlkey in tempkey.keys():  # tempdic =  {name: {aUrl:kind}}
                tempkey = tempkey[urlkey]
                a = get_link(urlkey)
                tempstr = '磁力链接：' + a
                endDic.update({key: {tempstr: tempkey}})
                fenzhulis.append({key: {tempstr: tempkey}})
            time.sleep(0.5)
    except Exception as e:
        print('links错误')
        print(e)
        errorlink.append(links)
print('番号总数')
print('长度' + str(len(lisinforurl)))
print('错误的pageurl')
print(errorlistpage)
print('错误列表')
print(errorlist)
print('请求到的')
print(fenzhulis)
print('没有请求到的')
print(errorlink)
with open('Pantyhose.json', 'w', encoding='utf-8') as json_file:
    try:
        json.dump(endDic, json_file, ensure_ascii=False)
        print("write json file success!")
    except AttributeError:
        print(AttributeError)
wlist=[]
translator = Translator()
def seveimg(tempfile,key,imgsrc,text):


    file=tempfile
    tempkey=key
    img=imgsrc
    t=text
    try:
        for imgurl in text.keys():
            imgrespone=None
            while imgrespone==None:
                imgrespone = requests.get(imgurl, timeout=3)
                time.sleep(1)
            if imgrespone:
                with open(tempfile + '/' + key + '.jpg', 'wb') as f:
                    f.write(imgrespone.content)
                file_handle = open(tempfile + '/' + key + '.txt', 'w', encoding='utf-8')

                texts = translator.translate(text[imgurl], dest='zh-CN').text
                file_handle.write(texts+'\n')

                file_handle.write(imgsrc)

            else:
                time.sleep(1)
                seveimg(file, tempkey, img, t)
    except Exception as e :
        print(e)
        time.sleep(1)
        seveimg(file, tempkey, img, t)
        # wlist.append({key:{img,img}})


filename = 'doolumove'

a = os.path.exists(filename)

if (a):
    shutil.rmtree(filename)
    os.mkdir(filename)
else:
    os.mkdir(filename)
print('fenzhulis的长度')
print(len(fenzhulis))
threaWritelist=[]
num=0


for tempkey in fenzhulis:
    for key in tempkey.keys():
        tempdic=tempkey[key]
        tempfile = filename + '/' + key
        sf = os.path.exists(tempfile)
        if (sf):
            shutil.rmtree(tempfile)
            os.mkdir(tempfile)
            for clurl in tempdic.keys():
                # print('imgsrc')
                # print(tempdic[imgsrc])
                threaWrite=threading.Thread(target=seveimg,args=(tempfile,key,clurl,tempdic[clurl],))
                threaWrite.start()
                print(threaWrite.name + '开始')
                threaWritelist.append(threaWrite)



        else:
            os.mkdir(tempfile)
            for clurl in tempdic.keys():
                # print('imgsrc')
                # print(tempdic[imgsrc])
                threaWrite = threading.Thread(target=seveimg, args=(tempfile, key, clurl, tempdic[clurl],))
                threaWrite.start()
                print(threaWrite.name+'开始')
                threaWritelist.append(threaWrite)

    num+=1
    if(num>=60):
        print('等待一部分线程结束')
        for thr in threaWritelist:
            thr.join()
            num=0
        print('等待完成')
    time.sleep(1)
print('等待全部线程结束')
for thr in threaWritelist:
    thr.join()
    print(thr.name+'结束')
