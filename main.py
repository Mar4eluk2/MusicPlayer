# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.music_player import MusicPlayer

def main():
    app = QApplication(sys.argv)

    # Создаем экземпляр плеера
    player = MusicPlayer()

    # Создаем главное окно и передаем плеер
    window = MainWindow(player)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()