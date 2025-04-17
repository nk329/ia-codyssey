# calculator.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mars Calculator')
        self.setFixedSize(320, 480)
        self.init_ui()

    def init_ui(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Arial', 32))
        self.display.setStyleSheet('background-color: black; color: white; border: none;')
        self.display.setFixedHeight(80)

        grid = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row in range(len(buttons)):
            for col in range(len(buttons[row])):
                text = buttons[row][col]
                button = QPushButton(text)
                button.setFont(QFont('Arial', 18))
                button.setFixedSize(70, 70)

                # 스타일 지정
                if text in ['AC', '+/-', '%']:
                    button.setStyleSheet('background-color: #a5a5a5; color: black; border-radius: 35px;')
                elif text in ['÷', '×', '-', '+', '=']:
                    button.setStyleSheet('background-color: #ff9500; color: white; border-radius: 35px;')
                else:
                    button.setStyleSheet('background-color: #333333; color: white; border-radius: 35px;')

                button.clicked.connect(self.button_clicked)

                if text == '0':
                    grid.addWidget(button, row, 0, 1, 2)
                elif text == '.' and row == 4:
                    grid.addWidget(button, row, 2)
                elif text == '=' and row == 4:
                    grid.addWidget(button, row, 3)
                else:
                    if text != '0':
                        grid.addWidget(button, row, col)

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        self.setLayout(layout)
        self.setStyleSheet('background-color: black;')

    def button_clicked(self):
        clicked_button = self.sender()
        current_text = self.display.text()
        button_value = clicked_button.text()

        if button_value == 'AC':
            self.display.setText('')
        elif button_value == '+/-':
            if current_text:
                try:
                    if current_text.startswith('-'):
                        self.display.setText(current_text[1:])
                    else:
                        self.display.setText('-' + current_text)
                except Exception:
                    self.display.setText('Error')
        elif button_value == '%':
            try:
                result = str(eval(current_text) / 100)
                self.display.setText(result)
            except Exception:
                self.display.setText('Error')
        elif button_value == '=':
            try:
                expression = current_text.replace('×', '*').replace('÷', '/')
                result = str(eval(expression))
                self.display.setText(result)
            except Exception:
                self.display.setText('Error')
        else:
            self.display.setText(current_text + button_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
