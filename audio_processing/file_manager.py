from tkinter import filedialog
import os

def select_audio_files():
    #Otwórz okno i zwróć listę z piosenkami
    files = filedialog.askopenfilenames(
        title="Wybierz pliki audio",
        filetypes=[("Pliki audio", "*.mp3 *.wav *.ogg *.flac")]
    )
    return list(files)

def is_valid_audio_file(file_path):
    #Sprawdź czy format pliku jest zgodny
    return os.path.isfile(file_path) and file_path.endswith(('.mp3', '.wav', '.ogg', '.flac'))
