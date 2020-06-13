## CCD-Data-Process 
#### 程序说明
1. 本来计划基于imagepy的基础，开发数据处理的插件使用，结果发现有些想要的功能不知道怎么快速实现；
2. 于是，直接使用wxpython开发了GUI，然后把数据处理的功能加进去，目前功能简陋，只能适应特定的情况；
3. 数据处理的内容主要是针对常规光电测试的：读出噪声、暗电流、PTC曲线、增益、PRNU；
4. 数据格式目前只支持`.fits`和`.raw`，灵活性较低；
#### ToList
 - [ ] 量子效率数据处理
 - [ ] 像元内不均匀性数据处理
 - [ ] 增加支持多种数据格式
 - [ ] 图像预览功能需要加强（实现可调节灰度）
 
---
#### Imagepy 插件路径
* 开发适用于Imagepy的CCD数据处理插件，进行常规光电测试数据的处理；
* -Mac环境下:
 * imagepy 安装在 pyenv 3.6.5 的环境下，位于`/usr/local/var/pyenv/versions/3.6.5/lib/python3.6/site-packages/imagepy`；
 * 在pyenv下安装3.6.5时没有权限启动wxpython，解决办法是重新安装3.6.5，在终端调用`env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -f 3.6.5`；
 * imagepy 在mac下启动 `python -m imagepy`；
 * 提示某些插件没有加载成功，忽略；
 * 插件安装在 `../imagepy/memus/Plugins` 下，重新启动imagepy会自动加载插件；
* -Windows环境下:
 * 在windwows下使用anaconda环境下`pip install imagepy`时出现了些问题，python 3.8.x版本安装不成功， 3.7.x可以；没有自己编译成功过；
 * 可以直接使用编译好的版本，启动`Imagepy.bat`即可(简单粗暴安全)；
 * 插件安装在 `..\ImagePy\programs\Lib\site-packages\imagepy\menus\Plugins`下，重新启动imagepy会自动加载插件；