from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale,QPointF, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame


from qframelesswindow import AcrylicWindow
from qfluentwidgets import PushButton,ComboBox,VBoxLayout, setTheme, Theme, setThemeColor, setFont, ExpandLayout,SpinBox,SwitchButton, Theme, FluentIcon,ToolButton,ScrollArea,CheckBox
from qfluentwidgets.multimedia import MediaPlayBarButton
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase
from qfluentwidgets.components.widgets.label import CaptionLabel

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
        self.label2.move(295, 275)
        self.label2.setFont(afont)##修改字体
############################在顶部无需移动
        self.label3 = QtWidgets.QLabel(self.tr("歌词未显示"), self)
        self.label3.move(125, 60)
        self.label3.setFont(afont)##修改字体

        self.label4 = QtWidgets.QLabel(self.tr("歌词效果查看"), self)
        self.label4.move(25, 60)
        self.label4.setFont(afont)##修改字体
#############################在顶部无需移动
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
        self.label8.move(25, 440)
        self.label8.setFont(afont)##修改字体

        self.label9 = QtWidgets.QLabel(self.tr("歌曲id："), self)
        self.label9.move(299, 440)
        self.label9.setFont(afont)##修改字体

        self.label10 = QtWidgets.QLabel(self.tr("Tips：修改置顶会显示歌词"), self)
        self.label10.move(300, 355)
        self.label10.setFont(afont)##修改字体

        self.label11 = QtWidgets.QLabel(self.tr("当前歌曲网易云热评："), self)
        self.label11.move(25, 470)
        self.label11.setFont(afont)##修改字体

        self.label12 = QtWidgets.QLabel(self.tr("       热评"), self)
        self.label12.move(25, 500)
        self.label12.setFont(afont)##修改字体
        self.label12.setFixedSize(465, self.label12.heightForWidth(465))
        self.label12.setMaximumWidth(465)
        self.label12.setAlignment(Qt.AlignHCenter)
        self.label12.setWordWrap(True)
        self.label12.setFixedHeight(200)

############字号修改控制
        # 创建一个DoubleSpinBox对象
        self.pointSize = SpinBox(self)
        self.pointSize.move(295, 300)
        self.pointSize.setRange(1,99)
        self.pointSize.setSuffix("  px")
        self.pointSize.setValue(20)
        self.pointSize.setSingleStep(1)
        self.pointSize.setWrapping(True)
########字体加粗控制
        self.switchbold = SwitchButton(self)
        self.switchbold.move(25, 400)
        self.switchbold.setChecked(True)####默认加粗
        self.switchbold.setOnText(self.tr('加粗'))
        self.switchbold.setOffText(self.tr('加粗'))
        self.switchbold.setFont(afont)
##########字体下划线控制ToolButton
        self.switchunderline = SwitchButton(self)
        self.switchunderline.move(125, 400)
        self.switchunderline.setChecked(False)####默认加粗
        self.switchunderline.setOnText(self.tr('下划线'))
        self.switchunderline.setOffText(self.tr('下划线'))
        self.switchunderline.setFont(afont)
#########字体颜色控制
        self.button2 = PushButton(self.tr("颜色设置"), self)
        self.button2.move(110, 350)

#############
        self.ismoving = SwitchButton(self)
        self.ismoving.move(240, 400)
        self.ismoving.setChecked(True)####默认加粗
        self.ismoving.setOnText(self.tr('歌词可移动'))
        self.ismoving.setOffText(self.tr('歌词不可移动'))
        self.ismoving.checkedChanged.connect(self.ismov)
        self.ismoving.setChecked(True)


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
        self.button1.move(25, 350)

        self.CheckBox1 = CheckBox(self.tr("置顶歌词"), self)
        self.CheckBox1.move(203, 355)
        self.CheckBox1.setFont(afont)

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


