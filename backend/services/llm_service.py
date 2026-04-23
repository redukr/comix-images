"""
Сервіс для роботи з LLM Studio (OpenAI-compatible API)
"""

import openai
from typing import Dict, List, Any
import json

class LLMService:
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key="not-needed"  # Локальний LLM не потребує ключа
        )
        self.model = "local-model"
        
    def is_available(self) -> bool:
        """Перевірка доступності LLM Studio"""
        try:
            self.client.models.list()
            return True
        except:
            return False
    
    def generate_comic_story(self, rank_from: Dict, rank_to: Dict, theme: str, num_pages: int = 8) -> Dict[str, Any]:
        """
        Генерація сюжету коміксу про кар'єрний ріст в ЗСУ
        
        Args:
            rank_from: Дані про початковий ранг (recruit)
            rank_to: Дані про кінцевий ранг (general)
            theme: Тема коміксу (military, career, heroic)
            num_pages: Кількість сторінок/панелей
        """
        
        system_prompt = """Ти — сценарист військових коміксів про ЗСУ. 
Створюй реалістичні, емоційні історії про кар'єрний ріст в армії.
Використовуй українську мову. Додавай діалоги з військовим гумором.
"""
        
        user_prompt = f"""Створи сюжет коміксу про шлях від "{rank_from['name']}" до "{rank_to['name']}" в ЗСУ.

Контекст:
- Початковий ранг: {rank_from['name']} — "{rank_from.get('flavor', '')}"
- Кінцевий ранг: {rank_to['name']} — "{rank_to.get('flavor', '')}"
- Тема: {theme}
- Кількість сторінок: {num_pages}

Для кожної сторінки вкажи:
1. Назву сцени
2. Опис дії (для зображення)
3. Діалоги персонажів
4. Підпис (caption)
5. Який ранг відображається на цій сторінці

Відповідь у форматі JSON:
{{
    "story": "Короткий опис загальної історії",
    "panels": [
        {{
            "page": 1,
            "title": "Назва сцени",
            "description": "Опис для зображення",
            "speech": "Діалоги",
            "caption": "Підпис до панелі",
            "rank": "soldier",
            "location": "Казарма/Полігон/..."
        }}
    ]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # Парсинг JSON з відповіді
            # Видаляємо можливі markdown блоки ```json ... ```
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            story_data = json.loads(content)
            return story_data
            
        except Exception as e:
            # Якщо LLM не повернув валідний JSON, повертаємо структуру з текстом
            return {
                "story": content if 'content' in locals() else "Error generating story",
                "panels": [],
                "error": str(e)
            }
    
    def generate_dialog(self, scene: str, characters: str, mood: str = "neutral") -> str:
        """Генерація діалогу для конкретної сцени"""
        
        prompt = f"""Напиши діалог для військової сцени.

Сцена: {scene}
Персонажі: {characters}
Настрій: {mood}

Стиль: реалістичний військовий гумор, українська мова, розмовний стиль.
Формат: 
- Ім'я: "Репліка"
- Ім'я: "Відповідь"
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_joj_card(self, card_data: Dict) -> Dict[str, str]:
        """Аналіз карти JOJ для використання в коміксі"""
        
        prompt = f"""Проаналізуй цю карту з військової гри та запропонуй, як її використати в коміксі:

Карта: {card_data.get('title', 'Unknown')}
Категорія: {card_data.get('category', 'Unknown')}
Flavor текст: {card_data.get('flavor', 'None')}
Ефекти: {card_data.get('effects', [])}

Відповідь у форматі JSON:
{{
    "scene_idea": "Ідея сцени",
    "dialog_suggestion": "Пропозиція діалогу",
    "visual_description": "Опис для ілюстрації",
    "mood": "emotional/comedic/dramatic/intense"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except:
            return {
                "scene_idea": "Використати карту в коміксі",
                "dialog_suggestion": "Військові обговорюють ситуацію",
                "visual_description": card_data.get('title', 'Military scene'),
                "mood": "neutral"
            }
