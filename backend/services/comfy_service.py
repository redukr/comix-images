"""
Сервіс для роботи з ComfyUI API
"""

import json
import uuid
import requests
from typing import Dict, Optional, Any
import time

class ComfyService:
    def __init__(self, server_address: str = "127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.jobs = {}  # Відстеження job_id -> status
        
    def is_available(self) -> bool:
        """Перевірка доступності ComfyUI"""
        try:
            response = requests.get(f"http://{self.server_address}/system_stats", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_queue_size(self) -> int:
        """Отримати кількість завдань у черзі"""
        try:
            response = requests.get(f"http://{self.server_address}/queue")
            data = response.json()
            return len(data.get("queue_running", [])) + len(data.get("queue_pending", []))
        except:
            return -1
    
    def queue_prompt(self, workflow: Dict) -> str:
        """Додати workflow до черги ComfyUI"""
        try:
            p = {"prompt": workflow, "client_id": self.client_id}
            response = requests.post(
                f"http://{self.server_address}/prompt",
                json=p,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            job_id = data.get("prompt_id", str(uuid.uuid4()))
            self.jobs[job_id] = {"status": "queued", "progress": 0}
            return job_id
            
        except Exception as e:
            raise Exception(f"Failed to queue prompt: {str(e)}")
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Отримати статус завдання"""
        try:
            # Перевіряємо історію
            response = requests.get(f"http://{self.server_address}/history/{job_id}")
            if response.status_code == 200:
                data = response.json()
                if job_id in data:
                    return {
                        "status": "completed",
                        "outputs": data[job_id].get("outputs", {}),
                        "progress": 100
                    }
            
            # Перевіряємо чергу
            response = requests.get(f"http://{self.server_address}/queue")
            queue_data = response.json()
            
            for item in queue_data.get("queue_running", []):
                if item[1] == job_id:
                    return {"status": "running", "progress": 50}
            
            for item in queue_data.get("queue_pending", []):
                if item[1] == job_id:
                    return {"status": "queued", "progress": 0}
            
            return {"status": "unknown", "progress": 0}
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024, 
                       seed: Optional[int] = None, workflow_template: str = "basic") -> Dict[str, Any]:
        """
        Генерація зображення через ComfyUI
        
        Args:
            prompt: Промпт для генерації
            width: Ширина зображення
            height: Висота зображення  
            seed: Seed для відтворюваності
            workflow_template: Назва workflow (basic, comic, realistic)
        """
        # Завантажуємо workflow шаблон
        workflow = self._load_workflow(workflow_template)
        
        # Модифікуємо workflow
        workflow = self._modify_workflow(
            workflow, 
            prompt=prompt,
            width=width,
            height=height,
            seed=seed
        )
        
        # Додаємо до черги
        job_id = self.queue_prompt(workflow)
        
        return {
            "job_id": job_id,
            "status": "queued",
            "message": "Image generation started"
        }
    
    def queue_image_generation(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        """Додати генерацію зображення до черги, повернути job_id"""
        workflow = self._load_workflow("comic")
        workflow = self._modify_workflow(workflow, prompt=prompt, width=width, height=height)
        return self.queue_prompt(workflow)
    
    def _load_workflow(self, template_name: str) -> Dict:
        """Завантажити workflow шаблон з файлу"""
        workflow_path = f"../workflows/{template_name}_api.json"
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Повертаємо базовий workflow, якщо файл не знайдено
            return self._create_basic_workflow()
    
    def _modify_workflow(self, workflow: Dict, prompt: str, width: int, 
                         height: int, seed: Optional[int] = None) -> Dict:
        """Модифікувати workflow з новими параметрами"""
        workflow_copy = json.loads(json.dumps(workflow))  # Deep copy
        
        # Знаходимо вузли KSampler та CLIPTextEncode
        for node_id, node in workflow_copy.items():
            if node.get("class_type") == "CLIPTextEncode":
                # Замінюємо позитивний промпт
                if node.get("inputs", {}).get("text", "") == "__POSITIVE_PROMPT__":
                    node["inputs"]["text"] = prompt
            
            if node.get("class_type") == "KSampler":
                # Встановлюємо seed
                if seed is not None:
                    node["inputs"]["seed"] = seed
                else:
                    node["inputs"]["seed"] = int(time.time())
            
            if node.get("class_type") in ["EmptyLatentImage", "EmptySD3LatentImage"]:
                # Встановлюємо розмір
                node["inputs"]["width"] = width
                node["inputs"]["height"] = height
        
        return workflow_copy
    
    def _create_basic_workflow(self) -> Dict:
        """Створити базовий workflow для генерації"""
        # Це мінімальний workflow для SDXL
        return {
            "1": {
                "inputs": {"ckpt_name": "SDXL/sd_xl_base_1.0.safetensors"},
                "class_type": "CheckpointLoaderSimple"
            },
            "2": {
                "inputs": {"text": "__POSITIVE_PROMPT__", "clip": ["1", 1]},
                "class_type": "CLIPTextEncode"
            },
            "3": {
                "inputs": {"text": "blurry, low quality, worst quality", "clip": ["1", 1]},
                "class_type": "CLIPTextEncode"
            },
            "4": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "5": {
                "inputs": {
                    "seed": 0,
                    "steps": 30,
                    "cfg": 8,
                    "sampler_name": "euler_ancestral",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["1", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["4", 0]
                },
                "class_type": "KSampler"
            },
            "6": {
                "inputs": {"samples": ["5", 0], "vae": ["1", 2]},
                "class_type": "VAEDecode"
            },
            "7": {
                "inputs": {"filename_prefix": "Comic", "images": ["6", 0]},
                "class_type": "SaveImage"
            }
        }
    
    def get_output_image(self, job_id: str) -> Optional[str]:
        """Отримати шлях до згенерованого зображення (після завершення)"""
        status = self.get_job_status(job_id)
        
        if status.get("status") == "completed":
            outputs = status.get("outputs", {})
            for node_id, node_output in outputs.items():
                if "images" in node_output:
                    return node_output["images"][0].get("filename")
        
        return None
