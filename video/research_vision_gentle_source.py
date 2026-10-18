"""192-second challenge-led research story. Original palette; illustrative scenario, no performance claims.
Run: python research_vision_gentle_source.py
Dependencies: Pillow, numpy, imageio-ffmpeg (or ffmpeg on PATH).
Outputs are relative to this script. Original video remains unchanged.
"""
import math, subprocess, os, shutil, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1280,720,24
DURATION=192
MOTION_STATUS=[]
MOTION_DURATION=8.0
TRANSITION_FRAMES=20
TRANSITION_DURATION=TRANSITION_FRAMES/FPS
ROOT=Path(__file__).resolve().parent
BG='#F7F9FC'; INK='#1F2A44'; BLUE='#4F7DF3'; PALE='#DCE7FF'; LINE='#D9E2EC'; MUTED='#A7B6CC'; LIGHT='#ECF2F8'; WHITE='#FFFFFF'; GREEN='#7DAE9B'; WARM='#E8C8A8'
font=next(str(p) for p in [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists())
bold=next(str(p) for p in [Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')] if p.exists())
F=ImageFont.truetype(font,28); Fsmall=ImageFont.truetype(font,23)
TITLE=ImageFont.truetype(bold,40); LABEL=ImageFont.truetype(bold,18); SMALL=ImageFont.truetype(font,17); BIG=ImageFont.truetype(bold,58)
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
    lengths=[math.dist(a,b) for a,b in zip(points,points[1:])];dist=clip(p)*sum(lengths)
    MOTION_STATUS.append(p>=1-1e-9)
    for a,b,l in zip(points,points[1:],lengths):
        if dist<=l:dot(d,mix(a[0],b[0],dist/l),mix(a[1],b[1],dist/l),7,color);return
        dist-=l


# Read the film as one evolving problem, not a list of research keywords.
lengths=[8]*24
starts=np.cumsum([0]+lengths[:-1]).tolist()
CAPTIONS=['When we take the bus to work, changing road conditions can make us late.', 'A digital twin system can use sensor data to help the bus choose a route.', 'Choosing the right route in time is not as simple as it seems.', 'If the digital twin system has not received the latest road conditions,', 'even an on-time instruction can be unhelpful or lead to costly mistakes.', 'Could we solve this by updating every digital state immediately?', 'At scale, these updates compete for limited bandwidth.', 'Trying to send everything can leave important changes waiting.', 'The key is that different updates have different value for each task.', 'Age and frequency of change offer clues, but do not capture the full picture.', 'So we need to prioritize the updates that matter to the decision.', 'Alongside these updates, digital twin systems run many computational tasks.', 'These tasks are distributed across edge and cloud resources.', 'With limited resources and tight deadlines, deciding what runs where becomes difficult.', 'Task execution and state updates must work together to meet diverse requirements.', 'To address these challenges, we study scheduling through modeling and theoretical optimization.', 'We then develop and evaluate methods for task execution and state synchronization.', 'We will also explore agentic methods that adapt scheduling as conditions change.', 'Across these settings, scheduling objectives and constraints vary widely.', 'No single scheduling method is best for every combination of requirements.', 'This also motivates us to explore how AI can generate scheduling algorithms.', 'These AI-generated candidates must be tested against constraints and performance goals.', 'Together, these efforts help digital twin systems turn data into timely, useful decisions.', 'Our goal is to build better digital twin systems that improve everyday life.']
assert sum(lengths)==DURATION

def label(d,xy,s,fill=INK,font=LABEL):d.text(xy,s,font=font,fill=fill,anchor='mm')
def check(d,x,y):line(d,[(x-14,y),(x-3,y+12),(x+21,y-16)],GREEN,5)
def cross(d,x,y):
    line(d,[(x-12,y-12),(x+12,y+12)],INK,4);line(d,[(x-12,y+12),(x+12,y-12)],INK,4)
def clock(d,x,y,p):
    d.ellipse((x-30,y-30,x+30,y+30),fill=WHITE,outline=INK,width=3)
    a=-math.pi/2+p*math.tau;line(d,[(x,y),(x+23*math.cos(a),y+23*math.sin(a))],BLUE,3)
def update(d,x,y,urgent=False):
    box(d,(x-13,y-13,x+13,y+13),WARM if urgent else PALE,INK if urgent else BLUE,6,2)
    if urgent:label(d,(x,y),'!')
def travel(d,points,p,urgent=False):
    lens=[math.dist(a,b) for a,b in zip(points,points[1:])];distance=clip(p)*sum(lens)
    MOTION_STATUS.append(p>=1-1e-9)
    for a,b,l in zip(points,points[1:],lens):
        if distance<=l:
            update(d,mix(a[0],b[0],distance/l),mix(a[1],b[1],distance/l),urgent);return
        distance-=l

def mini_map(d,x,y,wet=False,route=False,progress=0):
    box(d,(x,y,x+480,y+300),WHITE,LINE,16,2)
    for xx,yy in [(35,35),(185,35),(340,35),(35,215),(340,215)]:
        box(d,(x+xx,y+yy,x+xx+75,y+yy+48),LIGHT,LINE,5,1)
    pts=[(x+25,y+150),(x+455,y+150)];line(d,pts,LINE,10)
    detour=[(x+210,y+150),(x+210,y+260),(x+455,y+260)];line(d,detour,LINE,10)
    if wet:
        d.ellipse((x+300,y+118,x+430,y+177),fill=PALE)
        for j in range(6):
            yy=y+75+(progress*70+j*14)%70
            line(d,[(x+300+j*23,yy),(x+294+j*23,yy+13)],BLUE,2)
    if route=='straight':line(d,pts,BLUE,4)
    elif route:line(d,detour,BLUE,4)
    bus(d,x+40+min(progress,1)*70,y+128,.48)
    dot(d,x+210,y+150,6,INK)

def sensors(d,u):
    # Explicit physical sensing devices, linked to the outgoing data stream.
    x,y=175,265
    box(d,(x-32,y-18,x+24,y+14),WHITE,BLUE,5,2)
    d.polygon([(x+24,y-10),(x+40,y-19),(x+40,y+16),(x+24,y+7)],fill=PALE,outline=BLUE)
    line(d,[(x-10,y+14),(x-10,y+28)],INK,3)
    label(d,(x,311),'TRAFFIC CAMERA',font=SMALL)
    x,y=465,262
    d.polygon([(x-28,y-18),(x+28,y-18),(x+12,y+2),(x-12,y+2)],fill=PALE,outline=BLUE)
    box(d,(x-12,y+2,x+12,y+30),WHITE,BLUE,3,2)
    for j in range(3):
        yy=y-46+(u*50+j*12)%25
        line(d,[(x-15+j*15,yy),(x-18+j*15,yy+8)],BLUE,2)
    label(d,(x,311),'RAIN GAUGE',font=SMALL)
    for start in [(215,265),(490,265)]:
        pts=[start,(550,start[1]),(550,345),(565,345)]
        line(d,pts,PALE,2);pathdot(d,pts,u*2)
    label(d,(640,302),'SENSOR DATA',font=SMALL)

def worlds(d,u,shot):
    wet=shot>=3
    label(d,(325,154),'PHYSICAL WORLD');label(d,(955,154),'DIGITAL TWIN SYSTEM',BLUE)
    mini_map(d,85,195,wet=wet,progress=u)
    sensors(d,u)
    mini_map(d,715,195,wet=(shot>=23 and u>.35),route=('straight' if shot in [1,2,3,4] else shot>=23),progress=u)
    pts=[(565,345),(715,345)];line(d,pts,LINE,3)
    if shot<3 or shot>=23:travel(d,pts,u*2,wet)
    else:
        update(d,620,345,True)
        line(d,[(660,325),(660,365)],INK,3)
    if shot==2:
        clock(d,1000,535,u);check(d,1080,535)
    if shot in [3,4]:
        # Explicitly different state timestamps, with an advancing physical state.
        label(d,(325,530),'NOW',INK);label(d,(955,530),'EARLIER STATE',INK)
    if shot==23:
        label(d,(640,550),'Observe  →  update  →  compute  →  act',BLUE,Fsmall)

def bandwidth(d,u,shot):
    for r in range(3):
        for c in range(4):
            x=130+c*90;y=220+r*100
            node(d,x,y,42,WHITE,BLUE)
            dot(d,x,y,5,BLUE)
    box(d,(770,235,1150,465),WHITE,BLUE,15,3)
    # A narrow shared channel instead of a wall of explanatory labels.
    line(d,[(470,320),(750,320)],LINE,4);line(d,[(470,375),(750,375)],LINE,4)
    label(d,(600,267),'LIMITED BANDWIDTH',INK)
    for j in range(9):
        if shot==5:
            travel(d,[(400,220+(j%3)*100),(510,347),(770,347)],u*.9+j*.11,j==7)
        else:
            x=485+(j%6)*43;y=347 if j<6 else 420
            update(d,x,y,j==7)
    travel(d,[(760,347),(1090,347)],u*.8)
    if shot==7:
        clock(d,610,500,u)
        update(d,670,500,True)
    label(d,(960,500),'DIGITAL STATES',BLUE)

def relevance(d,u,shot):
    mini_map(d,110,210,wet=True,route=True,progress=u)
    # Contrast update frequency with relevance to the current route.
    node(d,800,240,50,WHITE,BLUE);clock(d,890,240,.9)
    label(d,(1005,215),'Frequent changes',font=SMALL)
    label(d,(1005,245),'Away from the route',font=SMALL)
    node(d,800,430,50,WHITE,INK);update(d,800,430,True)
    label(d,(980,430),'On this route',font=SMALL)
    if shot==8:
        line(d,[(600,360),(740,360)],LINE,3);label(d,(670,330),'?',BLUE,TITLE)
    elif shot==9:
        line(d,[(600,265),(760,240)],LINE,3)
        line(d,[(600,400),(760,430)],BLUE,4)
        d.arc((770,400,830,460),0,int(u*360),fill=INK,width=3)
    else:
        pts=[(775,430),(650,430),(650,365),(530,365)]
        line(d,pts,BLUE,3);travel(d,pts,u*1.3,True)
        check(d,1020,500)

def machine(d,x,y,name):
    box(d,(x,y,x+270,y+170),WHITE,LINE,16,2);label(d,(x+135,y+140),name)
    for j in range(4):box(d,(x+30+j*54,y+55,x+67+j*54,y+74),PALE,PALE,4,1)

def tradeoffs(d,u,shot):
    machine(d,170,310,'EDGE');machine(d,840,310,'CLOUD')
    update(d,640,200,True)
    for x in [305,975]:line(d,[(640,215),(x,275),(x,310)],LINE,3)
    if shot==11:travel(d,[(640,200),(305,275),(305,365)],u,True)
    if shot>=12:
        for j in range(4):update(d,205+j*60,270)
        travel(d,[(640,200),(975,275),(975,365)],u*.7,True)
    if shot==13:
        # A fixed energy budget makes the processing/energy trade-off visible.
        box(d,(510,415,740,465),WHITE,INK,6,2)
        box(d,(740,430,750,450),INK,INK,1,1)
        amount=int(200*(1-.75*u))
        box(d,(520,425,520+max(4,amount),455),WARM,WARM,3,1)
        label(d,(625,500),'ENERGY BUDGET',font=SMALL)
    if shot==14:
        clock(d,620,370,u)
        update(d,565,490,True);node(d,680,490,30,PALE,BLUE)
        label(d,(625,550),'State updates + service execution',BLUE,Fsmall)

def algorithm(d,x,y,variant=0):
    box(d,(x-75,y-65,x+75,y+65),WHITE,BLUE,12,2)
    pts=[(x,y-32),(x-35,y+28),(x+35,y+28)]
    for a,b in [(0,1),(0,2)]:line(d,[pts[a],pts[b]],BLUE,3)
    for xx,yy in pts:dot(d,xx,yy,7,BLUE)
    if variant:line(d,[(x-35,y+28),(x+35,y+28)],INK,3)

def design(d,u,shot):
    if shot in [15,16,17]:
        algorithm(d,260,350)
        for j,x in enumerate([620,860,1100]):
            box(d,(x-85,255,x+85,445),WHITE,LINE,12,2)
            if j==0:clock(d,x,350,u)
            elif j==1:
                box(d,(x-45,328,x+45,372),WARM,INK,4,2)
            else:
                node(d,x-32,325,25);node(d,x+32,375,25);line(d,[(x-18,325),(x+20,375)],BLUE,3)
            if shot>=16:
                if j==0:check(d,x,480)
                else:cross(d,x,480)
        for x in [620,860,1100]:line(d,[(340,350),(x-90,350)],LINE,2)
        if shot==17:
            # Design iterations, not an implication that one algorithm works everywhere.
            algorithm(d,260,350,int(u*4)%2)
            d.arc((160,245,360,455),-90,-90+int(u*340),fill=BLUE,width=3)
    else:
        for j in range(3):
            box(d,(110+j*20,240+j*30,260+j*20,410+j*30),WHITE,LINE,8,2)
            for k in range(3):line(d,[(140+j*20,280+j*30+k*24),(230+j*20,280+j*30+k*24)],BLUE,3)
        center=(590,350)
        for j in range(6):
            a=j*math.tau/6;pt=(590+75*math.cos(a),350+75*math.sin(a));line(d,[center,pt],PALE,3);dot(d,*pt,10,BLUE)
        dot(d,*center,18,BLUE)
        line(d,[(330,350),(500,350)],LINE,3);travel(d,[(330,350),(500,350)],u)
        algorithm(d,970,350,int(u*3)%2)
        line(d,[(680,350),(885,350)],LINE,3);travel(d,[(680,350),(885,350)],u)
        if shot==21:
            pts=[(970,425),(970,525),(590,525),(590,440)];line(d,pts,BLUE,3);travel(d,pts,u)
        label(d,(210,545),'KNOWLEDGE',font=SMALL)
        label(d,(590,545 if shot!=21 else 200),'AI DESIGN',font=SMALL)
        label(d,(970,545 if shot!=21 else 200),'CANDIDATES',font=SMALL)

def testing(d,u):
    for j,y in enumerate([220,365,510]):
        algorithm(d,235,y)
        line(d,[(315,y),(1090,y)],LINE,3)
        x=mix(360,1030,sm(clip(u*1.7-j*.18)))
        update(d,x,y,j==0)
        line(d,[(730,y-40),(730,y+40)],INK,3)
        if u>.65:
            if j==0:cross(d,1135,y)
            else:check(d,1135,y)
    label(d,(235,135),'AI-GENERATED ALGORITHMS',BLUE)
    label(d,(730,150),'CONSTRAINTS AND PERFORMANCE',font=SMALL)

def adaptive(d,u):
    label(d,(640,150),'AGENTIC ADAPTIVE SCHEDULING',BLUE)
    label(d,(640,540),'Agents observe, coordinate and adapt',font=Fsmall)
    pts=[(290,310),(640,240),(990,310)]
    for x,y in pts:node(d,x,y,55);dot(d,x,y,8,BLUE)
    for a,b in [(0,1),(1,2)]:line(d,[pts[a],pts[b]],LINE,3)
    cross(d,815,275)
    alternative=[pts[0],(290,470),(990,470),pts[2]]
    line(d,alternative,BLUE,3);travel(d,alternative,u)
    clock(d,640,400,u)

def research_methods(d,u,shot):
    # Keep scheduling and optimization visible as the main research programme.
    if shot==17:
        for i,x in enumerate([270,640,1010]):
            box(d,(x-120,240,x+120,450),WHITE,LINE,16,2)
            label(d,(x,490),['MODEL','OPTIMIZE','VALIDATE'][i],BLUE)
        clock(d,270,340,u)
        algorithm(d,640,340,int(u*3)%2)
        check(d,1010,340)
        for a,b in [(395,515),(765,885)]:
            line(d,[(a,345),(b,345)],LINE,3)
            travel(d,[(a,345),(b,345)],u*1.5)
    elif shot==18:
        box(d,(140,230,570,470),WHITE,LINE,16,2)
        box(d,(710,230,1140,470),WHITE,LINE,16,2)
        for i in range(3):
            line(d,[(190,290+i*55),(520,290+i*55)],LINE,3)
            travel(d,[(190,290+i*55),(520,290+i*55)],u+i*.2,i==0)
        for i in range(3):
            node(d,790+i*110,350,44,WHITE,BLUE)
        travel(d,[(790,350),(1010,350)],u,True)
        label(d,(355,510),'SERVICE EXECUTION',BLUE)
        label(d,(925,510),'STATE SYNCHRONIZATION',BLUE)
    else:
        labels=['SCHEDULING','OPTIMIZATION','AI-ASSISTED DESIGN']
        for i,x in enumerate([270,640,1010]):
            box(d,(x-135,240,x+135,450),WHITE,LINE,16,2)
            label(d,(x,495),labels[i],BLUE)
        clock(d,270,345,u)
        algorithm(d,640,345)
        for i in range(6):
            a=i*math.tau/6;p=(1010+65*math.cos(a),345+65*math.sin(a))
            line(d,[(1010,345),p],PALE,3);dot(d,*p,8,BLUE)
        dot(d,1010,345,14,BLUE)

def draw_caption(d, sentence):
    words=sentence.split(); lines=[]; current=''
    for word in words:
        candidate=(current+' '+word).strip()
        if d.textlength(candidate,font=F)>1120:
            lines.append(current);current=word
        else:current=candidate
    lines.append(current)
    for j,value in enumerate(lines):
        label(d,(640,634+(j-(len(lines)-1)/2)*36),value,font=F)

def frame(i,t):
    MOTION_STATUS.clear()
    u=t/MOTION_DURATION;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    caption_index=i
    i=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 15, 16, 20, 21, 22, 23][i]
    if i<5 or i==23:worlds(d,u,i)
    elif i<8:bandwidth(d,u,i)
    elif i<11:relevance(d,u,i)
    elif i<15:tradeoffs(d,u,i)
    elif i in [15,16]:design(d,u,i)
    elif i in [17,18]:research_methods(d,u,i)
    elif i==19:adaptive(d,u)
    elif i==20:design(d,u,i)
    elif i==21:testing(d,u)
    elif i==22:worlds(d,u,23)
    draw_caption(d,CAPTIONS[caption_index])
    if i==0:
        d.text((65,40),'Mengbing Zhou · Research vision',font=SMALL,fill=INK)
    if i==23:label(d,(640,686),'Mengbing Zhou · University of Amsterdam',font=SMALL)
    return im

def timeline_frame(t):
    i=max(j for j,start in enumerate(starts) if start<=t+1e-8)
    local=t-starts[i]
    if local<lengths[i]-1e-8 or i==len(lengths)-1:
        return frame(i,local)
    # Keep the scene visible throughout; only captions fade sequentially.
    p=clip((local-lengths[i]+1/FPS)/TRANSITION_DURATION)
    old=frame(i,lengths[i]-1/FPS)
    new=frame(i+1,0)
    result=Image.blend(old,new,sm(p))
    band=(0,595,W,670)
    blank=Image.new('RGB',(W,75),BG)
    if p<=.5:
        caption_band=Image.blend(old.crop(band),blank,sm(p*2))
    else:
        caption_band=Image.blend(blank,new.crop(band),sm((p-.5)*2))
    result.paste(caption_band,(0,595))
    return result


def timestamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}.{ms%1000:03d}'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    if args.preview:
        for sheetindex in range(2):
            sheet=Image.new('RGB',(960,270*6),WHITE)
            for j in range(12):
                i=sheetindex*12+j
                sheet.paste(frame(i,lengths[i]*.76).resize((480,270)),((j%2)*480,(j//2)*270))
            sheet.save(ROOT/f'research_vision_challenges_board_{sheetindex+1}.jpg')
        return
    ff=shutil.which('ffmpeg')
    if not ff:
        import imageio_ffmpeg
        ff=imageio_ffmpeg.get_ffmpeg_exe()
    output=ROOT/'research_vision_gentle_silent_temp.mp4'
    proc=subprocess.Popen([ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],stdin=subprocess.PIPE)
    for n in range(round(DURATION*FPS)):
        t=n/FPS;im=timeline_frame(t)
        proc.stdin.write(im.tobytes())
        if n%(FPS*15)==0:print(f'Rendered {int(t)} / {DURATION} seconds',flush=True)
    proc.stdin.close()
    if proc.wait():raise RuntimeError('Encoding failed')
    (ROOT/'research_vision_gentle.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{timestamp(starts[i])} --> {timestamp(starts[i]+lengths[i])}\n{c}' for i,c in enumerate(CAPTIONS)))
    frame(4,2).save(ROOT/'research_vision_gentle_poster.jpg')
    music=ROOT/'polytunes-heroes-never-die-617232.mp3'
    assert music.is_file(), 'Missing supplied background music'
    final=ROOT/'research_vision_gentle.mp4'
    subprocess.run([ff,'-y','-loglevel','error','-i',str(output),'-i',str(music),'-i',str(music),
                    '-filter_complex',f'[1:a]atrim=start=0:end=144,asetpts=PTS-STARTPTS[m1];[2:a]atrim=start=24,asetpts=PTS-STARTPTS[m2];[m1][m2]acrossfade=d=3:c1=tri:c2=tri,loudnorm=I=-22:TP=-3:LRA=7,afade=t=in:st=0:d=1.5,afade=t=out:st={DURATION-4}:d=4[music]',
                    '-map','0:v:0','-map','[music]','-c:v','copy','-c:a','aac','-b:a','160k',
                    '-ar','44100','-t',str(DURATION),
                    '-movflags','+faststart',str(final)],check=True)
    output.unlink() # Only the intermediate produced by this run.
    print(final)
def resolve_scene_timings():
    global lengths, starts, DURATION
    lengths=[]; report=[]
    for i in range(len(CAPTIONS)):
        n=8*FPS
        while True:
            frame(i,n/FPS)
            if all(MOTION_STATUS):break
            n+=1
            if n>30*FPS:raise RuntimeError(f'Scene {i+1} never completes')
        # Let viewers see the arrived state before the cut; decorative loops
        # such as rain and clock hands do not block scene completion.
        end_frame=n+(6 if MOTION_STATUS else 0)
        lengths.append(end_frame/FPS)
        report.append(f'{i+1:02d}  completed at {n/FPS:.3f}s  cut at {end_frame/FPS:.3f}s  {CAPTIONS[i]}')
    starts=np.cumsum([0]+[v+TRANSITION_DURATION for v in lengths[:-1]]).tolist()
    DURATION=round((sum(lengths)+(len(lengths)-1)*TRANSITION_DURATION)*FPS)/FPS
    (ROOT/'research_vision_gentle_timing.txt').write_text('Critical motion is checked at every frame. Minimum scene duration 8 seconds. Additional 0.833-second cross-dissolve transitions follow completed scenes.\n\n'+'\n'.join(report)+f'\n\nTotal {DURATION:.3f} seconds.\n')

if __name__=='__main__':
    resolve_scene_timings()
    main()
