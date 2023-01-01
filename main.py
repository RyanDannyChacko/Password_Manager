import random
import sys
from tkinter import font

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Password Manager")

        # Create the font object
        font = QFont()

        # Set the font family and size
        font.setFamily("Segoe UI")
        font.setPointSize(11)

        # Create widgets
        self.username_label = QLabel("Username or Email:", self)
        self.username_field = QLineEdit(self)
        self.password_label = QLabel("Password (you can generate a strong password by typing the letter G (in caps) in here):", self)
        self.password_field = QLineEdit(self)
        self.save_button = QPushButton("Save", self)
        self.output_field = QTextEdit(self)

        # Set the font of the widgets
        self.username_label.setFont(font)
        self.username_field.setFont(font)
        self.password_label.setFont(font)
        self.password_field.setFont(font)
        self.save_button.setFont(font)
        self.output_field.setFont(font)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_field)
        layout.addWidget(self.save_button)
        layout.addWidget(self.output_field)

        # Set central widget and layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect signals and slots
        self.password_field.textChanged.connect(self.check_password)
        self.save_button.clicked.connect(self.save_username_and_password)

    def check_password(self):
        password = self.password_field.text()
        if password == "G":
            # Open the password length input dialog
            self.password_length_dialog = QDialog(self)
            self.password_length_dialog.setWindowTitle("Password Length")

            # Create widgets
            password_length_label = QLabel("Enter the required length of the password ranging from 8 to 16:", self.password_length_dialog)
            self.password_length_field = QLineEdit(self.password_length_dialog)
            password_length_button = QPushButton("Generate Password", self.password_length_dialog)

            # Set the font of the widgets
            password_length_label.setFont(font)
            self.password_length_field.setFont(font)
            password_length_button.setFont(font)

            # Create layout and add widgets
            layout = QGridLayout()
            layout.addWidget(password_length_label, 0, 0)
            layout.addWidget(self.password_length_field, 0, 1)
            layout.addWidget(password_length_button, 1, 0, 1, 2)

            # Set layout and connect signals and slots
            self.password_length_dialog.setLayout(layout)
            password_length_button.clicked.connect(self.generate_password)

            # Show the dialog
            self.password_length_dialog.show()
        else:
            # Hide the dialog if it is open
            if hasattr(self, "password_length_dialog") and self.password_length_dialog.isVisible():
                self.password_length_dialog.hide()

    def generate_password(self):
        # Generate a strong password
        char_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        password_length = int(self.password_length_field.text())
        if password_length >= 8 and password_length <= 16:
            password = ''
            for len in range(password_length):
                random_char = random.choice(char_seq)
                password += random_char

            list_pass = list(password)
            random.shuffle(list_pass)
            self.password_field.setText(''.join(list_pass))
            self.password_length_dialog.hide()
        else:
            self.output_field.setText("Enter a suitable range")

    def save_username_and_password(self):
        # Get the input values
        username = self.username_field.text()
        password = self.password_field.text()

        # Save the username to a file
        random_number = random.randint(1, 9999)
        with open('usernames/' + str(random_number) + '.txt', 'w', encoding='utf-8') as u:
            u.write('Username or Email: ')
            u.write(username)

        # Save the password to a file
        with open('passwords/' + str(random_number) + '_password' + '.txt', 'w', encoding='utf-8') as p:
            p.write('Password: ')
            p.write(password)

        # Display the output
        self.output_field.setText("Your username was saved to usernames/" + str(random_number) + ".txt\nYour password was saved to passwords/" + str(random_number) + "_password" + ".txt")


if __name__ == "__main__":
    # Create the main window and run the application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
