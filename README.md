## CCD-Data-Process 
本程序是基于wxpython的UI框架编写的计算探测器常规光电测试性能的软件。
#### 程序依赖
* wxpython （4.1.0）
* numpy
* matplotlib
* astropy
#### 程序说明
1. 本来计划基于imagepy的基础，开发数据处理的插件使用，结果发现有些想要的功能不知道怎么快速实现；
2. 于是，直接使用wxpython开发了GUI，然后把数据处理的功能加进去，目前功能简陋，只能适应特定的情况；
3. 数据处理的内容主要是针对常规光电测试的：读出噪声、暗电流、PTC曲线、增益、PRNU；
4. 数据格式目前只支持`.fits`和`.raw`，灵活性较低；

#### 使用说明

![image](https://github.com/bitursa/CCD-Data-Process/blob/master/img/panel.png)

1. 程序主要分为三个面板：设置面板（上）、文件路径面板（左下）和计算面板（右下）。
2. **文件预览** ： 可以实现打开单个图像文件(单帧或多帧)预览的功能，需要先设置Size Format属性（必须），ROI设置可选。
3. **Size Format**： 支持打开的图像文件类型为.fits 或 .raw 格式文件，dtype为数据读取格式， Skip为raw文件header长度（默认为0）。Width和Height为图像的长宽，程序按照设定值组织二维图像。
4. **ROI设置**： 可选功能。按照设定值开窗。
5. **文件路径**： 包括本底场图像路径、平常图像路径和暗场图像路径。**打开文件**可以选择单个或多个文件，**打开文件夹**会读取所选目录下的所有文件。
6. **计算面板**：可根据不同的测试项目选择点击不同的标签页，然后根据计算要求填写必要的参数，计算结果的显示控件调整为灰色，只读。

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