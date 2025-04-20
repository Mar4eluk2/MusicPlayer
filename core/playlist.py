# core/playlist.py
from core.track import Track

class Playlist:
    """
    Класс, представляющий плейлист
    """
    def __init__(self, name):
        self.__name = name
        self.__tracks = []

    @property
    def name(self):
        """Получить название плейлиста"""
        return self.__name

    @name.setter
    def name(self, value):
        """Установить название плейлиста"""
        self.__name = value

    def add_track(self, track_path):
        """Добавить трек в плейлист"""
        track = Track(track_path)
        self.__tracks.append(track)
        return len(self.__tracks) - 1  # Возвращаем индекс добавленного трека

    def remove_track(self, index):
        """Удалить трек из плейлиста по индексу"""
        if 0 <= index < len(self.__tracks):
            self.__tracks.pop(index)
            return True
        return False

    def get_track(self, index):
        """Получить трек по индексу"""
        if 0 <= index < len(self.__tracks):
            return self.__tracks[index]
        return None

    def get_tracks(self):
        """Получить список всех треков"""
        return self.__tracks

    def size(self):
        """Получить количество треков в плейлисте"""
        return len(self.__tracks)

    def __str__(self):
        """Строковое представление плейлиста"""
        return f"{self.__name} ({len(self.__tracks)} треков)"
