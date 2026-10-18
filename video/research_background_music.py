"""Generate an original, instrumental ambient score with no sampled recordings.
Python dependencies: NumPy. Outputs 165 seconds of stereo PCM audio.
"""
from pathlib import Path
import wave
import numpy as np
RATE=44100
DURATION=165

def compose(output=None):
    output=Path(output or Path(__file__).with_name('research_background_music.wav'))
    sound=np.zeros((RATE*DURATION,2),dtype=np.float32)
    def note(start,length,midi,gain,pan=0.0,pluck=False):
        offset=int(start*RATE);n=min(int(length*RATE),len(sound)-offset)
        if n<=0:return
        t=np.arange(n,dtype=np.float32)/RATE
        hz=440*2**((midi-69)/12)
        if pluck:
            envelope=(1-np.exp(-t/0.018))*np.exp(-t/1.8)*np.minimum(1,(length-t)/.45)
            tone=np.sin(2*np.pi*hz*t)+.19*np.sin(2*np.pi*2*hz*t)+.05*np.sin(2*np.pi*3*hz*t)
        else:
            envelope=np.minimum(t/2.5,1)*np.minimum((length-t)/3,1)
            tone=(np.sin(2*np.pi*hz*t)+.35*np.sin(2*np.pi*(hz*1.0015)*t)+.12*np.sin(2*np.pi*2*hz*t))
            envelope*=.92+.08*np.sin(2*np.pi*.13*t)
        value=(tone*envelope*gain).astype(np.float32)
        sound[offset:offset+n,0]+=value*np.sqrt((1-pan)/2)
        sound[offset:offset+n,1]+=value*np.sqrt((1+pan)/2)
    # Open voicings and a sparse motif, with slightly more tension in the middle.
    chords=[[48,55,62,64],[45,52,59,60],[41,48,55,57],[43,50,57,59]]
    for i,start in enumerate(np.arange(0,156,8.0)):
        chord=chords[i%4]
        for j,pitch in enumerate(chord):note(float(start),11,pitch,.022,pan=(j-1.5)*.27)
        note(float(start),9,chord[0]-12,.014)
        for j,pitch in enumerate([chord[2]+12,chord[1]+12,chord[3]+12]):
            note(float(start+1.6+j*2.0),4.5,pitch,.014 if start<110 else .018,pan=(-.3 if j%2 else .3),pluck=True)
    # Resolve softly to C; no percussion or voice competes with reading.
    for j,pitch in enumerate([48,55,60,64,74]):note(156,9,pitch,.018,pan=(j-2)*.18)
    # Very subtle stereo echoes from the original motif.
    for delay,gain in [(.31,.12),(.62,.06)]:
        shift=int(delay*RATE);sound[shift:]+=sound[:-shift,::-1].copy()*gain
    t=np.arange(len(sound),dtype=np.float32)/RATE
    sound*= (np.minimum(t/4,1)*np.minimum((DURATION-t)/7,1))[:,None]
    peak=float(np.max(np.abs(sound)))
    if peak>.7:sound*=.7/peak
    with wave.open(str(output),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE)
        w.writeframes((np.clip(sound,-1,1)*32767).astype('<i2').tobytes())
    return output
if __name__=='__main__':print(compose())
