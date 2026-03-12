from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import threading
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Base URL for KhronosGroup official glTF Sample Models (guaranteed free & public)
_BASE = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0"

# ---- MODEL CATALOG (15 models, fetched in real-time & cached locally) ----
MODEL_MAP = {
    "duck": {
        "keywords": ["duck", "rubber duck", "bird", "toy", "quack", "water bird"],
        "remote_url": f"{_BASE}/Duck/glTF-Binary/Duck.glb",
        "description": "A classic rubber duck — cheerful and iconic!"
    },
    "avocado": {
        "keywords": ["avocado", "fruit", "food", "guacamole", "green fruit", "vegetable"],
        "remote_url": f"{_BASE}/Avocado/glTF-Binary/Avocado.glb",
        "description": "A detailed 3D avocado with realistic texture."
    },
    "lamborghini": {
        "keywords": ["lamborghini", "lambo", "supercar", "sports car", "car"],
        "remote_url": None,
        "description": "A sleek Lamborghini supercar. (Note: Locally hosted model required)"
    },
    "bmw": {
        "keywords": ["bmw", "car", "sedan", "vehicle", "auto"],
        "remote_url": None,
        "description": "A luxury BMW vehicle. (Note: Locally hosted model required)"
    },
    "helmet": {
        "keywords": ["helmet", "armor", "head gear", "battle", "warrior", "knight", "sci-fi", "damaged"],
        "remote_url": f"{_BASE}/DamagedHelmet/glTF-Binary/DamagedHelmet.glb",
        "description": "A battle-damaged sci-fi helmet — detailed game asset."
    },
    "lantern": {
        "keywords": ["lantern", "lamp", "light", "torch", "glow", "candle", "fire"],
        "remote_url": f"{_BASE}/Lantern/glTF-Binary/Lantern.glb",
        "description": "A beautifully detailed antique lantern."
    },
    "camera": {
        "keywords": ["camera", "antique", "vintage", "photo", "photography", "lens", "old camera"],
        "remote_url": f"{_BASE}/AntiqueCamera/glTF-Binary/AntiqueCamera.glb",
        "description": "A vintage antique camera with fine mechanical detail."
    },
    "corset": {
        "keywords": ["corset", "clothing", "fashion", "dress", "garment", "costume", "apparel", "cloth"],
        "remote_url": f"{_BASE}/Corset/glTF-Binary/Corset.glb",
        "description": "A highly detailed vintage corset model."
    },
    "fish": {
        "keywords": ["fish", "barramundi", "sea", "ocean", "aquatic", "marine", "underwater"],
        "remote_url": f"{_BASE}/BarramundiFish/glTF-Binary/BarramundiFish.glb",
        "description": "A Barramundi fish with realistic scales and texture."
    },
    "bottle": {
        "keywords": ["bottle", "water bottle", "container", "drink", "flask", "water"],
        "remote_url": f"{_BASE}/WaterBottle/glTF-Binary/WaterBottle.glb",
        "description": "A shiny metallic water bottle — great for PBR material demo."
    },
    "truck": {
        "keywords": ["truck", "vehicle", "car", "milk truck", "transport", "automobile"],
        "remote_url": f"{_BASE}/CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb",
        "description": "A classic Cesium milk truck with animated wheels."
    },
    "boombox": {
        "keywords": ["boombox", "speaker", "music", "radio", "stereo", "audio", "sound"],
        "remote_url": f"{_BASE}/BoomBox/glTF-Binary/BoomBox.glb",
        "description": "A retro boombox speaker with highly detailed metal textures."
    },
    "robot": {
        "keywords": ["robot", "android", "machine", "humanoid", "mech", "cesium man", "cyborg"],
        "remote_url": f"{_BASE}/CesiumMan/glTF-Binary/CesiumMan.glb",
        "description": "A walking humanoid robot — animated Cesium Man."
    },
    "heart": {
        "keywords": ["heart", "cardiac", "organ", "cardiology", "medical"],
        "remote_url": None,
        "description": "A realistic human heart model. (Note: Locally hosted model required)"
    },
    "scifihelmet": {
        "keywords": ["sci fi helmet", "scifi", "space helmet", "futuristic", "astronaut", "space"],
        "remote_url": f"{_BASE}/SciFiHelmet/glTF-Binary/SciFiHelmet.glb",
        "description": "A futuristic sci-fi helmet with advanced PBR materials."
    },
    "bike": {
        "keywords": ["bike", "bicycle", "cycle", "motorcycle", "motorbike", "vehicle"],
        "remote_url": None,
        "description": "A highly detailed two-wheeler bike. (Note: Locally hosted model required)"
    }
}

# ---- Tracks which models are currently being downloaded ----
_downloading = {}
_lock = threading.Lock()


@app.get("/")
def home():
    return {"status": "Backend running", "total_models": len(MODEL_MAP)}


@app.get("/models")
def list_models():
    """Returns list of all available models with their keywords."""
    return {
        name: {
            "keywords": data["keywords"],
            "description": data["description"],
            "cached": os.path.exists(os.path.join(MODEL_DIR, f"{name}.glb"))
        }
        for name, data in MODEL_MAP.items()
    }


@app.get("/generate")
def generate_model(prompt: str):
    """Match a text prompt to the best model."""
    prompt_lower = prompt.lower().strip()

    for model_name, data in MODEL_MAP.items():
        for keyword in data["keywords"]:
            if keyword in prompt_lower:
                return {
                    "model": model_name,
                    "reply": f"✅ I understood your request.\n{data['description']}"
                }

    return {
        "model": None,
        "reply": (
            "❌ Sorry, I couldn't recognize that. Try:\n"
            "duck, lamborghini, bmw, fish, robot, truck, heart,\n"
            "boombox, bottle, helmet, lantern, camera, corset,\n"
            "avocado, scifi helmet, or bike."
        )
    }


@app.get("/model/{model_name:path}")
def serve_model(model_name: str):
    """Serve a GLB model — fetch from remote & cache locally on first request."""
    model_name = model_name.lower().strip()

    if model_name not in MODEL_MAP:
        return JSONResponse({"error": f"Model '{model_name}' not found."}, status_code=404)

    local_path = os.path.join(MODEL_DIR, f"{model_name}.glb")

    # Serve from local cache if already downloaded
    if os.path.exists(local_path):
        return FileResponse(
            local_path,
            media_type="model/gltf-binary",
            filename=f"{model_name}.glb"
        )

    # Prevent duplicate simultaneous downloads
    with _lock:
        if model_name in _downloading:
            return JSONResponse(
                {"error": "Model is currently downloading. Please try again in a moment."},
                status_code=503
            )
        _downloading[model_name] = True

    # Fetch from remote URL and cache
    try:
        remote_url = MODEL_MAP[model_name].get("remote_url")
        if not remote_url:
            with _lock:
                _downloading.pop(model_name, None)
            return JSONResponse({
                "error": f"Model '{model_name}' must be uploaded manually by placing '{model_name}.glb' in the 'models' directory at the root of the project."
            }, status_code=404)

        print(f"[INFO] Fetching {model_name} from: {remote_url}")

        response = requests.get(remote_url, timeout=60, stream=True)
        response.raise_for_status()

        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[INFO] Cached {model_name} at {local_path}")

    except Exception as e:
        print(f"[ERROR] Failed to fetch {model_name}: {e}")
        return JSONResponse({"error": f"Failed to fetch model: {str(e)}"}, status_code=500)

    finally:
        with _lock:
            _downloading.pop(model_name, None)

    return FileResponse(
        local_path,
        media_type="model/gltf-binary",
        filename=f"{model_name}.glb"
    )
