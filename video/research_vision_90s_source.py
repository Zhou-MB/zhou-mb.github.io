"""Editable, self-contained 90-second academic homepage animation.
Dependencies: Pillow, NumPy, FFmpeg. Run: python research_vision_90s_source.py
No third-party stock assets or audio. Text only one full sentence per frame.
"""
import math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1280,720,24
DURATION=90
OUT='/mnt/data/research_vision_90s.mp4'
BG='#F7F9FC'; INK='#1F2A44'; BLUE='#4F7DF3'; PALE='#DCE7FF'; LINE='#D9E2EC'; MUTED='#A7B6CC'; LIGHT='#ECF2F8'; WHITE='#FFFFFF'; GREEN='#7DAE9B'; WARM='#E8C8A8'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
medium='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F=ImageFont.truetype(font,31)
Fsmall=ImageFont.truetype(font,24)

# Scene lengths total 90 seconds
lengths=[9,10,10,11,10,11,11,10,8]
starts=[]; z=0
for l in lengths: starts.append(z); z+=l
CAPTIONS=[
 'The world never stands still.',
 'A digital twin helps us understand what is happening.',
 'And explore what might happen next.',
 'One twin is simple; thousands tell another story.',
 'Connected twins must work across distributed resources.',
 'But time, computing power, and information are limited.',
 'Intelligent agents can coordinate what runs, where, and when.',
 'Could AI help us design the algorithms themselves?',
 'For a world that works better for everyone.'
]
assert sum(lengths)==90

def clip(v,lo=0,hi=1): return max(lo,min(hi,v))
def sm(x): x=clip(x);return x*x*(3-2*x)
def mix(a,b,t):return a+(b-a)*t

def line(d,pts,fill=LINE,w=3):d.line(pts,fill=fill,width=w,joint='curve')
def box(d,b,fill=WHITE,outline=LINE,r=16,w=3):d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=w)
def dot(d,x,y,r=7,fill=BLUE):d.ellipse((x-r,y-r,x+r,y+r),fill=fill)
def node(d,x,y,s=50,fill=WHITE,stroke=BLUE):box(d,(x-s/2,y-s/2,x+s/2,y+s/2),fill,stroke,r=10)

def caption(d,txt,local,dur):
    # Single sentence in a dedicated, uncluttered bottom band.
    a=sm(local/.6)*sm((dur-local)/.65)
    if a<=0:return
    rgb1=(247,249,252); rgb2=(31,42,68)
    c=tuple(round(mix(rgb1[i],rgb2[i],a)) for i in range(3))
    w=d.textbbox((0,0),txt,font=F)[2]
    if w>W-140:
        ff=Fsmall;w=d.textbbox((0,0),txt,font=ff)[2]
    else:ff=F
    d.text(((W-w)/2,627),txt,font=ff,fill=c)

def bus(d,x,y,sc=1,color=BLUE):
    w,h=134*sc,48*sc
    box(d,(x,y,x+w,y+h),WHITE,color,r=int(9*sc),w=max(2,int(3*sc)))
    box(d,(x+12*sc,y+9*sc,x+100*sc,y+31*sc),LIGHT,color,r=int(4*sc),w=2)
    line(d,[(x+55*sc,y+9*sc),(x+55*sc,y+31*sc)],color,2)
    for wx in [29,104]:dot(d,x+wx*sc,y+h,8*sc,INK)

def person(d,x,y,sc=1):
    dot(d,x,y-28*sc,9*sc,INK)
    line(d,[(x,y-17*sc),(x,y+17*sc)],INK,4)
    line(d,[(x,y-1*sc),(x-13*sc,y+12*sc)],INK,3)
    line(d,[(x,y-1*sc),(x+13*sc,y+12*sc)],INK,3)
    line(d,[(x,y+17*sc),(x-13*sc,y+35*sc)],INK,3)
    line(d,[(x,y+17*sc),(x+12*sc,y+35*sc)],INK,3)

def bike(d,x,y,sc=1):
    R=20*sc
    for xx in [x-35*sc,x+35*sc]:d.ellipse((xx-R,y-R,xx+R,y+R),outline=INK,width=3)
    line(d,[(x-35*sc,y),(x-4*sc,y-23*sc),(x+35*sc,y),(x-35*sc,y),(x+7*sc,y)],BLUE,3)
    line(d,[(x+7*sc,y),(x+19*sc,y-31*sc),(x+31*sc,y-31*sc)],INK,3)
    dot(d,x-5*sc,y-64*sc,10*sc,INK)
    line(d,[(x-5*sc,y-52*sc),(x+3*sc,y-23*sc)],INK,4)
    line(d,[(x+3*sc,y-34*sc),(x+19*sc,y-31*sc)],INK,3)

