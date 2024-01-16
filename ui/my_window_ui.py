from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale,QPointF, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame,QSpacerItem, QSizePolicy
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QToolButton, QVBoxLayout, QPushButton

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, HyperlinkCard,InfoBar,
                            ComboBoxSettingCard, ScrollArea, ExpandLayout, InfoBarPosition,SettingCard)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import AcrylicWindow
from qfluentwidgets import PushButton,ComboBox,VBoxLayout, setTheme, Theme, setThemeColor, setFont, ExpandLayout,SpinBox,SwitchButton, Theme, FluentIcon,ToolButton,ScrollArea,CheckBox
from qfluentwidgets.multimedia import MediaPlayBarButton
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase
from qfluentwidgets.components.widgets.label import CaptionLabel
from typing import Union
from qfluentwidgets.components.widgets.switch_button import SwitchButton, IndicatorPosition
from qfluentwidgets.common.icon import FluentIconBase
from qfluentwidgets.common.config import qconfig, isDarkTheme, ConfigItem, OptionsConfigItem

import qfluentwidgets
import os

basedir = os.path.dirname(__file__)

ismoving = True

class MyWindowUI(ScrollArea):
    def __init__(self, sizeHintdb: tuple[int, int], parent=None):
        super().__init__(parent=parent)
        # setting label
#        value = 1
        self.setObjectName("MyWindowUI")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.label = QtWidgets.QLabel(self.tr("初始文字"), self)######显示歌词
        self.label.move(50, 100)
#########界面字体控制
        afont = QFont()
        afont.setFamily("黑体")  # 字体
        afont.setPointSize(11)  # 字体大小
        afont.setBold(True)  # 粗体

        ###文本

        ######针对会变动的文字修改保证修改语言后不会文字叠一起
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(50, 65, 851, 23))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        #########
        self.label8 = QtWidgets.QLabel(self.tr("Tips：如遇歌词显示问题，可提交 Issue,"), self)
        self.label8.move(25, 440)
        self.label8.setFont(afont)##修改字体

        self.label9 = QtWidgets.QLabel(self.tr("歌曲id："), self)
        self.label9.move(299, 440)
        self.label9.setFont(afont)##修改字体

        self.label3 = QtWidgets.QLabel(self.tr("歌词未显示，"), self)
        self.label3.move(125, 60)
        self.label3.setFont(afont)##修改字体

        self.horizontalLayout.addWidget(self.label3)
        self.horizontalLayout.addWidget(self.label8)
        self.horizontalLayout.addWidget(self.label9)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

############################在顶部无需移动
        self.label4 = QtWidgets.QLabel(self.tr("设置"), self)
        self.label4.move(50, 20)
