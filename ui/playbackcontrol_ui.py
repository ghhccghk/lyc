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

from module.widget import playWidget,SimpleMediaPlayBar,SettingCardGroup

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
