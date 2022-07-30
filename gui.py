import wx  # 导入wxpython模块
import word_cloud as createPic
import crawl
import tkinter as tk


class MyFrame(wx.Frame):  # 创建一个子类继承父类
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title='创建boxsizer', size=(400, 300))  # 调用父类构造方法
        panel = wx.Panel(self)
        self.title = wx.StaticText(panel, label='请输入需要分析的知乎ID')  # 创建文本框
        self.text_id = wx.TextCtrl(panel, style=wx.TE_LEFT)  # 创建用户名输入框
        self.bt_confirm = wx.Button(panel, label='确定')  # 创建确定按钮
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.send)
        self.bt_cancel = wx.Button(panel, label='重置')  # 创建取消按钮
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.cancel)
        self.imgPos = wx.Image('./Pos.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        # self.imgNeg = wx.Image('./Neg.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        # self.imgMid = wx.Image('./Mid.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        hsizer_img = wx.BoxSizer(wx.HORIZONTAL)
        #
        self.m_bitmap2 = wx.StaticBitmap(self, bitmap=self.imgPos)
        hsizer_img.Add(self.m_bitmap2, 0, wx.ALL, 5)

        # self.m_bitmap3 = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        # hsizer_img.Add(self.m_bitmap3, 0, wx.ALL, 5)
        #
        # self.m_bitmap4 = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        # hsizer_img.Add(self.m_bitmap4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # 添加容器，将容器中控件横向排列
        hsizer_user = wx.BoxSizer(wx.HORIZONTAL)  # HORIZONTAL是横向排列,每创建一个容器，容器中控件为一组
        hsizer_user.Add(self.text_id, proportion=1, flag=wx.ALL, border=5)

        hsizer_button = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_button.Add(self.bt_confirm, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_button.Add(self.bt_cancel, proportion=1, flag=wx.ALIGN_CENTER, border=5)

        # hsizer_img = wx.BoxSizer(wx.HORIZONTAL)
        # hsizer_img.Add(self.imgPos,proportion=0,flag=wx.ALIGN_CENTER,border=5)
        # hsizer_img.Add(self.imgNeg, proportion=1, flag=wx.ALIGN_CENTER, border=5)
        # hsizer_img.Add(self.imgMid, proportion=2, flag=wx.ALIGN_CENTER, border=5)

        ##添加容器，将所有控件纵向排列
        vsizer_all = wx.BoxSizer(wx.VERTICAL)
        vsizer_all.Add(self.title, proportion=0, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER, border=15)
        vsizer_all.Add(hsizer_user, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_button, proportion=0, flag=wx.ALIGN_CENTER | wx.TOP, border=15)
        # vsizer_all.Add(hsizer_img,proportion=0,border=15)
        panel.SetSizer(vsizer_all)

    def send(self, event):
        print('send')
        id = self.text_id.GetValue()
        if id == '':
            wx.MessageBox('请输入ID！')
            return
        crawl.run(id)
        createPic.run()

    def cancel(self, event):
        print('cancel')
        self.text_id.SetValue('')


if __name__ == '__main__':
    app = wx.App()  # 初始化应用
    frame = MyFrame(parent=None, id=-1)  # 实现Myframe类，并传递参数
    frame.Show()  # 显示窗口
    app.MainLoop()  # 调用主循环方法
