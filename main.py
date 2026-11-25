import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; BG=(250,246,236); INK=(20,20,20); RED=(178,34,34); NAVY=(24,48,96); GOLD=(176,132,32)
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
SER=lambda s: F('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',s)
SAN=lambda s: F('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',s)
SAB=lambda s: F('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s)
def wrap(d,t,f,mw):
    words,lines,cur=t.split(),[],''
    for w in words:
        x=(cur+' '+w).strip()
        if d.textlength(x,font=f)<=mw: cur=x
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def txt(d,x,y,t,f,fill=INK,anchor='la'):
    d.text((x,y),t,font=f,fill=fill,anchor=anchor)
def chip(d,x,y,t):
    c={'CONFIRMED':(34,120,60),'OFFICIAL':(24,80,180),'REPORTED':(90,90,90),'CLAIM':(200,110,0),'ONGOING':(170,140,0)}.get(t,(90,90,90)); w=d.textlength(t,font=SAB(7))+8
    d.rounded_rectangle([x,y,x+w,y+11],2,fill=c); d.text((x+4,y+1),t,font=SAB(7),fill=(255,255,255)); return x+w+4
def scene(d,x,y,w,h,kind):
    d.rectangle([x,y,x+w,y+h],fill=(214,228,238)); d.rectangle([x,y+h-14,x+w,y+h],fill=(120,140,110))
    if kind=='tower':
        d.rectangle([x+w*0.42,y+8,x+w*0.58,y+h-14],fill=(40,60,110)); d.polygon([(x+w*0.42,y+8),(x+w*0.5,y-2),(x+w*0.58,y+8)],fill=(200,60,40))
        for i in range(4): d.rectangle([x+w*0.45,y+16+i*10,x+w*0.55,y+22+i*10],fill=(250,220,120))
        d.ellipse([x+w*0.62,y+14,x+w*0.78,y+30],fill=(255,180,60)); d.ellipse([x+w*0.66,y+18,x+w*0.74,y+26],fill=(255,90,40))
        d.rectangle([x+w*0.08,y+h-34,x+w*0.34,y+h-14],fill=(70,80,100)); d.rectangle([x+w*0.68,y+h-40,x+w*0.94,y+h-14],fill=(90,100,120))
    elif kind=='gate':
        d.rectangle([x+w*0.15,y+18,x+w*0.85,y+h-14],fill=(150,40,40)); d.rectangle([x+w*0.42,y+38,x+w*0.58,y+h-14],fill=(250,246,236))
        d.polygon([(x+w*0.15,y+18),(x+w*0.5,y+2),(x+w*0.85,y+18)],fill=(120,30,30)); d.rectangle([x+w*0.30,y+52,x+w*0.70,y+62],fill=(255,255,255))
    elif kind=='court':
        d.rectangle([x+w*0.10,y+20,x+w*0.90,y+h-14],fill=(200,190,170)); d.polygon([(x+w*0.10,y+20),(x+w*0.5,y+4),(x+w*0.90,y+20)],fill=(150,140,125))
        for i in range(4): d.rectangle([x+w*0.16+i*w*0.18,y+30,x+w*0.28+i*w*0.18,y+h-14],fill=(240,235,220))
        d.ellipse([x+w*0.42,y+34,x+w*0.58,y+50],fill=(200,40,40)); d.text((x+w*0.44,y+36),'10/12',font=SAB(8),fill=(255,255,255))
    elif kind=='drones':
        d.rectangle([x,y,x+w,y+h],fill=(30,32,60))
        for i,(px,py) in enumerate([(0.2,0.3),(0.5,0.2),(0.75,0.35)]): d.ellipse([x+w*px-4,y+h*py-3,x+w*px+4,y+h*py+3],fill=(255,200,80))
        d.polygon([(x+w*0.3,y+h-14),(x+w*0.42,y+h*0.25),(x+w*0.5,y+h-14)],fill=(90,90,110)); d.polygon([(x+w*0.55,y+h-14),(x+w*0.65,y+h*0.35),(x+w*0.78,y+h-14)],fill=(70,70,90))
        d.ellipse([x+w*0.6,y+h*0.12,x+w*0.72,y+h*0.28],fill=(255,140,40))
    elif kind=='trophy':
        d.ellipse([x+w*0.38,y+h*0.05,x+w*0.62,y+h*0.55],fill=(230,190,40)); d.rectangle([x+w*0.46,y+h*0.55,x+w*0.54,y+h*0.72],fill=(200,160,30)); d.rectangle([x+w*0.38,y+h*0.72,x+w*0.62,y+h*0.82],fill=(200,160,30))
        d.rectangle([x+w*0.08,y+h-14,x+w*0.30,y+h-4],fill=(0,120,60)); d.rectangle([x+w*0.70,y+h-14,x+w*0.92,y+h-4],fill=(200,40,40))
    elif kind=='ship':
        d.rectangle([x,y,x+w,y+h],fill=(90,160,200)); d.rectangle([x+w*0.15,y+h*0.65,x+w*0.85,y+h*0.9],fill=(180,60,40))
        for i in range(4): d.rectangle([x+w*0.22+i*w*0.16,y+h*0.32,x+w*0.34+i*w*0.16,y+h*0.65],fill=(40,90,140))
        d.polygon([(x+w*0.55,y+h*0.32),(x+w*0.62,y+h*0.05),(x+w*0.66,y+h*0.32)],fill=(60,60,60))
    elif kind=='chart':
        d.rectangle([x,y,x+w,y+h],fill=(245,245,240)); d.line([(x+6,y+h-8),(x+w-6,y+8)],fill=(34,120,60),width=4)
        d.line([(x+6,y+h-6),(x+w-6,y+h-6)],fill=INK,width=2); d.text((x+8,y+2),'50,018',font=SAB(11),fill=(34,120,60))
    elif kind=='data':
        d.rectangle([x,y,x+w,y+h],fill=(40,20,20)); d.rectangle([x+w*0.1,y+h*0.15,x+w*0.9,y+h*0.85],fill=(120,20,20))
        d.text((x+w*0.18,y+h*0.35),'CODE RED',font=SAB(10),fill=(255,255,255))
    elif kind=='heli':
        d.ellipse([x+w*0.3,y+h*0.3,x+w*0.7,y+h*0.8],fill=(60,90,60)); d.line([(x+w*0.2,y+h*0.25),(x+w*0.8,y+h*0.25)],fill=INK,width=3); d.rectangle([x+w*0.62,y+h*0.5,x+w*0.92,y+h*0.62],fill=(60,90,60))
    elif kind=='market':
        d.rectangle([x+w*0.1,y+h*0.5,x+w*0.9,y+h-4],fill=(200,170,140)); d.polygon([(x+w*0.1,y+h*0.5),(x+w*0.5,y+2),(x+w*0.9,y+h*0.5)],fill=(178,34,34))
        d.rectangle([x+w*0.42,y+h*0.6,x+w*0.58,y+h-4],fill=(90,60,40))
    elif kind=='desert':
        d.rectangle([x,y,x+w,y+h],fill=(240,220,170)); d.polygon([(x,y+h-14),(x+w*0.4,y+h-44),(x+w*0.7,y+h-14)],fill=(220,190,120)); d.polygon([(x+w*0.5,y+h-14),(x+w*0.85,y+h-50),(x+w,y+h-14)],fill=(205,170,100))
    elif kind=='rocket':
        d.rectangle([x,y,x+w,y+h],fill=(20,24,60)); d.polygon([(x+w*0.45,y+h*0.05),(x+w*0.5,y),(x+w*0.55,y+h*0.05)],fill=(255,255,255)); d.rectangle([x+w*0.45,y+h*0.05,x+w*0.55,y+h*0.6],fill=(230,230,230))
        d.ellipse([x+w*0.46,y+h*0.2,x+w*0.54,y+h*0.35],fill=(60,120,220)); d.polygon([(x+w*0.45,y+h*0.6),(x+w*0.5,y+h*0.95),(x+w*0.55,y+h*0.6)],fill=(255,150,40))
        for sx,sy in [(0.15,0.6),(0.3,0.25),(0.8,0.3),(0.7,0.7)]: d.ellipse([x+w*sx-1,y+h*sy-1,x+w*sx+1,y+h*sy+1],fill=(255,255,255))
HERO=[('1','RIYADH','MIDDLE EAST','CONFIRMED','Houthi drone hits Riyadh\u2019s tallest tower again, 11 hurt','Drone hits the PIF tower, the city\u2019s tallest, for the second time in a week. At least 11 hurt: 2 Saudi, 2 Indian, 3 Nepali, 4 Egyptian.','Reuters \u00b7 AP','tower'),('2','SHANGHAI','ASIA','OFFICIAL','China probes Shanghai party chief Chen Jining','Chen Jining, 62, is probed for \u201cserious violations\u201d. He is the fourth Politburo member to fall under investigation this year.','CCDI \u00b7 Xinhua','gate'),('3','NEW YORK','US / TECH','CONFIRMED','Huawei guilty on 10 of 12 counts','A US jury convicts Huawei on 10 of 12 counts, including trade-secret theft and bank fraud. It is cleared of racketeering. Sentencing in Sep 2027.','US District Court','court')]
CARDS=[('4','ZAPORIZHZHIA','EUROPE / WAR','REPORTED','Russian attacks kill 9 across Ukraine in a day','Russia launches 96 drones; 73 are shot down or jammed. Nine are killed and 81 wounded.','Kyiv officials','drones'),('5','CAS \u00b7 SENEGAL','AFRICA / SPORT','OFFICIAL','CAS hands Senegal back the AFCON title','CAS rules Morocco forfeit 3\u20130, so Senegal win 1\u20130 and take the AFCON title back.','CAS','trophy'),('6','HORMUZ','MIDDLE EAST','REPORTED','IRGC attacks container ship in Hormuz','IRGC hits a container ship at 18:58 UTC; navigation is off and a zone north of Khasab is closed.','UKMTO','ship'),('7','NEW YORK','WORLD / MARKETS','CONFIRMED','Dow closes above 50,000 for the first time','Dow closes at 50,018, first above 50,000. Taiex jumps a record +8.99% to 40,122.','NYSE \u00b7 TWSE','chart'),('8','REDMOND','WORLD / TECH','REPORTED','Microsoft declares \u2018Code Red\u2019 after historic outage','After a 24-hour outage, the worst in Exchange Online history, Microsoft targets global recovery within 1 hour.','Reuters','data'),('9','ESKISEHIR','EUROPE','REPORTED','Turkish military helicopter crash kills 5','An AS-532 military helicopter crashes in Eskisehir at 19:52 UTC, killing all five people on board.','Turkish officials','heli'),('10','CARTAGENA','AMERICAS','REPORTED','Supermarket hostages: 25 held in Cartagena','Gunmen hold 25 people hostage in a Cartagena supermarket; five elderly women are freed and airport landings pause.','Colombian officials','market'),('11','ADEN','MIDDLE EAST','REPORTED','Houthis advance within 60 km of Aden','Houthi forces advance to within 60 km of Aden in Yemen, pressing south toward the port city.','Wires','desert'),('12','LAHJ','MIDDLE EAST','REPORTED','Saudi strikes kill 25, wound 6 in Yemen','Saudi strikes on a bus and truck in Wadi Maabaq, Lahj, kill or leave missing 25 people and wound six.','Yemeni officials','desert'),('13','JIUQUAN','WORLD / SPACE','OFFICIAL','China names first foreign astronaut for Tiangong','Crew: Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali of Pakistan, the first foreigner on Tiangong.','CMSA','rocket')]
NUMS=[('11','HURT IN RIYADH'),('9','KILLED IN UKRAINE'),('50,018','DOW CLOSE'),('+8.99%','TAIEX RECORD'),('25','KILLED IN LAHJ'),('26','CIKANDE TOLL'),('10/12','HUAWEI COUNTS'),('96','DRONES AT UKRAINE')]
UTC=[('00:30','Zelensky urges talks'),('02:15','NATO vows space defence'),('08:16','Hanoi hot-pot blast'),('10:42','Saudi strikes Yemen'),('14:27','Riyadh tower hit'),('16:51','Houthis 60 km from Aden'),('18:58','Hormuz ship attack'),('20:41','Huawei guilty')]
ALSO=[('14','Ankara','Haftar visits Turkey for the first time','REPORTED'),('15','London','UK sanctions Houthis + 4 officials','OFFICIAL'),('16','Villavicencio','Car bomb injures 23','REPORTED'),('17','Gaza','Israel kills Hamas internal security chief','REPORTED'),('18','Baghdad','Iraq orders federal control of Kurdish oilfields','OFFICIAL'),('19','Gaza','Meningitis epidemic alert: 272 cases in October','OFFICIAL'),('20','DR Congo','Missing Cessna 208; rebels claim shootdown','CLAIM'),('21','Hanoi','Hot-pot explosion kills at least 6','REPORTED'),('22','Gulf of Finland','Ukraine hits Russian ship Sparta II','REPORTED'),('23','Kuala Lumpur','Malaysia to return migrants to Myanmar','OFFICIAL'),('24','Ulleungdo','S. Korea shelter order as Russian jets enter ADIZ','OFFICIAL'),('25','Dhaka','Hasina plans return on 16 Dec','REPORTED'),('26','The Hague','14 nations endorse ICJ Myanmar ruling','REPORTED'),('27','Jakarta','Indonesia nominates 2 VP candidates','OFFICIAL'),('28','Beijing','China sentences official Ma to death for spying','OFFICIAL'),('29','Brussels','NATO vows defence against space threat','OFFICIAL'),('30','Mexico City','El Chapo Isidro: drone aid; Mexico to try him','REPORTED'),('31','San Salvador','Bukele names 3 soldiers killed in Haiti','OFFICIAL'),('32','Ottawa','Pentagon rebukes Canada: only 41.9% of air fleet ready','REPORTED'),('33','Washington','US adds Megaspeed to trade blacklist','OFFICIAL'),('34','Kyiv','Zelensky urges talks with Russia/US/Europe soon','REPORTED'),('35','Ras Al Khaimah','UAE bus-truck crash kills 13','REPORTED'),('36','London','England record 5,258 heat deaths, summer 2026','OFFICIAL'),('37','Kourou','Ariane 6 lofts 36 Amazon satellites','OFFICIAL'),('38','Cikande','Factory-fire toll rises to 26','REPORTED')]
PINS=[(1,24.7,46.7),(2,31.2,121.5),(3,40.7,-74.0),(4,47.8,35.2),(5,14.7,-17.4),(6,26.6,56.3),(7,40.7,-74.0),(8,47.7,-122.1),(9,39.8,30.5),(10,10.4,-75.5),(11,12.8,45.0),(12,13.0,44.9),(13,39.7,98.5)]
CONT=[([(-168,66),(-140,70),(-125,71),(-110,68),(-95,80),(-85,66),(-75,62),(-65,60),(-60,46),(-70,42),(-75,35),(-80,26),(-85,30),(-90,21),(-95,19),(-105,20),(-115,28),(-125,40),(-125,49),(-140,60),(-155,58),(-168,66)]),([(-58,64),(-45,60),(-30,68),(-20,70),(-30,76),(-55,76),(-58,70)]),([(-80,9),(-75,11),(-60,8),(-50,0),(-35,-8),(-40,-20),(-48,-28),(-55,-35),(-65,-45),(-70,-55),(-73,-40),(-73,-20),(-80,-5),(-80,9)]),([(-17,15),(-10,30),(0,36),(10,37),(20,32),(30,31),(35,28),(43,12),(51,11),(48,0),(40,-10),(35,-20),(30,-30),(20,-35),(15,-27),(12,-18),(9,-1),(9,4),(-8,5),(-17,15)]),([(-10,36),(-9,43),(-2,48),(0,50),(5,53),(8,57),(10,59),(18,56),(21,55),(24,59),(30,60),(30,70),(25,71),(18,69),(12,65),(5,60),(5,58),(-5,50),(-10,43),(-10,36)]),([(30,70),(40,68),(60,69),(80,73),(100,76),(120,73),(140,72),(160,70),(178,66),(170,60),(162,55),(158,52),(142,50),(140,40),(130,42),(127,40),(122,38),(120,32),(122,28),(115,22),(108,18),(105,10),(100,8),(98,12),(95,16),(90,22),(85,20),(80,15),(76,8),(72,20),(66,25),(60,25),(55,26),(50,29),(48,30),(43,28),(40,32),(36,36),(30,36),(30,42),(40,45),(35,55),(30,60),(30,70)]),([(113,-22),(114,-30),(115,-35),(124,-33),(130,-32),(137,-35),(140,-38),(147,-39),(150,-37),(153,-27),(146,-19),(142,-11),(136,-12),(132,-11),(126,-14),(122,-17),(118,-20),(113,-22)]),([(109,1),(117,4),(119,-2),(114,-4),(110,-3),(109,1)]),([(95,5),(100,0),(104,-4),(106,-6),(100,-2),(95,5)]),([(131,-1),(138,-2),(141,-8),(136,-6),(131,-3),(131,-1)]),([(130,31),(133,34),(137,35),(140,36),(141,40),(143,42),(140,44),(137,41),(134,38),(130,31)]),([(-5,50),(-3,53),(-5,56),(-2,58),(0,53),(-2,51),(-5,50)]),([(44,-16),(47,-15),(50,-17),(47,-25),(44,-22),(44,-16)])]
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.rectangle([0,0,W,16],fill=RED); txt(d,12,3,'THE WORLD ON ONE DAY',SAB(9),fill=(255,255,255)); txt(d,W-12,3,'38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS',SAB(9),fill=(255,255,255),anchor='ra')
txt(d,512,22,'Tuesday 24 November 2026',SER(30),fill=INK,anchor='ma')
txt(d,512,58,'Riyadh tower hit again \u00b7 Shanghai party chief probed \u00b7 Huawei guilty on 10 of 12 counts',SER(12),fill=RED,anchor='ma')
REG=[('Europe',9,(40,90,160)),('Middle East',8,(178,34,34)),('Asia',8,(200,120,0)),('Africa',2,(0,120,60)),('Americas',7,(110,60,140)),('World / Space',4,(60,60,60))]
x=12
for name,n,c in REG:
    w=168; d.rectangle([x,78,x+w,94],fill=c); txt(d,x+w/2,81,f'{name}  {n}',SAB(9),fill=(255,255,255),anchor='ma'); x+=w+2
txt(d,12,100,'THE DAY IN UTC',SAB(9),fill=RED)
xx=12
for t,ev in UTC:
    txt(d,xx,112,t,SAB(9),fill=RED); txt(d,xx,122,ev,SAN(8)); xx+=126
d.line([12,140,W-12,140],fill=(200,190,170),width=1)
txt(d,12,146,'THE DAY IN NUMBERS',SAB(9),fill=RED)
xx=12
for v,lab in NUMS:
    txt(d,xx,158,v,SER(17),fill=NAVY); txt(d,xx,178,lab,SAB(7),fill=(90,90,90)); xx+=126
d.line([12,194,W-12,194],fill=(200,190,170),width=1)
hy=200; hw=324; hx=12
for num,city,field,ch,hl,deck,src,kind in HERO:
    scene(d,hx,hy,hw,92,kind)
    txt(d,hx,hy+96,f'{num}  {city} \u00b7 {field}',SAB(9),fill=RED); chip(d,hx,hy+108,ch); txt(d,hx+0,hy+122,src,SAN(7),fill=(120,120,120))
    yy=hy+134
    for ln in wrap(d,hl,SAB(11),hw): txt(d,hx,yy,ln,SAB(11)); yy+=13
    for ln in wrap(d,deck,SAN(9),hw): txt(d,hx,yy,ln,SAN(9)); yy+=11
    hx+=hw+8
d.line([12,396,W-12,396],fill=(200,190,170),width=1)
cy=400; cw=196; chh=104
for i,(num,city,field,ch,hl,deck,src,kind) in enumerate(CARDS):
    cx=12+(i%5)*(cw+4); cy2=cy+(i//5)*(chh+6)
    scene(d,cx,cy2,cw,30,kind)
    txt(d,cx,cy2+33,f'{num}  {city} \u00b7 {field}',SAB(7),fill=RED)
    chip(d,cx,cy2+44,ch)
    yy=cy2+58
    for ln in wrap(d,hl,SAB(9),cw): txt(d,cx,yy,ln,SAB(9)); yy+=11
    for ln in wrap(d,deck,SAN(8),cw): txt(d,cx,yy,ln,SAN(8)); yy+=10
my=622; mx,myy,mw,mh=12,my+14,600,168
d.rectangle([mx,myy,mx+mw,myy+mh],fill=(196,216,232)); d.rectangle([mx,myy,mx+mw,myy+mh],outline=INK,width=1)
txt(d,12,my,'THE WORLD IN NUMBERS \u2014 WHERE IT HAPPENED',SAB(10),fill=RED)
def proj(lon,lat): return mx+(lon+180)/360*mw, myy+(80-lat)/140*mh
for poly in CONT:
    d.polygon([proj(lon,lat) for lon,lat in poly],fill=(140,170,120),outline=(90,120,80))
OFF={3:(0,0),7:(26,-16),11:(0,0),12:(-30,14),1:(0,0)}
pts={}
for n,lat,lon in PINS: pts[n]=proj(lon,lat)
for n,(px,py) in pts.items():
    ox,oy=OFF.get(n,(0,0))
    if (ox,oy)!=(0,0): d.line([px,py,px+ox,py+oy],fill=RED,width=1)
    cx2,cy2=px+ox,py+oy; d.ellipse([cx2-8,cy2-8,cx2+8,cy2+8],fill=RED,outline=(255,255,255),width=1); txt(d,cx2,cy2-5,str(n),SAB(8),fill=(255,255,255),anchor='ma')
lx=628; txt(d,lx,my,'1\u201313  ON THE MAP',SAB(10),fill=RED)
leg=[('1','Riyadh \u2014 PIF tower hit, 11 hurt'),('2','Shanghai \u2014 Chen Jining probed'),('3','New York \u2014 Huawei 10/12 guilty'),('4','Zaporizhzhia \u2014 9 killed, 96 drones'),('5','Dakar \u2014 CAS: Senegal AFCON title'),('6','Hormuz \u2014 IRGC hits container ship'),('7','New York \u2014 Dow 50,018'),('8','Redmond \u2014 Microsoft \u2018Code Red\u2019'),('9','Eskisehir \u2014 helicopter crash, 5 dead'),('10','Cartagena \u2014 25 hostages'),('11','Aden \u2014 Houthis 60 km away'),('12','Lahj \u2014 Saudi strikes kill 25'),('13','Jiuquan \u2014 Shenzhou-24 crew named')]
yy=my+16
for n,t in leg:
    d.ellipse([lx,yy+1,lx+10,yy+11],fill=RED); txt(d,lx+5,yy+1,n,SAB(7),fill=(255,255,255),anchor='ma'); txt(d,lx+14,yy,t,SAN(8)); yy+=12
ay=812; txt(d,12,ay,'ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE STORIES',SAB(10),fill=RED)
cols=[ALSO[0:9],ALSO[9:17],ALSO[17:25]]; colx=[12,348,684]
for ci,col in enumerate(cols):
    yy=ay+16
    for n,city,hl,ch in col:
        t=f'{n} {city}: {hl}'
        while d.textlength(t,font=SAN(8))>262 and ' ' in t: t=t[:t.rfind(' ')]
        txt(d,colx[ci],yy,t,SAN(8)); chip(d,colx[ci]+d.textlength(t,font=SAN(8))+3,yy,ch); yy+=12
dy=940; d.rectangle([12,dy,W-12,dy+58],fill=(255,235,235),outline=RED,width=1)
txt(d,18,dy+4,'DATE CHECK',SAB(9),fill=RED)
dc='Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claims (Mon 23 Nov); Huang returns as Nvidia CEO (Mon 23 Nov); EU 22nd sanctions package (Mon 23 Nov); COP31 ends with no deal (Sun 22 Nov); Merkury corvette sunk (Sat 22 Nov); El Chapo Isidro arrested (Fri 20 Nov); Cikande factory fire began (Sat 21 Nov); Trump hush-money appeal verdict (Mon 23 Nov); Russia warning to Estonia (Mon 23 Nov); ATP Finals (Sun 22 Nov); Las Vegas GP (Sat 21 Nov). NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC); MPR session picks VP (11 Dec); Huawei sentencing (Sep 2027); Hasina returns to Bangladesh (16 Dec).'
yy=dy+16
for ln in wrap(d,dc,SAN(8),W-36): txt(d,18,yy,ln,SAN(8)); yy+=10
txt(d,12,1006,'Sources: Reuters \u00b7 AP \u00b7 UKMTO \u00b7 CAS \u00b7 CCDI \u00b7 CMSA \u00b7 NYSE \u00b7 wires.  CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side\u2019s claim. Scenes are drawn illustrations, not photographs.',SAN(7),fill=(100,100,100))
out=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png'); os.makedirs(os.path.dirname(out),exist_ok=True); im.save(out)
print('saved',out,os.path.getsize(out))
