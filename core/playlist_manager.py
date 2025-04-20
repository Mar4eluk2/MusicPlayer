# core/playlist_manager.py
from core.playlist import Playlist

class PlaylistManager:
    """
    Класс для управления плейлистами
    """
    def __init__(self):
        self.__playlists = []
        self.__current_playlist_index = -1

        # Создаем плейлист "Избранное" по умолчанию
        self.create_playlist("Избранное")

    def create_playlist(self, name):
        """Создать новый плейлист"""
        playlist = Playlist(name)
        self.__playlists.append(playlist)

        # Если это первый плейлист, делаем его текущим
        if len(self.__playlists) == 1:
            self.__current_playlist_index = 0

        return len(self.__playlists) - 1  # Возвращаем индекс созданного плейлиста

    def delete_playlist(self, index):
        """Удалить плейлист по индексу"""
        if 0 <= index < len(self.__playlists):
            self.__playlists.pop(index)

            # Обновляем индекс текущего плейлиста
            if self.__current_playlist_index == index:
                if len(self.__playlists) > 0:
                    self.__current_playlist_index = 0
                else:
                    self.__current_playlist_index = -1
            elif self.__current_playlist_index > index:
                self.__current_playlist_index -= 1

            return True
        return False

    def get_playlist(self, index):
        """Получить плейлист по индексу"""
        if 0 <= index < len(self.__playlists):
            return self.__playlists[index]
        return None

    def get_playlists(self):
        """Получить список всех плейлистов"""
        return self.__playlists

    def set_current_playlist(self, index):
        """Установить текущий плейлист по индексу"""
        if 0 <= index < len(self.__playlists):
            self.__current_playlist_index = index
            return True
        return False

    def get_current_playlist(self):
        """Получить текущий плейлист"""
        if 0 <= self.__current_playlist_index < len(self.__playlists):
            return self.__playlists[self.__current_playlist_index]
        return None

    def get_current_playlist_index(self):
        """Получить индекс текущего плейлиста"""
        return self.__current_playlist_index

    def add_track_to_current_playlist(self, track_path):
        """Добавить трек в текущий плейлист"""
        if self.get_current_playlist():
            return self.get_current_playlist().add_track(track_path)
        return -1

    def add_tracks_to_current_playlist(self, track_paths):
        """Добавить несколько треков в текущий плейлист"""
        added_tracks = []
        for path in track_paths:
            index = self.add_track_to_current_playlist(path)
            if index >= 0:
                added_tracks.append(index)
        return added_tracks