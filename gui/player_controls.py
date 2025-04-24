# gui/player_controls.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QSlider, QLabel, QStyle)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from io import BytesIO
import datetime

class PlayerControls(QWidget):
    """
    Виджет с элементами управления плеером
    """
    def __init__(self, player):
        super().__init__()
        self.__player = player

        # Таймер для обновления информации о воспроизведении
        self.__update_timer = QTimer(self)
        self.__update_timer.setInterval(500)  # Обновление каждые 500 мс
        self.__update_timer.timeout.connect(self.__update_player_info)

        self.__setup_ui()
        self.__connect_signals()

        # Запускаем таймер
        self.__update_timer.start()

    def __setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)

        # Обложка альбома
        self.__album_cover = QLabel()
        self.__album_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__album_cover.setMinimumSize(200, 200)
        self.__album_cover.setMaximumSize(300, 300)
        main_layout.addWidget(self.__album_cover)

        # Информационная панель
        self.__info_label = QLabel("Нет воспроизведения")
        self.__info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.__info_label)

        # Прогресс воспроизведения
        progress_layout = QHBoxLayout()

        self.__time_label = QLabel("0:00")
        self.__position_slider = QSlider(Qt.Orientation.Horizontal)
        self.__duration_label = QLabel("0:00")

        progress_layout.addWidget(self.__time_label)
        progress_layout.addWidget(self.__position_slider, 1)
        progress_layout.addWidget(self.__duration_label)

        main_layout.addLayout(progress_layout)

        # Кнопки управления
        controls_layout = QHBoxLayout()

        self.__previous_button = QPushButton()
        self.__previous_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward))

        self.__play_button = QPushButton()
        self.__play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

        self.__next_button = QPushButton()
        self.__next_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))

        self.__stop_button = QPushButton()
        self.__stop_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))

        controls_layout.addWidget(self.__previous_button)
        controls_layout.addWidget(self.__play_button)
        controls_layout.addWidget(self.__stop_button)
        controls_layout.addWidget(self.__next_button)

        main_layout.addLayout(controls_layout)

        # Регулятор громкости
        volume_layout = QHBoxLayout()

        volume_label = QLabel("Громкость:")
        self.__volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.__volume_slider.setRange(0, 100)
        self.__volume_slider.setValue(50)  # Начальная громкость

        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.__volume_slider, 1)

        main_layout.addLayout(volume_layout)

    def __connect_signals(self):
        """Подключение сигналов"""
        self.__play_button.clicked.connect(self.__toggle_play)
        self.__stop_button.clicked.connect(self.__player.stop)
        self.__previous_button.clicked.connect(self.__player.previous_track)
        self.__next_button.clicked.connect(self.__player.next_track)

        self.__volume_slider.valueChanged.connect(self.__player.set_volume)

        # При перемещении ползунка положения трека
        self.__position_slider.sliderMoved.connect(self.__seek_position)

        # Обновляем при изменении состояния плеера
        # В реальной реализации здесь должны быть подключения к сигналам плеера

    def __toggle_play(self):
        """Переключение между воспроизведением и паузой"""
        if self.__player.is_playing():
            self.__player.pause()
            self.__play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            if self.__player.play():
                self.__play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def __seek_position(self, position):
        """Изменение позиции воспроизведения"""
        # Отключаем обновление слайдера во время перемотки
        self.__update_timer.stop()

        # Перематываем трек
        self.__player.set_position(position)  # Исправленная строка - напрямую устанавливаем позицию

        # Возобновляем обновление через небольшую задержку
        # чтобы не перезаписать позицию слайдера сразу после установки
        QTimer.singleShot(100, self.__update_timer.start)

    def __update_player_info(self):
        """Обновление информации о воспроизведении"""
        current_track = self.__player.get_current_track()

        if current_track:
            # Обновляем информацию о треке
            self.__info_label.setText(f"{current_track.artist} - {current_track.title}")

            # Загружаем обложку альбома
            cover_data = current_track.get_album_cover()
            if cover_data:
                pixmap = QPixmap()
                pixmap.loadFromData(cover_data)
                self.__album_cover.setPixmap(pixmap.scaled(
                    self.__album_cover.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
            else:
                # Если обложка не найдена, очищаем
                self.__album_cover.clear()

            # Обновляем длительность
            duration = current_track.duration
            self.__position_slider.setRange(0, duration)

            duration_str = str(datetime.timedelta(seconds=duration)).split('.')[0][-5:]
            self.__duration_label.setText(duration_str)

            # Проверяем, воспроизводится ли трек
            if self.__player.is_playing() or self.__player.is_paused():
                # Обновляем текущую позицию
                position = self.__player.get_position()
                if not self.__position_slider.isSliderDown():  # Не обновляем, если пользователь перемещает ползунок
                    self.__position_slider.setValue(int(position))

                position_str = str(datetime.timedelta(seconds=int(position))).split('.')[0][-5:]
                self.__time_label.setText(position_str)

                # Проверяем, не закончился ли трек
                if position >= duration and not self.__player.is_paused():
                    # Трек закончился, переходим к следующему
                    QTimer.singleShot(500, self.__player.next_track)

            # Обновляем иконку на кнопке воспроизведения
            if self.__player.is_playing():
                self.__play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            else:
                self.__play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            # Сбрасываем информацию, если нет текущего трека
            self.__info_label.setText("Нет воспроизведения")
            self.__time_label.setText("0:00")
            self.__duration_label.setText("0:00")
            self.__position_slider.setValue(0)
            self.__position_slider.setRange(0, 0)
            self.__play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.__album_cover.clear()