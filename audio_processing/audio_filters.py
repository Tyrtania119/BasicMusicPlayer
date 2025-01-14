from pydub import AudioSegment, utils
from pydub.effects import speedup, low_pass_filter

def change_tempo(audio_segment_path, speed) -> AudioSegment:
    """
    Zmienia tempo audio bez zmiany jego wysokości.
    :param audio_segment_path: Ścieżka do pliku audio jako string.
    :param speed: Tempo odtwarzania. speed >= 1.0
    :return: Obiekt AudioSegment z zmienionym tempem.
    """
    # Ustawienie ścieżki do ffmpeg
    prober_name = get_prober_name()
    AudioSegment.converter = prober_name
    utils.get_prober_name = get_prober_name

    # Wczytanie pliku audio
    sound = AudioSegment.from_file(audio_segment_path, format="wav")

    # Zmiana tempa
    final = speedup(sound, playback_speed=speed)

    return final  # Zwracamy zmieniony plik audio

def get_prober_name():
    """
    Zwraca ścieżkę do narzędzia ffmpeg.
    """
    return "C:/ffmpeg-7.1-essentials_build/bin/ffmpeg.exe"