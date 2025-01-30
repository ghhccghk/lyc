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
from qfluentwidgets import FluentWindow,ColorDialog,FluentIcon,NavigationItemPosition,MessageBox,InfoBar,InfoBarPosition
######
from urllib.parse import urlparse, unquote,urlunparse

import time

#####其他py文件引用
from ui.my_window_ui import MyWindowUI,LyricLabel
from ui.playbackcontrol_ui import playbackcontrol
from ui.aboueInterface_ui import aboueInterface
from ui.audio_see_and_test_ui import audioInterface
from lyrics_backend.interface import getCurrentLyric
import lyrics_backend.interface
from module.hotcomments import hotComments
from module.audio import MyAudioPlayer

#########对接linux dbus 引用
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import pympris

#######全局变量设置
from module import allset

from NeteaseCloudMusic import NeteaseCloudMusicApi, api_help, api_list
import os

# netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
# # netease_cloud_music_api.cookie = "003A959854B58FE9A9730D6A043D0E703F1726CEF413151C220DD56933B2596E4C602D350A23DD64E70339701D36D169E11CDED10A3CDDB9BBA7D55A0D0536D722D2A4C8D61B1295FED3396AC1C0C04A9893DADCCC5EE1B76F7CE518FC9BA82A033179AF074238D6082BD3E50F167B95D9FB158F5AE1322BE74FC266DB4EF0739730141AE8E0E9B06A275BD8D1F852EAF5ED6EE792F4B449CAEBE4FA09F4B67B89F07A860F1E011B2FC6BB12CFDF9F896A786CB041B654146C9431C0980D6447AB9F9B246A3A0B6BE0776632F0CC57148F9174911FE85A2CEB4FBE4F7A096A326721FBF61558482C9E42EDD708D26CF6DCD62CD9D370A5BD348B436E864A8EE18967EAE4D099B205F66FF821280A7689D816D4B1D2E268EADCADB1E298866C05D507489845CC48728886048349BD06B5C4D58D22FE2E25766EF8320B12630E8150601568DE637C5FEE661744D638DDF470"  # 设置cookie， 如果没有cookie需要先登录 具体见example.py
# netease_cloud_music_api.request("register_anonimous", {"keywords":"1"})
# response = netease_cloud_music_api.request("cloudsearch", {"keywords":"海阔天空","limit": "1"})  # 调用API
#
# # 获取帮助
# print(response)
#####默认字体变量
fonta: str = "文泉驿等宽微米黑"  ###字体
bold: bool = True  ####粗细
underline: bool = False #####下划线
pointSize: int = 20.22  ###字号
foncolor: str = "00000000" ####黑色
ids = 0
abc:bool = False
#debug使用
faulthandler.enable()
basedir = os.path.dirname(__file__)

shu:bool = False
loop:str = "None"
class Main(FluentWindow):
    global font,bold,underline,pointSize
    def __init__(self, minWidth=750, minHeight=650):
        super().__init__()
        self.resize(750,650)
        self.ui = MyWindowUI(sizeHintdb=(minWidth, minHeight), parent=self)
        self.ui1 = playbackcontrol(sizeHintdb=(minWidth, minHeight), parent=self)
        self.audioInterface = audioInterface(sizeHintdb=(minWidth, minHeight), parent=self)
        self.aboueInterface = aboueInterface(sizeHintdb=(minWidth, minHeight), parent=self)
##################ui修改
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(os.path.join(basedir,"res/icons/SystemPanel.png")))

        self.initNavigation()
##################功能代码

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.timeout.connect(self.button1)
        self.timer.timeout.connect(self.update_a)
        self.timer.timeout.connect(self.update_pic)
        self.timer.timeout.connect(self.updateplayer)
        self.timer.start(100)  # 每隔100毫秒更新一次

        self.c = QtCore.QTimer(self)
        self.c.timeout.connect(self.hotsettime)
        self.c.start(1000)  # 每隔1000毫秒更新一次



# ########## 字体更新
        self.ui.fontCard.currentTextChanged.connect(self.setfonta)
        self.ui.showlycCard.clicked.connect(self.show_desktopLyric)
        self.ui.fontsizeCard.valueChanged.connect(self.fontsize)
        self.ui.boldCard.checkedChanged.connect(self.setbold)
        self.ui.switchunderlineCard.checkedChanged.connect(self.setunderline)
        self.ui.setcolorCard.clicked.connect(self.showColorDialog)
######### 播放按钮控制
        self.ui1.bas.skipForwardButton.clicked.connect(self.next1)
        self.ui1.bas.skipBackButton.clicked.connect(self.ra)
        self.ui1.bas.play.clicked.connect(self.playa)
        self.ui1.bas.progressSlider.sliderMoved.connect(self.plaa)
        self.ui1.bas.Shuffle.clicked.connect(self.Shuffle1)
        self.ui1.bas.LoopStatus.clicked.connect(self.LoopStatus1)
