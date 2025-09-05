import sounddevice as sd
import numpy as np


class SoundMeter:
    """
    Classe pour mesurer le niveau sonore via le microphone.

    Attributs :
        sample_rate (int): Fréquence d'échantillonnage en Hz (par défaut 44100).
        channels (int): Nombre de canaux audio à capturer (1 = mono, 2 = stéréo).
        buffer (int): Taille du buffer audio en nombre d'échantillons.
        device (int ou None): ID du périphérique audio à utiliser (None = périphérique par défaut).
    """

    def __init__(self, sample_rate=44100, channels=1, buffer=1024, device=None):
        """
        Initialise le SoundMeter avec les paramètres audio.

        Args:
            sample_rate (int): Fréquence d'échantillonnage.
            channels (int): Nombre de canaux.
            buffer (int): Taille du buffer.
            device (int ou None): Périphérique audio.
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer = buffer
        self.device = device

    def get_max_db(self, duration=3):
        """
        Mesure le niveau sonore maximal pendant un intervalle de temps donné.

        Args:
            duration (int ou float): Durée de la mesure en secondes (par défaut 3s).

        Returns:
            float: Niveau sonore maximal en dB, arrondi à deux décimales.
        
        Fonctionnement :
            - Capture le flux audio en temps réel via sounddevice.
            - Calcule le RMS (Root Mean Square) pour chaque buffer.
            - Convertit le RMS en décibels.
            - Transforme les dB en valeurs positives pour affichage.
            - Retourne le maximum mesuré sur la durée.
        """
        self.max_db = 0.0

        def callback(indata, frames, time, status):
            """Fonction appelée pour chaque buffer audio capturé."""
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