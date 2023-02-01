import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os


class Actor(QLabel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.image_key = 1
        self.image_url = 'images/'
        self.image = self.image_url + str(self.image_key) + '.png'

    def rightMenuShow(self, pos):
        menu = QMenu(self)
        menu.addAction(QAction(QIcon('images/1.png'), '测试', self, triggered=self.net))
        menu.addAction(QAction(QIcon('images/3.png'), '隐藏', self, triggered=self.hide))
        menu.addAction(QAction(QIcon('images/4.png'), '退出', self, triggered=self.quit))
        menu.exec_(QCursor.pos())

    def gif(self):
        if self.image_key < 4:
            self.image_key += 1
        else:
            self.image_key = 1
        self.image = self.image_url + str(self.image_key) + '-2.png'
        return self.image

    def quit(self):
        self.close()
        sys.exit()

    def hide(self):
        self.setVisible(False)

    def net(self):
        try:
            os.startfile(r'C:\CatFish\CatFish.exe')
        except:
            print('路径不正确')


class TablePet(QWidget):
    def __init__(self):
        super(TablePet, self).__init__()

        self.is_follow_mouse = False
        self.wsize = 200
        self.hsize = 400
        self.xpos = 0
        self.ypos = 0
        self.lead_act = Actor(self)
        self.lead_act.cursor_x = QCursor.pos().x()
        self.lead_act.cursor_y = QCursor.pos().y()
        self.init_actor()
        self.tray()

        # 每隔一段时间执行
        self.gif_timer = QTimer(self)
        self.gif_timer.timeout.connect(self.actor_play)
        self.gif_timer.start(250)
        self._geometry = QRect()
        self.dock_animation = QPropertyAnimation(self, b'geometry')
        self.is_dock = False

    def actor_play(self):
        try:
            pix = QPixmap(self.lead_act.gif())
            self.lead_act.setPixmap(pix)
        except Exception as e:
            print(e)

    def init_actor(self):
        screen = app.primaryScreen().geometry()

        self.setGeometry(screen.width()-self.wsize, screen.height()-self.hsize, screen.width(), screen.height())
        self.resize(self.wsize, self.hsize)

        self.lead_act.setPixmap(QPixmap(self.lead_act.image))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.xpos = self.geometry().x()
            self.ypos = self.geometry().y()
            self.lead_act.cursor_x = QCursor.pos().x()
            self.lead_act.cursor_y = QCursor.pos().y()

            event.accept()
            # self.setCursor(QCursor(Qt.OpenHandCursor))

    def plat_actor(self, dock: bool):
        if self.is_dock == dock:
            return

        if dock:
            self.dock_animation.setStartValue(QRect(self.x(), self.y(), self.width(), self.height()))
            self.dock_animation.setEndValue(QRect(0, self.y(), self.width()/2, self.height()))
        else:
            self.dock_animation.setStartValue(QRect(self.x(), self.y(), self.width(), self.height()))
            self.dock_animation.setEndValue(QRect(10, self.y(), self.width(), self.height()))

        self.dock_animation.setDuration(100)
        self.dock_animation.start()
        self.is_dock = dock

    def mouseMoveEvent(self, event):
        delta_x = QCursor.pos().x() - self.lead_act.cursor_x
        delta_y = QCursor.pos().y() - self.lead_act.cursor_y

        xpos = delta_x + self.xpos
        ypos = delta_y + self.ypos
        screen = QApplication.primaryScreen().geometry()
        if xpos > screen.width() - self.width():
            xpos = screen.width() - self.width()
            self.plat_actor(False)
        elif xpos < 10:
            self.plat_actor(True)
            xpos = 0
        elif xpos < 0:
            xpos = 0

        if ypos > screen.height() - self.height():
            ypos = screen.height() - self.height()
        elif ypos < 0:
            ypos = 0

        self.move(xpos, ypos)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 系统托盘
    def tray(self):
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon("images/4-2.png"))
        tray.activated.connect(self.display)

        _display = QAction(QIcon('images/1.png'), '显示', self, triggered=self.display)
        _quit = QAction(QIcon('images/2.png'), '退出', self, triggered=self.quit)
        menu = QMenu(self)
        menu.addAction(_quit)
        menu.addAction(_display)
        tray.setContextMenu(menu)

        tray.show()

    def quit(self):
        self.close()
        self.gif_timer.stop()
        QApplication.instance().quit()

    def hide(self):
        self.lead_act.setVisible(False)

    def display(self):
        self.lead_act.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = TablePet()
    sys.exit(app.exec_())
