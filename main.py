import wx
import core.draw as draw
import os

class MainFrame(wx.Frame):
    def __init__(self, parent,title):
        super(MainFrame, self).__init__(parent, title=title)
        self.Init_Panel()
        self.Init_Box()
        self.Init_UpPanel()
        # 将二级垂直盒子添加到一级水平盒子
        self.Boxv1.Add(self.UpPanel, proportion = 1, border = 2, flag = wx.ALL | wx.EXPAND)
        self.Boxv1.Add(self.DownPanel, proportion = 2, border = 2, flag = wx.ALL | wx.EXPAND)
        # 将水平盒子和主框架关联
        self.SetSizer(self.Boxv1)
        self.Fit()
        self.Center()
        self.Show()

    def Init_Panel(self):
        self.UpPanel = wx.Panel(self)
        self.DownPanel = wx.Panel(self)

    def Init_Box(self):
        #一个垂直盒子
        self.Boxv1 = wx.BoxSizer(wx.VERTICAL)
        #三个水平盒子
        self.Boxh1 = wx.BoxSizer(wx.HORIZONTAL)
        self.Boxh2 = wx.BoxSizer(wx.HORIZONTAL)
        self.Boxh3 = wx.BoxSizer(wx.HORIZONTAL)

    def Init_UpPanel(self):
        '''
        初始化上面板, 包括 文件路径、文件类型和ROI设置
        :return:
        '''
        # 创建“文件路径”
        self.fp = wx.StaticBox(self.UpPanel, -1, '文件路径')
        self.fpSizer = wx.StaticBoxSizer(self.fp, wx.VERTICAL)
        # 构建平场图像文本框
        self. fp_modelname1 = wx.StaticText(self.UpPanel, -1, "平场图像路径")
        #添加平场图像文本框
        self.fpSizer.Add(self.fp_modelname1, 1,  wx.ALL, 3)
        #创建平场图像路径的控件
        self.fpBoxh1 = wx.BoxSizer(wx.HORIZONTAL)
        self.fp_textCtrl1 = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        self.fp_button1 = wx.Button(self.UpPanel, -1, "打开文件")
        self.fp_button2 = wx.Button(self.UpPanel, -1, "打开文件夹")
        self.fp_button3 = wx.Button(self.UpPanel, -1, "图像预览")
        self.fpBoxh1.Add(self.fp_textCtrl1, 0, wx.ALL | wx.EXPAND, 1)
        self.fpBoxh1.Add(self.fp_button3, 0, wx.ALL | wx.EXPAND, 1)
        self.fpBoxh1.Add(self.fp_button1, 0, wx.ALL | wx.EXPAND, 1)
        self.fpBoxh1.Add(self.fp_button2, 0, wx.ALL | wx.EXPAND, 1)
        self.fpSizer.Add(self.fpBoxh1, 0, wx.ALL | wx.EXPAND, 3)

        # 构建本底场图像文本框
        self.fp_modelname2 = wx.StaticText(self.UpPanel, -1, "本底场图像路径")
        #添加本底场图像文本框
        self.fpSizer.Add(self.fp_modelname2, 1, wx.EXPAND | wx.ALL, 3)
        #创建本底场图像路径的控件
        self.fpBoxh2 = wx.BoxSizer(wx.HORIZONTAL)
        self.fp_textCtrl2 = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        self.fp_button4 = wx.Button(self.UpPanel, -1, "打开文件")
        self.fp_button5 = wx.Button(self.UpPanel, -1, "打开文件夹")
        self.fp_button6 = wx.Button(self.UpPanel, -1, "图像预览")
        self.fpBoxh2.Add(self.fp_textCtrl2, 0, wx.ALL | wx.EXPAND , 1)
        self.fpBoxh2.Add(self.fp_button6, 0, wx.ALL | wx.EXPAND , 1)
        self.fpBoxh2.Add(self.fp_button4, 0, wx.ALL | wx.EXPAND , 1)
        self.fpBoxh2.Add(self.fp_button5, 0, wx.ALL | wx.EXPAND , 1)
        self.fpSizer.Add(self.fpBoxh2, 0, wx.ALL | wx.EXPAND, 3)


        # 创建size format
        self.ft = wx.StaticBox(self.UpPanel, -1, 'Size Format')
        self.ftSizer = wx.StaticBoxSizer(self.ft, wx.VERTICAL)
        self.sfSizer = wx.GridBagSizer(0,0)
        #dtype控件
        self.sf_dtypeText = wx.StaticText(self.UpPanel, -1, "dtype")
        self.sfSizer.Add(self.sf_dtypeText, pos = (0,0), flag=wx.EXPAND |wx.ALL, border=3)
        self.sf_dtypeSuffix = ['uint16', '>H', '<H', 'float']
        self.sf_dtypeCtrl = wx.ComboBox(self.UpPanel, choices=self.sf_dtypeSuffix, value=self.sf_dtypeSuffix[0])
        self.sfSizer.Add(self.sf_dtypeCtrl,pos=(1,0), flag=wx.EXPAND | wx.ALL, border=3)
        #skip控件
        self.sf_skipText = wx.StaticText(self.UpPanel, -1, "Skip")
        self.sf_skipCtrl = wx.TextCtrl(self.UpPanel)
        self.sf_skipCtrl.SetValue("0")
        self.sfSizer.Add(self.sf_skipText, pos=(0,1), flag=wx.EXPAND |wx.ALL, border=3)
        self.sfSizer.Add(self.sf_skipCtrl, pos=(1,1), flag=wx.EXPAND | wx.ALL, border=3)
        # width控件
        self.sf_widthText = wx.StaticText(self.UpPanel, -1, "Width")
        self.sf_widthCtrl = wx.TextCtrl(self.UpPanel)
        self.sf_widthCtrl.SetValue("1024")
        self.sfSizer.Add(self.sf_widthText, pos=(2,0), flag=wx.EXPAND |wx.ALL, border=3)
        self.sfSizer.Add(self.sf_widthCtrl, pos=(3,0), flag=wx.EXPAND | wx.ALL, border=3)
        # height控件
        self.sf_heightText = wx.StaticText(self.UpPanel, -1, "Height")
        self.sf_heightCtrl = wx.TextCtrl(self.UpPanel)
        self.sf_heightCtrl.SetValue("1024")
        self.sfSizer.Add(self.sf_heightText, pos=(2,1), flag=wx.EXPAND |wx.ALL, border=3)
        self.sfSizer.Add(self.sf_heightCtrl, pos=(3,1), flag=wx.EXPAND | wx.ALL, border=3)
        self.ftSizer.Add(self.sfSizer, 1, wx.EXPAND | wx.ALL, 0)

        # 创建Roi
        self.roi = wx.StaticBox(self.UpPanel, -1, 'ROI设置')
        self.roiSizer = wx.StaticBoxSizer(self.roi, wx.VERTICAL)
        self.roiTrigger = wx.CheckBox(self.UpPanel, -1, u"ROI on/off")
        self.roiBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.roiBoxh1 = wx.BoxSizer(wx.VERTICAL)
        self. roi_hOffsetText = wx.StaticText(self.UpPanel, -1, "Horizon Offset")
        self.roi_vOffsetText = wx.StaticText(self.UpPanel, -1, "Vertical Offset")
        self.roiBoxh1.Add(self.roi_hOffsetText, 0, wx.ALL | wx.BOTTOM, 7)
        self.roiBoxh1.Add(self.roi_vOffsetText, 0, wx.ALL | wx.BOTTOM, 7)

        self.roiBoxh2 = wx.BoxSizer(wx.VERTICAL)
        self.roi_hOffsetCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        self.roi_vOffsetCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        self.roiBoxh2.Add(self.roi_hOffsetCtrl, 0, wx.ALL | wx.BOTTOM, 3)
        self.roiBoxh2.Add(self.roi_vOffsetCtrl, 0, wx.ALL | wx.BOTTOM, 3)

        self.roiBoxh3 = wx.BoxSizer(wx.VERTICAL)
        self.roi_widthText = wx.StaticText(self.UpPanel, -1, "Width")
        self.roi_heightText = wx.StaticText(self.UpPanel, -1, "Height")
        self.roiBoxh3.Add(self.roi_widthText, 0, wx.ALL | wx.CENTER, 7)
        self.roiBoxh3.Add(self.roi_heightText, 0, wx.ALL | wx.CENTER, 7)

        self.roiBoxh4 = wx.BoxSizer(wx.VERTICAL)
        self.roi_widthCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        self.roi_heightCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        self.roiBoxh4.Add(self.roi_widthCtrl, 0, wx.ALL | wx.CENTER, 3)
        self.roiBoxh4.Add(self.roi_heightCtrl, 0, wx.ALL | wx.CENTER, 3)

        self.roiBoxSizer.Add(self.roiBoxh1, 0, wx.ALL | wx.EXPAND, 0)
        self.roiBoxSizer.Add(self.roiBoxh2, 0, wx.ALL | wx.EXPAND, 0)
        self.roiBoxSizer.Add(self.roiBoxh3, 0, wx.ALL | wx.EXPAND, 0)
        self.roiBoxSizer.Add(self.roiBoxh4, 0, wx.ALL | wx.EXPAND, 0)

        self.roiSizer.Add(self.roiTrigger, 0, wx.ALL | wx.EXPAND, 7)
        self.roiSizer.Add(self.roiBoxSizer, 0, wx.ALL | wx.EXPAND, 0)

        # 添加各个子部件
        self.Boxh1.Add(self.fpSizer, 0, wx.ALIGN_CENTER  | wx.ALL , 10)
        self.Boxh1.Add(self.ftSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.Boxh1.Add(self.roiSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.UpPanel.SetSizer(self.Boxh1)

        #绑定事件
        self.Bind(wx.EVT_BUTTON, self.OnButton_Flat_OpenFile, self.fp_button1)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Bias_OpenFile, self.fp_button4)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Flat_OpenDir, self.fp_button2)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Bias_OpenDir, self.fp_button5)
        self.Bind(wx.EVT_BUTTON, self.OnButton_FlatPreview, self.fp_button3)
        self.Bind(wx.EVT_BUTTON, self.OnButton_BiasPreview, self.fp_button6)

    def Init_DownPanel(self):
        pass

    def OnButton_FlatPreview(self, Event):
        filepath = self.fp_textCtrl1.GetValue()
        dtype = self.sf_dtypeCtrl.GetValue()
        skip = int(self.sf_skipCtrl.GetValue())
        width = int(self.sf_widthCtrl.GetValue())
        height = int(self.sf_heightCtrl.GetValue())
        draw.preview(filepath,dtype,width,height,skip)

    def OnButton_BiasPreview(self, Event):
        filepath = self.fp_textCtrl2.GetValue()
        dtype = self.sf_dtypeCtrl.GetValue()
        skip = int(self.sf_skipCtrl.GetValue())
        width = int(self.sf_widthCtrl.GetValue())
        height = int(self.sf_heightCtrl.GetValue())
        draw.preview(filepath, dtype, width, height, skip)

    def OnButton_Flat_OpenFile(self, Event):
        dlg = wx.FileDialog(self, '选择文件', style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fp_textCtrl1.SetValue(dlg.GetPath())
            dlg.Destroy()

    def OnButton_Bias_OpenFile(self, Event):
        dlg = wx.FileDialog(self, '选择文件', style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fp_textCtrl2.SetValue(dlg.GetPath())
            dlg.Destroy()

    def OnButton_Flat_OpenDir(self, Event):
        dlg = wx.DirDialog(self, '选择文件夹', style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fp_textCtrl1.SetValue(dlg.GetPath())
            dlg.Destroy()

    def OnButton_Bias_OpenDir(self, Event):
        dlg = wx.DirDialog(self, '选择文件夹', style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fp_textCtrl2.SetValue(dlg.GetPath())
            dlg.Destroy()



class PageOne(wx.Panel):
    pass

class PageTwo(wx.Panel):
    pass

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None,"CCD-Data-Process")
    app.MainLoop()