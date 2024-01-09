import json
import jsonpath
import requests
import sys
import os
import re
import io
import string
import faulthandler
import random
########PySide6 引用
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale, QObject,Signal,QUrl,QRect,QPoint
from PySide6.QtGui import QFontDatabase,QFont,QIcon,QPixmap,QColor, QAction,QGuiApplication
from PySide6.QtWidgets import QSystemTrayIcon,QMenu, QMessageBox,QApplication
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
#######qframelesswindow 引用
from qframelesswindow import AcrylicWindow
from qfluentwidgets import SplitFluentWindow,ColorDialog,FluentIcon,NavigationItemPosition,MessageBox,InfoBar,InfoBarPosition

import time

#####其他py文件引用
from ui.my_window_ui import MyWindowUI,LyricLabel
from ui.playbackcontrol_ui import playbackcontrol
from ui.aboueInterface_ui import aboueInterface
from lyrics_backend.interface import getCurrentLyric
import lyrics_backend.interface
from module.hotcomments import hotComments
# from module.font_setting import setbold,setunderline,setpointSize,setcolor,setfonta,change_font
from module.audio import MyAudioPlayer
# from module.systray import showlyrics,showwindows,showDialog

#########对接linux dbus 引用
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import pympris

#######全局变量设置
from module import allset
#####默认字体变量
fonta: str = "文泉驿等宽微米黑"  ###字体
bold: bool = True  ####粗细
underline: bool = False #####下划线
pointSize: int = 20.22  ###字号
foncolor: str = "00000000" ####黑色
ids = 0
#debug使用
#faulthandler.enable()
basedir = os.path.dirname(__file__)


class Main(SplitFluentWindow):
    global font,bold,underline,pointSize
    def __init__(self, minWidth=590, minHeight=650):
        super().__init__()
        self.resize(570,650)
        self.ui = MyWindowUI(sizeHintdb=(minWidth, minHeight), parent=self)
        self.ui1 = playbackcontrol(sizeHintdb=(minWidth, minHeight), parent=self)
        self.aboueInterface = aboueInterface(sizeHintdb=(minWidth, minHeight), parent=self)
##################ui修改
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(os.path.join(basedir,"res/icons/SystemPanel.png")))

        self.initNavigation()
##################功能代码

        if allset.players_ids != '' :
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)  # 每隔300毫秒（1秒）更新一次
        if allset.players_ids != '' :
#        self.initWindow()
            self.ab = QtCore.QTimer(self)
            self.ab.timeout.connect(self.button1)
            self.ab.start(100)  # 每隔100毫秒更新一次
        if allset.players_ids != '' :
            self.a = QtCore.QTimer(self)
            self.a.timeout.connect(self.update_a)
            self.a.start(100)  # 每隔100毫秒更新一次
        if allset.players_ids != '' :
            self.b = QtCore.QTimer(self)
            self.b.timeout.connect(self.update_pic)
            self.b.timeout.connect(self.updateplayer)
            self.b.start(100)  # 每隔100毫秒更新一次

        if allset.players_ids != '' :
            self.c = QtCore.QTimer(self)
            self.c.timeout.connect(self.hotsettime)
            self.c.start(1000)  # 每隔100毫秒更新一次



########## 字体更新
        self.ui.combo_box.currentTextChanged.connect(self.setfonta)
        self.ui.button1.clicked.connect(self.show_desktopLyric)
        self.ui.pointSize.valueChanged.connect(self.button2)
        self.ui.switchbold.checkedChanged.connect(self.setbold)
        # self.ui.switchbold.checkedChanged.connect(self.hot)
        self.ui.switchunderline.checkedChanged.connect(self.setunderline)
        self.ui.button2.clicked.connect(self.showColorDialog)
######### 播放按钮控制
        self.ui1.bas.skipForwardButton.clicked.connect(self.next1)
        self.ui1.bas.skipBackButton.clicked.connect(self.ra)
        self.ui1.bas.play.clicked.connect(self.playa)
        self.ui1.bas.progressSlider.sliderMoved.connect(self.plaa)
#########置顶更新
        self.ui.CheckBox1.clicked.connect(self.on_inTopCheckBox_clicked)
#########刷新播放器状态
        self.ui1.button1.clicked.connect(self.setplayers)
        self.ui1.combo_box.currentTextChanged.connect(self.playerss)

        self.desktopLyric = LyricLabel()
        self.change_font()
        self.setplayers()
