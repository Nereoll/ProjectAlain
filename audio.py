import sounddevice as sd
import numpy as np
import time

BUFFER = 1024 # taille du buffer
SAMPLE_RATE = 44100 # fréquence d'échantillonnage standard pour CD
CHANNELS = 1 # cannal audio (mono : 1 ou stéréo : 2)
DEVICE = None # entreé audio par défaut du système

def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    amplitude = np.sqrt(np.mean(indata**2)) # calcul de l'amplitude avec la courbe
    decibels = (20 * np.log10(amplitude + 1e-7))+80 # calcul des décibels avec l'amplitude de la courbe
    visuel = '#' * int(np.round(decibels, 0))
    #print(visuel) #Affichage (ou stockage dans une var de retour) des décibels
    print(int(np.round(decibels, 0)))


with sd.InputStream(callback=callback, channels=CHANNELS, samplerate=SAMPLE_RATE, blocksize=BUFFER, device=DEVICE):#appel du calcul des decibels # audio en mode mono #frequence d'echantillonnage # taille du buffer  # entree audio par défaut
    while True:
        time.sleep(0.01)