def city(d,u,closing=False):
    # Stylized human-scale city; objects on distinct planes and no labels.
    horizon=485
    line(d,[(45,horizon),(1235,horizon)],LINE,3)
    for i,(xx,ww,hh) in enumerate([(90,100,150),(225,92,205),(349,127,170),(870,98,135),(997,120,210),(1140,80,165)]):
        box(d,(xx,horizon-hh,xx+ww,horizon),WHITE,LINE,r=6,w=3)
        for c in range(2):
            for rr in range(2):
                px=xx+18+c*35;py=horizon-hh+29+rr*45
                box(d,(px,py,px+14,py+19),PALE,PALE,r=2,w=1)
    # Low sun, trees and road
    dot(d,751,163,40,WARM)
    for x in [53,595,816,1230]:
        line(d,[(x,478),(x,381)],MUTED,6)
        dot(d,x,354,40,'#D7E8DE')
    line(d,[(0,548),(1280,548)],MUTED,3)
    phase=u*1.9
    bx=210+760*sm(clip((u+.15)/1.2))
    bike(d,bx,527,1.1)
    bus(d,1020-220*sm(u),423,0.85)
    person(d,110,455,.7)
    if closing:
        # soft disappearing tiny digital support arcs in the distant background only
        for i in range(4):
            px=570+i*68
            dot(d,px,245+14*math.sin(i*.8),4,PALE)

def twin(d,u):
    bus(d,185,316,1.75,INK)
    # no boxes overlap the two objects, connecting dotted data is in the gap
    box(d,(800,215,1105,485),WHITE,LINE,r=20)
    bus(d,866,333,1.28,BLUE)
    for i in range(7):
        x=560+i*32
        dot(d,x,368,6 if i==int(u*7)%7 else 4,BLUE if i==int(u*7)%7 else PALE)
    for j,h in enumerate([42,65,30,53]):
        box(d,(851+j*42,442-h,874+j*42,442),PALE if j>int(4*u) else BLUE,PALE,r=4,w=1)

def simulate(d,u):
    # One represented bus and future trajectories, no crowding.
    bus(d,165+100*u,385,1.4,INK)
    # Continuous observation line becomes branching forecast paths
    line(d,[(400,416),(540,416)],PALE,6)
    hub=(562,416);dot(d,*hub,10,BLUE)
    for j,dy in enumerate([-105,0,105]):
        pts=[hub,(755,416+dy*.53),(980,416+dy)]
        k=sm(clip((u-j*.13)/.65))
        end=(mix(hub[0],pts[-1][0],k),mix(hub[1],pts[-1][1],k))
        line(d,[hub,(mix(hub[0],pts[1][0],k),mix(hub[1],pts[1][1],k)),end],BLUE if j==1 else LINE,4 if j==1 else 3)
        dot(d,*end,8,BLUE if j==1 else MUTED)
    # A simple predicted signal in its own clear corner
    for j,h in enumerate([22,35,42,57,72]):
        box(d,(1050+j*25,495-h,1064+j*25,495),PALE if j>int(u*5) else BLUE,PALE,3,1)

def multiply(d,u):
    # Single twin morphing into many, no intersecting lines or objects
    pts=[(170+113*c,225+103*r) for r in range(3) for c in range(9)]
    visible=1+int(u*(len(pts)-1))
    for idx,(x,y) in enumerate(pts[:visible]):
        size=45*sm((u*len(pts)-idx+.7)) if idx else 45
        if size<6:continue
        node(d,x,y,size,WHITE,BLUE if idx==0 else '#9FBAF8')
        if idx%3==0:dot(d,x,y,4,BLUE)

def distribution(d,u):
    # spatially separated twinned assets (top) and execution hosts (bottom)
    topxs=[228,480,732,984];bottomxs=[315,650,985]
    for i,x in enumerate(topxs):
        node(d,x,257,65,WHITE,BLUE)
        dot(d,x,257,9,PALE if i>0 else BLUE)
    for j,x in enumerate(bottomxs):
        box(d,(x-63,435,x+63,501),WHITE,INK,11,3)
        for yy in [452,468,484]:line(d,[(x-35,yy),(x+35,yy)],LINE,4)
    # links confined to vertical corridor
    edges=[(0,0),(1,1),(2,1),(3,2)]
    for e,(i,j) in enumerate(edges):
        px=topxs[i];qx=bottomxs[j]
        line(d,[(px,292),(px,366),(qx,366),(qx,435)],LINE,3)
        phase=(u*1.3+e*.22)%1
        points=[(px,292),(px,366),(qx,366),(qx,435)]
        L=[74,abs(qx-px),69];dist=phase*sum(L)
        for segment,seglen in enumerate(L):
            if dist<=seglen:
                x=mix(points[segment][0],points[segment+1][0],dist/(seglen or 1))
                y=mix(points[segment][1],points[segment+1][1],dist/(seglen or 1))
                dot(d,x,y,6,BLUE);break
            dist-=seglen

