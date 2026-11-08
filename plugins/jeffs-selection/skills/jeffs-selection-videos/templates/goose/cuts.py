import sys,os
sys.path.insert(0,"__ROOT__/eng")
import cutg
G=os.path.dirname(os.path.abspath(__file__))
A="/mnt/user-data/uploads/39490_1.mp4";B="/mnt/user-data/uploads/39492_1.mp4";DUCK=(180,640,720,1280)
STY={
 # 質感選物 — gourmet-flavors, 63.8 bpm
 "sA":dict(beat=0.9404,grade="curves=all='0/0.05 0.5/0.52 1/0.97',eq=saturation=0.97:contrast=0.98,colorbalance=rs=0.03:bs=-0.03:rh=0.02:bh=-0.03",
   seg=[("store",B,0.00,3.00,4),("case",B,3.30,5.90,3),("chop",B,6.05,7.65,3),("soup",A,0.00,1.15,3),("blood",A,1.70,3.35,3),
        ("duck",A,3.85,5.05,3,DUCK),("smoke",A,5.50,7.50,3),("all",A,7.60,9.65,4)]),
 # 職人紀錄 — lose-it, 92.3 bpm (beat drop on the chop shot)
 "sB":dict(beat=0.6502,grade="colorbalance=rs=-0.04:bs=0.05:rm=0.02:bm=-0.02:rh=0.06:gh=0.02:bh=-0.06,eq=contrast=1.08:saturation=0.9,vignette=PI/4.6,noise=alls=7:allf=t",
   seg=[("store",B,0.00,3.20,6),("case",B,3.30,5.90,4),("chop",B,5.95,7.70,6),("soup",A,0.00,1.15,4),("blood",A,1.70,3.35,4),
        ("duck",A,3.85,5.05,4,DUCK),("smoke",A,5.50,7.50,4),("all",A,7.60,9.65,5)]),
 # 美食手帳 — joyful-sparks, 105.5 bpm
 "sC":dict(beat=0.5689,grade="eq=brightness=0.02:saturation=1.08:contrast=1.02,colorbalance=rs=0.02:bs=-0.02",
   seg=[("store",B,0.00,3.20,8),("case",B,3.30,5.60,4),("chop",B,6.05,7.65,4),("soup",A,0.00,1.15,5),("blood",A,1.70,3.35,5),
        ("duck",A,3.85,5.05,5,DUCK),("smoke",A,5.50,7.50,5),("all",A,7.60,9.65,5)]),
}
if __name__=="__main__":
    for k in sys.argv[1:]:
        c=STY[k];os.makedirs(G+"/"+k,exist_ok=True);print(k,cutg.run(c["seg"],G+"/"+k,c["beat"],grade=c["grade"],interp_below=0.5),flush=True)
