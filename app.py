import os
import sys
from PyQt5 import QtWidgets
import resume_func as rf


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Обработка резюме")

        # Папка с резюме
        self.resume_folder_path = ""
        self.resume_folder_label = QtWidgets.QLabel("Папка с резюме:")
        self.resume_folder_edit = QtWidgets.QLineEdit()
        self.resume_folder_button = QtWidgets.QPushButton("...")
        self.resume_folder_button.clicked.connect(self.select_resume_folder)

        # Папка для сохранения
        self.save_folder_path = ""
        self.save_folder_label = QtWidgets.QLabel("Папка для сохранения:")
        self.save_folder_edit = QtWidgets.QLineEdit()
        self.save_folder_button = QtWidgets.QPushButton("...")
        self.save_folder_button.clicked.connect(self.select_save_folder)

        # Кнопка старт
        self.start_button = QtWidgets.QPushButton("Старт")
        self.start_button.clicked.connect(self.start_processing)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.resume_folder_label)
        layout.addWidget(self.resume_folder_edit)
        layout.addWidget(self.resume_folder_button)
        layout.addWidget(self.save_folder_label)
        layout.addWidget(self.save_folder_edit)
        layout.addWidget(self.save_folder_button)
        layout.addWidget(self.start_button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def select_resume_folder(self):
        self.resume_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку с резюме")
        self.resume_folder_edit.setText(self.resume_folder_path)

    def select_save_folder(self):
        self.save_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        self.save_folder_edit.setText(self.save_folder_path)

    def start_processing(self):
        print("Обработка резюме...")
        print(f"Папка с резюме: {self.resume_folder_path}")
        print(f"Папка для сохранения: {self.save_folder_path}")
        print("Сохранение результатов...")

        # TODO: Реализовать обработку резюме в файле resume_func.py
        for file in os.listdir(self.resume_folder_path):
            rf.process_resume(file)

        self.show_success_message()

    def show_success_message(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle("Успешно!")
        message_box.setText("Обработка резюме успешно завершена!")
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        message_box.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
