# 影片製作技能包（video-skills-pack）

整合網路上最常被推薦的開源影片技能，共 76 個（v0.1 有 42 個，v0.2 新增 12 個，v0.3 新增 22 個），安裝後 Claude 剪片、做動畫時會自動取用。每個技能的功能與費用，也整理在技能庫根目錄的「影音技能清單.txt」。

## 安裝
- Claude 應用程式：Customize → Plugins，從「jeff-video-skills」市集安裝「video-skills-pack」。
- Claude Code：`/plugin install video-skills-pack --marketplace jefflin0811/claude-video-skills`

## 內容
| 類別 | 技能 | 來源／授權 |
|---|---|---|
| 動畫與字幕主引擎 | hf-hyperframes（含字幕樣式、音效、音樂節拍、9:16 直式、動態圖形）、hf-hyperframes-cli、hf-hyperframes-registry、hf-slideshow、hf-reverse-any-video、hf-remotion-to-hyperframes | HeyGen HyperFrames／Apache-2.0 |
| 素材管理 | hf-media-use（配樂、音效、配音、圖示、去背、轉字幕，記錄出處） | HeyGen／Apache-2.0 |
| 真人短影音剪輯 | kit-cut-silences、kit-cut-mistakes、kit-short-form-edit、kit-short-form-video、kit-edit-video、kit-video-storytelling、kit-hyperframes-video-beats、kit-style-library、kit-gsap、kit-make-a-video、kit-motion-showreel | Nate Herk Student Kit／MIT |
| 產品影片 | guizang-product-video（中文，含配樂與動態音效） | op7418／AGPL-3.0（自用可，修改後對外散布須開源） |
| 動態設計 | motion-design（產品發表級動態、音效對拍、-14 LUFS） | Howseen AI／MIT |
| 短影音與電商 | iart-short-form-video、iart-caption-animation、iart-countdown-video、iart-promo-video、iart-product-demo-video、iart-photo-slideshow、iart-ad-creative-video、iart-launch-video、iart-testimonial-video | iart.ai／MIT |
| 說明動畫 | iart-explainer-video、iart-whiteboard-animation、iart-diagram-animation、iart-isometric-animation、iart-wrapped-video、iart-kinetic-typography、iart-lower-thirds、iart-talking-head-b-roll | iart.ai／MIT |
| 音效、配樂、配音 | elevenlabs-sound-effects、elevenlabs-music、elevenlabs-text-to-speech、elevenlabs-speech-to-text、elevenlabs-setup-api-key | ElevenLabs／MIT |

## 需要付費或帳號的部分
- **ElevenLabs 五個技能**：需要 ElevenLabs API 金鑰（付費方案才有商用授權與足夠額度）。沒有金鑰時這五個技能不會動作。
- **kit-motion-showreel**：AI 生圖／生影片部分呼叫 Kie.ai（需 KIE_API_KEY，依用量付費）；其餘動畫部分免費。
- **hf-media-use**：免費可用（內建 19 個可商用音效、本機語音），登入 HeyGen 免費帳號可解鎖更多音樂音效；部分配音選項用 Google Gemini API（需金鑰）。
- **Remotion 授權**（claude-shorts、remotion-ads 會用到）：個人、非營利組織與員工 3 人以下的公司免費；員工超過 3 人的公司需購買 Remotion 公司授權。這兩個技能的說明裡已加註：替公司做影片前先提醒使用者。
- v0.3 新增技能的付費項目見下方表格「費用」欄。
- 其他技能皆免費，在本機用 Chrome、FFmpeg、Node.js、Python 執行。

## 安全審查（2026-11-03）
- 已檢查所有腳本：無竊取憑證、遠端執行或刪除系統檔的程式碼。
- 已移除測試檔與大型示範影片。
- hf-media-use 內建匿名使用統計（PostHog），已在技能說明中規定執行時加上 DO_NOT_TRACK=1 關閉。
- ElevenLabs 文件中的「curl … | sh」安裝指令為官方 CLI 安裝方式，僅在你有金鑰並同意時才會用到。

## v0.2 新增（2026-11-06）
| 技能 | 用途 | 來源／授權 | 費用 |
|---|---|---|---|
| lottie-text-to-lottie | 用文字描述產生 Lottie 動畫（貼圖、圖示動態、轉場），可疊進影片或網頁 | Diffusion Studio／MIT | 免費 |
| manim-composer、manim-best-practices | 3Blue1Brown 風格的概念說明動畫（衛教機制、圖解） | adithya-s-k／MIT | 免費（本機 Python） |
| explainroo | 說明影片＋本機語音配音＋逐字時間軸，含配樂音效 | vincentsch／MIT | 免費，不需金鑰 |
| pixel2motion | 把 logo 圖片轉成向量 logo 動畫（片頭片尾） | nolangz／MIT | 免費 |
| chaojifeng-video-design | 中文影片設計方法論：主線、分鏡、聲畫節奏、製作與驗收 | mileson／MIT | 免費；部分選用流程可接 HeyGen 等付費服務 |
| motionmaxxing | 把平淡的 AI 動畫提升成電影感：鏡頭語言、字體、節奏審查 | Tejashmakwana／Apache-2.0 | 免費 |
| claude-shorts | 長影片自動挑段落剪成直式短影音，附動畫字幕 | AgriciDaniel／MIT | 免費（全部在電腦上處理；用 Remotion 算圖，公司使用注意授權） |
| anidoodle | 用程式畫插畫與動畫（手繪感、循環動畫、產品片） | alexgreensh／Apache-2.0 | 免費；選用 AI 配樂、配音需各家金鑰 |
| rm-embedded-captions | 35 種字幕樣式，可把字幕藏在人物後面（電影感字幕），全本機處理 | reelmimic／MIT | 免費 |
| rm-talking-head-recut | 真人講話影片重新剪輯 | reelmimic／MIT | 免費 |
| rm-ffmpeg | FFmpeg 剪輯、轉檔、混音實務指南 | reelmimic／MIT | 免費 |

