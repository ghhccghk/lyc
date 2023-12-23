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
from PySide6.QtCore import Qt, QLocale, QObject,Signal,QUrl,QRect
from PySide6.QtGui import QFontDatabase,QFont,QIcon,QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
#######qframelesswindow 引用
from qframelesswindow import AcrylicWindow
from qfluentwidgets import SplitFluentWindow,ColorDialog,FluentIcon,NavigationItemPosition

#####其他py文件引用
from my_window_ui import MyWindowUI,LyricLabel,playbackcontrol,aboueInterface
from lyrics_backend.interface import getCurrentLyric
import lyrics_backend.interface
from hotcomments import hotComments
#########对接linux dbus 引用
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import pympris


#debug使用
#faulthandler.enable()
basedir = os.path.dirname(__file__)


status: int
id: int
lyrics: dict = {}
trans: bool = True
tlyrics: dict = {}
progress: float
currentLyric: str
#####默认字体变量
fonta: str = "文泉驿等宽微米黑"  ###字体
bold: bool = True  ####粗细
underline: bool = False #####下划线
pointSize: int = 20.22  ###字号
foncolor: str = "00000000" ####黑色
ids = 0
#######对接linux dbus控制播放
dbus_loop = DBusGMainLoop()
bus = dbus.SessionBus(mainloop=dbus_loop)
players_ids = list(pympris.available_players())
picl: str = 0
picurl: str
ddd: str
idss: str = players_ids[0]
trackid: str
length: str
playaa: str = 0####播放状态指示

####随机数生成
stra = ''
a=stra.join(random.choice("0123456789abcdef") for i in range(32))
song_id: int
song_id1: int = 0

####网易云热评定义变量
new_comments: str

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

        if players_ids != '' :
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)  # 每隔300毫秒（1秒）更新一次
        if players_ids != '' :
#        self.initWindow()
            self.ab = QtCore.QTimer(self)
            self.ab.timeout.connect(self.button1)
            self.ab.start(100)  # 每隔100毫秒更新一次
        if players_ids != '' :
            self.a = QtCore.QTimer(self)
            self.a.timeout.connect(self.update_a)
            self.a.start(100)  # 每隔100毫秒更新一次
        if players_ids != '' :
            self.b = QtCore.QTimer(self)
            self.b.timeout.connect(self.update_pic)
            self.b.timeout.connect(self.updateplayer)
            self.b.start(100)  # 每隔100毫秒更新一次

        if players_ids != '' :
            self.c = QtCore.QTimer(self)
            self.c.timeout.connect(self.setplayers)
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

        self.desktopLyric = LyricLabel()
        self.change_font()
#        self.update_pic()

#        self.ui1.combo_box.currentTextChanged.connect(self.playerss)
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
            self.desktopLyric.close()
        else:
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
#####歌曲热评获取
    def hotsettime(self):
        global song_id
        global song_id1
        if song_id != song_id1 :
            self.hotset()

    def hotset(self):
      global new_comments
      self.hotget()
      random_number = random.randint(1, 15)
      aaaaa = random_number
      for item in new_comments:
          if "username_" + str(aaaaa) in item:
              username = item["username_" + str(aaaaa) ]
              hotcomments = item["hotcomments_" + str(aaaaa) ]
              hotcomment = hotcomments.replace("\n", " ； ")
              self.ui.label12.setText("       " + hotcomment + '\n'+ "         ———— 用户：" + username )



    def hotget(self):
      global a
      global song_id
      global song_id1
      global new_comments
      song_id1 = song_id
      comments = hotComments(song_id,a)
      new_comments = []
      for idx, comment in enumerate(comments, 1):
            new_comment = {}
            for key, value in comment.items():
                new_key = f"{key}_{idx}"
                new_value = value
                new_comment[new_key] = new_value
            new_comments.append(new_comment)

    def showColorDialog(self):
        w = ColorDialog(Qt.cyan, self.tr('颜色设置'), self.window(),enableAlpha=True)
        w.colorChanged.connect(lambda c: self.setcolor(c))
        w.exec()

