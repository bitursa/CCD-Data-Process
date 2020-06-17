import wx
import numpy as np
import matplotlib.pyplot as plt
import os
import core.load as load

def ReadoutNoiseProcess(MainFrame, path, gain):
    files = []
    if isinstance(path, str):
        # 输入路径为str，即目录
        for file in os.listdir(path):
            files.append(os.path.join(path, file))

    if isinstance(path, list):
        # 输入路径为list, 即文件名
        files = path

    tmp = []
    # arr = np.zeros(load.getData(MainFrame, files[0]).shape)
    for file in files:
        each_data = load.getData(MainFrame, file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            tmp = each_data
        else:
            tmp.append(each_data)
    data = np.array(tmp)
    # 剔除最大值和最小是
    data_sort = np.sort(data, axis=0)
    data_clip = data_sort[2:-2, :, :]
    # 计算N张本底图像各个像元的平均值
    data_mean = np.mean(data_clip, axis=0)
    # 计算N张本地图像各个像元的标准偏差作为该像元的读出噪声
    data_std = np.std(data_clip, axis=0)
    # 整个图像的平均读出噪声
    data_std_overall = np.mean(data_std)
    # 读出噪声结果（e-)
    res = gain * data_std_overall

    # 合并后的fits图像的平均值和标准差分布作图, 以及直方图
    plt.figure(1)
    plt.title("MeanValue Distribution")
    plt.axis('off')
    plt.imshow(data_mean, cmap=plt.cm.gray)

    plt.figure(2)
    plt.title("StdValue Distribution")
    plt.imshow(data_std, cmap=plt.cm.gray)
    plt.axis('off')

    plt.figure(3)

    n, bins, patches = plt.hist(data_std.flatten(), bins='auto', color='steelblue')
    plt.title("Readout Noise Historgam")
    plt.xlabel("Readout Noise (e-)")
    plt.ylabel("Counts")
    plt.tight_layout()

    plt.show()

    return res



