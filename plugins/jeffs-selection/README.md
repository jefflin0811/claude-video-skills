# 姐夫嚴選影片版型（jeffs-selection）

姐夫嚴選三個系列短影音的固定版型。安裝後，跟 Claude 說「做一支姐夫探店／姐夫開煮／姐夫開箱」，就會自動套用對應的版型、品牌規則與交付流程。

| 系列 | 版型 | 重點 |
|---|---|---|
| 姐夫探店 | 風格 B 職人紀錄 | 電影黑邊、調色與底片顆粒、切肉大標題字卡、左下菜名＋銅色線、黑底店家資訊頁 |
| 姐夫開煮 | 日系雜誌 | 米白紙感、大號斜體步驟數字、火候跑馬燈與時間軸、食譜頁 |
| 姐夫開箱 | 版本 A 手繪食材 | 手繪圖彈出後排成一排、米白底紅編號標籤、愛心閃光收尾 |

## 安裝
- Claude 應用程式：Customize → Plugins，從「jeff-video-skills」市集安裝「jeffs-selection」。
- Claude Code：`/plugin install jeffs-selection --marketplace jefflin0811/claude-video-skills`

## 內容
- 技能 jeffs-selection-videos：三個版型的完整規格、共用規則（logo 位置、字的安全區、手機可讀性、片尾）、檢查與交付流程。
- templates/：三套版型程式（Python）、姐夫嚴選 logo、程式產生的音效。
- scripts/setup.sh：建立工作資料夾、換好路徑、下載字型、檢查執行環境。
- references/adapt.md：換新店家、新菜色、新商品時要改的地方。

## 費用
免費。字型在建立工作資料夾時從 npm 下載（Google Fonts 開源字型）；影片在電腦上算圖，不用任何付費服務。

## 注意
- 背景音樂有版權，沒有放進技能庫；做影片時從電腦「下載\圖庫素材\背景音樂」提供（探店：通用_lose-it；開煮：食品開箱_gourmet-flavors；開箱：食品開箱_joyful-sparks）。
- 姐夫嚴選 logo 屬品牌所有，請勿用在其他品牌。
- 牛肉爐合作 logo 含合作品牌，沒有放進技能庫；三個版型都用不到。
- 舊版封面測試圖（約 23 MB）沒有放進來；程式偵測不到時會自動略過。
