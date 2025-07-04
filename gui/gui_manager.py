import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from audio_processing.library_manager import LibraryManager
from audio_processing.audio_manager import AudioManager
from audio_processing.file_manager import select_audio_files, is_valid_audio_file
from audio_processing.audio_player import AudioPlayer
from audio_processing.audio_filters import change_tempo
import datetime
import os

accent_color = '#c74874'
bg_color = '#2E2E2E'
alt_bg_color = '#525151'
font_color = 'white'

class GUIManager:
    def __init__(self):

        self.audio_manager = AudioManager()
        self.library_manager = LibraryManager()
        self.root = tk.Tk()
        self.root.geometry('1200x600')
        self.root.title("Audio Mixer")
        self.root.config(bg=bg_color)
        self.root.resizable(False, False)

        # Glowna ramka
        self.main_frame = tk.Frame(self.root, bg=bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Lewa ramka (biblioteka)
        self.library_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.library_frame.pack(side=tk.LEFT, fill=tk.BOTH)  # Wypełnia lewą część

        # Prawa ramka (interfejs główny)
        self.right_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)  # Wypełnia prawą część

        # Ramka odtwarzacza
        self.player_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.player_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Dodanie odtwarzacza z przekazaniem funkcji callback
        self.player = AudioPlayer(self.player_frame, self.get_active_track)

        #Filtry

        # Ustawienia dla prawego panelu
        tk.Label(self.right_frame, text="FILTRY", font="Calibri 16 bold", bg=bg_color, fg=font_color, bd=0).pack(pady=15)

        self.tempo_slider = tk.Scale(self.right_frame, from_=1.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL ,label="Tempo", bg="#2E2E2E", fg=accent_color, bd=0)
        self.tempo_slider.pack(pady=5)
        # W prawej ramce

        self.volume_slider = tk.Scale(self.right_frame, from_=-10, to=10, resolution=1, orient=tk.HORIZONTAL, label="Głośność (dB)", bg="#2E2E2E", fg=accent_color)
        self.volume_slider.pack(pady=5)

        self.bass_slider = tk.Scale(self.right_frame, from_=0, to=20, resolution=1, orient=tk.HORIZONTAL, label="Podbicie basu (dB)", bg="#2E2E2E", fg=accent_color)
        self.bass_slider.pack(pady=5)

        tk.Button(self.right_frame, text="Zastosuj filtry", command=self.apply_filters_to_selected, bg=accent_color, fg=font_color, font=("Calibri", 12), bd=0).pack(pady=10)

        # Ramka edytora kolejki
        self.editor_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.editor_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Lista plików dodanych do składanki
        self.file_listbox = tk.Listbox(self.main_frame, justify='center', selectmode=tk.SINGLE, bg='#3A3A3A', fg=font_color, font=("Arial", 12), selectbackground=accent_color)
        self.file_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=20, padx=(0,10))

        # Dodajemy output_label
        self.output_label = tk.Label(self.player_frame, text="", font="Calibri 12", bg=bg_color)
        self.output_label.pack(pady=10)

        self.setup_ui()

    def setup_ui(self):
        # Ustawienia dla lewego panelu (biblioteka)
        tk.Label(self.library_frame, text="BIBLIOTEKA", font="Calibri 16 bold", bg=bg_color, fg=font_color).pack(pady=(15,0))
        self.library_listbox = tk.Listbox(self.library_frame, width=30, bg=alt_bg_color, fg=font_color, bd=0, highlightthickness=0, selectbackground=accent_color)
        self.library_listbox.pack(pady=0, padx=10, fill=tk.BOTH, expand=True)  # Wypełnia całą dostępną przestrzeń

        # Przyciski biblioteki
        tk.Button(self.library_frame, text="Dodaj piosenkę do bilbioteki", command=self.add_file_to_library, bd=0, bg=accent_color, fg=font_color).pack(pady=5)
        tk.Button(self.library_frame, text="Dodaj piosenkę do składanki", command=self.add_library_file_to_mix, bd=0, bg=accent_color, fg=font_color).pack(pady=5)


        # Przyciski menedżera składanki
        tk.Button(self.right_frame, text="Utwórz składankę", command=self.create_mix, width=20).pack(pady=114, padx=0, side=tk.TOP)

        tk.Button(self.editor_frame, text="Usuń piosenkę", command=self.remove_song).pack(pady=10, padx=(260,0), side=tk.LEFT, anchor='center')
        tk.Button(self.editor_frame, text="Przenieś w górę", command=self.move_up).pack(pady=10, side=tk.LEFT, padx=15, anchor='center')
        tk.Button(self.editor_frame, text="Przenieś w dół", command=self.move_down).pack( pady=10,side=tk.LEFT, anchor='center')

        # Na koniec wczytaj bibliotekę do listy
        self.load_library_to_listbox()

    # Funkcje menedżera składanki
    def get_active_track(self):
        """
        Pobierz ścieżkę do aktywnego utworu z biblioteki lub listy składanki.
        """
        selected_library_index = self.library_listbox.curselection()
        selected_playlist_index = self.file_listbox.curselection()

        if selected_library_index:
            selected_file = self.library_listbox.get(selected_library_index)
            return os.path.join(self.library_manager.library_folder, selected_file)
        elif selected_playlist_index:
            selected_track = self.audio_manager.tracks[selected_playlist_index[0]]
            if isinstance(selected_track, tuple):
                selected_track = selected_track[0]
            return selected_track
        else:
            return None

    def add_files(self):
        files = select_audio_files()
        for file in files:
            if is_valid_audio_file(file):
                try:
                    self.audio_manager.add_track(file)
                    file_name = os.path.basename(file)
                    self.file_listbox.insert(tk.END, file_name)
                except ValueError as e:
                    messagebox.showerror("Błąd", str(e))
            else:
                messagebox.showwarning("Nieprawidłowy format pliku! ", file)

    def create_mix(self):
        output_path = filedialog.asksaveasfilename(
            title="Zapisz jako",
            defaultextension=".mp3",
            filetypes=[("MP3 file", "*.mp3")]
        )
        if output_path:
            try:
                self.audio_manager.create_mix(output_path)
                # Teraz ustawi się tekst w output_label
                date = datetime.datetime.now()
                self.output_label.config(text=f"Składanka zapisana jako {output_path}" + str(date))
            except ValueError as e:
                messagebox.showerror("Błąd", str(e))

    def remove_song(self):
        selected_index = self.file_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Brak zaznaczenia", "Wybierz piosenkę do usunięcia!")
            return

        selected_song = self.file_listbox.get(selected_index)
        try:
            self.audio_manager.remove_track(selected_song)
            self.file_listbox.delete(selected_index)
            self.output_label.config(text=f"Plik '{selected_song}' został usunięty ze składanki.")
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def move_up(self):
        selected_index = self.file_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Brak zaznaczenia", "Wybierz piosenkę do przeniesienia!")
            return

        selected_index = selected_index[0]
        if selected_index == 0:
            return

        self.audio_manager.move_track_up(selected_index)
        self.update_listbox()

    def move_down(self):
        selected_index = self.file_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Brak zaznaczenia", "Wybierz piosenkę do przeniesienia!")
            return

        selected_index = selected_index[0]
        if selected_index == len(self.audio_manager.tracks) - 1:
            return

        self.audio_manager.move_track_down(selected_index)
        self.update_listbox()

    def update_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for track in self.audio_manager.tracks:
            track = track[0] #pobranie sciezki z krotki
            self.file_listbox.insert(tk.END, os.path.basename(track))

    # Funkcje dla biblioteki
    def load_library_to_listbox(self):
        self.library_listbox.delete(0, tk.END)
        library_files = self.library_manager.load_library_files()
        for file in library_files:
            self.library_listbox.insert(tk.END, os.path.basename(file))

    def add_library_file_to_mix(self):
        selected_index = self.library_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Brak zaznaczenia", "Wybierz plik z biblioteki!")
            return

        selected_file = self.library_listbox.get(selected_index)
        full_path = os.path.join(self.library_manager.library_folder, selected_file)
        try:
            self.audio_manager.add_track(full_path)
            self.file_listbox.insert(tk.END, selected_file)
            self.output_label.config(text=f"Plik '{selected_file}' został dodany do składanki.")
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def add_file_to_library(self):
        if self.library_manager.add_file_to_library():
            self.load_library_to_listbox()
            self.output_label.config(text="Plik został dodany do biblioteki.")
        else:
            messagebox.showerror("Błąd", "Nie udało się dodać pliku do biblioteki.")

    def get_audio_segment(self):
        playlista = AudioSegment()
        for i in self.file_listbox:
            playlista += i
        return playlista

    def apply_filters_to_selected(self):
        selected_index = self.file_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Brak zaznaczenia", "Wybierz utwór, aby zastosować filtry!")
            return

        selected_index = selected_index[0]
        file_path, _ = self.audio_manager.tracks[selected_index]

        # Pobierz wartości filtrów
        tempo = self.tempo_slider.get()
        volume = self.volume_slider.get()
        bass_gain = self.bass_slider.get()

        # Zapisz filtry do słownika w AudioManager
        self.audio_manager.track_filters[file_path] = {
            "tempo": tempo,
            "volume": volume,
            "bass_gain": bass_gain}

        messagebox.showinfo("Sukces", f"Zastosowano filtry do utworu: Tempo={tempo}, Głośność={volume} dB,  Basy={bass_gain} dB")

    def run(self):
        self.root.mainloop()
