from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame, QSpacerItem, QSizePolicy


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
        self.label0.move(50, 20)
        # self.label0.setFont(afont)
        ######针对会变动的文字修改保证修改语言后不会文字叠一起
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(50, 80, 851, 23))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.label1 = QtWidgets.QLabel(self.tr("当前播放："),self.horizontalLayoutWidget)
        self.label1.setFont(afont)

        self.label2 = QtWidgets.QLabel(self.tr("显示播放歌手和歌曲名"),self.horizontalLayoutWidget)
        self.label2.setFont(afont)
        self.horizontalLayout.addWidget(self.label1)
        self.horizontalLayout.addWidget(self.label2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)
#########################################

        self.label3 = QtWidgets.QLabel(self.tr('设置播放器为:'), self)
        # self.label3.move(125, 570)
        self.label3.setFont(afont)

        self.label4 = QtWidgets.QLabel('播放器名字',self)
        # self.label4.move(230, 570)
        self.label4.setFont(afont)
#######专辑封面
        self.label_pic = QLabel(self)
        # self.label_pic.setGeometry(QRect(95, 135, 300, 300))
        self.label_pic.setMaximumSize(300, 300)
        self.label_pic.setFrameShape(QFrame.NoFrame)
        image = QPixmap(os.path.join(basedir, "../res/icons/108.png"))
        self.label_pic.setPixmap(image)
        self.label_pic.setScaledContents(True)
#######播放器选择
        self.combo_box = ComboBox(self)
        # self.combo_box.move(130, 600)
        # self.combo_box.resize(100, 30)
######刷新播放器状态
        self.button1 = PushButton(self.tr("更新列表"), self)
        # self.button1.move(240, 600)
##########控件
        self.bas = SimpleMediaPlayBar(self)
        # self.bas.move(95, 450)
        # self.bas.resize(300, 250)
#############添加卡片
        self.playcontrolcard = SettingCardGroup(self.horizontalLayoutWidget, self.scrollWidget)
# def __init__(self, label3, label4, label_pic, combo_box, button , bas , parent=None):
        self.card = playWidget(
          self.label3,
          self.label4,
          self.label_pic,
          self.combo_box,
          self.button1,
          self.bas,
          self.playcontrolcard)
        self.card.adjustSize()
        self.__initWidget()

    def __initWidget(self):
        #self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, 95, 0, 20)
        self.setViewportMargins(0, 75, 0, 20)
        self.setWidget(self.scrollWidget)
        #self.scrollWidget.resize(1000, 800)
        self.setWidgetResizable(True)

        # # initialize style sheet
        self.__setQss()

        # initialize layout
        self.__initLayout()
        #self.__connectSignalToSlot()

    def __initLayout(self):
        self.playcontrolcard.addSettingCard(self.card)
        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.playcontrolcard)

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

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.label0.setObjectName('settingLabel')

        theme = 'light' #if isDarkTheme() else 'light'
        with open(os.path.join(basedir, '../res/icons/system/qss/', theme, 'setting_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())


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

from typing import List
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qfluentwidgets.common.font import setFont


class SettingCardGroup(QWidget):
    """ Setting card group """

    def __init__(self,card: QWidget,parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = ExpandLayout()

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSpacing(0)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)
        self.cardLayout.setSpacing(2)

        self.vBoxLayout.addWidget(card)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addLayout(self.cardLayout, 1)

        FluentStyleSheet.SETTING_CARD_GROUP.apply(self)


    def addSettingCard(self, card: QWidget):
        """ add setting card to group """
        card.setParent(self)
        self.cardLayout.addWidget(card)
        self.adjustSize()

    def addSettingCards(self, cards: List[QWidget]):
        """ add setting cards to group """
        for card in cards:
            self.addSettingCard(card)

    def adjustSize(self):
        h = self.cardLayout.heightForWidth(self.width()) + 46
        return self.resize(self.width(), h)

####播放界面

#
#         self.label3 = QtWidgets.QLabel(self.tr('设置播放器为:'), self)
#         self.label3.move(125, 570)
#         self.label3.setFont(afont)
#
#         self.label4 = QtWidgets.QLabel('播放器名字',self)
#         self.label4.move(230, 570)
#         self.label4.setFont(afont)
# #######专辑封面
#         self.label_pic = QLabel(self)
#         self.label_pic.setGeometry(QRect(95, 135, 300, 300))
#         self.label_pic.setFrameShape(QFrame.NoFrame)
#         image = QPixmap(os.path.join(basedir, "../res/icons/108.png"))
#         self.label_pic.setPixmap(image)
#         self.label_pic.setScaledContents(True)
# #######播放器选择
#         self.combo_box = ComboBox(self)
#         self.combo_box.move(130, 600)
#         self.combo_box.resize(100, 30)
# ######刷新播放器状态
#         self.button1 = PushButton(self.tr("更新列表"), self)
#         self.button1.move(240, 600)
# ##########控件
#         self.bas = SimpleMediaPlayBar(self)
#         self.bas.move(95, 450)
#         self.bas.resize(300, 250)
class playWidget(QWidget):
    def __init__(self, label3, label4, label_pic, combo_box, button , bas , parent=None):
        super(playWidget, self).__init__(parent)

        # 传入定义的组件
        self.label3 = label3
        self.label4 = label4
        self.label_pic = label_pic
        self.combo_box = combo_box
        self.button = button
        self.bas = bas

        # 设置布局
        layout = QHBoxLayout(self)
        ####设置播放器文字
        setplaytxtlayout = QHBoxLayout()
        setplaytxtlayout.addStretch()
        setplaytxtlayout.addWidget(self.label3)
        setplaytxtlayout.addWidget(self.label4)
        setplaytxtlayout.addStretch()

        ###设置播放器按钮
        setplaygetlayout = QHBoxLayout()
        setplaygetlayout.addSpacing(5)
        setplaygetlayout.addWidget(self.combo_box)
        setplaygetlayout.addSpacing(5)
        setplaygetlayout.addWidget(self.button)
        setplaygetlayout.addSpacing(5)

        ####播放器控件
        setplaylayout = QHBoxLayout()
        setplaylayout.addWidget(self.bas)


        # 添加图片左侧的水平伸缩
        layout.addStretch()

        # 创建垂直布局用于放置名称和简介以及上下伸缩
        info_layout = QVBoxLayout()
        info_layout.addSpacing(55) # 添加顶部垂直伸缩
        info_layout.addLayout(setplaytxtlayout)
        info_layout.addSpacing(10)
        info_layout.addLayout(setplaygetlayout)
        info_layout.addStretch()  # 添加底部垂直伸缩
        info_layout.addLayout(setplaylayout)

        layout.addWidget(self.label_pic)
        layout.addSpacing(30)
        layout.addLayout(info_layout)
        # 添加图片右侧的水平伸缩
        layout.addStretch()



