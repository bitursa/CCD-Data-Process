import numpy as np
import wx
import astropy.io.fits as pyfits
import os


def getData(MainFrame, path):
    # 读取参数
    dtype = MainFrame.sf_dtypeCtrl.GetValue()
    skip = int(MainFrame.sf_skipCtrl.GetValue())
    width = int(MainFrame.sf_widthCtrl.GetValue())
    height = int(MainFrame.sf_heightCtrl.GetValue())
    # 设置roi
    roiFlag = MainFrame.roiTrigger.GetValue()
    if roiFlag:
        roi_hOffset = int(MainFrame.roi_hOffsetCtrl.GetValue())
        roi_vOffset = int(MainFrame.roi_vOffsetCtrl.GetValue())
        roi_width = int(MainFrame.roi_widthCtrl.GetValue())
        roi_height = int(MainFrame.roi_heightCtrl.GetValue())

    # 判断文件路径
    # if not os.path.isfile(path) or not path.endswith(".fits") or not path.endswith(".raw"):
    if not os.path.isfile(path):
        dlg = wx.MessageDialog(None, "无效路径！请选择一个文件（.fits or .raw)", caption="警告", style=wx.OK)
        dlg.ShowModal()
        return None

    # 读取数据
    if os.path.splitext(path)[-1] == ".fits":
        data = pyfits.getdata(path, dtype=dtype)
        # 设置roi
        if roiFlag:
            if data.ndim > 2:
                data = data[:, roi_vOffset:roi_vOffset + roi_height, roi_hOffset: roi_hOffset + roi_width]
            else:
                data = data[roi_vOffset:roi_vOffset + roi_height, roi_hOffset: roi_hOffset + roi_width]
    # if os.path.splitext(path)[-1] == ".raw":
    else:
        data = np.fromfile(path, dtype=dtype)
        data = data[skip:]
        data = np.reshape(data, (height, width))
        if roiFlag:
            data = data[roi_vOffset:roi_vOffset + roi_height, roi_hOffset: roi_hOffset + roi_width]

    return data


def im_select(data):
    """
    选出平均值最近的两幅图像，并返回这两幅图像数据
    """
    mean_value = []
    img_diff = []
    length = data.shape[0]
    for i in range(length):
        mean_value.append(np.mean(data[i, :, :]))

    mean_value = np.array(mean_value,dtype=float)
    sort_Mean = np.sort(mean_value)
    sort_Arg = np.argsort(mean_value)

    for i in range(length - 1):
        img_diff.append(sort_Mean[i+1] - sort_Mean[i])

    res = np.argsort(img_diff)
    arg1 = res[0]
    arg2 = arg1 + 1
    sort1 = sort_Arg[arg1]
    sort2 = sort_Arg[arg2]
    return data[sort1], data[sort2]


def im_combine(data):
    data_sort = np.sort(data, axis=0)
    data_clip = data_sort[:-1, :, :]
    data_mean = np.mean(data_clip, axis=0)

    return data_mean
