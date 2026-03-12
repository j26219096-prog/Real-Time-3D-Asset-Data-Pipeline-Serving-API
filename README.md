# Real-Time 3D Asset Data Pipeline & Serving API

> **🌍 Live Demo:** [https://j26219096-prog.github.io/Real-Time-3D-Asset-Data-Pipeline-Serving-API/](https://j26219096-prog.github.io/Real-Time-3D-Asset-Data-Pipeline-Serving-API/)

> A real-time data ingestion and serving pipeline built with FastAPI. It uses NLP keyword matching to query an internal metadata catalog, dynamically extracting heavy 3D assets from external sources, loading them into a thread-safe local cache, and serving the payload to a Three.js frontend. Showcases ETL, API design, and data caching.

## 🚀 Architecture Overview

This project demonstrates core Data Engineering principles applied to 3D asset delivery:

- **Extract (Ingestion):** Dynamically fetches remote binary (`.glb`) files from external APIs (KhronosGroup) on demand.
- **Transform (Metadata & Processing):** Parses natural language text prompts into structured metadata queries using keyword mapping.
- **Load (Caching):** Implements a thread-safe local caching layer to eliminate redundant network requests and optimize bandwidth.
- **Serve (API Layer):** Exposes a scalable REST API via FastAPI to serve the binary payload to a WebGL frontend.

## 🗂️ Tech Stack
- **Data Serving API:** Python, FastAPI, Uvicorn *(Hosted entirely on Render.com)*
- **Data Ingestion:** Python `requests`, OS-level thread concurrency locks
- **Frontend Visualization:** HTML, CSS, JavaScript, Three.js *(Hosted on GitHub Pages)*
- **Data Source:** KhronosGroup glTF Sample Models (Remote Object Store)

## 🧱 Data Flow Diagram

```text
User Prompt (Text)
      ↓
FastAPI /generate Endpoint  →  Keyword Extraction & Mapping  →  Asset Metadata ID
      ↓
FastAPI /model/{id} Endpoint
      ↓ (Cache Miss)
Extract from Remote GitHub Object Store (HTTP Stream)
      ↓
Load to Thread-Safe Local Cache (Disk IO)
      ↓ (Cache Hit)
Serve Streaming GLB Binary Payload → Three.js WebGL Renderer
```

## 🚀 How to Run

### 1. Install Dependencies
Navigate to the `backend` directory and install the Python requirements:
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Data Serving API
```bash
python -m uvicorn main:app --reload
```
*The API gateway will be available at `http://127.0.0.1:8000`*

### 3. Open the Frontend Client
Simply open `index.html` in any modern web browser to interact. (Note: the current `index.html` points to the production Render API. To test the local backend, temporarily replace the Render URLs in `index.html` with `http://127.0.0.1:8000`).

### 4. Trigger Ingestion via Prompts
Try searching for the mapped keywords:
- `show me a fox`
- `vintage camera`
- `robot`
- `sci-fi helmet`
- `toy car`

> **Note:** The first time an asset is requested, the backend performs a remote extraction (download). Subsequent requests hit the local cache layer instantly. Binary `.glb` files are intentionally excluded from version control via `.gitignore`.
