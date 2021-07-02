from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
#import os.path
import traceback, sys
import os

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow, self).__init__(*args,*kwargs)
        self.setWindowTitle("Terhuchu MENU")


        titleText = QLabel()
        titleText.setText("Terhuchu")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Impact',32))

        self.subtitleText = QLabel()
        self.subtitleText.setText("Select a game mode")
        self.subtitleText.setAlignment(Qt.AlignCenter)
        self.subtitleText.setFont(QFont('Impact',20))



        self.messageFromFileButton = QFileDialog()
        self.keyFromFileButton = QFileDialog()

        PlayerButton = QPushButton()
        PlayerButton.setText("Player vs Player")
        PlayerButton.clicked.connect(self.PlayerClicked)

        MinimaxButton = QPushButton()
        MinimaxButton.setText("Player vs AI (Minimax)")
        MinimaxButton.clicked.connect(self.MinimaxClicked)

        MCTSButton = QPushButton()
        MCTSButton.setText("Player vs AI (MCTS)")
        MCTSButton.clicked.connect(self.MCTSClicked)

        buttonsLayout = QVBoxLayout()
        buttonsLayout.addWidget(PlayerButton)
        buttonsLayout.addWidget(MinimaxButton)
        buttonsLayout.addWidget(MCTSButton)
        buttonsLayoutW = QWidget()
        buttonsLayoutW.setLayout(buttonsLayout)


        mainMenu = QVBoxLayout()
        #mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(titleText)
        #mainMenu.addWidget(QWidget())
        mainMenu.addWidget(self.subtitleText)
        mainMenu.addWidget(buttonsLayoutW)





        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)

    def PlayerClicked(self):
        os.system('2Players\main.py')
        pass


    def MinimaxClicked(self):
        os.system('1PlayerMinimax\main.py')
        pass

    def MCTSClicked(self):
        os.system('1PlayerMCTS\main.py')
        pass



##################      MAIN
app = QApplication(sys.argv)

window = MainWindow()
window.setFixedSize(400, 650)
window.setStyleSheet("background-color: rgb(245,245,220);")
window.show()

app.exec_()