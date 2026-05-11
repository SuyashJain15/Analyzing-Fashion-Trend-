"""
Occasion Detection for Outfits
Classifies outfits by occasion type
"""
from typing import Dict, List
import random


class OccasionDetector:
    """Detects outfit occasion type"""
    
    def __init__(self):
        self.occasion_patterns = {
            'Traditional/Wedding': {
                'colors': ['beige', 'white', 'gold', 'maroon', 'red', 'navy', 'black'],
                'items': ['dress', 'shirt', 'jacket', 'top', 'bottom'],
                'confidence': 0.95,
                'color_bonus': ['beige', 'maroon', 'gold', 'red'],
                'style_keywords': ['sherwani', 'traditional', 'ethnic', 'wedding', 'safa', 'turban']
            },
            'Formal': {
                'colors': ['black', 'navy', 'white', 'gray'],
                'items': ['shirt', 'suit', 'jacket', 'dress'],
                'confidence': 0.85
            },
            'Casual': {
                'colors': ['black', 'white', 'blue', 'gray', 'beige'],
                'items': ['tshirt', 'jeans', 'sneakers', 'hoodie'],
                'confidence': 0.8
            },
            'Streetwear': {
                'colors': ['black', 'white', 'beige', 'gray'],
                'items': ['hoodie', 'sneakers', 'jacket', 'cap'],
                'confidence': 0.75
            },
            'Party': {
                'colors': ['black', 'red', 'navy', 'white'],
                'items': ['dress', 'shirt', 'jacket'],
                'confidence': 0.7
            },
            'Athletic': {
                'colors': ['black', 'white', 'blue', 'gray'],
                'items': ['sneakers', 'hoodie', 'jacket'],
                'confidence': 0.8
            }
        }
    
    def detect_occasion(self, outfit_data: Dict) -> Dict[str, any]:
        """
        Detect occasion type from outfit
        
        Args:
            outfit_data: Outfit analysis data
        
        Returns:
            Dict with occasion type and confidence
        """
        colors = [c.lower() for c in outfit_data.get('colors', [])]
        items = [i.lower() for i in outfit_data.get('items', [])]
        
        scores = {}
        
        # Check for Traditional/Wedding FIRST with smart detection
        # Traditional colors: beige, maroon, gold, red (for wedding outfits)
        traditional_colors = ['beige', 'maroon', 'gold', 'red']
        traditional_color_count = sum(1 for c in colors if c in traditional_colors)
        
        # Check for specific color combinations
        has_beige = 'beige' in colors
        has_maroon = 'maroon' in colors
        has_gold = 'gold' in colors
        has_red = 'red' in colors
        
        # Wedding outfit patterns:
        # 1. Beige + Maroon (classic wedding combo)
        # 2. Beige + Gold (traditional wedding)
        # 3. Maroon + Gold (wedding colors)
        # 4. Red + Gold (wedding colors)
        # 5. Multiple traditional colors (2+)
        is_traditional = (
            (has_beige and has_maroon) or  # Classic wedding combo
            (has_beige and has_gold) or    # Traditional wedding
            (has_maroon and has_gold) or   # Wedding colors
            (has_red and has_gold) or       # Wedding colors
            (traditional_color_count >= 2) # Multiple traditional colors
        )
        
        # Only consider Traditional/Wedding if we have traditional colors
        if not is_traditional:
            # Remove Traditional/Wedding from consideration
            patterns_to_check = {k: v for k, v in self.occasion_patterns.items() if 'Traditional' not in k}
        else:
            patterns_to_check = self.occasion_patterns
        
        for occasion, patterns in patterns_to_check.items():
            score = 0
            
            # Color matching
            color_matches = sum(1 for c in colors if c in patterns['colors'])
            if colors:
                score += (color_matches / len(colors)) * 0.5
            
            # Item matching
            item_matches = sum(1 for i in items if i in patterns['items'])
            if items:
                score += (item_matches / len(items)) * 0.5
            
            # Boost Traditional/Wedding for specific color combinations
            if 'Traditional/Wedding' in occasion:
                # Wedding color combinations boost score
                if (has_beige and has_maroon) or (has_beige and has_gold) or (has_maroon and has_gold):
                    score += 0.4  # Strong boost for wedding colors
                if traditional_color_count >= 2:
                    score += 0.3  # Bonus for multiple traditional colors
            
            # Boost Casual for common casual items
            if 'Casual' in occasion:
                casual_items = ['tshirt', 'jeans', 'sneakers', 'hoodie', 'top', 'bottom']
                if any(casual in items for casual in casual_items):
                    score += 0.5  # Very strong boost for casual items
            
            # Boost Formal for formal items
            if 'Formal' in occasion:
                formal_items = ['shirt', 'suit', 'jacket', 'dress']
                if any(formal in items for formal in formal_items):
                    score += 0.2
            
            scores[occasion] = score * patterns['confidence']
        
        # Get best match
        best_occasion = max(scores, key=scores.get)
        confidence = scores[best_occasion]
        
        # Cap confidence at 100%
        confidence = min(confidence, 1.0)
        
        # Ensure minimum confidence of 40%
        if confidence < 0.4:
            confidence = 0.45
        
        return {
            'occasion': best_occasion,
            'confidence': round(confidence, 2),
            'all_scores': scores
        }
    
    def get_occasion_suggestions(self, occasion: str) -> List[str]:
        """Get suggestions based on occasion"""
        suggestions_map = {
            'Traditional/Wedding': [
                "Perfect for weddings and traditional ceremonies",
                "Great for cultural celebrations and formal gatherings",
                "Ideal for religious events and festive occasions"
            ],
            'Casual': [
                "Perfect for everyday wear and casual outings",
                "Great for weekend activities and social gatherings",
                "Ideal for relaxed, comfortable style"
            ],
            'Formal': [
                "Appropriate for business meetings and formal events",
                "Suitable for professional settings",
                "Great for ceremonies and important occasions"
            ],
            'Streetwear': [
                "Perfect for urban, edgy fashion style",
                "Great for concerts, festivals, and casual hangouts",
                "Ideal for expressing personal style"
            ],
            'Party': [
                "Perfect for nightlife and social events",
                "Great for celebrations and parties",
                "Ideal for standing out at events"
            ],
            'Athletic': [
                "Perfect for sports and fitness activities",
                "Great for active lifestyle",
                "Ideal for gym and outdoor activities"
            ]
        }
        
        return suggestions_map.get(occasion, [
            "Adaptable for various occasions",
            "Versatile outfit for multiple settings"
        ])


# Singleton instance
_detector_instance = None

def get_detector() -> OccasionDetector:
    """Get singleton detector instance"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = OccasionDetector()
    return _detector_instance

