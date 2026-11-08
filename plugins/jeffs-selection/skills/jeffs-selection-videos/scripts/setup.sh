#!/usr/bin/env bash
# 姐夫嚴選版型：建立工作資料夾（可以重跑，已存在的檔案不會被覆蓋）
# 用法：bash setup.sh <工作資料夾>
set -eo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -z "$1" ]; then echo "用法：bash setup.sh <工作資料夾>"; exit 1; fi
mkdir -p "$1"
ROOT="$(cd "$1" && pwd)"
echo "工作資料夾：$ROOT"

# 1. 版型程式：複製（不覆蓋已改過的檔案），再把 __ROOT__ 換成工作資料夾路徑
python3 - "$SKILL_DIR/templates" "$ROOT" <<'PY'
import sys, shutil, pathlib
src, root = pathlib.Path(sys.argv[1]), sys.argv[2]
c = n = 0
for p in src.rglob("*"):
    d = pathlib.Path(root, p.relative_to(src))
    if p.is_dir():
        d.mkdir(parents=True, exist_ok=True); continue
    if not d.exists():
        d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, d); c += 1
    if d.suffix == ".py":
        t = d.read_text(encoding="utf-8")
        if "__ROOT__" in t:
            d.write_text(t.replace("__ROOT__", root), encoding="utf-8"); n += 1
print(f"版型程式：複製 {c} 個檔案，更新路徑 {n} 個檔案")
PY

# 2. 字型（Google Fonts，SIL 開源授權，從 npm 下載；已下載過就跳過）
F="$ROOT/fonts"
mkdir -p "$F/x2"
cd "$F"
get() {  # $1=套件名 $2=版本 $3=解壓目的地 $4=檢查用的檔案
  if [ -f "$4" ]; then return; fi
  mkdir -p "$3"
  local tgz
  tgz="$(npm pack "@expo-google-fonts/$1@$2" --silent | tail -1)"
  tar xzf "$tgz" -C "$3"
  rm -f "$tgz"
}
get noto-serif-tc 0.4.5 x2 x2/package/600SemiBold/NotoSerifTC_600SemiBold.ttf
get noto-sans-tc 0.4.4 x2 x2/package/900Black/NotoSansTC_900Black.ttf
get lxgw-wenkai-tc 0.4.3 x2 x2/package/700Bold/LXGWWenKaiTC_700Bold.ttf
get cormorant-garamond 0.4.1 x2 x2/package/400Regular_Italic/CormorantGaramond_400Regular_Italic.ttf
get chiron-goround-tc 0.4.3 _round ChironGoRoundTC_900Black.ttf
get huninn 0.4.3 _round Huninn_400Regular.ttf
for f in _round/package/900Black/ChironGoRoundTC_900Black.ttf \
         _round/package/800ExtraBold/ChironGoRoundTC_800ExtraBold.ttf \
         _round/package/400Regular/Huninn_400Regular.ttf \
         x2/package/900Black/NotoSansTC_900Black.ttf; do
  b="$(basename "$f")"
  if [ ! -f "$b" ] && [ -f "$f" ]; then cp "$f" "$b"; fi
done
rm -rf _round
echo "字型已就緒"

# 3. 背景音樂：偵測到 Jeff 電腦同步進來的「下載／圖庫素材／背景音樂」就複製
mkdir -p "$ROOT/music"
for d in "/mnt/user-data/uploads/Downloads/圖庫素材/背景音樂" "$HOME/mnt/Downloads/圖庫素材/背景音樂"; do
  if [ -d "$d" ]; then
    for m in "$d"/*.mp3; do
      if [ -f "$m" ] && [ ! -f "$ROOT/music/$(basename "$m")" ]; then cp "$m" "$ROOT/music/"; fi
    done
  fi
done
for m in 通用_lose-it.mp3 食品開箱_gourmet-flavors.mp3 食品開箱_joyful-sparks.mp3; do
  [ -f "$ROOT/music/$m" ] || echo "缺少背景音樂：$m（請從「下載／圖庫素材／背景音樂」放進 $ROOT/music/）"
done

# 4. 執行環境
python3 -c "import PIL, numpy, soundfile" 2>/dev/null || pip install --break-system-packages -q pillow numpy soundfile
command -v ffmpeg >/dev/null || echo "缺少 FFmpeg，請先安裝"
echo "完成。入口程式與要改的地方見 $SKILL_DIR/references/adapt.md"
