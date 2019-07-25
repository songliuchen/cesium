cesium demo，cesium 研究过程中资料整理，包括：  
1、示例，提供常规的cesium示例以及综合性的业务示例  
2、工具，整理研究过程中写的一些数据获取、处理、分析的工具，例如网络3dtiles数据爬虫工具  
3、插件，根据研究过程中cesium感觉使用不方便的地方，添加插件，包括针对显示控件的汉化中文语言插件等
  
## Cesium 脑图（完善中）
[脑图](http://naotu.baidu.com/file/1bb0734b72b6f7efb888a93a2cb642ce)  
[3DTiles数据结构脑图](http://naotu.baidu.com/file/ef3c88cd75ebad82f4f4bd552658e9b3)

## Cesium DEMO集合（完善中）
演示效果直接下载代码后账访问index.html 文件即可，ip方式访问可通过VS Code+Live Server 插件或通过HBuilder 运行 即可预览效果  
  
效果图1  
![效果图1](/assets/readme/demo1.gif)  
- [示例集合](http://129.211.11.95/cesium)  
- [基础：Hello World](http://129.211.11.95/cesium/base/load_cesium.html)    
- [基础：去除所有控件](http://129.211.11.95/cesium/base/load_cesium2.html) 
- [基础：动态显示隐藏控件](http://129.211.11.95/cesium/base/load_cesium3.html)  
- [模型：模型属性修改](http://129.211.11.95/cesium/model/show.html)  
- [模型：地下模型展示](http://129.211.11.95/cesium/model/show_underline.html)  
- [数据源：Geo JSON](http://129.211.11.95/cesium/datasource/geojson.html)  
- [数据源：Topo JSON](http://129.211.11.95/cesium/datasource/geojson.html)  
- [路线：飞行](http://129.211.11.95/cesium/fly/fly.html)  
- [3DTiles：加载黄浦江数据](http://129.211.11.95/cesium/3dtiles/load_3dtiles.html)  
- [3DTiles：加载工厂数据](http://129.211.11.95/cesium/3dtiles/load_3dtiles2.html)  
- [3DTiles：加载小区数据](http://129.211.11.95/cesium/3dtiles/load_official.html)  
- [3DTiles：加载点云数据](http://129.211.11.95/cesium/3dtiles/load_point_cloud.html)  
- [工具：爬取网络3DTiles数据](http://129.211.11.95/cesium/tools/3dtiles_download.py)  
- [工具：解析3dTiles切片文件中的b3dm文件，提取gltf模型](http://129.211.11.95/cesium/tools/transb3dm_to_gltf.py)  
- [插件：汉化](http://129.211.11.95/cesium/plugins/cesium_zh.html)  

##  cesium 工具整理
- 在线3DTiles数据爬取工具  
 ```
1、使用python3.7版本编写  
2、默认需要修改两个地方： 
    1）全局的url地址.  
    2）修改   downloadJson调用中的 tileset.json 文件名  
3、遇到的问题：  
    1）、部分网站为https域名，需要引入ssl包    
    2）、部分网站进行了gzip压缩，需要判断并解压数据
    3）、部分网站进行了权限校验（例如：官网）需要添加一些头信息
    4）、部分3dTiles content 文件地址对应的为uri参数名，部分为url参数名，url参数只给出文件名，不给文件相对路径，需要单独处理 
4、存在问题：
    1）、不支持多线程操作，大模型下载耗时严重
    2）、特殊URL需要二次处理，目前只接受正常以.json结尾的url
    3）、缺少增量爬取功能，出现异常不能从异常文件重新爬取，整个需要重头开始
    4）、缺少日志本地存储功能
 ```
 -  解析3dTiles 切片文件中的b3dm文件，提取gltf模型  
 ```
1、使用python3.7版本编写  
2、通过指定3dtiles 目录解析目录下所有b3dm文件中的gltf 模型
3、解析出来的模型文件和b3dm文件保存在同一目录中
 ```
 
## cesium 插件整理
-  汉化插件，针对界面可视化部分进行汉化  
 ```
1、汉化方式非从源码层面进行，而是外挂了一个插件执行，使用方便，但是汉化程度不深，只汉化了cesium可见的控件部分
2、汉化内容包括：
   1）、右上角所有工具，包括影像选择的显示标题，鼠标滑过title，帮助面板描述等
   2）、左下角动画面板
   3）、状态栏时间刻度线、全屏按钮
   4）、cesium 描述字符
3、中文通过百度、谷歌翻译实现
4、针对cesium 1.58版本汉化
 ```