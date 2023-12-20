from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale,QPointF, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame


from qfluentwidgets import  FluentTranslator,ScrollArea
from qframelesswindow import AcrylicWindow
from qfluentwidgets import setThemeColor
from qfluentwidgets import FluentTranslator,SplitTitleBar,MSFluentWindow,FluentWindow,SplitFluentWindow,PushButton,ComboBox,VBoxLayout, ComboBox, setTheme, Theme, setThemeColor, EditableComboBox, setFont, FluentThemeColor, ExpandLayout,SpinBox,SwitchButton,getIconColor, Theme, FluentIcon,ToolButton
from qfluentwidgets.multimedia import MediaPlayBarButton
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase
from qfluentwidgets.multimedia.media_player import MediaPlayer, MediaPlayerBase
from qfluentwidgets.components.widgets.label import CaptionLabel
import os
from sys import platform

if platform == 'win32':
    basedir = ''
else:
    basedir = os.path.dirname(__file__)

class MyWindowUI(ScrollArea):
    def __init__(self, sizeHintdb: tuple[int, int], parent=None):
        super().__init__(parent=parent)
        # setting label
#        value = 1
        self.setObjectName("MyWindowUI")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.label = QtWidgets.QLabel(self.tr("初始文字"), self)
        self.label.move(25, 100)
#########界面字体控制
        afont = QFont()
        afont.setFamily("黑体")  # 字体
        afont.setPointSize(11)  # 字体大小
        afont.setBold(True)  # 粗体

        ###文本

        self.label1 = QtWidgets.QLabel(self.tr("设置字体"), self)
        self.label1.move(25, 275)
        self.label1.setFont(afont)##修改字体

        self.label2 = QtWidgets.QLabel(self.tr("字体大小设置"), self)
        self.label2.move(25, 417)
        self.label2.setFont(afont)##修改字体

        self.label3 = QtWidgets.QLabel(self.tr("歌词未显示"), self)
        self.label3.move(125, 60)
        self.label3.setFont(afont)##修改字体

        self.label4 = QtWidgets.QLabel(self.tr("歌词效果查看"), self)
        self.label4.move(25, 60)
        self.label4.setFont(afont)##修改字体

#        self.label5 = QtWidgets.QLabel("显示歌手和歌曲名", self)
#        self.label5.move(210, 60)
#        self.label5.setFont(afont)##修改字体
 #       self.label5.adjustSize()

        # self.label6 = QtWidgets.QLabel("歌词加粗", self)
        # self.label6.move(210, 417)
        # self.label6.setFont(afont)##修改字体

        # self.label7 = QtWidgets.QLabel("歌词加下划线", self)
        # self.label7.move(327, 417)
        # self.label7.setFont(afont)##修改字体

        self.label8 = QtWidgets.QLabel(self.tr("Tips：如遇歌词显示问题，可提交 Issue。"), self)
        self.label8.move(25, 490)
        self.label8.setFont(afont)##修改字体

        self.label9 = QtWidgets.QLabel(self.tr("歌曲id："), self)
        self.label9.move(299, 490)
        self.label9.setFont(afont)##修改字体

############字号修改控制
        # 创建一个DoubleSpinBox对象
        self.pointSize = SpinBox(self)
        self.pointSize.move(25, 445)
        self.pointSize.setRange(1,99)
        self.pointSize.setSuffix("  px")
        self.pointSize.setValue(20)
        self.pointSize.setSingleStep(1)
        self.pointSize.setWrapping(True)
########字体加粗控制
        self.switchbold = SwitchButton(self)
        self.switchbold.move(210, 452)
        self.switchbold.setChecked(True)####默认加粗
        self.switchbold.setOnText(self.tr('加粗'))
        self.switchbold.setOffText(self.tr('加粗'))