###############窗口置顶
    def on_inTopCheckBox_clicked(self, checked):
        # print(checked)
        if checked != True :
            self.desktopLyric.setWindowFlags(QtCore.Qt.Widget | Qt.FramelessWindowHint)# 取消置顶
            # self.desktopLyric.setWindowFlags(Qt.FramelessWindowHint)
            self.desktopLyric.show()
        else:
            self.desktopLyric.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)# 置顶
            # self.desktopLyric.setWindowFlags(Qt.FramelessWindowHint)
            self.desktopLyric.show()


##########侧边栏添加
    def initNavigation(self):
        # add sub interface
        self.addSubInterface(self.ui1,
                             QIcon(os.path.join(basedir, "res/icons/jump.svg")),
                             self.tr('播放控制'))
        self.addSubInterface(self.ui,
                             FluentIcon.SETTING,
                             self.tr('设置'),
                             NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboueInterface,
                             FluentIcon.INFO,
                             self.tr('关于'),
                             NavigationItemPosition.BOTTOM)

##########控制歌词显示代码
    def show_desktopLyric(self):
        self.desktopLyric.set_lyrics(self.tr('这是一首很长的歌词'),self.tr('需要滚动显示'))
        if self.desktopLyric.isVisible():
            self.ui.CheckBox1.setChecked(False)
            allset.lycl = 0
            self.desktopLyric.close()
        else:
            allset.lycl = 1
            self.desktopLyric.show()

########字体设置
    def setbold(self, checked):
        global bold
        if checked:
            bold = True
            self.change_font()
        else:
            bold = False
            self.change_font()

    def setunderline(self, checked):
        global underline
        if checked:
            underline = True
            self.change_font()
        else:
            underline = False
            self.change_font()

    def button2(self):
        global pointSize
        pointSize = int(self.ui.pointSize.value())
#        print(pointSize)
        self.change_font()

    def showColorDialog(self):
        global foncolor
        # print(foncolor)
        colorset = ColorDialog(QColor(foncolor), self.tr('颜色设置'), self.window(),enableAlpha=False)
        colorset.setColor(QColor(foncolor), movePicker=True)
        colorset.colorChanged.connect(lambda c: self.setcolor(c))
        colorset.exec()

    def setcolor(self,c):
        global foncolor
        foncolor = c.name()
        self.change_font()


    def setfonta(self,font):
        global fonta
        fonta = font
        self.change_font()

    def change_font(self):
        global pointSize
        global fonta
        global bold
        global underline
        global foncolor
        # 创建QFont对象
        qfont = QFont(fonta)
        qfont.setPointSize(pointSize)# 设置字体大小
#        print(fonta)
        qfont.setBold(bold)
        qfont.setUnderline(underline)
        self.ui.label.setStyleSheet("color:"+foncolor)
        self.ui.label.setFont(qfont)
        if self.desktopLyric.isVisible():
            self.desktopLyric.setStyleSheet("color:"+foncolor)
            self.desktopLyric.setFont(qfont)
        else:
            self.desktopLyric.setFont(qfont)


###############设置控制的播放器

    def setplayers(self):
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        aa = str(mp.root.Identity)
        self.ui1.combo_box.clear()
        self.ui1.combo_box.addItems(list(pympris.available_players()))
        self.ui1.label4.setText(aa)
        self.ui1.label4.adjustSize()

##################歌词更新代码
    def update_label(self):
        res = lyrics_backend.interface.getCurrentLyric(0)
        lyric = res.get('lyric', '')  # 如果 'lyric' 键不存在，返回空字符串
        tlyric = res.get('tlyric', '') # 如果 'lyric' 键不存在，返回空字符串
        status = res.get('status', '')
        asa = res.get('e', '正常')
        allset.song_id = asa
              ##读取歌词显示情况
        if self.desktopLyric.isVisible():
            self.ui.label3.setText(self.tr("歌词：已显示"))
            self.ui.label3.adjustSize()
        else:
            self.ui.label3.setText(self.tr("歌词：未显示"))
            self.ui.label3.adjustSize()
        # if status == 200 :

#        print(singername)

        if status == 414:
            self.ui.label.setText(lyric)
            self.desktopLyric.set_lyrics(lyric,tlyric)
            self.ui.label.adjustSize()
        else:

            # self.desktopLyric.set_lyrics("间奏或纯音乐，如遇歌词有但是显示这句话","请提交issue，歌曲id" + str(asa) )
            self.ui.label.setText(lyric + ' ' + tlyric)
            self.desktopLyric.set_lyrics(lyric,tlyric)
            self.ui.label.adjustSize()
            # print(res)

