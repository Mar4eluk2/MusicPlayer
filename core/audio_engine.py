# core/audio_engine.py
from abc import ABC, abstractmethod

class AudioEngine(ABC):
    """
    Абстрактный класс для аудио-движка
    """
    @abstractmethod
    def play(self, track_path):
        """Начать воспроизведение аудиофайла"""
        pass

    @abstractmethod
    def pause(self):
        """Поставить воспроизведение на паузу"""
        pass

    @abstractmethod
    def stop(self):
        """Остановить воспроизведение"""
        pass

    @abstractmethod
    def get_position(self):
        """Получить текущую позицию воспроизведения в секундах"""
        pass

    @abstractmethod
    def set_position(self, position):
        """Установить позицию воспроизведения в секундах"""
        pass

    @abstractmethod
    def get_duration(self):
        """Получить длительность текущего трека в секундах"""
        pass

    @abstractmethod
    def set_volume(self, volume):
        """Установить громкость (0-100)"""
        pass

    @abstractmethod
    def get_volume(self):
        """Получить текущую громкость"""
        pass