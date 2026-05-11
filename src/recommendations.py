"""
Advanced outfit recommendation engine
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple
import random


class OutfitRecommender:
    """Generate outfit recommendations based on trends and analysis"""
    
    def __init__(self):
        self.trends_path = Path(__file__).parent.parent / 'artifacts' / 'top_trends.json'
        self.load_trends()
    
    def load_trends(self):
        """Load current trends"""
        if self.trends_path.exists():
            with open(self.trends_path, 'r', encoding='utf-8') as f:
                self.trends = json.load(f)
        else:
            self.trends = {
                "colors": ["black", "navy", "beige", "white"],
                "items": ["jacket", "sneakers", "jeans"]
            }
    
    def generate_outfit_recommendations(self, current_outfit: Dict, trend_status: str) -> List[Dict]:
        """
        Generate outfit recommendations
        
        Args:
            current_outfit: Current outfit analysis
            trend_status: 'Trending' or 'Outdated'
        
        Returns:
            List of outfit recommendations
        """
        recommendations = []
        
        if trend_status == 'Outdated':
            # Generate complete outfit overhauls
            recommendations.extend(self._outdated_outfit_suggestions(current_outfit))
        else:
            # Suggest minor improvements
            recommendations.extend(self._trending_outfit_suggestions(current_outfit))
        
        return recommendations
    
    def _outdated_outfit_suggestions(self, outfit: Dict) -> List[Dict]:
        """Suggestions for outdated outfits"""
        suggestions = []
        
        current_colors = outfit.get('colors', [])
        trending_colors = self.trends.get('colors', [])
        
        # Color upgrade suggestions
        for color in trending_colors[:2]:
            if color not in current_colors:
                suggestions.append({
                    'type': 'color_change',
                    'title': f'Try {color.capitalize()}',
                    'description': f'Switch to trending {color} for a modern look',
                    'priority': 'high'
                })
        
        # Item suggestions
        items = ["jacket", "sneakers", "jeans", "shirt"]
        for item in items[:2]:
            suggestions.append({
                'type': 'add_item',
                'title': f'Add a {item}',
                'description': f'A stylish {item} can elevate your outfit',
                'priority': 'medium'
            })
        
        return suggestions
    
    def _trending_outfit_suggestions(self, outfit: Dict) -> List[Dict]:
        """Suggestions for trending outfits"""
        suggestions = []
        
        # Accessory suggestions
        accessories = [
            {'name': 'Watch', 'emoji': '⌚'},
            {'name': 'Sunglasses', 'emoji': '🕶️'},
            {'name': 'Cap', 'emoji': '🧢'},
            {'name': 'Belt', 'emoji': '💼'}
        ]
        
        for acc in random.sample(accessories, 2):
            suggestions.append({
                'type': 'accessory',
                'title': f'Add {acc["name"]}',
                'description': f'{acc["emoji"]} A {acc["name"].lower()} adds personality',
                'priority': 'low'
            })
        
        # Layering suggestions
        suggestions.append({
            'type': 'layering',
            'title': 'Try Layering',
            'description': 'Layer a jacket or cardigan for depth',
            'priority': 'medium'
        })
        
        return suggestions
    
    def get_complementary_colors(self, base_color: str) -> List[str]:
        """Get complementary colors for a base color"""
        color_map = {
            'black': ['white', 'beige', 'navy'],
            'white': ['black', 'navy', 'pastel'],
            'navy': ['white', 'beige', 'burgundy'],
            'beige': ['black', 'navy', 'olive'],
            'red': ['black', 'white', 'navy'],
            'blue': ['white', 'beige', 'tan']
        }
        
        return color_map.get(base_color.lower(), ['black', 'white', 'beige'])


# Singleton instance
_recommender_instance = None

def get_recommender() -> OutfitRecommender:
    """Get singleton recommender instance"""
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = OutfitRecommender()
    return _recommender_instance






