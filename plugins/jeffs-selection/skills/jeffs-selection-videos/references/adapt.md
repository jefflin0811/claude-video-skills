# 改版指南：換新店家、新菜色、新商品時要改的地方

以下路徑都相對於 setup.sh 建立的工作資料夾。行號是目前版本的大約位置，改之前先打開檔案確認。

## 共通流程

1. 把 Jeff 的素材放到容器裡（附件會在 /mnt/user-data/uploads/，從他電腦同步的會在 /mnt/user-data/uploads/Downloads/...），剪輯腳本裡的素材路徑直接改成實際位置。
2. 先改剪輯段落 → 執行剪輯指令，產生 video.mp4 與 cut.json（節拍剪輯＋調色，鏡頭速度會自動配合拍數）。
3. 再改文字 → 出抽幀表檢查 → 沒問題才算整支。
4. 輸出檔名寫死在每個入口程式最後幾行，記得改成這次的主題。
5. 鏡頭代號（例如 s1、soup、duck）只是程式內部的名字，可以沿用，只改畫面上顯示的文字；如果改代號，剪輯段落、字幕表、文字表裡的名字要一起改。

## 姐夫開煮｜日系雜誌（入口：soup/magv4.py）

繼承順序：magv4 → magv3 → magv2 → prem2 → base3 → eng（字型與 logo 在 brand/kit5、goose/sty）。

剪輯：soup/run2.py
- 第 10 行 BEAT（一拍的秒數）。
- 第 11 到 18 行 SEG：每段是（代號, 素材檔, 起點秒, 終點秒, 拍數[, 裁切]）。代號固定為 hook（封面）、s1 到 s5（步驟）、s6a、s6b（上桌）。裁切可以是 (x, y, w, h)，或 FFmpeg crop 字串（例如 s5 的橫移裁切）。
- 執行 `python3 soup/run2.py cut` → soup/build2/video.mp4 與 cut.json。

文字：
- soup/prem2.py 第 120 到 121 行 STEPS：（代號, 編號 01, 中文數字, 小標, 字幕）；火候段的字幕寫成兩句的 tuple。
- soup/magv4.py
  - 第 48 行 MQ：火候段跑馬燈的兩句。
  - timeline4（約第 50 到 62 行）：火候時間軸的「中火」「小火」與 20／60 分鐘的比例；d_step 第 86 行的 20、40 也要跟著改。
  - d_step（約第 79 到 94 行）：`if i==4` 代表第 5 個步驟是火候段（跑馬燈＋時間軸）；步驟數或火候段位置不同時改這裡。
  - d_open（約第 73 到 78 行）：封面「姐夫開煮」「60 分鐘」、菜名、食材清單。
  - d_fin（約第 95 到 102 行）：「60 分鐘後」、成品句、「上桌了」。
  - endparts 第 106 行：食譜頁的材料與份量（leader3 每列一樣，第三個數字是點線長度）。
  - recipe（約第 108 到 133 行）：食譜頁的菜名、「5 種食材｜60 分鐘」、做法兩行、「先收藏，下次照著煮」。
- 背景音樂：soup/prem2.py 第 10 行 GBGM（食品開箱_gourmet-flavors，從頭開始）。

檢查與輸出：
- `python3 soup/magv4.py sheet 0.3,5,12,20,26.5,30.5`（時間點自訂）→ soup/mag4_sheet.jpg
- `python3 soup/magv4.py render`（檔名在第 136 行）

## 姐夫探店｜風格 B 職人紀錄（入口：goose/bfinal.py）

繼承順序：bfinal（BFinal）→ craft（Cinema → Craft）→ sty（SV）；craft 也會載入 soup/magv4 的文字工具。

