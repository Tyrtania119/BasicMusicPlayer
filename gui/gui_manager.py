import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from audio_processing.library_manager import LibraryManager
from audio_processing.audio_manager import AudioManager
from audio_processing.file_manager import select_audio_files
from audio_processing.file_manager import is_valid_audio_file
import os

class GUIManager:
    def __init__(self):
        self.audio_manager = AudioManager()
        self.library_manager = LibraryManager()
        self.root = tk.Tk()
        self.root.geometry('1200x600')  # Określamy rozmiar okna
        self.root.title("Audio Mixer")
        self.root.resizable(True, True)  # Zezwól na zmianę rozmiaru okna

        # Glowna ramka
        self.main_frame = tk.Frame(self.root, bg='blue')
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # Rozciągnij główną ramkę na całą szerokość i wysokość

        # Lewa ramka (biblioteka)
        self.library_frame = tk.Frame(self.main_frame, bg='lightgrey')
        self.library_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Wypełnia lewą część

        # Prawa ramka (interfejs główny)
        self.right_frame = tk.Frame(self.main_frame, bg='lightgrey')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Wypełnia prawą część

        # Lista plików dodanych do składanki
        self.file_listbox = tk.Listbox(self.main_frame, height=10, justify='center', selectmode=tk.SINGLE, bg='red')
        self.file_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)  # Wypełnia całą szerokość, a wysokość jest dynamiczna

        # Dodajemy output_label
        self.output_label = tk.Label(self.main_frame, text="", font="Calibri 12", bg='blue')
        self.output_label.pack(pady=10)

        self.setup_ui()

    def setup_ui(self):
        # Ustawienia dla lewego panelu (biblioteka)
        tk.Label(self.library_frame, text="Biblioteka", font="Calibri 14 bold", bg="lightgrey").pack(pady=10)
        self.library_listbox = tk.Listbox(self.library_frame, width=30)
        self.library_listbox.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)  # Wypełnia całą dostępną przestrzeń

        # Przyciski biblioteki
        tk.Button(self.library_frame, text="Dodaj piosenkę do bilbioteki", command=self.add_file_to_library).pack(pady=5)
        tk.Button(self.library_frame, text="Dodaj piosenkę do składanki", command=self.add_library_file_to_mix).pack(pady=5)

        # Ustawienia dla prawego panelu

        # Przyciski menedżera składanki
        tk.Button(self.right_frame, text="Dodaj pliki", command=self.add_files).pack(fill=tk.X, pady=10)
        tk.Button(self.right_frame, text="Utwórz składankę", command=self.create_mix).pack(fill=tk.X, pady=10)
        tk.Button(self.main_frame, text="Usuń piosenkę", command=self.remove_song).pack(fill=tk.X, pady=10)
        tk.Button(self.main_frame, text="Przenieś w górę", command=self.move_up).pack(fill=tk.X, pady=10)
        tk.Button(self.main_frame, text="Przenieś w dół", command=self.move_down).pack(fill=tk.X, pady=10)

        # Na koniec wczytaj bibliotekę do listy
        self.load_library_to_listbox()

    # Funkcje menedżera składanki
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
                self.output_label.config(text=f"Składanka: {output_path}")
                messagebox.showinfo("Sukces", f"Składanka zapisana jako {output_path}")
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
            messagebox.showinfo("Usunięto", f"Plik '{selected_song}' został usunięty ze składanki.")
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
            messagebox.showinfo("Dodano", f"Plik '{selected_file}' został dodany do składanki.")
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def add_file_to_library(self):
        if self.library_manager.add_file_to_library():
            self.load_library_to_listbox()
            messagebox.showinfo("Sukces", "Plik został dodany do biblioteki.")
        else:
            messagebox.showerror("Błąd", "Nie udało się dodać pliku do biblioteki.")

    def run(self):
        self.root.mainloop()
