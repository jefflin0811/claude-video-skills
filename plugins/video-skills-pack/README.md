# 影片製作技能包（video-skills-pack）

整合網路上最常被推薦的開源影片技能，共 42 個，安裝後 Claude 剪片、做動畫時會自動取用。

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
| claude-shorts | 長影片自動挑段落剪成直式短影音，附動畫字幕 | AgriciDaniel／MIT | 免費；選用 Suno 配樂需付費 |
| anidoodle | 用程式畫插畫與動畫（手繪感、循環動畫、產品片） | alexgreensh／Apache-2.0 | 免費；選用 AI 配樂、配音需各家金鑰 |
| rm-embedded-captions | 35 種字幕樣式，可把字幕藏在人物後面（電影感字幕），全本機處理 | reelmimic／MIT | 免費 |
| rm-talking-head-recut | 真人講話影片重新剪輯 | reelmimic／MIT | 免費 |
| rm-ffmpeg | FFmpeg 剪輯、轉檔、混音實務指南 | reelmimic／MIT | 免費 |

評估後未收錄：BrewReel（字型只含簡體字、依中國廣告法）、Khan 風格說明片（僅限 macOS）、YouTube 剪輯包與 Papercut 系列（必須搭配原作者整個專案資料夾才能運作，並需 ElevenLabs／Gemini／AssemblyAI 付費金鑰）、故事轉手繪影片（需原作者 1.3 GB 專案）。

v0.2 新增技能已做同樣的安全審查：無竊取憑證、遠端執行、刪除系統檔或使用統計程式碼。