# #
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
        global idss
        mp = pympris.MediaPlayer(idss, bus)
        aa = str(mp.root.Identity)
        self.ui1.combo_box.clear()
        self.ui1.combo_box.addItems(list(pympris.available_players()))
        self.ui1.label4.setText(aa)
        self.ui1.label4.adjustSize()

##################歌词更新代码
    def update_label(self):
        global song_id
        res = lyrics_backend.interface.getCurrentLyric(0)
        lyric = res.get('lyric', '')  # 如果 'lyric' 键不存在，返回空字符串
        tlyric = res.get('tlyric', '') # 如果 'lyric' 键不存在，返回空字符串
        status = res.get('status', '')
        asa = res.get('e', '正常')
        song_id = asa
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
            self.ui.label9.setText(self.tr("当前歌曲ID：") + str(asa))
            self.ui.label.adjustSize()
            self.ui.label9.adjustSize()
        else:
            self.ui.label9.setText(self.tr("当前歌曲ID：" )+ str(asa))
            self.ui.label9.adjustSize()
            # self.desktopLyric.set_lyrics("间奏或纯音乐，如遇歌词有但是显示这句话","请提交issue，歌曲id" + str(asa) )
            self.ui.label.setText(lyric + ' ' + tlyric)
            self.desktopLyric.set_lyrics(lyric,tlyric)
            self.ui.label.adjustSize()
            # print(res)

####信息更新
    def update_a(self):
        global picurl
        global ddd
        res1 = requests.get("http://127.0.0.1:27232/player")
        res11 = json.loads(res1.text)
        res111 = res11["currentTrack"]
        res1111 = res111.get("position","")
        ddd = res11["currentTrack"]["id"]
        if res1111 != "" :
            singername = res11["currentTrack"]["artists"][0]
            alname = res11["currentTrack"]["album"]["name"]
            picurl = res11["currentTrack"]["album"]["blurPicUrl"]
        else:
            singername = res11["currentTrack"]["ar"][0]
            alname = res11["currentTrack"]["al"]["name"]
            picurl = res11["currentTrack"]["al"]["picUrl"]
        singername1 = singername.get('name', '')
        name = res111.get('name', '')
        self.ui1.label2.setText(name + ' - ' + singername1 + ' - ' + alname )
        self.ui1.label2.adjustSize()


    def updateplayer(self):
        global trackid
        global length
        global playaa
        global idss
        mp = pympris.MediaPlayer(idss, bus)
        playerdata = mp.player.Metadata
        data = playerdata
        trackid = data.get('mpris:trackid', '')
        length = data.get('mpris:length', '')#####总时长
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


    def update_pic(self):
          global picl
          global ddd
          if ddd != picl :
              picl = ddd
              # print(picl)
              self.pica()

    def pica(self):
        global picurl
        self.manager = QNetworkAccessManager(self)
        self.request = QNetworkRequest()
        self.request.CacheLoadControl.AlwaysNetwork
        self.request.setUrl(picurl)
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

#############
    def button1(self):
        if self.desktopLyric.isVisible():
          self.ui.button1.setText(self.tr("关闭歌词"))
        else:
            self.ui.button1.setText(self.tr("显示歌词"))

    def next1(self):
        global idss
        mp = pympris.MediaPlayer(idss, bus)
        mp.player.Next()

    def ra(self):
        global idss
        mp = pympris.MediaPlayer(idss, bus)
        mp.player.Previous()

    def playa(self):
        global idss
        mp = pympris.MediaPlayer(idss, bus)
        mp.player.PlayPause()

    def plaa(self, position: int):
        global trackid
        global idss
        append_num = "000000"
        str_num = str(position)
        str_append_num = str(append_num)
        new_str_num = str_num + str_append_num
        new_num = int(new_str_num)
        mp = pympris.MediaPlayer(idss, bus)
        mp.player.SetPosition(trackid,new_num)
        self.ui1.bas.progressSlider.setValue(position)
        print(trackid,new_num)

    def playerss(self,abc):
        global idss
        aa = str(abc)
        idss = aa

app = QtWidgets.QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec())
