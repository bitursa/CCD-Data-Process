import wx
import matplotlib.pyplot as plt


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title)
        # 创建白板
        panel = wx.Panel(self)
        # 创建垂直与水平box盒子
        vbox = wx.BoxSizer(wx.VERTICAL)
        nmbox = wx.BoxSizer(wx.HORIZONTAL)

        # 创建一个wx.StaticBox对象。
        # 声明一个wx.StaticBoxSizer与创建的wx.StaticBox对象作为其参数。
        nm = wx.StaticBox(panel, -1, 'Name:')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        # 构建静态文本框与输入框
        fn = wx.StaticText(panel, -1, "First Name")
        nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        ln = wx.StaticText(panel, -1, "Last Name")
        self.nm2 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT| wx.TE_READONLY)
        self.b = wx.Button(panel, -1, '...')
        # self.b = wx.File(panel, -1)
        # 在水平盒子里添加进上面四个
        nmbox.Add(fn, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(nm1, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(self.nm2, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(self.b, 0, wx.ALL | wx.CENTER, 5)
        #Bind
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.b)
        # self.b.Bind(wx.EVT_BUTTON, self.OnButton)
        # 在StaticBoxSizer添加进水平盒子
        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 10)

        # 在垂直盒子里添加StaticBoxSizer盒子
        vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(vbox)
        panel.Fit()
        self.Centre()

        self.Show()
        # 关系：
        # 垂直box盒子添加StaticBoxSizer盒子
        # StaticBoxSizer盒子添加水平盒子

    def OnButton(self, event):
        # dlg = wx.MultiChoiceDialog(self)
        dlg = wx.FileDialog(self, '选择文件夹', style= wx.FD_MULTIPLE | wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            filelist = dlg.GetPaths()
            self.nm2.SetValue(filelist[0])
            dlg.Destroy()

        # xs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # ys = [10, 12, 16, 22, 26, 28, 30, 30, 25, 21, 16, 11]
        # lbs = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
        #        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # plt.xticks(xs, lbs)
        #
        # plt.plot(xs, ys, '-o')
        # plt.grid()
        #
        # plt.title('Temperature in ChengDu')
        # plt.xlabel('Month')
        # plt.ylabel('Temperature (C)')
        #
        # plt.show()




app = wx.App()
Mywin(None, 'StaticBoxSizer')
app.MainLoop()