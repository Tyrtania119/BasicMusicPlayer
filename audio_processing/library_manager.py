import os
from audio_processing.file_manager import is_valid_audio_file
from tkinter import filedialog

class LibraryManager:
    def __init__(self, library_folder="library"):
        self.library_folder = library_folder
        self.check_library_exists()

    def check_library_exists(self):
        #stworz folder bilbioteki jesli nie istnieje
        if not os.path.exists(self.library_folder):
            os.makedirs(self.library_folder)

    def load_library_files(self):
        #wczytaj wszyskie pliki audio z folderu
        return [
            os.path.join(self.library_folder, file)
            for file in os.listdir(self.library_folder)
            if file.endswith(('.mp3', '.wav', '.ogg', '.flac'))
        ]

    def add_file_to_library(self):
        """Dodaje plik z lokalizacji użytkownika do folderu biblioteki."""
        file_path = filedialog.askopenfilename(
            title="Wybierz plik audio",
            filetypes=[("Pliki audio", "*.mp3 *.wav *.ogg *.flac")]
        )

        if file_path and is_valid_audio_file(file_path):
            try:
                # Skopiuj plik do folderu biblioteki
                destination = os.path.join(self.library_folder, os.path.basename(file_path))
                shutil.copy(file_path, destination)
                return True
            except Exception as e:
                print(f"Błąd przy kopiowaniu pliku do biblioteki: {e}")
                return False
        return False