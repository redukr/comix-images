"""
Сервіс для роботи з даними JOJ гри
"""

import json
import os
from typing import List, Dict, Optional, Any

class JOJService:
    def __init__(self, ranks_path: str, cards_path: str, images_path: str):
        self.ranks_path = ranks_path
        self.cards_path = cards_path
        self.images_path = images_path
        
        self._ranks = None
        self._cards = None
        self._loaded = False
    
    def is_available(self) -> bool:
        """Перевірка доступності JOJ даних"""
        return os.path.exists(self.ranks_path) and os.path.exists(self.cards_path)
    
    def _load_data(self):
        """Завантажити дані з JSON файлів"""
        if self._loaded:
            return
        
        # Завантажуємо ранги
        if os.path.exists(self.ranks_path):
            with open(self.ranks_path, 'r', encoding='utf-8') as f:
                self._ranks = json.load(f)
        else:
            self._ranks = []
        
        # Завантажуємо карти
        if os.path.exists(self.cards_path):
            with open(self.cards_path, 'r', encoding='utf-8') as f:
                cards_data = json.load(f)
                self._cards = cards_data.get("catalog", [])
        else:
            self._cards = []
        
        self._loaded = True
    
    def get_ranks(self) -> List[Dict[str, Any]]:
        """Отримати всі ранги ЗСУ"""
        self._load_data()
        return self._ranks
    
    def get_rank_by_id(self, rank_id: str) -> Optional[Dict[str, Any]]:
        """Отримати ранг за ID"""
        self._load_data()
        for rank in self._ranks:
            if rank.get("id") == rank_id:
                return rank
        return None
    
    def get_rank_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Отримати ранг за назвою (українською)"""
        self._load_data()
        for rank in self._ranks:
            if rank.get("name") == name:
                return rank
        return None
    
    def get_rank_progression(self, from_rank_id: str, to_rank_id: str) -> List[Dict[str, Any]]:
        """Отримати послідовність рангів від from до to"""
        self._load_data()
        
        # Знаходимо індекси
        from_idx = -1
        to_idx = -1
        
        for i, rank in enumerate(self._ranks):
            if rank.get("id") == from_rank_id:
                from_idx = i
            if rank.get("id") == to_rank_id:
                to_idx = i
        
        if from_idx == -1 or to_idx == -1:
            return []
        
        # Повертаємо діапазон
        if from_idx <= to_idx:
            return self._ranks[from_idx:to_idx + 1]
        else:
            return self._ranks[to_idx:from_idx + 1]
    
    def get_cards(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Отримати карти, опціонально фільтруючи за категорією"""
        self._load_data()
        
        if category:
            return [card for card in self._cards if card.get("category") == category]
        return self._cards
    
    def get_card_by_id(self, card_id: str) -> Optional[Dict[str, Any]]:
        """Отримати карту за ID"""
        self._load_data()
        for card in self._cards:
            if card.get("id") == card_id:
                return card
        return None
    
    def get_cards_for_rank(self, rank_id: str) -> List[Dict[str, Any]]:
        """Отримати карти, пов'язані з конкретним рангом"""
        self._load_data()
        
        result = []
        rank_data = self.get_rank_by_id(rank_id)
        
        if not rank_data:
            return result
        
        rank_name = rank_data.get("name", "")
        
        for card in self._cards:
            # Перевіряємо grantRank
            if card.get("grantRank") == rank_id:
                result.append(card)
                continue
            
            # Перевіряємо чи є збіги в назві категорії та рангу
            category = card.get("category", "")
            
            # VVNZ карти для офіцерських рангів
            if category == "VVNZ" and rank_id in [
                "junior_lieutenant", "lieutenant", "senior_lieutenant",
                "captain", "major", "lieutenant_colonel", "colonel", "general"
            ]:
                result.append(card)
            
            # COMMAND карти для сержантів та офіцерів
            elif category == "COMMAND" and rank_id in [
                "junior_sergeant", "sergeant", "senior_sergeant", "chief_sergeant",
                "staff_sergeant", "master_sergeant", "senior_master_sergeant",
                "chief_master_sergeant", "junior_lieutenant"
            ]:
                result.append(card)
            
            # Початкові карти для солдатів
            elif category in ["SCANDAL", "SUPPORT"] and rank_id in [
                "recruit", "soldier", "senior_soldier"
            ]:
                result.append(card)
        
        return result
    
    def get_card_image_path(self, card_id: str) -> Optional[str]:
        """Отримати шлях до зображення карти"""
        card = self.get_card_by_id(card_id)
        if not card:
            return None
        
        image_path = card.get("image", "")
        if image_path:
            # Конвертуємо /cards/ шлях в локальний
            if image_path.startswith("/cards/"):
                filename = os.path.basename(image_path)
                return os.path.join(self.images_path, filename)
        
        return None
    
    def get_cards_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Отримати всі карти певної категорії"""
        return self.get_cards(category=category)
    
    def get_random_cards_for_story(self, rank_progression: List[str], count: int = 8) -> List[Dict[str, Any]]:
        """
        Підібрати набор карт для історії на основі прогресії рангів
        
        Args:
            rank_progression: Список ID рангів в історії
            count: Скільки карт потрібно
        """
        import random
        
        selected_cards = []
        ranks_per_card = len(rank_progression) // count if count > 0 else 1
        
        for i in range(count):
            start_idx = i * ranks_per_card
            end_idx = min((i + 1) * ranks_per_card, len(rank_progression))
            
            # Беремо середній ранг для цього сегмента
            segment_ranks = rank_progression[start_idx:end_idx]
            if segment_ranks:
                target_rank = segment_ranks[len(segment_ranks) // 2]
                
                # Отримуємо карти для цього рангу
                available_cards = self.get_cards_for_rank(target_rank)
                
                if available_cards:
                    # Вибираємо одну випадкову карту
                    card = random.choice(available_cards)
                    card_copy = card.copy()
                    card_copy["story_rank"] = target_rank
                    card_copy["story_segment"] = i + 1
                    selected_cards.append(card_copy)
        
        return selected_cards
    
    def get_rank_story_context(self, rank_id: str) -> Dict[str, Any]:
        """Отримати контекст для історії про конкретний ранг"""
        rank = self.get_rank_by_id(rank_id)
        if not rank:
            return {}
        
        # Отримуємо карти цього рангу
        cards = self.get_cards_for_rank(rank_id)
        
        # Формуємо контекст
        context = {
            "rank": rank,
            "available_cards": cards,
            "flavor": rank.get("flavor", ""),
            "requirements": rank.get("requirement", {}),
            "costs": rank.get("cost", {}),
            "bonuses": rank.get("bonus", {}),
            "story_prompt": f"""
Ранг: {rank.get('name')}
Опис: {rank.get('flavor')}
Вимоги: {rank.get('requirement', {})}
"""
        }
        
        return context
    
    def export_for_comic(self, from_rank: str, to_rank: str) -> Dict[str, Any]:
        """Експортувати дані для генерації коміксу"""
        progression = self.get_rank_progression(from_rank, to_rank)
        rank_ids = [r.get("id") for r in progression]
        
        # Підбираємо карти
        cards = self.get_random_cards_for_story(rank_ids, count=min(8, len(progression)))
        
        return {
            "rank_progression": progression,
            "selected_cards": cards,
            "total_ranks": len(progression),
            "estimated_pages": min(8, len(progression))
        }