#############################在顶部无需移动

        self.hot = SettingCardGroup(self.tr('当前歌曲网易云热评'), self.scrollWidget)
        self.testcard = hotWidget()
        self.testcard.setMaximumHeight(300)
        # 歌词效果设置 ==============================================================================
        self.setting = SettingCardGroup(self.tr('歌词效果设置'), self.scrollWidget)

        self.fontCard = ComboBoxCard(
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('字体设置'),
            self.tr('设置歌词的字体'),
            self.setting

        )
        # 获取系统中所有的字体
        fonts = QFontDatabase.families()
        # 将字体添加到下拉列表中
        for font in fonts:
            self.fontCard.addItem(font)
            self.fontCard.setCurrentIndex(0)
        #


        self.boldCard = SwitchCard(
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('字体加粗'),
            self.tr('设置歌词是否加粗'),
            # None,
            self.setting,
            # Checked = True,
            OnText = self.tr("已加"),
            OffText = self.tr("未加")

        )
        self.boldCard.setChecked(True)


        self.switchunderlineCard = SwitchCard(
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('字体加下划线'),
            self.tr('设置歌词是否加下划线'),
            # None,
            self.setting,
            # Checked = True,
            OnText = self.tr("已加"),
            OffText = self.tr("未加")
        )
        self.switchunderlineCard.setChecked(False)

        self.setcolorCard = PushCard(
            self.tr('设置字体颜色'),
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('字体颜色'),
            self.tr('修改歌词字体颜色'),
            self.setting
        )


        self.fontsizeCard = SpinBoxCard(
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('字体大小'),
            self.tr('设置歌词字体的大小'),
            self.setting
        )
        self.fontsizeCard.setRange(1,99)
        self.fontsizeCard.setSuffix("  px")
        self.fontsizeCard.setValue(20)
        self.fontsizeCard.setSingleStep(1)
        self.fontsizeCard.setWrapping(True)


        self.showlyctopCard = SwitchCard(
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('歌词置顶'),
            self.tr('设置歌词是否置顶'),
            # None,
            self.setting,
            # Checked = True,
            OnText = self.tr("置顶"),
            OffText = self.tr("未置顶")
        )


        self.showlycCard = PushCard(
            self.tr('显示歌词'),
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('显示歌词'),
            self.tr('设置歌词是否显示在独立窗口'),
            self.setting
        )

        self.__initWidget()
        self.__setQss()


    def __initWidget(self):
        #self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, 95, 0, 20)
        self.setViewportMargins(0, 240, 0, 30)
        self.setWidget(self.scrollWidget)
        #self.scrollWidget.resize(1000, 800)
        self.setWidgetResizable(True)

        # # initialize style sheet
        self.__setQss()

        # initialize layout
        self.__initLayout()
        #self.__connectSignalToSlot()

    def __initLayout(self):
        self.hot.addSettingCard(self.testcard)
        self.setting.addSettingCard(self.fontCard)
        self.setting.addSettingCard(self.setcolorCard)
        self.setting.addSettingCard(self.boldCard)
        self.setting.addSettingCard(self.switchunderlineCard)
        self.setting.addSettingCard(self.fontsizeCard)
        self.setting.addSettingCard(self.showlyctopCard)
        self.setting.addSettingCard(self.showlycCard)


        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        # self.expandLayout.addWidget(self.app_name)
        self.expandLayout.addWidget(self.hot)
        self.expandLayout.addWidget(self.setting)



    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.label4.setObjectName('settingLabel')

        theme = 'light' #if isDarkTheme() else 'light'
        with open(os.path.join(basedir, '../res/icons/system/qss/', theme, 'setting_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def ismov(self, checked):
        global ismoving
        if checked:
            ismoving = True
        else:
            ismoving = False

    def heightForWidth(self, width):
        self.setWordWrap(True)  # 设置 label 可以换行
        height = self.fontMetrics().boundingRect(0, 0, width, 0, self.wordWrap()).height()
        return height


class ComboBoxCard(SettingCard):
    """ Setting card with switch button """

    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                  parent=None,):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget

        OnText: "On"
          设置打开按钮文本
        """

        super().__init__(icon, title, content, parent)
        # self.configItem = configItem
        self.ComboBox = ComboBox()

        # add SpinBox to layout
        self.hBoxLayout.addWidget(self.ComboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.ComboBox.currentTextChanged.connect(self.__oncurrentTextChanged)

    def __oncurrentTextChanged(self, isChecked: str):
        """ switch button checked state changed slot """
        self.currentTextChanged.emit(isChecked)

    def addItem(self, Item: str):
        self.ComboBox.addItem(Item)

    def setCurrentIndex(self, CurrentIndex: int):
        self.ComboBox.setCurrentIndex(CurrentIndex)

class SpinBoxCard(SettingCard):
    """ Setting card with switch button """

    valueChanged = Signal(int)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                  parent=None,):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget

        OnText: "On"
          设置打开按钮文本
        """

        super().__init__(icon, title, content, parent)
        # self.configItem = configItem
        self.SpinBox = SpinBox()

        # add SpinBox to layout
        self.hBoxLayout.addWidget(self.SpinBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.SpinBox.valueChanged.connect(self.__onvalueChanged)

    def __onvalueChanged(self, isChecked: int):
        """ switch button checked state changed slot """
        self.valueChanged.emit(isChecked)

    def setValue(self, Value: int):
        self.SpinBox.setValue(Value)

    def setSuffix(self, Value: str):
        self.SpinBox.setSuffix(Value)

    def setSingleStep(self, SingleStep: int):
        self.SpinBox.setSingleStep(SingleStep)

    def setWrapping(self,Wrapping: bool):
        self.SpinBox.setWrapping(Wrapping)

    def setRange(self,mins: int,miax: int):
        self.SpinBox.setRange(mins,miax)

    def value(self):
        return self.SpinBox.value()

class PushCard(SettingCard):
    """ Setting card with a push button """

    clicked = Signal()

    def __init__(self, text, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        """
        Parameters
        ----------

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.button = QPushButton(text, self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def setText(self,text):
        self.button.setText(text)

class SwitchCard(SettingCard):
    """ Setting card with switch button """

    checkedChanged = Signal(bool)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                  parent=None, OnText = "On",OffText = "Off"):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget

        OnText: "On"
          设置打开按钮文本
        """
        super().__init__(icon, title, content, parent)
        # self.configItem = configItem
        self.switchButton = SwitchButton()
        # self.switchButton.setChecked(Checked)
        self.switchButton.setOnText(OnText)
        self.switchButton.setOffText(OffText)

        #
        # if configItem:
        #     self.setValue(qconfig.get(configItem))
        #     configItem.valueChanged.connect(self.setValue)

        # add switch button to layout
        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.switchButton.checkedChanged.connect(self.__onCheckedChanged)

    def __onCheckedChanged(self, isChecked: bool):
        """ switch button checked state changed slot """
        self.setValue(isChecked)
        self.checkedChanged.emit(isChecked)

    def setValue(self, isChecked: bool):
        # if self.configItem:
        #     qconfig.set(self.configItem, isChecked)

        self.switchButton.setChecked(isChecked)

    def setChecked(self, isChecked: bool):
        self.setValue(isChecked)

    def isChecked(self):
        return self.switchButton.isChecked()

class hotWidget(QWidget):
    def __init__(self, parent=None):
        super(hotWidget, self).__init__(parent)

        # 创建 QLabel 用于热评
        self.name_label = QLabel(self)

        # 设置字体样式
        name_font = QFont()
        name_font.setPointSize(15)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.name_label.setWordWrap(True)
        self.name_label.setText("test 测试文字test")

        # 设置布局
        layout = QHBoxLayout(self)
        # 创建垂直布局用于放置名称和简介以及上下伸缩
        info_layout = QVBoxLayout()
        info_layout.addStretch()  # 添加顶部垂直伸缩
        info_layout.addWidget(self.name_label)
        info_layout.addStretch()  # 添加底部垂直伸缩

        layout.addSpacing(10)
        layout.addLayout(info_layout)
        layout.addSpacing(10)

    def set_hot_content(self, hot):
        self.name_label.setText(hot)

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


    ###歌词滚动 废弃
    def scroll_lyric(self):
        if len(self.lyric1) > 0 and len(self.lyric2) > 0:
            self.lyric1 = self.lyric1[1:] + self.lyric1[0]
            self.lyric2 = self.lyric2[1:] + self.lyric2[0]
            self.setText(self.lyric1 + '\n' + self.lyric2)
        else:
            self.timer.stop()


    ###鼠标行为
    def mousePressEvent(self, e):
        global ismoving
        if e.button() == Qt.LeftButton:
            self.ismoving = ismoving
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        global ismoving
        self.ismoving = ismoving
        if self.ismoving:
            relpos = e.globalPos() - self.start_point  # QPoint 类型可以直接相减
            self.move(self.window_point + relpos)      # 所以说 Qt 真是赞！

    # def mouseReleaseEvent(self, e):
        # self.ismoving = False


