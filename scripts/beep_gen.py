import math
import struct
import wave

sample_rate = 44100
duration = 0.25
frequency = 880
amplitude = 0.4

with wave.open('beep.wav', 'w') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    for i in range(int(sample_rate * duration)):
        value = int(32767 * amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
        wav.writeframes(struct.pack('<h', value))

print('Created beep.wav')