#############信息更新
    def update_a(self):
        res1 = requests.get("http://127.0.0.1:27232/player")
        res11 = json.loads(res1.text)
        res111 = res11["currentTrack"]
        res1111 = res111.get("position","")
        allset.ddd = res11["currentTrack"]["id"]
        if res1111 != "" :
            singername = res11["currentTrack"]["artists"][0]
            alname = res11["currentTrack"]["album"]["name"]
            allset.picurl = res11["currentTrack"]["album"]["blurPicUrl"]
        else:
            singername = res11["currentTrack"]["ar"][0]
            alname = res11["currentTrack"]["al"]["name"]
            allset.picurl = res11["currentTrack"]["al"]["picUrl"]
        singername1 = singername.get('name', '')
        name = res111.get('name', '')
        self.ui.label9.setText(self.tr("当前歌曲ID：" )+ str(allset.ddd))
        self.ui.label9.adjustSize()
        self.ui1.label2.setText(name + ' - ' + singername1 + ' - ' + alname )
        self.ui1.label2.adjustSize()

#####读取播放状态
    def updateplayer(self):
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        playerdata = mp.player.Metadata
        data = playerdata
        allset.trackid = data.get('mpris:trackid', '')
        length = data.get('mpris:length', '')#####总时长
        allset.length = data.get('mpris:length', '')#####总时长
        progress = mp.player.Position
        p = str(progress)
        l = str(length)
        progress1 = p[:-6] + '.' + p[-6:]
        length1 = l[:-6] + '.' + l[-6:]
        progress1 = float(progress1)
        length1 = float(length1)
        self.playbackstatus = mp.player.PlaybackStatus
        if  self.playbackstatus == 'Paused' :
              self.playaa = False
        else:
              self.playaa = True
        self.ui1.setrr(progress1,length1)
        self.ui1.bas.play.setPlay(self.playaa)
        # print(self.playaa)

########更新专辑图片
    def update_pic(self):
          if allset.ddd != allset.picl :
              allset.picl = allset.ddd
              # print(picl)
              self.pica()

    def pica(self):
        self.manager = QNetworkAccessManager(self)
        self.request = QNetworkRequest()
        self.request.CacheLoadControl.AlwaysNetwork
        self.request.setUrl(allset.picurl)
        self.reply =  self.manager.get(self.request)
        self.reply.finished.connect(self.handle_image)# 将槽函数连接到响应信号

    def handle_image(self):
        # 从响应中读取数据
        reply = self.sender()
        data = reply.readAll()

        # 创建 QPixmap 并设置给 QLabel
        pixmap = QPixmap()
        pixmap.loadFromData(data)
#        print(pixmap)
        self.ui1.label_pic.setPixmap(pixmap)
        self.ui1.label_pic.setScaledContents(True)

#############歌词显示按钮控制
    def button1(self):
        if self.desktopLyric.isVisible():
          self.ui.button1.setText(self.tr("关闭歌词"))
        else:
            self.ui.button1.setText(self.tr("显示歌词"))
##########下一首控制
    def next1(self):
        global idss
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        mp.player.Next()
#########上一首控制
    def ra(self):
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        mp.player.Previous()
########播放暂停控制
    def playa(self):
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        mp.player.PlayPause()
########获取播放状态
    def plaa(self, position: int):
        append_num = "000000"
        str_num = str(position)
        str_append_num = str(append_num)
        new_str_num = str_num + str_append_num
        new_num = int(new_str_num)
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        mp.player.SetPosition(allset.trackid,new_num)
        self.ui1.bas.progressSlider.setValue(position)
        # print(allset.trackid,new_num)
########设置播放id
    def playerss(self,abc):
        aa = str(abc)
        allset.idss = aa
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        aaa = str(mp.root.Identity)
        self.ui1.label4.setText(aaa)
        self.ui1.label4.adjustSize()
