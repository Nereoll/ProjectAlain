import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
CHANNELS = 1
BUFFER = 1024
DEVICE = None

def get_max_db(duration=3):
    """
    Mesure le niveau sonore maximal du micro pendant `duration` secondes.
    Retourne la valeur en dB positifs lisibles (comme un sonomètre).
    """
    max_db = 0  # valeur maximale trouvée

    def callback(indata, frames, time, status):
        nonlocal max_db
        if status:
            print(status)
        rms = np.sqrt(np.mean(indata**2))
        db = 20 * np.log10(rms + 1e-6)
        db_pos = max(0, -db + 100)  # dB positif lisible
        if db_pos > max_db:
            max_db = db_pos

    with sd.InputStream(callback=callback, channels=CHANNELS,
                        samplerate=SAMPLE_RATE, blocksize=BUFFER, device=DEVICE):
        sd.sleep(int(duration * 1000))

    return max_db