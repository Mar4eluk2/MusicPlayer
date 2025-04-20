# gui/playlist_view.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                            QListWidgetItem, QComboBox, QLabel, QPushButton)
from PyQt6.QtCore import Qt

class PlaylistView(QWidget):
    """
    Виджет для отображения плейлиста
    """
    def __init__(self, player):
        super().__init__()
        self.__player = player

        self.__setup_ui()
        self.__connect_signals()

        # Обновляем список плейлистов и содержимое текущего плейлиста
        self.update_playlists()
        self.update_playlist()

    def __setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)

        # Выбор плейлиста
        playlist_selector_layout = QHBoxLayout()
        self.__playlist_selector = QComboBox()
        playlist_selector_layout.addWidget(QLabel("Плейлист:"))
        playlist_selector_layout.addWidget(self.__playlist_selector, 1)
        main_layout.addLayout(playlist_selector_layout)

        # Список треков
        self.__track_list = QListWidget()
        main_layout.addWidget(self.__track_list, 1)  # 1 - растягивается при изменении размеров

        # Кнопки управления плейлистом
        playlist_controls_layout = QHBoxLayout()

        self.__add_track_button = QPushButton("Добавить трек")
        self.__remove_track_button = QPushButton("Удалить трек")

        playlist_controls_layout.addWidget(self.__add_track_button)
        playlist_controls_layout.addWidget(self.__remove_track_button)

        main_layout.addLayout(playlist_controls_layout)

    def __connect_signals(self):
        """Подключение сигналов"""
        # При выборе плейлиста
        self.__playlist_selector.currentIndexChanged.connect(self.__on_playlist_changed)

        # При двойном клике на треке
        self.__track_list.itemDoubleClicked.connect(self.__on_track_double_clicked)

        # Кнопки управления плейлистом
        self.__add_track_button.clicked.connect(self.__add_track)
        self.__remove_track_button.clicked.connect(self.__remove_track)

    def update_playlists(self):
        """Обновление списка плейлистов"""
        self.__playlist_selector.clear()

        playlists = self.__player.get_playlists()
        for playlist in playlists:
            self.__playlist_selector.addItem(playlist.name)

        # Устанавливаем текущий плейлист
        current_index = self.__player.get_playlist_manager().get_current_playlist_index()
        if current_index >= 0:
            self.__playlist_selector.setCurrentIndex(current_index)

    def update_playlist(self):
        """Обновление содержимого плейлиста"""
        self.__track_list.clear()

        current_playlist = self.__player.get_current_playlist()
        if current_playlist:
            for track in current_playlist.get_tracks():
                item = QListWidgetItem(f"{track.artist} - {track.title} ({track.get_duration_str()})")
                self.__track_list.addItem(item)

    def __on_playlist_changed(self, index):
        """Обработчик изменения выбранного плейлиста"""
        if index >= 0:
            self.__player.set_current_playlist(index)
            self.update_playlist()

    def __on_track_double_clicked(self, item):
        """Обработчик двойного клика на треке"""
        index = self.__track_list.row(item)
        if index >= 0:
            self.__player.set_track(index)
            self.__player.play()

    def __add_track(self):
        """Добавление трека в плейлист"""
        from PyQt6.QtWidgets import QFileDialog

        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Аудио файлы (*.mp3)")

        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            self.__player.add_tracks(files)
            self.update_playlist()

    def __remove_track(self):
        """Удаление трека из плейлиста"""
        selected_items = self.__track_list.selectedItems()
        if selected_items:
            # Получаем индексы выбранных элементов
            indices = [self.__track_list.row(item) for item in selected_items]

            # Сортируем по убыванию, чтобы удаление не влияло на индексы
            indices.sort(reverse=True)

            # Удаляем треки
            current_playlist = self.__player.get_current_playlist()
            if current_playlist:
                for index in indices:
                    current_playlist.remove_track(index)

                # Обновляем отображение плейлиста
                self.update_playlist()