評估後未收錄：BrewReel（字型只含簡體字、依中國廣告法）、Khan 風格說明片（僅限 macOS）、YouTube 剪輯包與 Papercut 系列（必須搭配原作者整個專案資料夾才能運作，並需 ElevenLabs／Gemini／AssemblyAI 付費金鑰）、故事轉手繪影片（需原作者 1.3 GB 專案）。

v0.2 新增技能已做同樣的安全審查：無竊取憑證、遠端執行、刪除系統檔或使用統計程式碼。

## v0.3 新增（2026-11-09）
| 技能 | 用途 | 來源／授權 | 費用 |
|---|---|---|---|
| laoxu-video-script | 自媒體起號方法論：帳號定位、找選題、寫口播稿、自我檢查與迭代（原文簡體中文） | 老徐 chenmisss／MIT | 免費 |
| video-structure-analyzer | 拆解爆款影片：逐鏡頭拉片表、爆款機制、可重複使用的結構、批量選題、腳本與分鏡 | sharon-laicc／MIT | 免費 |
| brand-intake | 品牌設定：訪談加參考畫面，整理品牌資料與動態規範，之後做動畫都會先讀 | Charlie Hills／MIT | 免費 |
| motion-brief-writer | 把模糊的動畫想法寫成精準的製作說明，不捏造數據 | Charlie Hills／MIT | 免費 |
| motion-prompt-writer | 為一段循環動態圖形寫 8 段式製作指令 | Charlie Hills／MIT | 免費 |
| reference-to-motion | 「做一支像這樣的」：參考影片的動作＋參考品牌的風格 → 逐場景製作指令 | Charlie Hills／MIT | 免費 |
| motion-effects | 16 種高級動態效果，各做成 8 秒循環，可輸出 MP4 或 GIF | Charlie Hills／MIT | 免費 |
| animated-chart | 循環圖表動畫：長條變折線、數字跳動、前後對比，數值照實 | Charlie Hills／MIT | 免費 |
| milestone-reveal | 12 秒里程碑影片：星點聚合成真實數字（粉絲數、營收等） | Charlie Hills／MIT | 免費 |
| newsletter-promo | 把一篇電子報或文章做成 12 到 20 秒導讀短片 | Charlie Hills／MIT | 免費 |
| title-sequence-3d | 8 到 15 秒電影感 3D 片頭（Three.js） | Charlie Hills／MIT | 免費 |
| vox-explainer | 30 到 60 秒 Vox 風格紀錄片式說明影片 | Charlie Hills／MIT | 免費 |
| reel-export | 橫式或方形影片轉 1080×1920 直式：安全區、平台編碼、上傳前檢查 | Charlie Hills／MIT | 免費 |
| remotion-ads | 專業影片廣告：IG Reels、網站說明片、輪播圖；含文案公式、字幕、配樂音效 | Maarten van Onoesen／MIT | 選用付費：ElevenLabs 配音、Gemini 配音（有免費額度）；Remotion 授權見上方 |
| business-motion-film | 替真實商家做高質感商業短片：程式動態、選用 3D、獨立評審把關 | echris6／MIT | 選用付費：AI 生成畫面 |
| promo-workflow | 產品宣傳片總控：串起下面 5 個步驟，每階段確認 | kangarooking／MIT | 免費 |
| promo-brief | 宣傳片創意簡報：提煉賣點、建議風格與敘事 | kangarooking／MIT | 免費 |
| promo-storyboard | 宣傳片逐鏡頭分鏡腳本 | kangarooking／MIT | 免費 |
| promo-asset-producer | 宣傳片素材：AI 生圖＋蒐集真實產品資料 | kangarooking／MIT | AI 生圖視當時工具而定，可能付費 |
| promo-editor | 依分鏡串起素材、加字與轉場，算出宣傳片 MP4 | kangarooking／MIT | 免費 |
| promo-music-maker | 宣傳片配樂企劃：風格、速度、卡點表與生成指令 | kangarooking／MIT | 企劃免費；直接生成配樂需 Mureka／Skywork 付費金鑰 |
| vlog-auto-edit | 旅行 Vlog 自動剪輯：分析素材、剪輯計畫、剪出成品 | nyx研究所 znyupup／MIT | 免費 |

v0.3 調整：
- remotion-ads 原本附的 Suno 配樂工具會把使用者的 Suno 登入權杖交給第三方 browser-use 服務，已移除，相關說明改成用 ElevenLabs 或自己的音樂庫。
- brand-intake 建議的下一步改指向技能包內已有的 iart-launch-video。
- promo-music-maker 一併附上原專案共用的參考文件與 Mureka 腳本。

評估後未收錄（v0.3）：ghost-editor（和現有口播剪輯技能重疊，且安裝位置寫死，放進技能包會無法運作）、erduo B-roll 循環剪輯（舊版流程、步驟複雜）、creator-style-kit（174 MB，字型只有簡體字）、Charlie Hills 包裡的蘋果風 Mac 發表片、軟體發表片、電子報封面 GIF、三個 AI 模型比較片（關聯低或已有同功能技能）。

v0.3 新增技能已做同樣的安全審查：無竊取憑證、遠端執行、刪除系統檔或使用統計程式碼。
