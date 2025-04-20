# core/music_player.py
from core.audio_engine import AudioEngine
from core.playlist_manager import PlaylistManager
from core.mp3_engine import MP3Engine

class MusicPlayer:
    """
    Основной класс приложения, который координирует работу
    аудио-движка и менеджера плейлистов
    """

    def get_playlist_manager(self):
        """Получить менеджер плейлистов"""
        return self.__playlist_manager

    def __init__(self):
        # Инкапсуляция: скрываем внутреннюю реализацию аудио-движка и плейлистов
        self.__audio_engine = MP3Engine()
        self.__playlist_manager = PlaylistManager()
        self.__current_track_index = -1
        self.__is_playing = False

    def play(self):
        """Начать воспроизведение текущего трека или возобновить после паузы"""
        if self.__is_playing:
            return False

        if self.__audio_engine.is_paused():
            # Возобновляем после паузы
            if self.__audio_engine.play():
                self.__is_playing = True
                return True
        elif self.__current_track_index >= 0:
            # Начинаем воспроизведение текущего трека
            current_track = self.__playlist_manager.get_current_playlist().get_track(self.__current_track_index)
            if self.__audio_engine.play(current_track.path):
                self.__is_playing = True
                return True

        return False

    def pause(self):
        """Поставить воспроизведение на паузу"""
        if self.__is_playing:
            self.__audio_engine.pause()
            self.__is_playing = False
            return True
        return False

    def stop(self):
        """Остановить воспроизведение"""
        self.__audio_engine.stop()
        self.__is_playing = False

    def next_track(self):
        """Перейти к следующему треку"""
        if self.__playlist_manager.get_current_playlist():
            playlist = self.__playlist_manager.get_current_playlist()
            if self.__current_track_index < playlist.size() - 1:
                self.__current_track_index += 1
                was_playing = self.__is_playing
                self.stop()
                if was_playing:
                    self.play()
                return True
        return False

    def previous_track(self):
        """Перейти к предыдущему треку"""
        if self.__current_track_index > 0:
            self.__current_track_index -= 1
            was_playing = self.__is_playing
            self.stop()
            if was_playing:
                self.play()
            return True
        return False

    def set_track(self, index):
        """Установить текущий трек по индексу"""
        if self.__playlist_manager.get_current_playlist() and 0 <= index < self.__playlist_manager.get_current_playlist().size():
            self.__current_track_index = index
            was_playing = self.__is_playing
            self.stop()
            if was_playing:
                self.play()
            return True
        return False

    def get_current_track(self):
        """Получить текущий трек"""
        if self.__current_track_index >= 0 and self.__playlist_manager.get_current_playlist():
            return self.__playlist_manager.get_current_playlist().get_track(self.__current_track_index)
        return None

    def is_playing(self):
        """Проверить, воспроизводится ли музыка в данный момент"""
        # Обновляем флаг на основе данных от аудио-движка
        self.__is_playing = self.__audio_engine.is_playing()
        return self.__is_playing

    def is_paused(self):
        """Проверить, на паузе ли воспроизведение"""
        return self.__audio_engine.is_paused()

    def add_track(self, path):
        """Добавить трек в текущий плейлист"""
        return self.__playlist_manager.add_track_to_current_playlist(path)

    def add_tracks(self, paths):
        """Добавить несколько треков в текущий плейлист"""
        return self.__playlist_manager.add_tracks_to_current_playlist(paths)

    def create_playlist(self, name):
        """Создать новый плейлист"""
        return self.__playlist_manager.create_playlist(name)

    def get_playlists(self):
        """Получить список всех плейлистов"""
        return self.__playlist_manager.get_playlists()

    def get_current_playlist(self):
        """Получить текущий плейлист"""
        return self.__playlist_manager.get_current_playlist()

    def set_current_playlist(self, index):
        """Установить текущий плейлист по индексу"""
        result = self.__playlist_manager.set_current_playlist(index)
        if result:
            self.__current_track_index = -1
            self.stop()
        return result

    def get_position(self):
        """Получить текущую позицию воспроизведения в секундах"""
        return self.__audio_engine.get_position()

    def set_position(self, position):
        """Установить позицию воспроизведения в секундах"""
        return self.__audio_engine.set_position(position)

    def get_duration(self):
        """Получить длительность текущего трека в секундах"""
        return self.__audio_engine.get_duration()

    def set_volume(self, volume):
        """Установить громкость (0-100)"""
        return self.__audio_engine.set_volume(volume)

    def get_volume(self):
        """Получить текущую громкость"""
        return self.__audio_engine.get_volume()

    def delete_playlist(self, index):
        """Удалить плейлист по индексу"""
        return self.__playlist_manager.delete_playlist(index)

    def get_playlist(self, index):
        """Получить плейлист по индексу"""
        return self.__playlist_manager.get_playlist(index)