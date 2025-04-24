# core/track.py
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import datetime

class Track:
    """
    Класс, представляющий музыкальный трек
    """
    def __init__(self, path):
        self.__path = path
        self.__title = ""
        self.__artist = ""
        self.__album = ""
        self.__duration = 0
        self.__load_metadata()

    def __load_metadata(self):
        """Загрузка метаданных трека"""
        try:
            if os.path.exists(self.__path) and self.__path.lower().endswith('.mp3'):
                audio = MP3(self.__path)
                id3 = ID3(self.__path)

                # Извлекаем название
                if "TIT2" in id3:
                    self.__title = str(id3["TIT2"])
                else:
                    self.__title = os.path.basename(self.__path)

                # Извлекаем исполнителя
                if "TPE1" in id3:
                    self.__artist = str(id3["TPE1"])
                else:
                    self.__artist = "Неизвестный исполнитель"

                # Извлекаем альбом
                if "TALB" in id3:
                    self.__album = str(id3["TALB"])
                else:
                    self.__album = "Неизвестный альбом"

                # Длительность трека
                self.__duration = int(audio.info.length)
            else:
                self.__title = os.path.basename(self.__path)
        except Exception as e:
            print(f"Ошибка загрузки метаданных: {e}")
            self.__title = os.path.basename(self.__path)

    @property
    def path(self):
        """Получить путь к файлу трека"""
        return self.__path

    @property
    def title(self):
        """Получить название трека"""
        return self.__title

    @property
    def artist(self):
        """Получить исполнителя трека"""
        return self.__artist

    @property
    def album(self):
        """Получить альбом трека"""
        return self.__album

    @property
    def duration(self):
        """Получить длительность трека в секундах"""
        return self.__duration

    def get_duration_str(self):
        """Получить длительность трека в формате MM:SS"""
        return str(datetime.timedelta(seconds=self.__duration)).split('.')[0][-5:]

    def get_album_cover(self):
        """Получить обложку альбома (bytes)"""
        try:
            if os.path.exists(self.__path) and self.__path.lower().endswith('.mp3'):
                id3 = ID3(self.__path)
                for tag in id3.keys():
                    if tag.startswith('APIC'):  # APIC - тег, содержащий изображение
                        return id3[tag].data
        except Exception as e:
            print(f"Ошибка при получении обложки: {e}")
        return None

    def __str__(self):
        """Строковое представление трека"""
        return f"{self.__artist} - {self.__title}"