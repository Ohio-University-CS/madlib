import sys
import logic 
import main 
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QIcon
)

class MadLibApp(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ChatLib")
        self.setGeometry(480, 270, 960, 540)

        # --- Central widget and layout ---
        self.loading_screen = LoadingWidget()
        self.type_words = UserInputScreen()
        self.display = DisplayResultWidget()

        self.setCentralWidget(self.loading_screen) # set the main widget to be the central widget


#Widget to load while AI generating
class LoadingWidget(QFrame):

    def __init__(self):
        super().__init__()
        
        self.loading_screen_layout = QVBoxLayout()
        self.setLayout(self.loading_screen_layout)

        self.generating_label = QLabel("Generating a ChatLib...")
        self.generating_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.generating_label.setStyleSheet("color:black; font-weight: bold;")

        self.loading_screen_layout.addWidget(self.generating_label)

class UserInputScreen(QFrame):
    pass

class DisplayResultWidget(QFrame):
    pass

# MAIN FUNCTION
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MadLibApp()
    window.show()
    sys.exit(app.exec_())
