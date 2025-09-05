import sounddevice as sd
import numpy as np


class SoundMeter:
    def __init__(self, sample_rate=44100, channels=1, buffer=1024, device=None):
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer = buffer
        self.device = device

    def get_max_db(self, duration=3):
        """
        Mesure le niveau sonore maximal du micro pendant `duration` secondes.
        Retourne la valeur en dB (valeur positive lisible comme sur un sonomètre).
        """
        self.max_db = 0.0

        def callback(indata, frames, time, status):
            if status:
                print(f"[SoundMeter Warning] {status}")

            # RMS → dB
            rms = np.sqrt(np.mean(indata**2))
            db = 20 * np.log10(rms + 1e-6)

            # Décibels "positifs" pour affichage
            db_pos = max(0, -db + 100)

            self.max_db = max(self.max_db, db_pos)

        with sd.InputStream(callback=callback,
                            channels=self.channels,
                            samplerate=self.sample_rate,
                            blocksize=self.buffer,
                            device=self.device):
            sd.sleep(int(duration * 1000))

        return round(self.max_db, 2)  # arrondi pour lecture

    def get_realtime_db(self, duration=3):
        """
        Retourne une liste de valeurs en dB mesurées en temps réel pendant `duration` secondes.
        Utile pour tracer un graphe ou afficher une jauge dynamique.
        """
        db_values = []

        def callback(indata, frames, time, status):
            if status:
                print(f"[SoundMeter Warning] {status}")

            rms = np.sqrt(np.mean(indata**2))
            db = 20 * np.log10(rms + 1e-6)
            db_pos = max(0, -db + 100)
            db_values.append(round(db_pos, 2))

        with sd.InputStream(callback=callback,
                            channels=self.channels,
                            samplerate=self.sample_rate,
                            blocksize=self.buffer,
                            device=self.device):
            sd.sleep(int(duration * 1000))

        return db_values
