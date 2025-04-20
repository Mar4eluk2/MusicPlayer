# core/mp3_engine.py
from core.audio_engine import AudioEngine
import pygame
import os
import time

class MP3Engine(AudioEngine):
    """
    Реализация аудио-движка с использованием pygame.mixer
    """
    def __init__(self):
        pygame.mixer.init()
        self.__current_track = None
        self.__volume = 50  # Громкость от 0 до 100
        self.__paused = False
        self.__playing = False
        self.__start_time = 0
        self.__pause_position = 0
        pygame.mixer.music.set_volume(self.__volume / 100)

        # Регистрируем обработчик события окончания трека
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def play(self, track_path=None):
        """
        Начать воспроизведение аудиофайла.
        Если track_path не указан, возобновляет воспроизведение после паузы.
        """
        try:
            if track_path is not None:
                # Новый трек - загружаем и воспроизводим
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
                self.__current_track = track_path
                self.__start_time = time.time()
                self.__paused = False
                self.__playing = True
                self.__pause_position = 0
                return True
            elif self.__paused and self.__current_track:
                # Возобновляем после паузы
                pygame.mixer.music.unpause()
                self.__start_time = time.time() - self.__pause_position
                self.__paused = False
                self.__playing = True
                return True
            return False
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")
            return False

    def pause(self):
        """Поставить воспроизведение на паузу"""
        if self.__current_track and not self.__paused and pygame.mixer.music.get_busy():
            self.__pause_position = time.time() - self.__start_time
            pygame.mixer.music.pause()
            self.__paused = True
            return True
        return False

    def stop(self):
        """Остановить воспроизведение"""
        pygame.mixer.music.stop()
        self.__paused = False
        self.__playing = False
        self.__pause_position = 0
        return True

    def is_playing(self):
        """Проверить, воспроизводится ли трек"""
        # Проверяем фактическое состояние pygame
        actually_playing = pygame.mixer.music.get_busy()

        # Если мы думаем, что трек играет, но pygame говорит, что нет - значит трек закончился
        if self.__playing and not actually_playing and not self.__paused:
            self.__playing = False
            return False

        return self.__playing and not self.__paused

    def is_paused(self):
        """Проверить, на паузе ли воспроизведение"""
        return self.__paused

    def get_position(self):
        """Получить текущую позицию воспроизведения в секундах"""
        if not self.__current_track:
            return 0

        # Если трек не воспроизводится и не на паузе, возвращаем 0
        if not self.__playing and not self.__paused:
            return 0

        # Если трек на паузе, возвращаем сохраненную позицию
        if self.__paused:
            return self.__pause_position

        # Проверяем, не закончился ли трек
        if not pygame.mixer.music.get_busy() and not self.__paused:
            self.__playing = False
            # Если трек закончился, возвращаем его длительность
            return self.get_duration()

        # Если трек воспроизводится, вычисляем текущую позицию
        current_pos = time.time() - self.__start_time
        # Проверяем, не превышает ли позиция длительность трека
        duration = self.get_duration()
        if duration > 0 and current_pos > duration:
            return duration

        return current_pos

    def set_position(self, position):
        """
        Установить позицию воспроизведения в секундах
        Pygame не поддерживает перемотку напрямую, поэтому перезагружаем трек
        и устанавливаем начальное время на position секунд назад
        """
        if not self.__current_track or position < 0:
            return False

        try:
            # Сохраняем, воспроизводится ли трек сейчас
            was_playing = pygame.mixer.music.get_busy() and not self.__paused

            # Останавливаем воспроизведение
            pygame.mixer.music.stop()

            # Загружаем трек заново и устанавливаем начальную позицию
            pygame.mixer.music.load(self.__current_track)
            pygame.mixer.music.play(start=position)

            # Обновляем время начала
            self.__start_time = time.time() - position

            # Если трек был на паузе, снова ставим на паузу
            if not was_playing and self.__paused:
                pygame.mixer.music.pause()
                self.__pause_position = position
            else:
                self.__paused = False

            return True
        except Exception as e:
            print(f"Ошибка при перемотке: {e}")
            return False

    def get_duration(self):
        """Получить длительность текущего трека в секундах"""
        try:
            if self.__current_track and os.path.exists(self.__current_track):
                from mutagen.mp3 import MP3
                audio = MP3(self.__current_track)
                return int(audio.info.length)
        except Exception as e:
            print(f"Ошибка при получении длительности: {e}")
        return 0

    def set_volume(self, volume):
        """Установить громкость (0-100)"""
        if 0 <= volume <= 100:
            self.__volume = volume
            pygame.mixer.music.set_volume(volume / 100)
            return True
        return False

    def get_volume(self):
        """Получить текущую громкость"""
        return self.__volume