##########字体下划线控制ToolButton
        self.switchunderline = SwitchButton(self)
        self.switchunderline.move(327, 452)
        self.switchunderline.setChecked(False)####默认加粗
        self.switchunderline.setOnText(self.tr('下划线'))
        self.switchunderline.setOffText(self.tr('下划线'))
#########字体颜色控制
        self.button2 = PushButton(self.tr("颜色设置"), self)
        self.button2.move(110, 360)

        # 创建ComboBox对象
        self.combo_box = ComboBox(self)
        self.combo_box.move(25, 300)
        self.combo_box.resize(240, 30)

        # 获取系统中所有的字体
        fonts = QFontDatabase.families()
        # 将字体添加到下拉列表中
        for font in fonts:
            self.combo_box.addItem(font)
            self.combo_box.setCurrentIndex(0)

        self.button1 = PushButton(self.tr("显示歌词"), self)
        self.button1.move(25, 360)



class playbackcontrol(ScrollArea):
    def __init__(self, sizeHintdb: tuple[int, int], parent=None):
        super().__init__(parent=parent)
        # setting label
        self.setObjectName("playbackcontrol")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)


        afont = QFont()
        afont.setFamily("黑体")  # 字体
        afont.setPointSize(11)  # 字体大小
        afont.setBold(True)  # 粗体

        self.label0 = QtWidgets.QLabel(self.tr("播放控制"), self)
        self.label0.move(25, 60)
        self.label0.setFont(afont)

        self.label1 = QtWidgets.QLabel(self.tr("当前播放："), self)
        self.label1.move(25, 90)
        self.label1.setFont(afont)

        self.label2 = QtWidgets.QLabel(self.tr("显示播放歌手和歌曲名"), self)
        self.label2.move(105, 90)
        self.label2.setFont(afont)

        self.label3 = QtWidgets.QLabel(self.tr('设置播放器为:'), self)
        self.label3.move(125, 570)
        self.label3.setFont(afont)

        self.label4 = QtWidgets.QLabel('播放器名字',self)
        self.label4.move(230, 570)
        self.label4.setFont(afont)

#######专辑封面
        self.label_pic = QLabel(self)
        self.label_pic.setGeometry(QRect(95, 135, 300, 300))
        self.label_pic.setFrameShape(QFrame.NoFrame)
        image = QPixmap(os.path.join(basedir, "res/icons/108.png"))
        self.label_pic.setPixmap(image)
        self.label_pic.setScaledContents(True)

        self.combo_box = ComboBox(self)
        self.combo_box.move(120, 600)
        self.combo_box.resize(240, 30)

#######控件
#        self.button0 = ToolButton(self)
#        self.button0.setIcon(FluentIcon.PLAY)
 #       self.button0.move(220, 500)

        # self.button1 = ToolButton(self)
        # self.button1.setIcon(QIcon(os.path.join(basedir,"res/icons/上一首.png")))
        # self.button1.move(175, 500)

        # self.button2 = ToolButton(self)
        # self.button2.setIcon(QIcon(os.path.join(basedir,"res/icons/下一首.png")))
        # self.button2.move(265, 500)

        self.bas = SimpleMediaPlayBar(self)
        self.bas.move(95, 450)
        self.bas.resize(300, 250)

    def setrr(self, position: int, duration: int):
        self.bas.progressSlider.setValue(position)
        self.bas.progressSlider.setMaximum(duration)
        self.bas.currentTimeLabel.setText(self._formatTime(position))
        self.bas.remainTimeLabel.setText(self._formatTime(duration - position))

    def _formatTime(self, time: int):
        time = int(time)
        s = time % 60
        m = int(time / 60)
        h = int(time / 3600)
        return f'{h}:{m:02}:{s:02}'


class SimpleMediaPlayBar(MediaPlayBarBase):
    """ Standard media play bar """
