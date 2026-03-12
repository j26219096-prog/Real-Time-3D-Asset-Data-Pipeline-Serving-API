# Text to 3D Web Application

A browser-based project that converts text prompts into 3D visualizations using Three.js and a FastAPI backend. 3D models are fetched **in real-time** from the [KhronosGroup glTF Sample Models](https://github.com/KhronosGroup/glTF-Sample-Models) library and cached locally.

## ✨ Features
- 💬 Text-based chat UI
- 🔍 Smart keyword-based prompt matching (15+ models)
- 🌐 Real-time model fetching + local caching
- 🧊 3D model rendering with Three.js (GLB / glTF)
- 🖱 Orbit controls (drag to rotate, scroll to zoom)
- 🎨 Premium UI with glassmorphism dark panel

## 🗂️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript, Three.js + GLTFLoader
- **Backend**: Python + FastAPI
- **Model Source**: KhronosGroup glTF Sample Models (fetched on-demand)

## 🧱 Architecture
```
User Prompt (text)
      ↓
FastAPI /generate  →  Keyword Matching  →  Model Name
      ↓
FastAPI /model/{name}
      ↓ (if not cached)
Fetch from KhronosGroup GitHub (remote)  →  Cache locally
      ↓
Stream GLB → Three.js Renderer
```

## 🚀 How to Run

### 1. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the backend server
```bash
python -m uvicorn main:app --reload
```

### 3. Open the frontend
Open `frontend/index.html` in your browser.

### 4. Try a prompt
Click any chip or type something like:
- `show me a fox`
- `robot`
- `vintage camera`
- `sci-fi helmet`
- `toy car`

## 📦 Available Models (15)
| Model | Keywords |
|-------|---------|
| 🦆 Duck | duck, bird, rubber duck, toy |
| 🥑 Avocado | avocado, fruit, food |
| 🦊 Fox | fox, animal, wolf, dog |
| ⛑ Helmet | helmet, armor, warrior, knight |
| 🏮 Lantern | lantern, lamp, torch, fire |
| 📷 Camera | camera, vintage, photography |
| 👗 Corset | corset, clothing, fashion, dress |
| 🐟 Fish | fish, barramundi, ocean, marine |
| 💧 Bottle | bottle, water, flask |
| 🚚 Truck | truck, vehicle, milk truck |
| 🔊 Boombox | boombox, speaker, music, radio |
| 🤖 Robot | robot, android, humanoid |
| 🏎 Buggy | buggy, off-road, jeep |
| 🚀 Sci-Fi | scifi, space helmet, astronaut |
| 🚗 Toy Car | toy car, miniature, model car |

> **Note:** Models are fetched from the internet on first use and cached locally. GLB files are **not** committed to git.

## Status
Learning project 🚀 — Data Engineering domain