剪輯：goose/cutP.py
- A、B 是素材檔；seg 每段是（代號, 素材檔, 起點秒, 終點秒, 拍數[, 裁切 (x, y, w, h)]）。
- 代號順序：store（店門 6 拍）、case（櫃台 4 拍）、chop（師傅切肉 6 拍）、四道菜 soup／blood／duck／smoke（各 4 拍）、all（全桌 5 拍）。
- 節拍 0.6502 秒（通用_lose-it），interp_below=0.5 會把太慢的鏡頭補幀變順。
- 執行 `python3 goose/cutP.py` → goose/sP/video.mp4 與 cut.json。

文字：
- goose/sty.py 第 100 行 DISH：四道菜名（畫面左下的大字）。
- goose/craft.py
  - 第 12 行 CN（壹貳參肆）、ORD。
  - 第 13 行 ADDR（地址）、MRT（交通），用在店門到櫃台的跑馬燈與資訊頁。
  - 第 14 到 15 行 SUB：每個鏡頭的字幕。
  - 第 16 行 DISHES：菜的鏡頭代號；道數不同時改這裡、DISH、CN、SUB 與 cutP.py 的 seg。
  - Cinema.info（約第 145 到 156 行）：資訊頁的店名與「必點」兩行。
  - 第 10 行 BGM、BGM_OFF（音樂起點秒數）；第 11 行 INFO（資訊頁秒數）、ENDC（片尾秒數）。
- goose/bfinal.py text()
  - 第 25 到 28 行：封面「姐夫探店」、店名、「地點・巷弄老店」。
  - 第 30 到 38 行：切肉字卡的標語（「巷弄裡的老味道」）與「姐夫嚴選・地點」。
  - 第 43 到 46 行：收尾直排「四道必點」。

檢查與輸出：
- `python3 goose/bfinal.py sheet 0.3,4,8.5,14,22,25,28` → goose/bfinal_sheet.jpg
- `python3 goose/bfinal.py render`（檔名在第 55 行）

## 姐夫開箱｜版本 A 手繪食材（入口：soup/runA.py）

這個版型原本是用無水雞湯的素材做的示範，做開箱時沿用它的畫面語言，把「步驟」換成「商品」。

一定要改：
- 第 6 行 TAG：目前寫「姐夫開煮」，開箱影片要改成「姐夫開箱」。
- 第 7 行 TITLE：大標題（商品名）。
- 第 4 行 ICONS、第 8 行 MINI：手繪圖。圖在 soup/doodles.py（onion、cabbage、drumstick、apple、corn、flame、bowl 等函式），新商品照同樣的畫法新增：細線外框、圓角、淺色填色、白色貼紙邊；畫不出來就用去背商品照加白色貼紙邊。
- setup() 第 12 到 13 行 s.ing：哪個鏡頭、第幾秒跳出哪個手繪圖、彈出的位置。
- 第 53 行 STEPS：每樣商品的編號與一句介紹（米白底紅編號標籤，從左滑入）。
- 第 56 行：第 5 段的兩個標籤；第 59 行：收尾句；第 9 行 FINH：收尾大字。
- end_extra（約第 46 到 50 行）：片尾下方那排手繪小圖。

剪輯：
- 開箱和開煮共用 soup/build2（soup/run2.py 的 SEG，代號 hook、s1 到 s5、s6a、s6b）。同時做兩支時，先把 soup/run2.py 與 soup/base3.py 的 WD 改成另一個資料夾（例如 soup/build_unbox），再執行 `python3 soup/run2.py cut`。
- 背景音樂：soup/base3.py 第 9 行 BGM（食品開箱_joyful-sparks）與 BGM_OFF。

檢查與輸出：
- `python3 soup/runA.py test` → soup/A_sheet.jpg
- `python3 soup/runA.py render`（檔名在第 74 行）

## 常見問題

- 找不到字型：重跑 setup.sh（需要能連 npm）。
- 缺背景音樂：把需要的 mp3 放進 music/，檔名要和程式裡的一致。
- 畫面上的字被吃掉：照 SKILL.md「手機上要看得清楚」的規則加大、加粗或加光暈，不用底色塊。
- soup/run3.py、soup/runB.py、goose/craft.py 的 Docu、Oldshop 是當初比較用的其他版本，只當參考，不用在正式影片。
