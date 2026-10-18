"""Narrative research film. Original palette, illustrative scenario, no performance claims.
Run: python research_vision_story_source.py
Dependencies: Pillow, numpy, imageio-ffmpeg (or ffmpeg on PATH).
Outputs are relative to this script. Original video remains unchanged.
"""
import math, subprocess, os, shutil, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1280,720,24
DURATION=90
ROOT=Path(__file__).resolve().parent
BG='#F7F9FC'; INK='#1F2A44'; BLUE='#4F7DF3'; PALE='#DCE7FF'; LINE='#D9E2EC'; MUTED='#A7B6CC'; LIGHT='#ECF2F8'; WHITE='#FFFFFF'; GREEN='#7DAE9B'; WARM='#E8C8A8'
font=next(str(p) for p in [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists())
bold=next(str(p) for p in [Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')] if p.exists())
F=ImageFont.truetype(font,28); Fsmall=ImageFont.truetype(font,23)
TITLE=ImageFont.truetype(bold,40); LABEL=ImageFont.truetype(bold,18); SMALL=ImageFont.truetype(font,17); BIG=ImageFont.truetype(bold,58)
lengths=[8,9,8,9,10,10,9,10,9,8]
starts=np.cumsum([0]+lengths[:-1]).tolist()
HEADINGS=['Can the next decision arrive in time?', 'First, build a living picture.', 'Then, explore what happens next.', 'But the world does not wait.', 'More computing is not enough.', 'Choose what runs, where, and when.', 'Let agents coordinate the work.', 'And when conditions change?', 'Can AI help design better algorithms?', 'The right insight. In time to act.']
CAPTIONS=[
'Imagine heavy rain approaching a city. A bus needs a safer route.',
'A digital twin connects observations of the road, the rain, and the bus.',
'Simulations compare possible routes before the bus reaches the junction.',
'A useful answer can become useless if it arrives too late.',
'Across edge and cloud, tasks compete for compute and communication.',
'Time-critical scheduling puts the urgent route decision first.',
'Agents share local conditions and coordinate tasks across resources.',
'The schedule must adapt as connections and workloads change.',
'I study how AI can help design and evaluate scheduling algorithms.',
'My goal: distributed digital twins that support timely decisions.'
]
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


def text(d,xy,value,font=SMALL,fill=INK,anchor=None):
    d.text(xy,value,font=font,fill=fill,anchor=anchor)

def packet(d,x,y,urgent=False):
    box(d,(x-15,y-15,x+15,y+15),WARM if urgent else PALE,INK if urgent else BLUE,7,2)
    if urgent:text(d,(x,y),'!',LABEL,INK,'mm')

def pathdot(d,points,p,color=BLUE):
    lengths=[math.dist(a,b) for a,b in zip(points,points[1:])];dist=(p%1)*sum(lengths)
    for a,b,l in zip(points,points[1:],lengths):
        if dist<=l:dot(d,mix(a[0],b[0],dist/l),mix(a[1],b[1],dist/l),7,color);return
        dist-=l

def route_map(d,u,mode='rain'):
    # A consistent city map returns in the final shot.
    for x,y,w,h in [(145,237,120,72),(335,233,115,75),(151,411,115,76),(340,411,110,76),(745,237,118,72),(938,237,124,72),(750,414,115,72),(943,415,118,72)]:
        box(d,(x,y,x+w,y+h),WHITE,LINE,8,2)
        for k in range(3):box(d,(x+15+k*29,y+18,x+30+k*29,y+35),LIGHT,LIGHT,2,1)
    normal=[(118,360),(585,360),(1110,360)]
    detour=[(470,360),(590,360),(590,530),(1125,530)]
    line(d,normal,LINE,15);line(d,detour,LINE,15)
    d.ellipse((820,322,1035,395),fill=PALE)
    text(d,(927,421),'Flood risk',SMALL,INK,'mm')
    for i in range(9):
        x=830+i*24;y=265+((u*110+i*19)%70)
        line(d,[(x,y),(x-6,y+16)],BLUE,2)
    if mode in ['predict','resolve']:
        line(d,detour,BLUE,5)
        pathdot(d,detour,u*.8)
        text(d,(850,564),'Alternative route',LABEL,BLUE,'mm')
    if mode=='resolve':
        if u<.25: bx,by=mix(455,555,sm(u/.25)),329
        elif u<.55: bx,by=555,mix(329,499,sm((u-.25)/.3))
        else: bx,by=mix(555,1010,sm((u-.55)/.45)),499
        bus(d,bx,by,.72)
    else:
        bus(d,160+260*sm(u),329,.72)
    dot(d,590,360,10,INK)
    text(d,(592,300),'Decision point',SMALL,INK,'mm')
    if mode=='resolve':
        box(d,(735,164,1085,211),PALE,PALE,12,1)
        text(d,(910,187),'Route ready before the junction',LABEL,BLUE,'mm')

def twin_story(d,u):
    labels=['ROAD','WEATHER','BUS']
    for i,y in enumerate([258,370,482]):
        box(d,(110,y-34,310,y+34),WHITE,LINE,12,2);text(d,(210,y),labels[i],LABEL,INK,'mm')
        pts=[(310,y),(490,y),(575,370)]
        line(d,pts,LINE,3);pathdot(d,pts,u*1.6+i*.23)
    box(d,(575,225,1105,515),WHITE,BLUE,20,3)
    text(d,(840,260),'A SHARED DIGITAL PICTURE',LABEL,BLUE,'mm')
    for i,(x,y) in enumerate([(650,350),(830,330),(1000,405),(780,450)]):
        for xx,yy in [(830,330),(780,450)]:line(d,[(x,y),(xx,yy)],LINE,2)
        dot(d,x,y,13,BLUE if i%2 else GREEN)
    bus(d,825,425,.62)
    text(d,(840,552),'Observe → update → simulate',Fsmall,INK,'mm')

def deadline(d,u):
    text(d,(140,230),'DECISION NEEDED',LABEL,INK)
    line(d,[(145,365),(1130,365)],LINE,8)
    xdeadline=815
    line(d,[(xdeadline,285),(xdeadline,450)],INK,3)
    text(d,(xdeadline,480),'Bus reaches junction',SMALL,INK,'mm')
    x=160+900*sm(u)
    packet(d,x,365,True)
    box(d,(140,520,550,563),WHITE,LINE,8,2)
    text(d,(345,541),'Route simulation is still waiting…',SMALL,INK,'mm')
    if u>.64:
        text(d,(950,270),'Too late',TITLE,INK,'mm')
        text(d,(950,310),'Correct is not enough.',SMALL,INK,'mm')
    else:text(d,(x,315),'Route decision',LABEL,INK,'mm')

def resources(d,u,mode):
    xs=[280,640,1000];names=['EDGE / ROAD','EDGE / DISTRICT','CLOUD']
    for i,x in enumerate(xs):
        box(d,(x-132,380,x+132,507),WHITE,LINE,15,2)
        text(d,(x,490),names[i],LABEL,INK,'mm')
        for j in range(4):box(d,(x-94+j*48,454,x-58+j*48,470),PALE,PALE,4,1)
    line(d,[(280,330),(1000,330)],LINE,3)
    for x in xs:line(d,[(x,330),(x,380)],LINE,3)
    if mode=='congested':
        for j in range(7):packet(d,470+j*58,260,j==5)
        text(d,(640,205),'One queue. Different deadlines.',Fsmall,INK,'mm')
        text(d,(640,554),'Nearby ≠ available     •     Powerful ≠ timely',Fsmall,INK,'mm')
        packet(d,760+35*math.sin(u*4),330,True)
    else:
        urgentx=mix(760,280,sm(min(1,u*1.6)));urgenty=mix(260,452,sm(min(1,u*1.6)))
        packet(d,urgentx,urgenty,True)
        for j in range(5):
            start=(470+j*58,260);target=(xs[1+j%2]-75+(j//2)*50,455)
            v=sm(clip((u-.08*j)/.75))
            packet(d,mix(start[0],target[0],v),mix(start[1],target[1],v))
        text(d,(280,540),'Urgent route decision',LABEL,INK,'mm')
        text(d,(820,540),'Background updates',LABEL,BLUE,'mm')
        if mode in ['agents','adapt']:
            for i,x in enumerate(xs):
                node(d,x,230,60,WHITE,BLUE);dot(d,x,230,8,BLUE)
                line(d,[(x,260),(x,330)],LINE,2)
            text(d,(640,165),'LOCAL AGENTS · SHARED CONSTRAINTS',LABEL,BLUE,'mm')
            for i in range(2):
                pts=[(xs[i]+32,230),(xs[i+1]-32,230)];line(d,pts,LINE,2);pathdot(d,pts,u*2+i*.3)
        else:text(d,(640,190),'Prioritize by urgency and resource availability',Fsmall,INK,'mm')
        if mode=='adapt':
            box(d,(473,294,805,353),BG,WARM,10,2)
            text(d,(640,323),'Connection slows → re-plan',LABEL,INK,'mm')
            pathdot(d,[(640,265),(640,285),(280,285),(280,380)],u*1.2,WARM)

def ai_story(d,u):
    labels=['PROPOSE','SIMULATE','EVALUATE']
    xs=[270,640,1010]
    for i,x in enumerate(xs):
        box(d,(x-130,275,x+130,440),WHITE,BLUE if i==0 else LINE,16,3)
        text(d,(x,310),labels[i],LABEL,BLUE,'mm')
        if i==0:
            for j in range(3):line(d,[(x-65,350+j*22),(x+45-j*14,350+j*22)],BLUE,4)
        elif i==1:
            for j in range(3):node(d,x-60+j*60,375,28,PALE,BLUE)
        else:
            for j,label in enumerate(['Deadlines','Resources','Robustness']):text(d,(x,350+j*27),label,SMALL,INK,'mm')
    for a,b in [(400,510),(770,880)]:
        line(d,[(a,365),(b,365)],LINE,3);pathdot(d,[(a,365),(b,365)],u*2)
    pts=[(1010,440),(1010,505),(270,505),(270,440)]
    line(d,pts,LINE,3);pathdot(d,pts,u,BLUE)
    text(d,(640,550),'Test candidates. Refine the design. Repeat.',Fsmall,INK,'mm')

def frame(index,t):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);dur=lengths[index];u=clip(t/dur)
    text(d,(65,37),'MENGBING ZHOU  /  RESEARCH VISION',SMALL,INK)
    text(d,(1215,37),f'{index+1:02d} / 10',SMALL,INK,'ra')
    line(d,[(65,74),(1215,74)],LINE,2)
    text(d,(65,103),HEADINGS[index],TITLE,INK)
    if index==0:route_map(d,u)
    elif index==1:twin_story(d,u)
    elif index==2:route_map(d,u,'predict')
    elif index==3:deadline(d,u)
    elif index==4:resources(d,u,'congested')
    elif index==5:resources(d,u,'scheduled')
    elif index==6:resources(d,u,'agents')
    elif index==7:resources(d,u,'adapt')
    elif index==8:ai_story(d,u)
    else:route_map(d,u,'resolve')
    # Persistent readable subtitles, rather than captions disappearing between slides.
    text(d,(640,626),CAPTIONS[index],F,'#1F2A44','mm')
    text(d,(65,683),'Illustrative scenario · Research vision, not experimental results',SMALL,'#68778C')
    text(d,(1215,683),'University of Amsterdam',SMALL,'#68778C','ra')
    line(d,[(65,710),(65+1150*(starts[index]+t)/90,710)],BLUE,3)
    return im

def timestamp(t):
    return f'00:{int(t)//60:02d}:{int(t)%60:02d}.000'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    if args.preview:
        sheet=Image.new('RGB',(960,270*5),WHITE)
        for i in range(10):sheet.paste(frame(i,lengths[i]*.72).resize((480,270)),((i%2)*480,(i//2)*270))
        sheet.save(ROOT/'research_vision_storyboard.jpg');return
    ff=shutil.which('ffmpeg')
    if not ff:
        import imageio_ffmpeg
        ff=imageio_ffmpeg.get_ffmpeg_exe()
    output=ROOT/'research_vision_story_90s.mp4'
    cmd=[ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(DURATION*FPS):
        t=n/FPS;idx=max(i for i,s in enumerate(starts) if s<=t);local=t-starts[idx]
        im=frame(idx,local)
        # Short dissolves keep the pace and preserve a continuous visual thread.
        if idx and local<.28:
            im=Image.blend(frame(idx-1,lengths[idx-1]-.28+local),im,sm(local/.28))
        proc.stdin.write(im.tobytes())
        if n%(FPS*10)==0:print(f'Rendered {int(t)} / 90 seconds',flush=True)
    proc.stdin.close()
    if proc.wait():raise RuntimeError('Video encoding failed')
    vtt='WEBVTT\n\n'+'\n\n'.join(f'{timestamp(starts[i])} --> {timestamp(starts[i]+lengths[i])}\n{c}' for i,c in enumerate(CAPTIONS))
    (ROOT/'research_vision_story_90s.vtt').write_text(vtt)
    print(output,flush=True)
if __name__=='__main__':main()
