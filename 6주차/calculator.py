# calculator.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mars Calculator')
        self.setGeometry(100, 100, 300, 400)
        self.init_ui()

    def init_ui(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(50)

        grid = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row in range(5):
            for col in range(len(buttons[row])):
                text = buttons[row][col]
                button = QPushButton(text)
                button.setFixedSize(60, 60)
                button.clicked.connect(self.button_clicked)
                if text == '0':
                    grid.addWidget(button, row, 0, 1, 2)
                elif text == '.' and row == 4:
                    grid.addWidget(button, row, 2)
                elif text == '=' and row == 4:
                    grid.addWidget(button, row, 3)
                else:
                    grid.addWidget(button, row, col)

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        self.setLayout(layout)

    def button_clicked(self):
        clicked_button = self.sender()
        current_text = self.display.text()
        button_value = clicked_button.text()

        if button_value == 'AC':
            self.display.setText('')
        else:
            self.display.setText(current_text + button_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
