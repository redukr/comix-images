"""
JOJ Comic Generator - Backend API
FastAPI сервер для роботи з LLM Studio, ComfyUI та JOJ даними
"""

import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

# Імпорт сервісів
from services.llm_service import LLMService
from services.comfy_service import ComfyService
from services.joj_service import JOJService

app = FastAPI(
    title="JOJ Comic Generator API",
    description="API для генерації коміксів на основі гри JOJ",
    version="1.0.0"
)

# CORS для роботи з Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ініціалізація сервісів
llm_service = LLMService(base_url="http://localhost:1234/v1")
comfy_service = ComfyService(server_address="127.0.0.1:8188")
joj_service = JOJService(
    ranks_path="../data/joj-ranks.json",
    cards_path="../data/joj-cards.json",
    images_path="../data/card-images"
)

# ===== MODELS =====

class StoryRequest(BaseModel):
    rank_from: str  # recruit
    rank_to: str    # general
    theme: str      # military, career, heroic
    num_pages: int = 8
    
class StoryResponse(BaseModel):
    story: str
    panels: List[Dict[str, Any]]
    
class ImageGenerationRequest(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024
    seed: Optional[int] = None

class ComicBuildRequest(BaseModel):
    rank_from: str
    rank_to: str
    use_comfy: bool = True
    use_joj_cards: bool = True

# ===== ROUTES =====

@app.get("/")
async def root():
    return {
        "message": "JOJ Comic Generator API",
        "status": "running",
        "services": {
            "llm": llm_service.is_available(),
            "comfy": comfy_service.is_available(),
            "joj": joj_service.is_available()
        }
    }

# ----- JOJ Data Routes -----

@app.get("/api/joj/ranks")
async def get_ranks():
    """Отримати список усіх рангів ЗСУ"""
    try:
        ranks = joj_service.get_ranks()
        return {"ranks": ranks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/joj/cards")
async def get_cards(category: Optional[str] = None):
    """Отримати карти (опціонально фільтр за категорією)"""
    try:
        cards = joj_service.get_cards(category=category)
        return {"cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/joj/cards-by-rank/{rank_id}")
async def get_cards_by_rank(rank_id: str):
    """Отримати карти, пов'язані з конкретним рангом"""
    try:
        cards = joj_service.get_cards_for_rank(rank_id)
        return {"rank": rank_id, "cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- LLM Routes -----

@app.post("/api/llm/story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """Генерація сюжету коміксу через LLM Studio"""
    try:
        # Отримуємо дані про ранги
        rank_from_data = joj_service.get_rank_by_id(request.rank_from)
        rank_to_data = joj_service.get_rank_by_id(request.rank_to)
        
        if not rank_from_data or not rank_to_data:
            raise HTTPException(status_code=400, detail="Invalid rank ID")
        
        # Генеруємо сюжет
        story_data = llm_service.generate_comic_story(
            rank_from=rank_from_data,
            rank_to=rank_to_data,
            theme=request.theme,
            num_pages=request.num_pages
        )
        
        return story_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/llm/dialog")
async def generate_dialog(request: Dict[str, str]):
    """Генерація діалогу для конкретної сцени"""
    try:
        scene = request.get("scene", "")
        characters = request.get("characters", "")
        mood = request.get("mood", "neutral")
        
        dialog = llm_service.generate_dialog(scene, characters, mood)
        return {"dialog": dialog}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- ComfyUI Routes -----

@app.post("/api/comfy/generate")
async def generate_image(request: ImageGenerationRequest):
    """Генерація зображення через ComfyUI"""
    try:
        result = comfy_service.generate_image(
            prompt=request.prompt,
            width=request.width,
            height=request.height,
            seed=request.seed
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/comfy/status")
async def get_comfy_status():
    """Перевірка статусу ComfyUI"""
    return {
        "available": comfy_service.is_available(),
        "queue_size": comfy_service.get_queue_size()
    }

# ----- Comic Builder Routes -----

@app.post("/api/comic/build")
async def build_comic(request: ComicBuildRequest):
    """Повний пайплайн: сюжет + зображення + компонування"""
    try:
        # 1. Генеруємо сюжет
        rank_from_data = joj_service.get_rank_by_id(request.rank_from)
        rank_to_data = joj_service.get_rank_by_id(request.rank_to)
        
        story_data = llm_service.generate_comic_story(
            rank_from=rank_from_data,
            rank_to=rank_to_data,
            theme="military",
            num_pages=8
        )
        
        # 2. Для кожної панелі генеруємо/підбираємо зображення
        for panel in story_data["panels"]:
            if request.use_joj_cards and panel.get("joj_card_id"):
                # Використовуємо існуючу карту JOJ
                card = joj_service.get_card_by_id(panel["joj_card_id"])
                panel["image_path"] = card.get("image") if card else None
            elif request.use_comfy:
                # Генеруємо нове зображення через ComfyUI
                # (асинхронно - повертаємо job_id)
                job_id = comfy_service.queue_image_generation(
                    prompt=panel.get("image_prompt", panel.get("description", "")),
                    width=1024,
                    height=1024
                )
                panel["generation_job_id"] = job_id
        
        return {
            "status": "building",
            "story": story_data["story"],
            "panels": story_data["panels"],
            "metadata": {
                "rank_from": request.rank_from,
                "rank_to": request.rank_to,
                "use_comfy": request.use_comfy,
                "use_joj_cards": request.use_joj_cards
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/comic/status/{job_id}")
async def get_generation_status(job_id: str):
    """Перевірка статусу генерації зображення"""
    try:
        status = comfy_service.get_job_status(job_id)
        return {"job_id": job_id, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MAIN =====

if __name__ == "__main__":
    print("🚀 Запуск JOJ Comic Generator API...")
    print("📡 LLM Studio: http://localhost:1234/v1")
    print("🎨 ComfyUI: http://127.0.0.1:8188")
    print("🌐 API доступний за адресою: http://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
