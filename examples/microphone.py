from waveutil.microphone import open_microphone
from waveutil.io import wavwrite


with open_microphone() as m:
    data = m.read(5) # read 5 seconds data, shape: [5 * 44100, 2]
np.save('data.dat', data)
wavwrite('out.wav', data)
