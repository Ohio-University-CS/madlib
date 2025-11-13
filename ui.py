import sys
from logic import (
    extract_placeholders,
    initialize_input_queue,
    add_user_input,
    fill_story
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QIcon
)

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit
)
from collections import deque

from logic import (
    extract_placeholders,
    initialize_input_queue,
    add_user_input,
    fill_story
)
class MadLibsWindow(QWidget):
    def init(self, ai_text):
        super().init()

        self.ai_text = ai_text
        self.placeholders = extract_placeholders(ai_text)
        self.user_inputs = initialize_input_queue(len(self.placeholders))

        self.input_fields = []   # list of QLineEdit widgets

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Show the template text
        layout.addWidget(QLabel("MadLib Template:"))
        self.template_label = QLabel(self.ai_text)
        layout.addWidget(self.template_label)

        # Create input boxes based on placeholders
        layout.addWidget(QLabel("Fill in the blanks:"))

        for token in self.placeholders:
            label = QLabel(f"{token}:")
            field = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(field)

            self.input_fields.append(field)

        # Submit button
        submit_btn = QPushButton("Generate Story")
        submit_btn.clicked.connect(self.generate_story)
        layout.addWidget(submit_btn)

        # Output
        self.output_box = QTextEdit()
        layout.addWidget(self.output_box)

        self.setLayout(layout)

# -----------------------------------------------------------
# READ INPUT FIELDS → PUSH INTO user_inputs QUEUE
# -----------------------------------------------------------
def generate_story(self):
    """
    Read each QLineEdit, push value into user_inputs queue,
    then fill the story.
    """
    # Empty the queue so we can refill it
    self.user_inputs = deque()

    # Read UI fields and push into queue in correct order
    for field in self.input_fields:
        value = field.text()
        self.user_inputs.append(value)

    # Make a copy because fill_story consumes queues
    filled_story = fill_story(
        self.ai_text,
        deque(self.placeholders),
        deque(self.user_inputs)
    )

    # Display
    self.output_box.setText(filled_story)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example AI text (in real usage you will call Gemini here)
    ai_output = (
        "Today I went to the {place} to meet a {adjective} {animal}. "
        "We decided to {verb} together."
    )

    window = MadLibsWindow(ai_output)
    window.show()

    sys.exit(app.exec())