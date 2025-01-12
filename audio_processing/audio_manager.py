from pydub import AudioSegment
from pydub.effects import speedup, normalize
import os
class AudioManager:
    def __init__(self):
        #Lista piosenek krotka (ścieżka, obiekt AudioSegment)
        self.tracks = []
        self.track_filters = {} #Słownik przechowujący zastosowanych filtrow dla kazdej pojedynczej piosenki

    def add_track(self, file_path):
        #Dodaj piosenkę do składanki
        try:
            track = AudioSegment.from_file(file_path)
            self.tracks.append((file_path, track)) #Sciezka jest potrzebna do usuwania
            self.track_filters[file_path] = {"tempo": 1.0}  # Domyślne tempo

        except Exception as e:
            raise ValueError(f"Błąd przy dodawaniu pliku: {e}")

    def remove_track(self, song_name):
        """Usuń piosenkę z listy składanki."""
        for i, (file_path, track) in enumerate(self.tracks):
            if os.path.basename(file_path) == song_name:
                del self.tracks[i]
                return
        raise ValueError(f"Nie znaleziono piosenki '{song_name}' w składance")

    def move_track_up(self, index):
        """Przenieś piosenkę na wyższy poziom (do góry)."""
        if index > 0:
            self.tracks[index], self.tracks[index - 1] = self.tracks[index - 1], self.tracks[index]

    def move_track_down(self, index):
        """Przenieś piosenkę na niższy poziom (w dół)."""
        if index < len(self.tracks) - 1:
            self.tracks[index], self.tracks[index + 1] = self.tracks[index + 1], self.tracks[index]
    def create_mix(self, output_path):
        """Utwórz składankę i zapisz ją do pliku."""
        if not self.tracks:
            raise ValueError("Brak piosenek do utworzenia składanki")
        mix = sum(track[1] for track in self.tracks)  # Sumowanie tylko obiektów AudioSegment
        mix.export(output_path, format="mp3", codec="libmp3lame")

    def apply_filters(self, track, filters):
        """
        Nakłada filtry na podany utwór AudioSegment.
        :param track: Obiekt AudioSegment.
        :param filters: Słownik z nazwami filtrów i ich wartościami.
        :return: Zmieniony obiekt AudioSegment.
        """
        if 'tempo' in filters:
            track = speedup(track, playback_speed=filters['tempo'])
        if 'volume' in filters:
            track = track + filters['volume']
        return track

    def create_mix(self, output_path):
        """Utwórz składankę i zapisz ją do pliku."""
        if not self.tracks:
            raise ValueError("Brak piosenek do utworzenia składanki")
        mix = AudioSegment.silent(duration=0)  # Pusta składanka

        for file_path, track in self.tracks:
            filters = self.track_filters.get(file_path, {})
            track = self.apply_filters(track, filters)  # Zastosuj filtry
            mix += track

        mix.export(output_path, format="mp3", codec="libmp3lame")