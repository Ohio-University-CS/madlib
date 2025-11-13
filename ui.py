import sys
import logic 
import ai
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QScrollArea, QFrame, QLineEdit, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

class AIWorker(QThread):
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            # Always use local generation for now
            result = ai.generate_local_story()
            if result:
                self.finished_signal.emit(result)
            else:
                self.error_signal.emit("Failed to generate story")
        except Exception as e:
            self.error_signal.emit(str(e))

class MadLibApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ChatLib")
        self.setGeometry(480, 270, 960, 540)
        
        # Initialize screens
        self.loading_screen = LoadingWidget()
        self.type_words = UserInputScreen(self)
        self.display = DisplayResultWidget(self)
        
        # Start with loading screen and generate story
        self.setCentralWidget(self.loading_screen)
        self.generate_story()

    def generate_story(self):
        self.worker = AIWorker()
        self.worker.finished_signal.connect(self.on_story_generated)
        self.worker.error_signal.connect(self.on_generation_error)
        self.worker.start()

    def on_story_generated(self, story_template):
        print(f"Generated template: {story_template}")
        self.story_template = story_template
        self.placeholders = logic.extract_placeholders(story_template)
        print(f"Found placeholders: {list(self.placeholders)}")
        
        self.type_words.setup_inputs(self.placeholders)
        self.setCentralWidget(self.type_words)

    def on_generation_error(self, error_msg):
        self.loading_screen.set_error(error_msg)
        # Show error but provide a default story
        QMessageBox.warning(self, "Generation Issue", f"{error_msg}\n\nUsing demo story.")
        default_story = "In a {place}, a {adjective} {noun} decided to {verb}. It was {emotion}!"
        self.on_story_generated(default_story)

    def show_result(self, filled_story):
        self.display.set_story(filled_story)
        self.setCentralWidget(self.display)

class LoadingWidget(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.generating_label = QLabel("Generating a ChatLib...")
        self.generating_label.setAlignment(Qt.AlignCenter)
        self.generating_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        layout.addWidget(self.generating_label)
    
    def set_error(self, error_msg):
        self.generating_label.setText(f"Error: {error_msg}")

class UserInputScreen(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.input_fields = {}  # Dictionary to store input fields
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.title = QLabel("Fill in the blanks!")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.title)
        
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        
        scroll = QScrollArea()
        scroll.setWidget(self.form_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        self.submit_btn = QPushButton("Generate Story")
        self.submit_btn.clicked.connect(self.submit_inputs)
        layout.addWidget(self.submit_btn)
    
    def setup_inputs(self, placeholders):
        # Clear previous inputs
        for i in reversed(range(self.form_layout.count())): 
            widget = self.form_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.input_fields.clear()
        self.placeholders = placeholders
        
        # Use set to get unique placeholders
        unique_placeholders = set(placeholders)
        
        for placeholder in unique_placeholders:
            label = QLabel(placeholder.capitalize() + ":")
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter a {placeholder}")
            self.form_layout.addRow(label, input_field)
            self.input_fields[placeholder] = input_field
    
    def submit_inputs(self):
        try:
            user_inputs = logic.initialize_input_queue(len(self.main_window.placeholders))
            
            # Fill the queue with user inputs in the correct order
            for i, placeholder in enumerate(self.main_window.placeholders):
                input_field = self.input_fields[placeholder]
                value = input_field.text().strip()
                if not value:
                    value = "______"  # Default if empty
                logic.add_user_input(user_inputs, value)
            
            print(f"Placeholders: {list(self.main_window.placeholders)}")
            print(f"User inputs: {list(user_inputs)}")
            
            filled_story = logic.fill_story(
                self.main_window.story_template, 
                self.main_window.placeholders, 
                user_inputs
            )
            
            self.main_window.show_result(filled_story)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate story: {str(e)}")

class DisplayResultWidget(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.title = QLabel("Your MadLib Story!")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.title)
        
        self.story_display = QTextEdit()
        self.story_display.setReadOnly(True)
        self.story_display.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.story_display)
        
        button_layout = QHBoxLayout()
        
        self.new_story_btn = QPushButton("Create New Story")
        self.new_story_btn.clicked.connect(self.new_story)
        button_layout.addWidget(self.new_story_btn)
        
        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(QApplication.quit)
        button_layout.addWidget(self.quit_btn)
        
        layout.addLayout(button_layout)
    
    def set_story(self, story_text):
        self.story_display.setText(story_text)
    
    def new_story(self):
        self.main_window.setCentralWidget(self.main_window.loading_screen)
        self.main_window.generate_story()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MadLibApp()
    window.show()
    sys.exit(app.exec_())