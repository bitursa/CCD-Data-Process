import wx

class MainFrame(wx.Frame):
    def __init__(self, parent,title):
        super(MainFrame, self).__init__(parent, title=title)
        self.Init_Panel()
        self.Init_Box()
        self.Init_Up()
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

    def Init_Up(self):
        '''
        初始化上面板, 包括 文件路径、文件类型和ROI设置
        :return:
        '''
        # 创建“文件路径”
        fp = wx.StaticBox(self.UpPanel, -1, '文件路径')
        fpSizer = wx.StaticBoxSizer(fp, wx.VERTICAL)
        # 构建平场图像文本框
        fp_modelname1 = wx.StaticText(self.UpPanel, -1, "平场图像路径")
        #添加平场图像文本框
        fpSizer.Add(fp_modelname1, 1,  wx.ALL, 3)
        #创建平场图像路径的控件
        fpBoxh1 = wx.BoxSizer(wx.HORIZONTAL)
        fp_textCtrl1 = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        fp_button1 = wx.Button(self.UpPanel, -1, "打开文件")
        fp_button2 = wx.Button(self.UpPanel, -1, "打开文件夹")
        fp_button3 = wx.Button(self.UpPanel, -1, "图像预览")
        fpBoxh1.Add(fp_textCtrl1, 0, wx.ALL | wx.EXPAND, 1)
        fpBoxh1.Add(fp_button3, 0, wx.ALL | wx.EXPAND, 1)
        fpBoxh1.Add(fp_button1, 0, wx.ALL | wx.EXPAND, 1)
        fpBoxh1.Add(fp_button2, 0, wx.ALL | wx.EXPAND, 1)
        fpSizer.Add(fpBoxh1, 0, wx.ALL | wx.EXPAND, 3)

        # 构建本底场图像文本框
        fp_modelname2 = wx.StaticText(self.UpPanel, -1, "本底场图像路径")
        #添加本底场图像文本框
        fpSizer.Add(fp_modelname2, 1, wx.EXPAND | wx.ALL, 3)
        #创建本底场图像路径的控件
        fpBoxh2 = wx.BoxSizer(wx.HORIZONTAL)
        fp_textCtrl2 = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        fp_button4 = wx.Button(self.UpPanel, -1, "打开文件")
        fp_button5 = wx.Button(self.UpPanel, -1, "打开文件夹")
        fp_button6 = wx.Button(self.UpPanel, -1, "图像预览")
        fpBoxh2.Add(fp_textCtrl2, 0, wx.ALL | wx.EXPAND , 1)
        fpBoxh2.Add(fp_button6, 0, wx.ALL | wx.EXPAND , 1)
        fpBoxh2.Add(fp_button4, 0, wx.ALL | wx.EXPAND , 1)
        fpBoxh2.Add(fp_button5, 0, wx.ALL | wx.EXPAND , 1)
        fpSizer.Add(fpBoxh2, 0, wx.ALL | wx.EXPAND, 3)


        # 创建文件类型
        ft = wx.StaticBox(self.UpPanel, -1, '文件类型')
        ftSizer = wx.StaticBoxSizer(ft, wx.VERTICAL)
        # 添加扩展名
        ft_modelname1 = wx.StaticText(self.UpPanel, -1, "扩展名")
        ftSizer.Add(ft_modelname1, 1, wx.ALL, 3)
        # 创建下拉框
        self.suffix1 = ['.fits','.raw']
        self.combo1 = wx.ComboBox(self.UpPanel, choices=self.suffix1, value=self.suffix1[0])
        # 在StaticBoxSizer盒子添加下拉框
        ftSizer.Add(self.combo1, 1, wx.EXPAND | wx.ALL, 0)
        # 添dtype
        ft_modelname2 = wx.StaticText(self.UpPanel, -1, "dtype")
        ftSizer.Add(ft_modelname2, 1, wx.ALL, 3)
        # 创建下拉框
        self.suffix2 = ['uint16','uint16 little endian','uint16 big endian','float']
        self.combo2 = wx.ComboBox(self.UpPanel, choices=self.suffix2, value=self.suffix2[0])
        # 在StaticBoxSizer盒子添加下拉框
        ftSizer.Add(self.combo2, 1, wx.EXPAND | wx.ALL, 0)


        # 创建Roi
        roi = wx.StaticBox(self.UpPanel, -1, 'ROI设置')
        roiSizer = wx.StaticBoxSizer(roi, wx.VERTICAL)
        roiTrigger = wx.CheckBox(self.UpPanel, -1, u"ROI on/off")
        roiBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        roiBoxh1 = wx.BoxSizer(wx.VERTICAL)
        roi_hOffsetText = wx.StaticText(self.UpPanel, -1, "Horizon Offset")
        roi_vOffsetText = wx.StaticText(self.UpPanel, -1, "Vertical Offset")
        roiBoxh1.Add(roi_hOffsetText, 0, wx.ALL | wx.BOTTOM, 7)
        roiBoxh1.Add(roi_vOffsetText, 0, wx.ALL | wx.BOTTOM, 7)

        roiBoxh2 = wx.BoxSizer(wx.VERTICAL)
        roi_hOffsetCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        roi_vOffsetCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        roiBoxh2.Add(roi_hOffsetCtrl, 0, wx.ALL | wx.BOTTOM, 3)
        roiBoxh2.Add(roi_vOffsetCtrl, 0, wx.ALL | wx.BOTTOM, 3)

        roiBoxh3 = wx.BoxSizer(wx.VERTICAL)
        roi_widthText = wx.StaticText(self.UpPanel, -1, "Width")
        roi_heightText = wx.StaticText(self.UpPanel, -1, "Height")
        roiBoxh3.Add(roi_widthText, 0, wx.ALL | wx.CENTER, 7)
        roiBoxh3.Add(roi_heightText, 0, wx.ALL | wx.CENTER, 7)

        roiBoxh4 = wx.BoxSizer(wx.VERTICAL)
        roi_widthCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        roi_heightCtrl = wx.TextCtrl(self.UpPanel, -1, style=wx.ALIGN_LEFT)
        roiBoxh4.Add(roi_widthCtrl, 0, wx.ALL | wx.CENTER, 3)
        roiBoxh4.Add(roi_heightCtrl, 0, wx.ALL | wx.CENTER, 3)

        roiBoxSizer.Add(roiBoxh1, 0, wx.ALL | wx.EXPAND, 0)
        roiBoxSizer.Add(roiBoxh2, 0, wx.ALL | wx.EXPAND, 0)
        roiBoxSizer.Add(roiBoxh3, 0, wx.ALL | wx.EXPAND, 0)
        roiBoxSizer.Add(roiBoxh4, 0, wx.ALL | wx.EXPAND, 0)

        roiSizer.Add(roiTrigger, 0, wx.ALL | wx.EXPAND, 7)
        roiSizer.Add(roiBoxSizer, 0, wx.ALL | wx.EXPAND, 0)

        # 添加各个子部件
        self.Boxh1.Add(fpSizer, 0, wx.ALIGN_CENTER  | wx.ALL , 10)
        self.Boxh1.Add(ftSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.Boxh1.Add(roiSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.UpPanel.SetSizer(self.Boxh1)

class PageOne(wx.Panel):
    pass

class PageTwo(wx.Panel):
    pass

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None,"CCD-Data-Process")
    app.MainLoop()