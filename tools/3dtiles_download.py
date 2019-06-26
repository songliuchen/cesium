#coding:utf8
# 1、使用python3.7版本编写
# 2、默认需要修改两个地方 1）全局的url地址，2）修改 downloadJson调用中的 tileset.json 文件名
# 3、遇到的问题：
#   1）、部分网站为https域名，需要引入ssl包
#   2）、部分网站进行了gzip压缩，需要判断并解压数据
#   3）、部分网站进行了权限校验（例如：官网）需要添加一些头信息
#   4）、部分3dTiles content 文件地址对应的为uri参数名，部分为url参数名，url参数只给出文件名，不给文件相对路径，需要单独处理 
# 4、存在问题：
#   1）、不支持多线程操作，大模型下载耗时严重
#   2）、特殊URL需要二次处理，目前只接受正常以.json结尾的url
#   3）、缺少增量爬取功能，出现异常不能从异常文件重新爬取，整个需要重头开始
#   4）、缺少日志本地存储功能
import urllib.request
#json解析库,对应到lxml
import json
#本地文件操作
import os
import shutil
import io

#https
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

#gizp压缩
import gzip
# 部分网站数据进行了gzip 压缩，需要进行解压处理
def ungzip(data):
    try:
        data=gzip.decompress(data)
    except:
        pass
    return data
#解压网络gzip流文件
def gzdecode(data):  
    compressedStream = io.BytesIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedStream)    
    data2 = gziper.read()   # 读取解压缩后数据   
    return data2 
url="https://assets.cesium.com/6074/"
# TODO song 解决需要token验证问题,可添加需要的头信息
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Accept":"*/*;access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNjc5OGJkYy0yNGE2LTQ3NmEtODBhOC00YTBlZmU3OTk1Y2QiLCJpZCI6MjU5LCJhc3NldHMiOnsiNjA3NCI6eyJ0eXBlIjoiM0RUSUxFUyJ9fSwic3JjIjoiZjlmNDY4ODctNTA1MS00OWFjLWJlM2UtM2QxNTYwODYyMWQ0IiwiaWF0IjoxNTYxNTI1MTE3LCJleHAiOjE1NjE1Mjg3MTd9._DNl37wGI-74_D23WJG9ViftC2XPgdmcBghjNpLnDdc"
}
#存储节点解析路径
_parentParsePath=""
def parseContentUri(item):
    if not item is None and 'content' in item and ('uri' in item['content'] or 'url' in item['content']):
        filePath = ""
        isUrl= True
        if 'uri' in item['content']:
            filePath = item['content']['uri']
            isUrl=False
        else:
            filePath = item['content']['url']
        #根据路径解析，除最最后一级为具体文件，其他为文件夹名称，根据名称及层次创建对应的文件夹
        filePaths = filePath.split('/')
        index = 0
        tempPath = "data"
        global _parentParsePath
        #url给的是文件名称，没给相对路径，需要存储
        if isUrl and len(filePaths)>1:
            _parentParsePath = ""
        for path in filePaths:
            tempPath= tempPath+"/"+path
            if index < len(filePaths)-1:
                if not os.path.exists(tempPath):
                    os.makedirs(tempPath)
                if isUrl and  index < len(filePaths)-1:
                    _parentParsePath =_parentParsePath+path+"/"
            #最后一级下载b3dm文件
            elif index == len(filePaths)-1:
                if isUrl and len(filePaths)== 1 and len(_parentParsePath)>0:
                    filePath = _parentParsePath+"/"+filePath
                if not os.path.exists(tempPath):
                    if path.endswith(".json"):
                        try:
                            downloadJson(url,filePath,False)
                        except Exception as e:
                            print('下载json文件异常：'+url+filePath)
                    else:
                        try: 
                            opener = urllib.request.build_opener()
                            # TODO song 解决需要token验证问题,可添加需要的头信息
                            opener.addheaders = [("Accept",header["Accept"])]
                            urllib.request.install_opener(opener)
                            a,b = urllib.request.urlretrieve(url+filePath, "data/"+filePath)
                            keyMap = dict(b)
                            if 'Content-Encoding' in keyMap and keyMap['Content-Encoding'] == 'gzip':
                                objectFile = open("data/"+filePath, 'rb+')#以读写模式打开
                                data = objectFile.read()
                                data = gzdecode(data)
                                objectFile.seek(0, 0)
                                objectFile.write(data)
                                objectFile.close()
                            print(url+filePath)
                        except Exception as e:
                            print('下载流文件异常：'+url+filePath)
            index = index+1
#下载数据，递归循环，判断uri有值创建对应的文件夹，下载相应文件
def downloadFile( rootdic ):
    parseContentUri(rootdic)
    if not rootdic is None and 'children' in rootdic and not rootdic['children'] is None:
        for item in rootdic['children']:
            parseContentUri(item)
            # 判断有子项，有子项解析子项
            if 'children' in item:
                downloadFile(item)
#下载titleset说明文件
def downloadJson( jsonUrl,jsonName,removeAll ):
    request=urllib.request.Request(url=jsonUrl+jsonName,headers=header)
    response=urllib.request.urlopen(request)
    #取出json文件里的内容，返回的格式是字符串
    html=response.read()
    #判断是否经过了gzip压缩
    if response.info().get('Content-Encoding'):
        html = ungzip(html)
    if removeAll == True:
        if os.path.exists("data"):
            #删除已有的数据
            shutil.rmtree("data")
    if not os.path.exists("data"):
        #创建新目录
        os.makedirs("data") 
    #把结果写入到tileset.json文件中
    with open("data/"+jsonName,"w") as f:
        f.write(html.decode("utf-8"))

    #解析titlset数据结构，下载子文件
    unicodestr=json.loads(html)
    rootdic = unicodestr['root']
    #下载b3dm文件
    downloadFile(rootdic)

downloadJson(url,"tileset.json",True)