#########置顶更新
        self.ui.showlyctopCard.checkedChanged.connect(self.on_inTopCheckBox_clicked)
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
            allset.lycl = 1
        else:
            self.desktopLyric.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)# 置顶
            # self.desktopLyric.setWindowFlags(Qt.FramelessWindowHint)
            self.desktopLyric.show()
            allset.lycl = 1


##########侧边栏添加
    def initNavigation(self):
        # add sub interface
        self.addSubInterface(self.ui1,
                             QIcon(os.path.join(basedir, "res/icons/jump.svg")),
                             self.tr('播放控制')
                             )
        self.addSubInterface(self.audioInterface,
                             QIcon(os.path.join(basedir, "res/icons/jump.svg")),
                             self.tr('音频可视化和控制郊狼')
                             )
        self.addSubInterface(self.ui,
                             FluentIcon.SETTING,
                             self.tr('设置'),
                             NavigationItemPosition.BOTTOM
                             )
        self.addSubInterface(self.aboueInterface,
                             FluentIcon.INFO,
                             self.tr('关于'),
                             NavigationItemPosition.BOTTOM
                             )


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

    def fontsize(self):
        global pointSize
        pointSize = int(self.ui.fontsizeCard.value())
#        print(pointSize)
        self.change_font()

    def showColorDialog(self):
        global foncolor
        # print(foncolor)
        colorset = ColorDialog(QColor(foncolor), self.tr('颜色设置'), self.window(),enableAlpha=True)
        colorset.setColor(QColor(foncolor), movePicker=True)
        colorset.colorChanged.connect(lambda c: self.setcolor(c))
        colorset.exec()

    def setcolor(self,c):
        global foncolor
        print(c)
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
##########控制歌词显示代码
    def show_desktopLyric(self):
        self.desktopLyric.set_lyrics(self.tr('这是一首很长的歌词'),self.tr('需要滚动显示'))
        if self.desktopLyric.isVisible():
            self.ui.showlyctopCard.setChecked(False)
            allset.lycl = 0
            self.desktopLyric.close()
        else:
            allset.lycl = 1
            self.desktopLyric.setStyleSheet("color:"+foncolor)
            self.desktopLyric.show()

    def close_desktopLyric(self):
            self.desktopLyric.close()



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
        global abc
        res = lyrics_backend.interface.getCurrentLyric(0)
        lyric = res.get('lyric', '')  # 如果 'lyric' 键不存在，返回空字符串
        tlyric = res.get('tlyric', '') # 如果 'lyric' 键不存在，返回空字符串
        status = res.get('status', '')
        asa = res.get('e', '正常')
        allset.song_id = asa
              ##读取歌词显示情况
        if self.desktopLyric.isVisible():
            self.ui.label3.setText(self.tr("歌词已显示，"))
            # self.ui.label3.adjustSize()
        else:
            self.ui.label3.setText(self.tr("歌词未显示，"))
            # self.ui.label3.adjustSize()
        # if status == 200 :

#        print(singername)
#        print(abc)
 #       print(allset.lyric)
        if allset.lyric != "":
            #print(abc)
            self.ui.label.setText(allset.lyric)
            self.desktopLyric.set_lyrics(allset.lyric,tlyric)
            self.ui.label.adjustSize()
        if abc == False:
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
      global abc
      mp = pympris.MediaPlayer(allset.idss, allset.bus)
      aa = str(mp.root.Identity)
      # print(aa)

      if aa == "YesPlayMusic" :
        res1 = requests.get("http://127.0.0.1:27232/player")
        res11 = json.loads(res1.text)
        res111 = res11["currentTrack"]
        res1111 = res111.get("position","")
        ddd = res11["currentTrack"]["id"]
        if res1111 != "" :
            allset.nolike = True
            self.ui1.bas.like.nolike(allset.nolike)
            singername = res11["currentTrack"]["artists"][0]
            alname = res11["currentTrack"]["album"]["name"]
            # if allset.kdenot:
            #   allset.picurl = res11["currentTrack"]["album"]["blurPicUrl"]
        else:
            allset.nolike = False
            self.ui1.bas.like.nolike(allset.nolike)
            singername = res11["currentTrack"]["ar"][0]
            alname = res11["currentTrack"]["al"]["name"]
            # if allset.kdenot:
            #   allset.picurl = res11["currentTrack"]["al"]["picUrl"]
        singername1 = singername.get('name', '')
        name = res111.get('name', '')
        self.ui.label9.setText(self.tr("当前歌曲ID：" )+ str(ddd))
        # self.ui.label9.adjustSize()
        # self.ui1.label2.setText(name + ' - ' + singername1 + ' - ' + alname )
        # self.ui1.label2.adjustSize()
        abc = False
      else:
          self.ui1.bas.like.nolike(False)
          abc = True
          self.ui.label9.setText(self.tr("不是Yesplaymusic，无法获取歌曲ID" ))

