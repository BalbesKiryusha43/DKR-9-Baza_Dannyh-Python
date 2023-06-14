import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem, QAction, QDialog, QDialogButtonBox


class EditUserDialog(QDialog):
    def __init__(self, user_id, name, surname, user_group, parent=None):
        super().__init__(parent)

        self.user_id = user_id

        # Создание меток и полей для ввода имени, фамилии и группы пользователя
        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.name_input.setText(name)

        self.surname_label = QLabel("Фамилия:")
        self.surname_input = QLineEdit()
        self.surname_input.setText(surname)

        self.group_label = QLabel("Группа:")
        self.group_input = QLineEdit()
        self.group_input.setText(user_group)

        # Установка названия окна
        self.setWindowTitle("Редактор")

        # Создание горизонтального компоновщика для меток и полей ввода
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(self.surname_label)
        self.layout.addWidget(self.surname_input)

        self.layout.addWidget(self.group_label)
        self.layout.addWidget(self.group_input)

        # Создание кнопок "Сохранить" и "Отмена"
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Изменение текста кнопок на русский язык
        self.save_button = self.button_box.button(QDialogButtonBox.Save)
        self.save_button.setText("Сохранить")
        self.cancel_button = self.button_box.button(QDialogButtonBox.Cancel)
        self.cancel_button.setText("Отмена")

        # Добавление компоновщика и кнопок в диалоговое окно
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_user_data(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        user_group = self.group_input.text().strip()
        return name, surname, user_group


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Инициализация графического интерфейса
        self.init_ui()

        # Инициализация базы данных
        self.init_db()

        # Создание базы данных
        self.create_database()

    def init_ui(self):
        # Создание главного виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создание вертикального компоновщика для центрального виджета
        self.layout = QVBoxLayout(self.central_widget)

        # Создание меток и полей для ввода имени, фамилии и группы пользователя
        self.name_label = QLabel("Имя студента:")
        self.name_input = QLineEdit()

        self.surname_label = QLabel("Фамилия студента:")
        self.surname_input = QLineEdit()

        self.group_label = QLabel("Группа:")
        self.group_input = QLineEdit()

        # Создание горизонтального компоновщика для меток и полей ввода
        self.name_layout = QHBoxLayout()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_input)

        self.name_layout.addWidget(self.surname_label)
        self.name_layout.addWidget(self.surname_input)

        self.name_layout.addWidget(self.group_label)
        self.name_layout.addWidget(self.group_input)

        # Создание кнопок для добавления, редактирования и удаления пользователей
        self.add_button = QPushButton("Добавить студента")
        self.edit_button = QPushButton("Редактировать студента")
        self.delete_button = QPushButton("Отчислить студента")

        # Подключение кнопок к соответствующим функциям
        self.add_button.clicked.connect(self.add_user)
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button.clicked.connect(self.delete_user)

        # Создание списка пользователей
        self.user_list = QListWidget()

        # Добавление компоновщиков и кнопок в центральный виджет
        self.layout.addLayout(self.name_layout)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.user_list)
        self.layout.addWidget(self.delete_button)

        # Создание действия для кнопки "Выход"
        exit_action = QAction(QIcon("exit.png"), "Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        # Создание меню
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(exit_action)

        # Установка заголовка окна и размеров
        self.setWindowTitle("Список студентов")
        self.setGeometry(100, 100, 400, 300)

    def init_db(self):
        # Инициализация базы данных SQLite
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database.db")
        if not self.db.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных")
            sys.exit(1)

    def add_user(self):
        # Получение имени, фамилии и группы пользователя из полей ввода
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        user_group = self.group_input.text().strip()

        if name and surname and user_group:
            # Вставка нового пользователя в базу данных
            query = QSqlQuery()
            query.prepare("INSERT INTO users (name, surname, user_group) VALUES (:name, :surname, :user_group)")
            query.bindValue(":name", name)
            query.bindValue(":surname", surname)
            query.bindValue(":user_group", user_group)
            if query.exec_():
                # Очистка полей ввода
                self.name_input.clear()
                self.surname_input.clear()
                self.group_input.clear()

                # Обновление информации о пользователях
                self.show_users()
                self.user_list.sortItems()
            else:
                QMessageBox.warning(self, "Предупреждение", "Не удалось добавить студента")
        else:
            QMessageBox.warning(self, "Предупреждение", "Введите имя, фамилию и группу студента")

    def edit_user(self):
        # Получение выбранного пользователя из списка
        selected_item = self.user_list.currentItem()

        if selected_item:
            selected_id = selected_item.data(32)
            query = QSqlQuery()
            query.prepare("SELECT * FROM users WHERE id = :id")
            query.bindValue(":id", selected_id)
            if query.exec_() and query.next():
                name = query.value(1)
                surname = query.value(2)
                user_group = query.value(3)

                # Создание диалогового окна для редактирования пользователя
                dialog = EditUserDialog(selected_id, name, surname, user_group, parent=self)
                if dialog.exec_() == QDialog.Accepted:
                    new_name, new_surname, new_user_group = dialog.get_user_data()

                    # Обновление информации о пользователе в базе данных
                    update_query = QSqlQuery()
                    update_query.prepare("UPDATE users SET name = :name, surname = :surname, user_group = :user_group WHERE id = :id")
                    update_query.bindValue(":name", new_name)
                    update_query.bindValue(":surname", new_surname)
                    update_query.bindValue(":user_group", new_user_group)
                    update_query.bindValue(":id", selected_id)
                    if update_query.exec_():
                        # Обновление информации о пользователях
                        self.show_users()
                        self.user_list.sortItems()
                    else:
                        QMessageBox.warning(self, "Предупреждение", "Не удалось обновить информацию о студенте")
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите студента для редактирования")

    def delete_user(self):
        # Получение выбранных пользователей из списка
        selected_items = self.user_list.selectedItems()

        if selected_items:
            # Удаление выбранных пользователей из базы данных
            for item in selected_items:
                selected_id = item.data(32)
                query = QSqlQuery()
                query.prepare("DELETE FROM users WHERE id = ?")
                query.addBindValue(selected_id)
                query.exec_()

            # Обновление информации о пользователях
            self.show_users()
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите студента для отчисления")

    def show_users(self):
        # Очистка списка пользователей
        self.user_list.clear()

        # Получение списка пользователей из базы данных
        query = QSqlQuery()
        query.exec_("SELECT * FROM users ORDER BY user_group")

        # Отображение информации о пользователях
        while query.next():
            id = query.value(0)
            name = query.value(1)
            surname = query.value(2)
            user_group = query.value(3)
            item = QListWidgetItem(f"ID: {id}, Имя: {name}, Фамилия: {surname}, Группа: {user_group}")
            item.setData(32, id)
            self.user_list.addItem(item)

    def create_database(self):
        query = QSqlQuery()
        query.exec_("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                user_group TEXT
            )
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.show_users()
    sys.exit(app.exec())
