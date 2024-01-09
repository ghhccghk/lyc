import random
#########对接linux dbus 引用
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import pympris
from PySide6.QtWidgets import QApplication, QMessageBox
import sys

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
if not players_ids:
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText("没有启动任何播放器.")
    msg_box.setInformativeText("即将退出程序.")
    msg_box.setWindowTitle("错误")
    msg_box.exec_()  # 隐藏主窗口
    sys.exit()

picl: str = 0
picurl: str
ddd: str
idss: str = players_ids[0]
trackid: str
length: str
# playaa: str = 0####播放状态指示

####随机数生成
stra = ''
a=stra.join(random.choice("0123456789abcdef") for i in range(32))
song_id: int
song_id1: int = 0

####网易云热评定义变量
new_comments: str

######歌词显示全局通告
lycl: str = 0

tt:str

status1:str
