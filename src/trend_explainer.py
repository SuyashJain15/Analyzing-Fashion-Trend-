"""
Trend Explanation Generator
Provides detailed reasoning behind trending/outdated classification
"""
from typing import Dict, List
import random


class TrendExplainer:
    """Generates detailed explanations for trend classifications"""
    
    def __init__(self):
        self.trending_reasons = [
            "Denim and monochrome black outfits are currently popular in streetwear fashion.",
            "Minimalist color palettes with neutral tones are trending this season.",
            "Layering with structured pieces creates a modern, sophisticated look.",
            "Athleisure elements combined with casual wear are dominating current trends.",
            "Oversized silhouettes and relaxed fits are popular in contemporary fashion.",
            "Monochromatic outfits with contrasting textures are on-trend.",
            "Sustainable fashion choices with classic pieces are gaining popularity.",
            "Streetwear influences with casual elegance are trending.",
        ]
        
        self.outdated_reasons = [
            "The color combination suggests styles from previous seasons.",
            "Fitted silhouettes are being replaced by more relaxed, modern cuts.",
            "This style pattern was popular 2-3 years ago but has declined.",
            "Bright, saturated colors are less common in current fashion trends.",
            "Traditional fits without modern updates appear dated.",
            "The overall aesthetic lacks contemporary fashion elements.",
            "This combination reflects older fashion sensibilities.",
            "Classic pieces need modern styling to stay current.",
        ]
    
    def generate_explanation(self, outfit_data: Dict, trend_status: str) -> str:
        """
        Generate detailed explanation for trend classification
        
        Args:
            outfit_data: Outfit analysis data
            trend_status: 'Trending' or 'Outdated'
        
        Returns:
            Detailed explanation string
        """
        colors = outfit_data.get('colors', [])
        items = outfit_data.get('items', [])
        
        if trend_status == 'Trending':
            return self._explain_trending(colors, items)
        else:
            return self._explain_outdated(colors, items)
    
    def _explain_trending(self, colors: List[str], items: List[str]) -> str:
        """Explain why outfit is trending"""
        explanations = []
        
        # Color-based explanations
        if 'black' in colors or 'navy' in colors:
            explanations.append("Monochromatic dark tones are currently dominating streetwear and casual fashion.")
        
        if 'beige' in colors or 'white' in colors:
            explanations.append("Neutral color palettes are trending for their versatility and sophistication.")
        
        # Item-based explanations
        if 'top' in items and 'bottom' in items:
            explanations.append("Coordinated separates create a cohesive, modern look that's trending.")
        
        # Overall explanation
        if not explanations:
            explanations.append(random.choice(self.trending_reasons))
        
        return " ".join(explanations[:2])  # Return first 2 explanations
    
    def _explain_outdated(self, colors: List[str], items: List[str]) -> str:
        """Explain why outfit is outdated"""
        explanations = []
        
        # Color-based explanations
        if 'red' in colors or 'blue' in colors:
            explanations.append("Bright, saturated colors are less common in current minimalist fashion trends.")
        
        # Item-based explanations
        if 'top' in items and 'bottom' in items:
            explanations.append("The outfit combination suggests older styling patterns that need modern updates.")
        
        # Overall explanation
        if not explanations:
            explanations.append(random.choice(self.outdated_reasons))
        
        return " ".join(explanations[:2])  # Return first 2 explanations


# Singleton instance
_explainer_instance = None

def get_explainer() -> TrendExplainer:
    """Get singleton explainer instance"""
    global _explainer_instance
    if _explainer_instance is None:
        _explainer_instance = TrendExplainer()
    return _explainer_instance






