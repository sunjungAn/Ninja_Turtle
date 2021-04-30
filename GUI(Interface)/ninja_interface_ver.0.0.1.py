import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QMainWindow, QDesktopWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):  # 가운데로 창이 뜨게함
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def initUI(self):
        btn1 = QPushButton('Quit', self) #창 종료 버튼
        btn1.move(50,430)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(QCoreApplication.instance().quit)

        btn2 = QPushButton('Start', self) #기능 실행 버튼
        btn2.move(330, 430)
        btn2.resize(btn2.sizeHint())
        btn2.setCheckable(True)
        btn2.toggle()
        btn2.clicked.connect(PageTwo)

        btn3 = QPushButton('Info', self) #정보 창 실행
        btn3.move(200, 430)
        btn3.resize(btn3.sizeHint())


        self.statusBar().showMessage('Main Page') #상태바
        self.setGeometry(500, 500, 500, 500) # x, y, height, width
        self.setWindowTitle("Ninja_Turtle")
        #self.setWindowIcon(QIcon("images/letter-s.png")) 아이콘 설정
        self.center() #창을 가운데로
        self.show()


class PageTwo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        def initUI(self):

            self.statusBar().showMessage('PageTwo')  # 상태바
            self.setGeometry(500, 500, 500, 500)  # x, y, height, width
            self.setWindowTitle("Ninja_Turtle")
            # self.setWindowIcon(QIcon("images/letter-s.png")) 아이콘 설정
            self.show()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
