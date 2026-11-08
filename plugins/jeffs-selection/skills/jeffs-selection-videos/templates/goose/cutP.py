import sys
sys.path.insert(0,"__ROOT__/soup")
import cutg2
A="/mnt/user-data/uploads/39490_1.mp4";B="/mnt/user-data/uploads/39492_1.mp4";DUCK=(180,640,720,1280)
seg=[("store",B,0.00,3.20,6),("case",B,3.30,5.90,4),("chop",B,5.95,7.70,6),("soup",A,0.00,1.15,4),("blood",A,1.70,3.35,4),
     ("duck",A,3.85,5.05,4,DUCK),("smoke",A,5.50,7.50,4),("all",A,7.60,9.65,5)]
print(cutg2.run(seg,"__ROOT__/goose/sP",0.6502,grade="curves=all='0/0.02 0.4/0.47 0.75/0.82 1/1',eq=saturation=0.96",interp_below=0.5),flush=True)
