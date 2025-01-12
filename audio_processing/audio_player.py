import tkinter as tk
import pygame.mixer
from tkinter import messagebox


class AudioPlayer:
    def __init__(self, parent_frame, get_active_track_callback):
        self.current_track = None
        self.is_playing = False
        self.is_paused = False
        self.get_active_track_callback = get_active_track_callback

        # Inicjalizacja Pygame Mixer
        pygame.mixer.init()

        # UI odtwarzacza
        self.frame = tk.Frame(parent_frame, bg='#2E2E2E')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.play_button = tk.Button(self.frame, text="▶️ Odtwórz", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=(265,1), pady=5)

        self.stop_button = tk.Button(self.frame, text="⏹️ Pauza", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=(16,0), pady=5)

        self.volume_slider = tk.Scale(self.frame, from_=0, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, command=self.set_volume, showvalue=0)
        self.volume_slider.set(0.2)  # Domyślna głośność 20%
        self.volume_slider.pack(side=tk.LEFT, padx=(16,0), pady=5)

    def play(self):
        """
        Odtwórz aktualnie wybrany utwór z biblioteki lub listy składanki.
        """
        if not self.is_playing:  # Odtwórz tylko, jeśli nie odtwarza
            track = self.get_active_track_callback()
            if not track:
                messagebox.showwarning("Brak utworu", "Wybierz utwór do odtworzenia!")
                return

            try:
                pygame.mixer.music.load(track)
                pygame.mixer.music.play()
                self.current_track = track
                self.is_playing = True
                self.is_paused = False

            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można odtworzyć utworu: {e}")
        else:  # Wznów odtwarzanie, jeśli było wstrzymane
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.stop_button.config(text="⏹️ Pauza")

    def stop(self):
        """
        Zatrzymaj odtwarzanie.
        """
        if not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.stop_button.config(text="⏹️ Przerwij")
        else:
            pygame.mixer.music.stop()
            self.is_paused = False
            self.is_playing = False
            self.stop_button.config(text="⏹️ Pauza")

    def set_volume(self, volume):
        """
        Ustaw głośność.
        """
        pygame.mixer.music.set_volume(float(volume))