#####歌曲热评获取
    def hotsettime(self):
        time.sleep(0.1)###由于代码执行速度原因添加。
        if allset.song_id != allset.song_id1 :
            self.hotset()

    def hotset(self):
      self.hotget()
      data = []
      comments = allset.new_comments
      for idx, comment in enumerate(comments, 1):
            data1 = {}
            for key, value in comment.items():
                new_key = f"{idx}"
                new_value = value
                data1[new_key] = new_value
            data.append(data1)
      all_keys = self.outkey(data)

      numeric_values = [int(key) for key in all_keys]  # 如果包含浮点数可以使用 float(key) 来转换
      max_numeric = max(numeric_values, default=None)
      min_numeric = min(numeric_values, default=None)
      random_number = random.randint(min_numeric, max_numeric)
      aaaaa = random_number
      for item in allset.new_comments:
          if "username_" + str(aaaaa) in item:
              username = item["username_" + str(aaaaa) ]
              hotcomments = item["hotcomments_" + str(aaaaa) ]
              hotcomment = hotcomments.replace("\n", " ； ")
              self.ui.label12.setText("       " + hotcomment + '\n'+ "         ———— 用户：" + username )

    def outkey(self,content) -> tuple:
        data = content
        # 提取数字的正则表达式
        pattern = r'\d+'

        # 存储提取到的数字
        keys = []

        # 遍历每个字典
        for item in data:
        # 提取键中的数字部分
            match = re.search(pattern, next(iter(item)))
            if match:
              keys.append(int(match.group()))
        return keys


    def hotget(self):
      ######json添加数字
      allset.song_id1 = allset.song_id
      comments = hotComments(allset.song_id,allset.a)
      allset.new_comments = []
      for idx, comment in enumerate(comments, 1):
            allset.new_comment = {}
            for key, value in comment.items():
                new_key = f"{key}_{idx}"
                new_value = value
                allset.new_comment[new_key] = new_value
            allset.new_comments.append(allset.new_comment)


app = QtWidgets.QApplication(sys.argv)
window = Main()
window.show()
# 创建系统托盘图标对象
tray_icon = QSystemTrayIcon()
MyAudioPlayer()
# 创建托盘图标菜单
tray_menu = QMenu()
action_show = QAction("显示应用程序")
lyrics_show = QAction("显示歌词")
action_quit = QAction("退出应用程序")

# 添加菜单项到菜单
tray_menu.addAction(action_show)
tray_menu.addAction(lyrics_show)
tray_menu.addAction(action_quit)

# 将菜单设置到托盘图标
tray_icon.setContextMenu(tray_menu)

# 设置托盘图标的默认图标
default_icon = QIcon("res/icons/GitHub.svg")
tray_icon.setIcon(default_icon)

# 设置托盘图标的鼠标提示
tray_icon.setToolTip("这是一个自定义的系统托盘图标")

def showDialog():
    if window.isVisible():
      title = '退出?'
      content = """这将退出应用。"""
      # w = MessageDialog(title, content, self)   # Win10 style message box
      w = MessageBox(title, content, window)
      if w.exec():
          sys.exit(app.exec())
    else:
      window.show()
      title = '退出?'
      content = """这将退出应用。"""
      # w = MessageDialog(title, content, self)   # Win10 style message box
      w = MessageBox(title, content, window)
      if w.exec():
          sys.exit(app.exec())

def showwindows():
  if window.isVisible():
    MyAudioPlayer.play(MyAudioPlayer)
    title = '应用已经打开了OvO?'
    content = allset.tt
    infobar = InfoBar.info(title, content, duration=4000)
    infobar.setWindowFlags(Qt.FramelessWindowHint)
    _endPos = QPoint(QGuiApplication.primaryScreen().geometry().width() - infobar.width() - 20  ,  QGuiApplication.primaryScreen().geometry().height() - infobar.height() - 70 )
    # 初始化位置到右下角
    infobar.move(_endPos)
    infobar.show()
  else:
    window.show()

def showlyrics():
  if allset.lycl == 1 :
    MyAudioPlayer.play(MyAudioPlayer)
    title = '歌词已经显示了OvO?'
    content = allset.tt
    infobar = InfoBar.info(title, content, duration=4000)
    infobar.setWindowFlags(Qt.FramelessWindowHint)
    _endPos = QPoint(QGuiApplication.primaryScreen().geometry().width() - infobar.width() - 20  ,  QGuiApplication.primaryScreen().geometry().height() - infobar.height() - 70 )
    # 初始化位置到右下角
    infobar.move(_endPos)
    infobar.show()
  else:
    Main.show_desktopLyric(window)
    allset.lycl = 1


# 为退出应用程序添加监听器
action_quit.triggered.connect(showDialog)
# 为显示应用程序添加监听器
action_show.triggered.connect(showwindows)
lyrics_show.triggered.connect(showlyrics)

# 在系统托盘中显示图标
tray_icon.show()

sys.exit(app.exec())
