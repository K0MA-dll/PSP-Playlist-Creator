![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FFmpeg](https://img.shields.io/badge/FFmpeg-enabled-green?logo=ffmpeg)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)

# 🎵 PSP Playlist Creator

Automatically generate PSP `.m3u8` playlists from your music folders. Scans subfolders, copies audio files to your PSP, and creates one playlist per folder with natural sorting and multi-format support.

<p align="center">
  Automatically generate PSP playlists from your music folders 🎧
</p>

---

# ✨ Features

* 🎵 Automatic `.m3u8` playlist generation
* 📂 Recursive music folder scanning
* ⚡ Fast local processing
* 🧠 Natural filename sorting
* 🛡️ Duplicate-safe file copy
* 🎮 PSP-ready folder structure
* 🖥️ Simple modern PyQt6 interface
* 📀 Multi-format audio support

---

# 📦 Supported Formats

```txt
.mp3
.flac
.wav
.ogg
.m4a
```

---

# 🚀 How It Works

## 1️⃣ Select your PSP root

The program automatically checks if the folder is a valid PSP root.

Required folders:

```txt
/PSP
/VIDEO
```

---

## 2️⃣ Select your music folder

Choose any folder containing music.

Example:

```txt
Music/
├── Initial D/
│   ├── Deja Vu.mp3
│   ├── Running in the 90s.mp3
│
├── Daft Punk/
│   ├── One More Time.mp3
```

---

## 3️⃣ Click "Generate Playlists"

The program will automatically:

* 🔍 Scan all subfolders
* 🎵 Detect folders containing music
* 📁 Copy all audio files into:

```txt
/PSP_ROOT/MUSIC/
```

* 📝 Generate playlists inside:

```txt
/PSP_ROOT/PSP/PLAYLIST/MUSIC/
```

---

# 📜 Example Playlist

Generated file:

```txt
PSP/PLAYLIST/MUSIC/Initial D.m3u8
```

Content:

```txt
\MUSIC\Deja Vu.mp3
\MUSIC\Running in the 90s.mp3
```

---

# ⚙️ Installation

## 📥 Install dependencies

```bash
pip install PyQt6
```

## ▶️ Run the application

```bash
python main.py
```

---

# 🛠️ Built With

* 🐍 Python
* 🖼️ PyQt6

---

# 📌 Notes

* ✅ Duplicate files are ignored silently
* ✅ Existing music files are never overwritten
* ✅ Playlist names are automatically cleaned
* ✅ Music filenames stay unchanged

---

# 📸 Screenshot

```md
![Screenshot](screenshot.png)
```

---

# 👤 Author

Made by **K0MA.dll**

🔗 GitHub: https://github.com/K0MA-dll
