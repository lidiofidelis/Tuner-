#! /usr/bin/env python
import numpy as np
import time
import pyaudio
import time

NOTE_MIN = 36       # C2
NOTE_MAX = 92       # C7
FSAMP = 30000       # Sampling frequency in Hz
FRAME_SIZE = 8192  # How many samples per frame?
FRAMES_PER_FFT = 4 # FFT takes average across how many frames?

######################################################################
# Derived quantities from constants above. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (so
# resolution increases); however, it will incur more delay to process
# new sounds.

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

######################################################################
# For printing out notes

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

######################################################################
# These three functions are based upon this very useful webpage:
# https://newt.phys.unsw.edu.au/jw/notes.html

def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
#def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1) alterado
def note_name(n): return NOTE_NAMES[n % 12]
######################################################################
# Ok, ready to go now.

###### teste ######
#dicionario = {"C":"CDEFGAB","":"",}
#a = "D"
#aux = 0

#for x in dicionario.values():
#    for i in range(len(x)):
#        if x[i]==a:
            #aux+=1
#print(aux)
    
#variables
u = []
xe = []
maior = 0
aux = []
trash = []
count1 = 0
# Get min/max index within FFT of notes we care about.
# See docs for numpy.rfftfreq()
def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

# Allocate space to run an FFT. 
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

# Initialize audio
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

# Create Hanning window function
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

# Print initial text
print ('sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')
print ()

print('digite 1 para iniciar')
variavel = input()
variavel = int(variavel)
# As long as we are getting data:
# while stream.is_active():
if variavel == 1:
    while True:#stream.is_active():
    # Shift the buffer down and new data in
        buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
        buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)

    # Run the FFT on the windowed buffer
        fft = np.fft.rfft(buf * window)

    # Get frequency of maximum response in range
        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

    # Get note number and nearest note
        n = freq_to_number(freq)
        n0 = int(round(n))

    # Console output once we have a full buffer
        num_frames += 1
        NOTA = {"C","D","E","F","G","A","B"},{"C#","D","E","F#","G","A","B"},{"C#","D#","E","F#","G","A","B"},{"C","D","E","F","G","A","A#"},{"C","D","E","F#","G","A","B"},{"C#","D","E","F#","G#","A","B"},{"C#","D#","E","F#","G#","A#","B"},{"C#","D#","F","F#","G#","A#","C"},{"D","D#","F","G","G#","A#","C"},{"C#","D#","F","F#","G#","A#","B"},{"C#","D#","F","G","G#","A#","C"},{"D","E","F","G","A","A#","C"}
        NOTA1 = 'C D E F G A B C# D# F# G# A#'.split()

        if len(xe)<40:
            xe.append(note_name(n0))
        elif len(xe)==40:
            #for i in xe: 
            #    for j in NOTA1:
            #        if j == i:
            #            count1 += 1
            #        if count1 < 3:
            #            count1 = 0 
            #            trash.append(j)      
            teste = set(xe)
            #trash = ' '.join(trash)
            #teste = teste.difference(trash)

        
            for i in NOTA:
                x = teste.intersection(i)
                u.append(len(x))
            for j in range(len(NOTA)):
                if u[j] > maior:
                    maior = u[j] 
            for i,v in enumerate(u):
                if v == maior:
                    aux.append(i)
            print(u)
            print(aux)
            for i in range(len(aux)):
                print(f'os possiveis tons sao {NOTA1[aux[i]]}:')
            
            #trash = list(trash)
            # limpar variáveis
            aux.clear()
            u.clear()
            xe.clear()
            maior = 0
            #trash.clear()
            #count1 = 0
        #    teste = set(xe)
        #    for i in NOTA:
        #        x = teste.intersection(i)
        #        u.append(len(x))
        #    for j in range(len(NOTA)):
        #        if u[j] > maior:
        #            maior = u[j] 
        #    for i,v in enumerate(u):
       #         if v == maior:
       #             aux.append(i)
            #print(u)
            #print(aux)
        #    for i in range(len(aux)):
       #         print(f'os possiveis tons sao {NOTA1[aux[i]]}:')

#        if len(u)<11:
#            u.append(note_name(n0))
#        elif len(u)==11:
#           break
        #if num_frames >= FRAMES_PER_FFT:
      #      print ('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
          #      freq, note_name(n0), n-n0))
else:
	print('operação finalizada.')