####qfluentwidgets拿过来魔改
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.timeLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.leftButtonContainer = QWidget()
        self.centerButtonContainer = QWidget()
        self.rightButtonContainer = QWidget()
        self.leftButtonLayout = QHBoxLayout(self.leftButtonContainer)
        self.centerButtonLayout = QHBoxLayout(self.centerButtonContainer)
        self.rightButtonLayout = QHBoxLayout(self.rightButtonContainer)

        self.skipBackButton = MediaPlayBarButton(QIcon(os.path.join(basedir,"res/icons/上一首.png")), self)
        self.skipForwardButton = MediaPlayBarButton(QIcon(os.path.join(basedir,"res/icons/下一首.png")), self)
        self.playButton.deleteLater()
        self.volumeButton.deleteLater()
        self.currentTimeLabel = CaptionLabel('0:00:00', self)
        self.remainTimeLabel = CaptionLabel('0:00:00', self)

        self.__initWidgets()

    def __initWidgets(self):
        self.setFixedHeight(102)
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(5, 9, 5, 9)
        self.vBoxLayout.addWidget(self.progressSlider, 1, Qt.AlignTop)
        self.play = Play(self)

        self.vBoxLayout.addLayout(self.timeLayout)
        self.timeLayout.setContentsMargins(10, 0, 10, 0)
        self.timeLayout.addWidget(self.currentTimeLabel, 0, Qt.AlignLeft)
        self.timeLayout.addWidget(self.remainTimeLabel, 0, Qt.AlignRight)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.leftButtonLayout.setContentsMargins(4, 0, 0, 0)
        self.centerButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.rightButtonLayout.setContentsMargins(0, 0, 4, 0)

        # self.leftButtonLayout.addWidget(self.volumeButton, 0, Qt.AlignLeft)
        self.centerButtonLayout.addWidget(self.skipBackButton)
        self.centerButtonLayout.addWidget(self.play)
        self.centerButtonLayout.addWidget(self.skipForwardButton)

        self.buttonLayout.addWidget(self.leftButtonContainer, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.centerButtonContainer, 0, Qt.AlignHCenter)
        self.buttonLayout.addWidget(self.rightButtonContainer, 0, Qt.AlignRight)
        self.setMediaPlayer(MediaPlayer(self))





class Play(MediaPlayBarButton):
    """ Play button """

    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(14, 14))
        self.setPlay(False)

    def setPlay(self, isPlay: bool):
        if isPlay:
            self.setIcon(FluentIcon.PAUSE)
            self.setToolTip(self.tr('Pause'))
        else:
            self.setIcon(FluentIcon.PLAY)
            self.setToolTip(self.tr('Play'))



class LyricLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.lyric1 = ''
        self.lyric2 = ''
#
    ###读取歌词
    def set_lyrics(self, lyric1, lyric2):
        self.lyric1 = lyric1
        self.lyric2 = lyric2
        self.update_lyric()

    ###歌词显示
    def update_lyric(self):
        self.setAlignment(Qt.AlignCenter)
        if  self.lyric1 == ""  :
            self.setText(" ")
        else:
            self.update_lyric1()

    def update_lyric1(self):
        if  self.lyric2 == ""  :
            self.setText(self.lyric1)
            self.adjustSize()
        else:
            self.setText(self.lyric1+'\n'+ self.lyric2)
            self.adjustSize()

    ###歌词动画 废弃
    def start_scroll_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_lyric)
        self.timer.start(300)


    ###歌词滚动
    def scroll_lyric(self):
        if len(self.lyric1) > 0 and len(self.lyric2) > 0:
            self.lyric1 = self.lyric1[1:] + self.lyric1[0]
            self.lyric2 = self.lyric2[1:] + self.lyric2[0]
            self.setText(self.lyric1 + '\n' + self.lyric2)
        else:
            self.timer.stop()


    ###鼠标行为
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.ismoving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.ismoving:
            relpos = e.globalPos() - self.start_point  # QPoint 类型可以直接相减
            self.move(self.window_point + relpos)      # 所以说 Qt 真是赞！

    def mouseReleaseEvent(self, e):
        self.ismoving = False


