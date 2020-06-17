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
    if not os.path.isfile(path) or not path.endswith(".fits") or not path.endswith(".raw"):
        dlg = wx.MessageDialog(None, "无效路径！请选择一个文件（.fits or .raw)", caption="警告", style=wx.OK)
        dlg.ShowModal()
        return None

    # 读取数据
    if os.path.splitext(path)[-1] == ".fits" :
        data = pyfits.getdata(path,dtype=dtype)
        # 设置roi
        if roiFlag:
            data = data[:,roi_vOffset:roi_vOffset+roi_height, roi_hOffset: roi_hOffset+roi_width]

    # if os.path.splitext(path)[-1] == ".raw":
    else:
        data = np.fromfile(path,dtype = dtype)
        data = data[skip:]
        data = np.reshape(data,(width,height))
        if roiFlag:
            data = data[roi_hOffset: roi_hOffset+roi_width, roi_vOffset:roi_vOffset+roi_height]

    return data


