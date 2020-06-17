import wx
import core.draw as draw
import core.load as load
import os

class MainFrame(wx.Frame):
    def __init__(self, parent,title):
        super(MainFrame, self).__init__(parent, title=title)
        self.Init_Panel()
        self.Init_Box()
        self.Init_UpPanel()
        self.Init_DownPanel()
        # 将二级垂直盒子添加到一级水平盒子
        self.Boxv1.Add(self.UpPanel, border = 2, flag = wx.ALL | wx.EXPAND)
        self.Boxv1.Add(self.DownPanel, border = 2, flag = wx.ALL | wx.EXPAND)
        # 将水平盒子和主框架关联
        self.SetSizer(self.Boxv1)
        self.Fit()
        self.Center()
        self.Show()

    def Init_Panel(self):
        self.UpPanel = wx.Panel(self)
        self.DownPanel = wx.Panel(self)

    def Init_Box(self):
        # #一个垂直盒子
        self.Boxv1 = wx.BoxSizer(wx.VERTICAL)
        # self.Boxv2 = wx.BoxSizer(wx.VERTICAL)

    def Init_UpPanel(self):
        '''
        初始化上面板, 包括 文件路径、文件类型和ROI设置
        :return:
        '''
        self.Boxh1 = wx.BoxSizer(wx.HORIZONTAL)
        # 创建“文件预览”
        self.fp = wx.StaticBox(self.UpPanel, -1, '文件预览')
        self.fpSizer = wx.StaticBoxSizer(self.fp, wx.VERTICAL)
        self.fViewSizer = wx.GridBagSizer(0,0)
        # 文件预览控件
        self.fViewText = wx.StaticText(self.UpPanel, -1, "图像路径")
        self.fViewCtrl = wx.FilePickerCtrl(self.UpPanel, -1, style=wx.FLP_DEFAULT_STYLE)
        self.fViewButton = wx.Button(self.UpPanel, -1, "图像预览")
        self.fViewSizer.Add(self.fViewText, pos=(0,0), flag=wx.EXPAND, border=3)
        self.fViewSizer.Add(self.fViewCtrl, pos=(1,0), flag=wx.EXPAND, border=3)
        self.fViewSizer.Add(self.fViewButton, pos=(1,1), flag=wx.EXPAND, border=3)
        self.fpSizer.Add(self.fViewSizer,1, wx.EXPAND|wx.ALL,0)


        # 创建size format
        self.ft = wx.StaticBox(self.UpPanel, -1, 'Size Format')
        self.ftSizer = wx.StaticBoxSizer(self.ft, wx.VERTICAL)
        self.sfSizer = wx.GridBagSizer(0,0)
        # dtype控件
        self.sf_dtypeText = wx.StaticText(self.UpPanel, -1, "dtype")
        self.sfSizer.Add(self.sf_dtypeText, pos = (0,0), flag=wx.EXPAND |wx.ALL, border=3)
        self.sf_dtypeSuffix = ['uint16', '>H', '<H', 'float']
        self.sf_dtypeCtrl = wx.ComboBox(self.UpPanel, choices=self.sf_dtypeSuffix, value=self.sf_dtypeSuffix[0])
        self.sfSizer.Add(self.sf_dtypeCtrl,pos=(1,0), flag=wx.EXPAND | wx.ALL, border=3)
        # skip控件
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

        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.OnButton_Preview, self.fViewButton)

    def Init_DownPanel(self):
        self.DownBoxh = wx.BoxSizer(wx.HORIZONTAL)

        # 创建文件路径 静态文本框
        self.fileBox = wx.StaticBox(self.DownPanel,-1,"文件路径")
        self.fileBoxSizer = wx.StaticBoxSizer(self.fileBox, wx.VERTICAL)

        self.fileSizer = wx.GridBagSizer(0, 0)
        self.file_FileText1  = wx.StaticText(self.DownPanel, -1, "本底场图像")
        self.file_textCtrl1 = wx.TextCtrl(self.DownPanel, -1, style= wx.TE_MULTILINE| wx.HSCROLL)
        self.file_button1 = wx.Button(self.DownPanel, -1, "打开文件")
        self.file_button2 = wx.Button(self.DownPanel, -1, "打开文件夹")
        self.file_FileText2  = wx.StaticText(self.DownPanel, -1, "平场图像")
        self.file_textCtrl2 = wx.TextCtrl(self.DownPanel, -1, style= wx.TE_MULTILINE | wx.HSCROLL)
        self.file_button3 = wx.Button(self.DownPanel, -1, "打开文件")
        self.file_button4 = wx.Button(self.DownPanel, -1, "打开文件夹")
        self.file_FileText3  = wx.StaticText(self.DownPanel, -1, "暗场图像")
        self.file_textCtrl3 = wx.TextCtrl(self.DownPanel, -1, style= wx.TE_MULTILINE| wx.HSCROLL)
        self.file_button5 = wx.Button(self.DownPanel, -1, "打开文件")
        self.file_button6 = wx.Button(self.DownPanel, -1, "打开文件夹")

        self.fileSizer.Add(self.file_FileText1, pos=(0,0), flag=wx.EXPAND | wx.ALL, border=3)
        self.fileSizer.Add(self.file_textCtrl1, pos=(1,0), span=(5,15),flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_button1,  pos=(1,16), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_button2,  pos=(2,16), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_FileText2, pos=(6,0), flag=wx.EXPAND | wx.ALL, border=3)
        self.fileSizer.Add(self.file_textCtrl2, pos=(7,0), span=(5,15), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_button3, pos=(7,16), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_button4, pos=(8,16), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_FileText3, pos=(12,0), flag=wx.EXPAND | wx.ALL, border=3)
        self.fileSizer.Add(self.file_textCtrl3, pos=(13,0), span=(5, 15), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_button5, pos=(13,16), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileSizer.Add(self.file_button6, pos=(14,16), flag=wx.ALL | wx.EXPAND, border=3)
        self.fileBoxSizer.Add(self.fileSizer, 1, wx.EXPAND | wx.ALL, 0)

        # 创建标签页
        self.DownNoteBook = wx.Notebook(self.DownPanel, style=wx.NB_FIXEDWIDTH)
        self.gain_rdnPage = GainAndReadoutNoisePage(self.DownNoteBook)
        self.ptcPage = PTCPage(self.DownNoteBook)
        self.darkcurrentPage = DarkCurrentPage(self.DownNoteBook)
        self.prnuPage = PRNUPage(self.DownNoteBook)

        self.DownNoteBook.AddPage(self.gain_rdnPage, "增益 读出噪声")
        self.DownNoteBook.AddPage(self.ptcPage, "PTC")
        self.DownNoteBook.AddPage(self.darkcurrentPage, "暗电流")
        self.DownNoteBook.AddPage(self.prnuPage, "PRNU")
        
        # self.Boxv2.Add(self.DownNoteBook, 1, wx.EXPAND | wx.ALL, 10)
        # self.DownPanel.SetSizer(self.Boxv2)
        self.DownBoxh.Add(self.fileBoxSizer, 1, wx.EXPAND |wx.ALL, 10)
        self.DownBoxh.Add(self.DownNoteBook, 1, wx.EXPAND | wx.ALL, 10)
        self.DownPanel.SetSizer(self.DownBoxh)

        # 绑定事件 （PTC，gain，prnu，readoutNoise）
        self.Bind(wx.EVT_BUTTON, self.OnButton_Flat_OpenFile, self.file_button3)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Flat_OpenDir, self.file_button4)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Bias_OpenFile, self.file_button1)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Bias_OpenDir, self.file_button2)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Dark_OpenFile, self.file_button5)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Dark_OpenDir, self.file_button6)
        self.Bind(wx.EVT_BUTTON, self.OnButton_ReadoutNoiseCal, self.gain_rdnPage.rdn_button)

    def OnButton_Preview(self, Event):
        draw.preview(self)

    def OnButton_OpenFile(self):
        dlg = wx.FileDialog(self, '选择文件', style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR | wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()
            dlg.Destroy()
            return path

    def OnButton_OpenDir(self):
        dlg = wx.DirDialog(self, '选择文件夹', style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path =  dlg.GetPath()
            dlg.Destroy()
            return path

    def OnButton_Flat_OpenFile(self, Event):
        paths = self.OnButton_OpenFile()
        if paths:
            self.file_textCtrl2.Clear()
            for path in paths:
                self.file_textCtrl2.AppendText(path+'\n')
            self.flatfilePath = paths

    def OnButton_Flat_OpenDir(self, Event):
        path = self.OnButton_OpenDir()
        if path:
            self.file_textCtrl2.Clear()
            self.file_textCtrl2.SetValue(path)
            self.flatfilePath = path

    def OnButton_Bias_OpenFile(self, Event):
        paths = self.OnButton_OpenFile()
        if paths:
            self.file_textCtrl1.Clear()
            for path in paths:
                self.file_textCtrl1.AppendText(path+'\n')
            self.biasfilePath = paths

    def OnButton_Bias_OpenDir(self, Event):
        path = self.OnButton_OpenDir()
        if path:
            self.file_textCtrl1.Clear()
            self.file_textCtrl1.SetValue(path)
            self.biasfilePath = path

    def OnButton_Dark_OpenFile(self, Event):
        paths = self.OnButton_OpenFile()
        if paths:
            self.file_textCtrl3.Clear()
            for path in paths:
                self.file_textCtrl3.AppendText(path + '\n')

    def OnButton_Dark_OpenDir(self, Event):
        path = self.OnButton_OpenDir()
        if path:
            self.file_textCtrl3.Clear()
            self.file_textCtrl3.SetValue(path)

    def OnButton_GainCal(self, Event):
        pass

    def OnButton_ReadoutNoiseCal(self,Event):
        if not hasattr(self, 'biasfilePath') or not self.biasfilePath:
            dlg = wx.MessageDialog(None, "无效路径!", caption="警告", style=wx.OK)
            dlg.ShowModal()
            return

        if not self.gain_rdnPage.rdn_textCtrl1.GetValue():
            dlg = wx.MessageDialog(None, "请输入增益参数！", caption="警告", style=wx.OK)
            dlg.ShowModal()
            return

        # load.getData(self, self.biasfilePath)




class GainAndReadoutNoisePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent)
        self.Box = wx.BoxSizer(wx.VERTICAL)
        # 创建gain 组件
        self.gainBox = wx.StaticBox(self,-1,"Gain计算")
        self.gainBoxSizer = wx.StaticBoxSizer(self.gainBox, wx.VERTICAL)
        self.gainSizer = wx.GridBagSizer(0, 0)

        self.gain_FileText = wx.StaticText(self, -1, "增益（e-/ADU)")
        self.gain_textCtrl = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT| wx.TE_READONLY)
        self.gain_button = wx.Button(self, -1, "计算...")

        self.gainSizer.Add(self.gain_FileText, pos=(0,0), flag=wx.ALL | wx.EXPAND, border=3)
        self.gainSizer.Add(self.gain_textCtrl, pos=(1,0), flag=wx.ALL | wx.EXPAND, border=3)
        self.gainSizer.Add(self.gain_button, pos=(1,1), flag=wx.ALL | wx.EXPAND, border=3)
        self.gainBoxSizer.Add(self.gainSizer, 1, wx.EXPAND | wx.ALL, 0)

        # 创建readout Noise 组件
        self.rdnBox = wx.StaticBox(self,-1,"读出噪声计算")
        self.rdnBoxSizer = wx.StaticBoxSizer(self.rdnBox, wx.VERTICAL)
        self.rdnSizer = wx.GridBagSizer(0, 0)

        self.rdn_FileText1 = wx.StaticText(self, -1, "增益（e-/ADU)")
        self.rdn_textCtrl1 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT)
        self.rdn_FileText2 = wx.StaticText(self, -1, "读出噪声结果 (e-)")
        self.rdn_textCtrl2 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.TE_READONLY)
        self.rdn_button = wx.Button(self, -1, "计算...")

        self.rdnSizer.Add(self.rdn_FileText1, pos=(0, 0), flag=wx.ALL | wx.EXPAND, border=3)
        self.rdnSizer.Add(self.rdn_textCtrl1, pos=(1, 0), flag=wx.ALL | wx.EXPAND, border=3)
        self.rdnSizer.Add(self.rdn_FileText2, pos=(2, 0), flag=wx.ALL | wx.EXPAND, border=3)
        self.rdnSizer.Add(self.rdn_textCtrl2, pos=(3, 0), flag=wx.ALL | wx.EXPAND, border=3)
        self.rdnSizer.Add(self.rdn_button, pos=(3, 1), flag=wx.ALL | wx.EXPAND, border=3)
        self.rdnBoxSizer.Add(self.rdnSizer, 1, wx.EXPAND | wx.ALL, 0)

        self.Box.Add(self.gainBoxSizer, 1, wx.EXPAND |wx.ALL, 10)
        self.Box.Add(self.rdnBoxSizer, 1, wx.EXPAND |wx.ALL, 10)
        self.SetSizer(self.Box)

