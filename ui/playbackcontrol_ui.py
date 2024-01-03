from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame


from qframelesswindow import AcrylicWindow
from qfluentwidgets import PushButton,ComboBox,VBoxLayout, setTheme, Theme, setThemeColor, setFont, ExpandLayout,SpinBox,SwitchButton, Theme, FluentIcon,ToolButton,ScrollArea,CheckBox
from qfluentwidgets.multimedia import MediaPlayBarButton
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase
from qfluentwidgets.components.widgets.label import CaptionLabel

import os

basedir = os.path.dirname(__file__)


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
        image = QPixmap(os.path.join(basedir, "../res/icons/108.png"))
        self.label_pic.setPixmap(image)
        self.label_pic.setScaledContents(True)

        self.combo_box = ComboBox(self)####qfluentwidgets拿过来魔改
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


####qfluentwidgets拿过来魔改
class SimpleMediaPlayBar(MediaPlayBarBase):
    """ Standard media play bar """

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

        self.skipBackButton = MediaPlayBarButton(QIcon(os.path.join(basedir,"../res/icons/上一首.png")), self)
        self.skipForwardButton = MediaPlayBarButton(QIcon(os.path.join(basedir,"../res/icons/下一首.png")), self)
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



