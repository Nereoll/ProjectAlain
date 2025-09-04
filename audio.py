import sounddevice as sd
import numpy as np

BUFFER = 1024
SAMPLE_RATE = 44100
CHANNELS = 1
DEVICE = None

def record_max_db(duration=5):
    """Mesure le niveau sonore max capté par le micro pendant <duration> secondes."""
    max_db = -np.inf

    def callback(indata, frames, time, status):
        nonlocal max_db
        if status:
            print(f"Status: {status}")
        rms = np.sqrt(np.mean(indata**2))
        decibels = 20 * np.log10(rms + 1e-6)
        if decibels > max_db:
            max_db = decibels
        print("RMS:", np.sqrt(np.mean(indata**2)))


    with sd.InputStream(callback=callback, channels=CHANNELS, samplerate=SAMPLE_RATE, blocksize=BUFFER, device=DEVICE):
        sd.sleep(int(duration * 1000))

    return max_db