class PTCPage(wx.Panel):
    def __init__(self, parent):
        super(PTCPage, self).__init__(parent)
        # wx.Panel.__init__(self,parent)
        # 创建PTC 组件
        self.ptcSizer = wx.GridBagSizer(0, 0)
        self.ptc_FileText3 = wx.StaticText(self, -1, "增益 (e-/ADU)")
        self.ptc_FileText4 = wx.StaticText(self, -1, "读出噪声 (e-)")
        self.ptc_FileText5 = wx.StaticText(self, -1, "满阱电荷（e-)")
        self.ptc_FileText6 = wx.StaticText(self, -1, "PTC 非线性度")
        self.ptc_textCtrl3 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT| wx.TE_READONLY)
        self.ptc_textCtrl4 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT| wx.TE_READONLY)
        self.ptc_textCtrl5 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT| wx.TE_READONLY)
        self.ptc_textCtrl6 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT| wx.TE_READONLY)

        self.ptc_button5 = wx.Button(self,- 1, "计算...")

        self.ptcSizer.Add(self.ptc_FileText3, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_FileText4, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_FileText5, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_FileText6, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_textCtrl3, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_textCtrl4, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_textCtrl5, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_textCtrl6, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.ptcSizer.Add(self.ptc_button5, pos=(5, 0), flag=wx.EXPAND | wx.ALL, border=3)

        self.SetSizer(self.ptcSizer)

class DarkCurrentPage(wx.Panel):
    def __init__(self, parent):
        super(DarkCurrentPage, self).__init__(parent)
        # wx.Panel.__init__(self,parent)
        # 创建darkcurrent 组件
        self.darkcurrentSizer = wx.GridBagSizer(0, 0)

        self.dc_FileText3 = wx.StaticText(self, -1, "增益 (e-/ADU)")
        self.dc_FileText4 = wx.StaticText(self, -1, "暗电流 (e-)")
        self.dc_FileText5 = wx.StaticText(self, -1, "热像元数量")
        self.dc_FileText6 = wx.StaticText(self, -1, "热像元比例")
        self.dc_FileText7 = wx.StaticText(self, -1, "热像元行/列")

        self.dc_textCtrl3 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT)
        self.dc_textCtrl4 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.TE_READONLY)
        self.dc_textCtrl5 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.TE_READONLY)
        self.dc_textCtrl6 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.TE_READONLY)
        self.dc_textCtrl7 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.TE_READONLY)

        self.dc_button5 = wx.Button(self, - 1, "计算...")

        self.darkcurrentSizer.Add(self.dc_FileText3, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_FileText4, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_FileText5, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_FileText6, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_FileText7, pos=(4, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_textCtrl3, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_textCtrl4, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_textCtrl5, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_textCtrl6, pos=(5, 0), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_textCtrl7, pos=(5, 1), flag=wx.EXPAND | wx.ALL, border=3)
        self.darkcurrentSizer.Add(self.dc_button5, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=3)

        self.SetSizerAndFit(self.darkcurrentSizer)

class PRNUPage(wx.Panel):
    def __init__(self, parent):
        # super(ReadoutNoisePage, self).__init__(parent)
        wx.Panel.__init__(self, parent)
        # 创建prnu 组件
        self.prnuSizer = wx.GridBagSizer(0, 0)

        self.prnu_FileText3 = wx.StaticText(self, -1, "PRNU")
        self.prnu_textCtrl3 = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.TE_READONLY)
        self.prnu_button5 = wx.Button(self, -1, "计算...")

        self.prnuSizer.Add(self.prnu_FileText3, pos=(0, 0), flag=wx.ALL | wx.EXPAND, border=3)
        self.prnuSizer.Add(self.prnu_textCtrl3, pos=(1, 0), flag=wx.ALL | wx.EXPAND, border=3)
        self.prnuSizer.Add(self.prnu_button5, pos=(1, 1), flag=wx.ALL | wx.EXPAND, border=3)
        self.SetSizer(self.prnuSizer)

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None,"CCD-Data-Process")
    app.MainLoop()