#####读取播放状态
    def updateplayer(self):
        global shu
        global loop
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        playerdata = mp.player.Metadata
        data = playerdata
        allset.trackid = data.get('mpris:trackid', '')
        allset.length = data.get('mpris:length', '')#####总时长
        title = data.get('xesam:title', '')
        album = data.get('xesam:album', '')
        artist = data.get('xesam:artist', '')
        # pid = data.get('mpris:artUrl', '')
        # if pid != '':
        #   allset.kdenot = False
        allset.picurl = data.get('mpris:artUrl', '')
        #   # print(allset.picurl)
        # else:
        #   allset.kdenot = True
        if artist != ['']:
            # print(artist)
            if not artist:
              artist_str = self.tr("无艺术家")
            else:
              artist_str = str(artist[0])
        else:
            artist_str = self.tr("无艺术家")
        if title != "":
            title = str(title)
            if abc == True :
              allset.lyric = title
            else:
              allset.lyric = ""
        else:
            title = self.tr("无标题")
        if album != "":
            album = str(album)
        else:
            album = self.tr("无专辑")
        # print(artist)
        self.ui1.label2.setText(str(title) + ' - ' + artist_str + ' - ' + str(album) )
        progress = mp.player.Position
        p = str(progress)
        l = str(allset.length)
        progress1 = p[:-6] + '.' + p[-6:]
        length1 = l[:-6] + '.' + l[-6:]
        progress1 = float(progress1)
        try:
            length1 = float(length1)
        except ValueError:
            length1 = 0.0  # 或者设为一个默认值
        self.playbackstatus = mp.player.PlaybackStatus
        if  self.playbackstatus == 'Paused' :
              self.playaa = False
        else:
              self.playaa = True
        self.ui1.setrr(progress1,length1)
        self.ui1.bas.play.setPlay(self.playaa)

        # self.LoopStatus = mp.player.LoopStatus
        try:
            self.LoopStatus = mp.player.LoopStatus
        except pympris.common.PyMPRISException as e:
            # 处理异常
            # print(f"错误：{e}")
            self.LoopStatus = "None"
        self.ui1.bas.LoopStatus.setLoopStatus(self.LoopStatus)
        try:
            self.Shuffle = mp.player.Shuffle
        except pympris.common.PyMPRISException as e:
            # 处理异常
            # print(f"错误：{e}")
            self.Shuffle = False
        self.ui1.bas.Shuffle.setShuffle(self.Shuffle)
        shu = self.Shuffle
        loop = self.LoopStatus




        # print(self.playaa)

########更新专辑图片
    def is_local_file(self):
        parsed_url = urlparse(allset.picurl)
        if allset.picurl == "":
          allset.picurl == ""
        else:
          allset.picurl = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, '', ''))

        return parsed_url.scheme == "file"

    def update_pic(self):
          if allset.ddd != allset.picurl :
              allset.ddd = allset.picurl
              # print(allset.picurl)
              self.pica()

    def pica(self):
        if self.is_local_file():
          if allset.picurl == "":
            pixmap = QPixmap(os.path.join(basedir, "res/icons/108.png"))
          else:
            pixmap = QPixmap(os.path.join(unquote(allset.picurl[len("file://"):])))
          # print(unquote(allset.picurl[len("file://"):]))
          self.ui1.label_pic.setPixmap(pixmap)
          self.ui1.label_pic.setScaledContents(True)
        else:
          # print(self.is_local_file())
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


        if allset.picurl == "":
          pixmap = QPixmap(os.path.join(basedir, "res/icons/108.png"))
        else:
          pixmap = QPixmap()
          pixmap.loadFromData(data)
        self.ui1.label_pic.setPixmap(pixmap)
        self.ui1.label_pic.setScaledContents(True)

#############歌词显示按钮控制
    def button1(self):
        if self.desktopLyric.isVisible():
            self.ui.showlycCard.setText(self.tr("关闭歌词"))
        else:
            self.ui.showlycCard.setText(self.tr("显示歌词"))
##########下一首控制
    def next1(self):
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
#########随机播放
    def Shuffle1(self):
        global shu
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        if shu:
            mp.player.Shuffle = bool(False)
        else:
            mp.player.Shuffle = bool(True)
#########列表循环
    def LoopStatus1(self):
        global loop
        mp = pympris.MediaPlayer(allset.idss, allset.bus)
        if loop == "None":
            mp.player.LoopStatus = str("Playlist")
        elif loop == "Playlist":
            mp.player.LoopStatus = str("Track")
        elif loop == "Track":
            mp.player.LoopStatus = str("None")

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
      # print(allset.new_comments)
      for item in allset.new_comments:
          if "username_" + str(aaaaa) in item:
              username = item["username_" + str(aaaaa) ]
              hotcomments = item["hotcomments_" + str(aaaaa) ]
              hotcomment = hotcomments.replace("\n", " ； ")
              # self.ui.label12.setText("       " + hotcomment + '\n'+ "         ———— 用户：" + username )
              self.ui.testcard.set_hot_content("       " + hotcomment + '\n',"———— 用户：" + username )

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
          if allset.lycl == 1 :
            Main.close_desktopLyric(window)
          window.close()
          tray_icon.close()
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
