# gui/main_window.py
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                           QSplitter, QMenuBar, QMenu, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from gui.player_controls import PlayerControls
from gui.playlist_view import PlaylistView

class MainWindow(QMainWindow):
    """
    Главное окно приложения
    """
    def __init__(self, player):
        super().__init__()
        self.__player = player

        self.setWindowTitle("Музыкальный плеер")
        self.setMinimumSize(QSize(800, 600))

        self.__setup_ui()
        self.__setup_menu()
        self.__connect_signals()

    def __setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной виджет и его компоновка
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Создаем разделитель для основной части окна
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Виджет для отображения плейлиста
        self.__playlist_view = PlaylistView(self.__player)

        # Элементы управления плеером
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        self.__player_controls = PlayerControls(self.__player)
        controls_layout.addWidget(self.__player_controls)

        # Добавляем виджеты в разделитель
        splitter.addWidget(self.__playlist_view)
        splitter.addWidget(controls_widget)
        splitter.setSizes([300, 500])  # Начальные размеры областей

        # Добавляем разделитель в основную компоновку
        main_layout.addWidget(splitter)

        # Устанавливаем центральный виджет
        self.setCentralWidget(central_widget)

    def __setup_menu(self):
        """Настройка главного меню"""
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")

        # Пункт "Открыть файл"
        open_file_action = file_menu.addAction("Открыть файл")
        open_file_action.triggered.connect(self.__open_file)

        # Пункт "Открыть папку"
        open_folder_action = file_menu.addAction("Открыть папку")
        open_folder_action.triggered.connect(self.__open_folder)

        file_menu.addSeparator()

        # Пункт "Выход"
        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)

        # Меню "Плейлист"
        playlist_menu = menubar.addMenu("Плейлист")

        # Пункт "Создать плейлист"
        create_playlist_action = playlist_menu.addAction("Создать плейлист")
        create_playlist_action.triggered.connect(self.__create_playlist)

        # Пункт "Удалить плейлист"
        delete_playlist_action = playlist_menu.addAction("Удалить плейлист")
        delete_playlist_action.triggered.connect(self.__delete_playlist)

    def __connect_signals(self):
        """Подключение сигналов"""
        # Здесь можно подключить сигналы от виджетов к слотам
        pass

    def __open_file(self):
        """Обработчик открытия файла"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Аудио файлы (*.mp3)")

        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            self.__player.add_tracks(files)
            self.__playlist_view.update_playlist()

    def __open_folder(self):
        """Обработчик открытия папки"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с музыкой")

        if folder:
            import os
            import glob

            # Получаем все mp3 файлы в выбранной папке
            mp3_files = glob.glob(os.path.join(folder, "*.mp3"))

            if mp3_files:
                self.__player.add_tracks(mp3_files)
                self.__playlist_view.update_playlist()
            else:
                QMessageBox.information(self, "Информация", "В выбранной папке не найдены MP3 файлы.")

    def __create_playlist(self):
        """Обработчик создания плейлиста"""
        from PyQt6.QtWidgets import QInputDialog

        name, ok = QInputDialog.getText(self, "Создание плейлиста", "Введите название плейлиста:")

        if ok and name:
            self.__player.create_playlist(name)
            self.__playlist_view.update_playlists()

    def __delete_playlist(self):
        """Обработчик удаления плейлиста"""
        # Получаем индекс текущего плейлиста
        current_index = self.__player.get_playlist_manager().get_current_playlist_index()

            # Нельзя удалить единственный плейлист
        if len(self.__player.get_playlists()) <= 1:
            QMessageBox.warning(self, "Предупреждение", "Нельзя удалить единственный плейлист.")
            return

        # Подтверждение удаления
        playlist_name = self.__player.get_current_playlist().name
        confirm = QMessageBox.question(self, "Подтверждение",
                                      f"Вы уверены, что хотите удалить плейлист '{playlist_name}'?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            # Используем метод из playlist_manager, а не из player
            self.__player.get_playlist_manager().delete_playlist(current_index)
            self.__playlist_view.update_playlists()
            self.__playlist_view.update_playlist()