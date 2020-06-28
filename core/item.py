import wx
import numpy as np
import matplotlib.pyplot as plt
import os
import core.load as load


def readout_noise_process(mainFrame):
    gain = float(mainFrame.gain_rdnPage.rdn_textCtrl1.GetValue())
    nClip = int(mainFrame.gain_rdnPage.rdn_textCtrl3.GetValue())
    path = mainFrame.biasfilePath
    files = []

    if isinstance(path, str):
        # 输入路径为str，即目录
        for file in os.listdir(path):
            files.append(os.path.join(path, file))

    if isinstance(path, list):
        # 输入路径为list, 即文件名
        files = path

    # 判断nClip是否合适
    if len(files) <= 2 * nClip:
        dlg = wx.MessageDialog(None, "请输入合适的nClip!", caption="警告", style=wx.OK)
        dlg.ShowModal()
        return

    tmp = []
    # arr = np.zeros(load.getData(MainFrame, files[0]).shape)
    for file in files:
        each_data = load.getData(mainFrame, file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            tmp = each_data
        else:
            tmp.append(each_data)

    # 全部图像堆叠
    data = np.array(tmp)
    # 剔除最大值和最小是
    data_sort = np.sort(data, axis=0)
    if nClip:
        data_clip = data_sort[nClip:-nClip, :, :]
    else:
        data_clip = data_sort
    # 计算N张本底图像各个像元的平均值
    data_mean = np.mean(data_clip, axis=0)
    # 计算N张本地图像各个像元的标准偏差作为该像元的读出噪声
    data_std = np.std(data_clip, axis=0)
    # 整个图像的平均读出噪声
    data_std_overall = np.mean(data_std)
    # 读出噪声结果（e-)
    res = gain * data_std_overall

    # 显示结果
    mainFrame.gain_rdnPage.rdn_textCtrl2.SetValue(str(round(res, 3)))

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


def gain_process(mainFrame):
    pass


def ptc_process(mainFrame):
    pass


def dark_current_process(mainFrame):
    gain = float(mainFrame.darkcurrentPage.dc_textCtrl1.GetValue())
    time = float(mainFrame.darkcurrentPage.dc_textCtrl2.GetValue())
    bias_path = mainFrame.biasfilePath
    dark_path = mainFrame.darkfilePath
    bias_files = []
    dark_files = []

    if isinstance(bias_path, str):
        # 输入路径为str，即目录
        for bias_file in os.listdir(bias_path):
            bias_files.append(os.path.join(bias_path, bias_file))

    if isinstance(bias_path, list):
        # 输入路径为list, 即文件名
        bias_files = bias_path

    if isinstance(dark_path, str):
        # 输入路径为str，即目录
        for dark_file in os.listdir(dark_path):
            dark_files.append(os.path.join(dark_path, dark_file))

    if isinstance(dark_path, list):
        # 输入路径为list, 即文件名
        dark_files = dark_path

    bias_tmp = []
    dark_tmp = []
    # arr = np.zeros(load.getData(MainFrame, files[0]).shape)
    # 读取本底场图像
    for bias_file in bias_files:
        each_data = load.getData(mainFrame, bias_file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            bias_tmp = each_data
        else:
            bias_tmp.append(each_data)
    # 读取暗场图像
    for dark_file in dark_files:
        each_data = load.getData(mainFrame, dark_file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            dark_tmp = each_data
        else:
            dark_tmp.append(each_data)
    # 图像堆叠转为array
    bias_data = np.array(bias_tmp)
    dark_data = np.array(dark_tmp)

    bias_mean = load.im_combine(bias_data)
    dark_mean = load.im_combine(dark_data)

    # 暗电流平均值
    res_darkCurrent = np.mean(dark_mean - bias_mean)

    # 计算热像元
    # 取第一帧暗场图像
    dark_firstFrame = dark_data[0, :, :]
    dark_res = dark_firstFrame - bias_mean
    # 计算阈值
    threshold_val = np.mean(dark_res) + 25
    # 热像元个数
    coords = np.where(dark_res >= threshold_val)
    hot_pixel_num = coords[0].shape[0]
    count_row = np.unique(coords[0],return_counts=True)
    count_col = np.unique(coords[1],return_counts=True)
    # 热像元缺陷行列
    hot_pixel_row = count_row[0][np.where(count_row[1] > 100)]
    hot_pixel_col = count_col[0][np.where(count_col[1] > 100)]

    # 计算超过4倍典型值的像元比例
    coord_hotPixel_over4x = np.where(dark_res > 4*res_darkCurrent)
    ratio_over4x = coord_hotPixel_over4x[0].shape[0] / dark_res.size

    # 显示结果
    mainFrame.darkcurrentPage.dc_textCtrl3.SetValue(str(round(res_darkCurrent, 6)/time*gain))
    mainFrame.darkcurrentPage.dc_textCtrl4.SetValue(str(hot_pixel_num))
    mainFrame.darkcurrentPage.dc_textCtrl5.SetValue(str(round(ratio_over4x, 5)))
    mainFrame.darkcurrentPage.dc_textCtrl6.SetValue(",".join(hot_pixel_row))
    mainFrame.darkcurrentPage.dc_textCtrl6.SetValue(",".join(hot_pixel_col))


def prnu_process(mainFrame):
    pass