def bottleneck(d,u):
    # 3 separate lanes: source / queue / resource; no overlapping shapes
    for r,y in enumerate([260,372,484]):
        node(d,169,y,57,WHITE,BLUE)
        line(d,[(211,y),(470,y)],LINE,3)
        for j in range(5):
            xx=300+j*43
            dot(d,xx,y,12,BLUE if j<2 or r==0 else MUTED)
        # Deadline indicators as visual timers, no text
        d.arc((514,y-26,566,y+26),0,360,fill=LINE,width=4)
        d.arc((514,y-26,566,y+26),-90,-90+int(270*(1-u if r else u)),fill=BLUE,width=5)
        line(d,[(584,y),(790,y)],LINE,3)
        box(d,(819,y-35,1005,y+35),WHITE,INK,13,3)
        # occupancy varies across lanes
        occupancy=[.9,.55,.35][r]
        fillw=round(150*occupancy)
        box(d,(836,y-12,836+fillw,y+12),PALE,PALE,5,1)
        for j in range(3):dot(d,1055+j*27,y,5,BLUE if j==0 else MUTED)

def schedule(d,u):
    # before-to-after is communicated through visible reordering and balanced lanes
    positions=[(130+i*54,320) for i in range(8)]
    targets=[(390+(i%4)*82,255+(i//4)*132) for i in range(8)]
    p=sm(clip((u-.16)/.65))
    for i,(start,target) in enumerate(zip(positions,targets)):
        xx=mix(start[0],target[0],p); yy=mix(start[1],target[1],p)
        node(d,xx,yy,34,PALE if i%3 else BLUE,BLUE if i%3 else INK)
    # three separate worker agents with message arcs, on right side
    agents=[(900,230),(1070,325),(900,425)]
    for i,(x,y) in enumerate(agents):
        node(d,x,y,54,WHITE,INK)
        dot(d,x,y,8,BLUE)
    for a,b in [(0,1),(1,2)]:
        pa,pb=agents[a],agents[b]
        line(d,[(pa[0]+35,pa[1]),(pb[0]-35,pb[1])],LINE,3)
        q=(u*1.5+a*.5)%1
        dot(d,mix(pa[0]+35,pb[0]-35,q),mix(pa[1],pb[1],q),5,BLUE)

def ai_design(d,u):
    # abstract transformations: raw constraints -> learned representation -> algorithm tree
    for i in range(4):
        box(d,(155,260+i*59,285,291+i*59),WHITE,LINE,8,2)
        line(d,[(180,275+i*59),(245-15*(i%2),275+i*59)],BLUE,4)
    line(d,[(316,379),(485,379)],LINE,4)
    for i in range(4):dot(d,350+i*36,379,5,BLUE if i<int(u*4) else PALE)
    box(d,(505,273,690,485),WHITE,BLUE,26,4)
    for i in range(7):
        a=i*2*math.pi/7
        x=598+60*math.cos(a);y=375+60*math.sin(a)
        line(d,[(598,375),(x,y)],PALE,3)
        dot(d,x,y,7,BLUE)
    dot(d,598,375,13,BLUE)
    line(d,[(715,379),(850,379)],LINE,4)
    # output is a decision tree (no flowchart text)
    points=[(957,269),(903,378),(1011,378),(876,477),(930,477),(984,477),(1038,477)]
    for a,b in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]:line(d,[points[a],points[b]],LINE,3)
    for j,(x,y) in enumerate(points):
        node(d,x,y,35,WHITE,BLUE if j>int(u*7) else INK)

def render(d,index,u):
    if index==0: city(d,u)
    elif index==1:twin(d,u)
    elif index==2:simulate(d,u)
    elif index==3:multiply(d,u)
    elif index==4:distribution(d,u)
    elif index==5:bottleneck(d,u)
    elif index==6:schedule(d,u)
    elif index==7:ai_design(d,u)
    else:city(d,u,True)

# Render each scene into independent transparent layer then fade scene as a whole at boundaries.
def scene_image(index,t):
    dur=lengths[index]
    u=clip(t/dur)
    im=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(im)
    # large uninterrupted negative space, subtle top rule only
    d.line([(83,93),(1197,93)],fill='#EDF1F7',width=2)
    render(d,index,u)
    caption(d,CAPTIONS[index],t,dur)
    return im

cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',OUT]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for frame in range(DURATION*FPS):
    t=frame/FPS
    idx=max(i for i,s in enumerate(starts) if s<=t)
    local=t-starts[idx]
    im=scene_image(idx,local)
    # 0.65 second dissolve at each boundary, with no simultaneous captions because each fades at boundary
    if idx>0 and local<.65:
        previous=scene_image(idx-1,lengths[idx-1]-.65+local)
        im=Image.blend(previous,im,sm(local/.65))
    proc.stdin.write(np.asarray(im,dtype=np.uint8).tobytes())
    if frame%240==0: print(f'{frame/FPS:>5.1f} / {DURATION}s',flush=True)
proc.stdin.close();status=proc.wait()
if status:raise RuntimeError('ffmpeg failed')
print('CREATED',OUT,os.path.getsize(OUT))
