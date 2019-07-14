#coding:utf8
# 1、使用python3.7版本编写
# 2、通过指定3dtiles 目录解析目录下所有b3dm文件中的gltf 模型
# 3、解析出来的模型文件和b3dm文件保存在同一目录中

import os
import struct
#解析b3dm文件中的gltf文件   
def parseB3DMToGltf(rootDir):
    #遍历根目录
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root,file)
            print(file_name)
            if file_name.endswith(".b3dm"):
                f = open(file_name,'rb')
                # 获取标识
                magic = f.read(4)
                magic = magic.decode("utf-8")
                #只有b3dm格式才解析
                if(magic =="b3dm"):
                    #获取版本
                    version = struct.unpack('I', f.read(4))
                    print(version[0])
                    #获取总字节数
                    byteLength = struct.unpack('I', f.read(4))
                    #获取featureTableJSONByteLength
                    featureTableJSONByteLength = struct.unpack('I', f.read(4))
                    #获取featureTableBinaryByteLength
                    featureTableBinaryByteLength = struct.unpack('I', f.read(4))
                    #获取batchTableJSONByteLength
                    batchTableJSONByteLength = struct.unpack('I', f.read(4))
                    #获取batchTableJSONByteLength
                    batchTableBinaryByteLength = struct.unpack('I', f.read(4))
                    # 解析gltf 文件内容，根据前面获取的其他其他数据长度判断解析gltf模型文件开始位置
                    gltfStart = 28 + featureTableJSONByteLength[0] + featureTableBinaryByteLength[0] + batchTableJSONByteLength[0] +  batchTableBinaryByteLength[0]
                    f.seek(gltfStart)
                    gltfBytes = f.read()
                    savePath = file_name.replace(".b3dm",".gltf")
                    objectFile = open(savePath, 'wb')#以读写模式打开
                    objectFile.write(gltfBytes)
                    objectFile.close()
                    f.close()

parseB3DMToGltf("./data/")