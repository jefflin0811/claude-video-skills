# beat-locked cut from high-res sources: SEG items (name, file, a, b, beats[, crop])
# crop = (x, y, w, h) in 1080x1920 output coordinates, applied on the source frame before scaling
# interp_below: segments slower than this speed get motion-interpolated (smoother slow motion)
import json,subprocess
def run(SEG,out_dir=".",beat=0.6502,fps=30,src_scale=2,grade="colorbalance=rs=0.04:gs=0.01:bs=-0.05:rm=0.03:bm=-0.03,eq=saturation=1.12:contrast=1.04",interp_below=0.0):
    args=[];fl=[];out=[];cum=0;f0=0
    for i,it in enumerate(SEG):
        n,vf,va,vb,nbeat=it[:5];crop=it[5] if len(it)>5 else None
        cum+=nbeat;f1=int(round(cum*beat*fps));nf=f1-f0;d=nf/fps;sp=(vb-va)/d
        args+=["-ss",f"{va:.3f}","-t",f"{vb-va+0.25:.3f}","-i",vf]
        cr=""
        if isinstance(crop,str):cr=crop+","
        elif crop:
            x,y,w,h=crop;k=src_scale;cr=f"crop={int(w*k)}:{int(h*k)}:{int(x*k)}:{int(y*k)},"
        mi=",minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if sp<interp_below else ""
        fl.append(f"[{i}:v:0]{cr}scale=1080:1920:flags=lanczos,setsar=1{mi},setpts=(PTS-STARTPTS)/{sp:.6f},fps={fps},tpad=stop_mode=clone:stop_duration=0.5,trim=end_frame={nf},setpts=PTS-STARTPTS[v{i}]")
        out.append(dict(name=n,o=round(f0/fps,4),d=round(d,4),speed=round(sp,4),src=vf,a=va,b=vb));f0=f1
    N=len(SEG)
    fl.append("".join(f"[v{i}]" for i in range(N))+f"concat=n={N}:v=1:a=0,{grade}[v]")
    subprocess.run(["ffmpeg","-v","error","-y"]+args+["-filter_complex",";".join(fl),"-map","[v]","-an","-c:v","libx264","-preset","veryfast","-crf","15","-pix_fmt","yuv420p",out_dir+"/video.mp4"],check=True)
    json.dump(dict(seg=out,total=round(f0/fps,4)),open(out_dir+"/cut.json","w"),indent=1,ensure_ascii=False);return f0/fps
