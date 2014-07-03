import wave
import numpy as np



wr = wave.open('/home/ubuntustudio2/Desktop/#makana#/input_21Khz.wav', 'r')
par = list(wr.getparams()) # Get the parameters from the input.

par[3] = 0 


ww = wave.open('/home/ubuntustudio2/Desktop/#makana#/input_21Khz_f.wav', 'w')
ww.setparams(tuple(par))

lowpass = 20900


sz = wr.getframerate()
c = int(wr.getnframes()/sz)
for num in range(c):
    print('Processing {}/{} s'.format(num+1, c))
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2] # left and right channel
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    lf[:lowpass], rf[:lowpass] = 0, 0
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
    ww.writeframes(ns.tostring())

wr.close()
ww.close()
