import tkinter as tk
import pygame.mixer
from tkinter import messagebox


class AudioPlayer:
    def __init__(self, parent_frame, get_active_track_callback):
        self.current_track = None
        self.is_playing = False
        self.get_active_track_callback = get_active_track_callback

        # Inicjalizacja Pygame Mixer
        pygame.mixer.init()

        # UI odtwarzacza
        self.frame = tk.Frame(parent_frame, bg='green')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.play_button = tk.Button(self.frame, text="▶️ Odtwórz", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_button = tk.Button(self.frame, text="⏹️ Zatrzymaj", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.volume_label = tk.Label(self.frame, text="Głośność:", bg='green', fg='white')
        self.volume_label.pack(side=tk.LEFT, padx=5)

        self.volume_slider = tk.Scale(self.frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(0.5)  # Domyślna głośność 50%
        self.volume_slider.pack(side=tk.LEFT, padx=5)

    def play(self):
        """
        Odtwórz aktualnie wybrany utwór z biblioteki lub listy składanki.
        """
        track = self.get_active_track_callback()
        if not track:
            messagebox.showwarning("Brak utworu", "Wybierz utwór do odtworzenia!")
            return

        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            self.current_track = track
            self.is_playing = True
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można odtworzyć utworu: {e}")

    def stop(self):
        """
        Zatrzymaj odtwarzanie.
        """
        pygame.mixer.music.stop()
        self.is_playing = False

    def set_volume(self, volume):
        """
        Ustaw głośność.
        """
        pygame.mixer.music.set_volume(float(volume))
