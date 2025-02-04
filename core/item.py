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

    return


def gain_process(mainFrame):
    bias_path = mainFrame.biasfilePath
    flat_path = mainFrame.flatfilePath
    bias_files = []
    flat_files = []
    if isinstance(bias_path, str):
        # 输入路径为str，即目录
        for bias_file in os.listdir(bias_path):
            bias_files.append(os.path.join(bias_path, bias_file))

    if isinstance(bias_path, list):
        # 输入路径为list, 即文件名
        bias_files = bias_path

    if isinstance(flat_path, str):
        # 输入路径为str，即目录
        for flat_file in os.listdir(flat_path):
            flat_files.append(os.path.join(flat_path, flat_file))

    if isinstance(flat_path, list):
        # 输入路径为list, 即文件名
        flat_files = flat_path

    bias_tmp = []
    flat_tmp = []

    # 读取本底场图像
    for bias_file in bias_files:
        each_data = load.getData(mainFrame, bias_file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            bias_tmp = each_data
        else:
            bias_tmp.append(each_data)
    # 读取平场图像
    for flat_file in flat_files:
        each_data = load.getData(mainFrame, flat_file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            flat_tmp = each_data
        else:
            flat_tmp.append(each_data)
    # 图像堆叠转为array
    bias_data = np.array(bias_tmp, dtype=float)
    flat_data = np.array(flat_tmp, dtype=float)

    # 选择两幅平均值最接近的图像
    bias1, bias2 = load.im_select(bias_data)
    flat1, flat2 = load.im_select(flat_data)

    bias_diff = bias1 - bias2
    flat_diff = flat1 - flat2

    bias_dif_var = np.var(bias_diff)
    flat_diff_var = np.var(flat_diff)

    # 计算增益
    gain = (np.mean(flat1) + np.mean(flat2) - np.mean(bias1) - np.mean(bias2)) / (flat_diff_var - bias_dif_var)

    # 显示结果
    mainFrame.gain_rdnPage.gain_textCtrl.SetValue(str(round(gain, 3)))
    return


def ptc_process(mainFrame):
    bias_path = mainFrame.biasfilePath
    flat_path = mainFrame.flatfilePath
    bias_files = []
    flat_files = []
    if isinstance(bias_path, str):
        # 输入路径为str，即目录
        for bias_file in os.listdir(bias_path):
            bias_files.append(os.path.join(bias_path, bias_file))

    if isinstance(bias_path, list):
        # 输入路径为list, 即文件名
        bias_files = bias_path

    if isinstance(flat_path, str):
        # 输入路径为str，即目录
        for flat_file in os.listdir(flat_path):
            flat_files.append(os.path.join(flat_path, flat_file))

    if isinstance(flat_path, list):
        # 输入路径为list, 即文件名
        flat_files = flat_path

    bias_tmp = []
    flat_tmp = []

    # 读取本底场图像
    for bias_file in bias_files:
        each_data = load.getData(mainFrame, bias_file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            bias_tmp = each_data
        else:
            bias_tmp.append(each_data)
    # 图像堆叠转为array
    bias_data = np.array(bias_tmp, dtype=float)
    # 选择两幅平均值最接近的图像
    bias1, bias2 = load.im_select(bias_data)
    bias_mean = (np.mean(bias1) + np.mean(bias2)) / 2
    bias_var = np.var(bias1 - bias2) / 2

    # 读取平场图像
    PTC_arr = np.zeros((2, len(flat_files)))
    index = 0

    for flat_file in flat_files:
        flat_tmp = []
        if os.path.isdir(flat_file):
            for item in os.listdir(flat_file):
                tmp_path = os.path.join(flat_file, item)
                flat_tmp.append(load.getData(mainFrame, tmp_path))
        else:
            each_data = load.getData(mainFrame, flat_file)
            # 多个三维fits 堆叠待解决
            if each_data.ndim > 2:
                # arr = np.concatenate((arr, each_data))
                flat_tmp = each_data
            else:
                flat_tmp.append(each_data)
        flat_data = np.array(flat_tmp, dtype=float)
        flat1, flat2 = load.im_select(flat_data)
        flat_mean = (np.mean(flat1) + np.mean(flat2)) / 2
        flat_var = np.var(flat1 - flat2) / 2

        PTC_arr[0, index] = flat_mean - bias_mean
        PTC_arr[1, index] = flat_var - bias_var
        index += 1

    # 找拐点
    argMax = PTC_arr[1, :].argmax()
    PTC_arr_fit = PTC_arr[:, :argMax + 1]

    # 拟合
    X_fit = PTC_arr_fit[0, :]
    Y_fit = PTC_arr_fit[1, :]
    Z_fit = np.polyfit(X_fit, Y_fit, 1)
    # 原始数据
    X_origin = PTC_arr[0, :argMax + 1]
    Y_origin = PTC_arr[1, :argMax + 1]

    # z[0]为曲线斜率， 1/z[0]为增益
    gain = 1 / Z_fit[0]
    readout_noise = np.sqrt(bias_var) * gain
    fullWellCapacity = gain * PTC_arr[0, argMax]

    # PTC 非线性度
    p = np.poly1d(Z_fit)
    delta = []
    for i in range(len(X_origin)):
        delta.append((Y_origin[i] - p(X_origin[i])) / p(X_origin[i]))
    delta = np.array(delta, dtype=float)
    none_linearity = np.mean(np.abs(delta))

    #  响应非线性度
    maxExposure = float(mainFrame.ptcPage.ptc_textCtrl1.GetValue())
    length = PTC_arr.shape[1]
    arr_exposure = np.linspace(0, maxExposure, length)
    coord_max = PTC_arr[1, :].argmax()
    response_x = arr_exposure[:coord_max + 1]
    response_y = PTC_arr[0, :coord_max + 1]
    response_fit = np.polyfit(response_x, response_y, 1)
    response_poly = np.poly1d(response_fit)
    response_yp = response_poly(response_x)
    res_non_linearity = np.mean((response_y - response_yp) / response_yp)

    # 显示结果
    mainFrame.ptcPage.ptc_textCtrl3.SetValue(str(round(gain, 4)))
    mainFrame.ptcPage.ptc_textCtrl4.SetValue(str(round(readout_noise, 4)))
    mainFrame.ptcPage.ptc_textCtrl5.SetValue(str(round(fullWellCapacity, 2)))
    mainFrame.ptcPage.ptc_textCtrl6.SetValue(str(np.abs(round(none_linearity, 2))))
    mainFrame.ptcPage.ptc_textCtrl7.SetValue(str(np.abs(round(res_non_linearity, 2))))

    # 作图
    if mainFrame.ptcPage.ptc_plot_trigger.GetValue():
        # PTC
        plt.figure(1)
        l1, = plt.plot(PTC_arr[0, :], PTC_arr[1, :], 'b*', label='Original Data')
        l2, = plt.plot(X_origin, p(X_origin), 'r--', label='Fit Curve')
        plt.legend(loc='best')
        plt.xlabel('Mean(ADU)')
        plt.ylabel('Variance')
        plt.legend(loc='best')
        plt.title('PTC')

        # PTC non-linearity
        plt.figure(2)
        l1, = plt.plot(X_origin, delta, 'b*', label='Non-linearity')
        l2, = plt.plot(X_origin, np.zeros(len(X_origin)), 'r--', label='zero line')
        plt.legend(loc='best')
        plt.xlabel('Mean(ADU)')
        plt.ylabel('Non-linearity')
        plt.title('PTC Non-linearity')

        # PTC response
        plt.figure(3)
        l1, = plt.plot(arr_exposure, PTC_arr[0, :], "b*", label='Original Data')
        l2, = plt.plot(response_x, response_yp, 'r--', label='Fit Curve')
        plt.legend(loc='best')
        plt.xlabel('Exposure Time / (s)')
        plt.ylabel('Signal / MeanValue')
        plt.title('PTC Response')

        # PTC response non-
        plt.figure(4)
        l1, = plt.plot(response_x, (response_y - response_yp) / response_yp, 'b*', label='Non-linearity')
        l2, = plt.plot(response_x, np.zeros(len(response_x)), 'r--', label='zero line')
        plt.legend(loc='best')
        plt.xlabel('Exposure Time / (s)')
        plt.ylabel('Non-linearity')
        plt.title('Response Non-linearity')

        plt.show()
    return


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
    count_row = np.unique(coords[0], return_counts=True)
    count_col = np.unique(coords[1], return_counts=True)
    # 热像元缺陷行列
    hot_pixel_row = count_row[0][np.where(count_row[1] > 100)]
    hot_pixel_col = count_col[0][np.where(count_col[1] > 100)]

    # 计算超过4倍典型值的像元比例
    coord_hotPixel_over4x = np.where(dark_res > 4 * res_darkCurrent)
    ratio_over4x = coord_hotPixel_over4x[0].shape[0] / dark_res.size

    # 显示结果
    mainFrame.darkcurrentPage.dc_textCtrl3.SetValue(str(round(res_darkCurrent, 6) / time * gain))
    mainFrame.darkcurrentPage.dc_textCtrl4.SetValue(str(hot_pixel_num))
    mainFrame.darkcurrentPage.dc_textCtrl5.SetValue(str(round(ratio_over4x, 5)))
    mainFrame.darkcurrentPage.dc_textCtrl6.SetValue(",".join(hot_pixel_row))
    mainFrame.darkcurrentPage.dc_textCtrl6.SetValue(",".join(hot_pixel_col))
    return


def prnu_process(mainFrame):
    bias_path = mainFrame.biasfilePath
    flat_path = mainFrame.flatfilePath
    bias_files = []
    flat_files = []
    if isinstance(bias_path, str):
        # 输入路径为str，即目录
        for bias_file in os.listdir(bias_path):
            bias_files.append(os.path.join(bias_path, bias_file))

    if isinstance(bias_path, list):
        # 输入路径为list, 即文件名
        bias_files = bias_path

    if isinstance(flat_path, str):
        # 输入路径为str，即目录
        for flat_file in os.listdir(flat_path):
            flat_files.append(os.path.join(flat_path, flat_file))

    if isinstance(flat_path, list):
        # 输入路径为list, 即文件名
        flat_files = flat_path

    bias_tmp = []
    flat_tmp = []

    # 读取本底场图像
    for bias_file in bias_files:
        each_data = load.getData(mainFrame, bias_file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            bias_tmp = each_data
        else:
            bias_tmp.append(each_data)
    # 读取平场图像
    for flat_file in flat_files:
        each_data = load.getData(mainFrame, flat_file)
        # 多个三维fits 堆叠待解决
        if each_data.ndim > 2:
            # arr = np.concatenate((arr, each_data))
            flat_tmp = each_data
        else:
            flat_tmp.append(each_data)
    # 图像堆叠转为array
    bias_data = np.array(bias_tmp, dtype=float)
    flat_data = np.array(flat_tmp, dtype=float)

    # 选择两幅平均值最接近的图像
    bias1, bias2 = load.im_select(bias_data)
    flat1, flat2 = load.im_select(flat_data)

    bias_diff = bias1 - bias2
    flat_diff = flat1 - flat2

    bias_dif_var = np.var(bias_diff)
    flat_diff_var = np.var(flat_diff)

    res_prnu = np.sqrt(2) * np.sqrt(
        np.var(flat1) + np.var(flat2) - np.var(bias1) - np.var(bias2) - (flat_diff_var - bias_dif_var)) \
               / (np.mean(flat1) + np.mean(flat2) - np.mean(bias1) - np.mean(bias2))

    mainFrame.prnuPage.prnu_textCtrl1.SetValue(str(round(res_prnu, 4)))
    return
