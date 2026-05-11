"""
E-Commerce Links Generator
Generates shopping links for similar items with gender detection
"""
from typing import Dict, List
import urllib.parse


class ShoppingLinks:
    """Generate e-commerce links for outfit items"""
    
    def __init__(self):
        self.base_urls = {
            'amazon': 'https://www.amazon.com/s?k={query}',
            'myntra': 'https://www.myntra.com/{query}',
            'flipkart': 'https://www.flipkart.com/search?q={query}'
        }
        
        self.item_keywords_male = {
            'top': 'mens sherwani kurta traditional wear',
            'bottom': 'mens dhoti pants traditional',
            'dress': 'mens formal wear',
            'jacket': 'mens jackets coats',
            'shoes': 'mens shoes sneakers',
            'accessories': 'mens accessories fashion',
            'hoodie': 'mens hoodies sweatshirts',
            'tshirt': 'mens t-shirts',
            'jeans': 'mens jeans',
            'shirt': 'mens shirts',
            'sneakers': 'mens sneakers',
            'watch': 'mens watches',
            'cap': 'mens caps hats',
            'belt': 'mens belts'
        }
        
        self.item_keywords_female = {
            'top': 'womens tops blouses shirts',
            'bottom': 'womens jeans pants trousers',
            'dress': 'womens dresses',
            'jacket': 'womens jackets coats',
            'shoes': 'womens shoes heels',
            'accessories': 'womens accessories fashion',
            'hoodie': 'womens hoodies sweatshirts',
            'tshirt': 'womens t-shirts',
            'jeans': 'womens jeans',
            'shirt': 'womens shirts blouses',
            'sneakers': 'womens sneakers',
            'watch': 'womens watches',
            'cap': 'womens caps hats',
            'belt': 'womens belts'
        }
    
    def detect_gender(self, outfit_data: Dict) -> str:
        """
        Detect gender from outfit items
        Returns 'male' or 'female' or 'unisex'
        """
        items = [i.lower() for i in outfit_data.get('items', [])]
        colors = [c.lower() for c in outfit_data.get('colors', [])]
        
        # Male indicators - more specific
        male_indicators = ['hoodie', 'sneakers', 'jeans', 'tshirt', 'shirt', 'jacket', 'cap']
        female_indicators = ['dress', 'skirt', 'blouse', 'heels']
        
        # Check for specific male patterns
        male_score = sum(1 for item in items if any(ind in item for ind in male_indicators))
        female_score = sum(1 for item in items if any(ind in item for ind in female_indicators))
        
        # Traditional outfit detection - if beige/maroon/gold/red colors, likely traditional
        if 'beige' in colors or 'maroon' in colors or 'gold' in colors or 'red' in colors:
            if 'top' in items and 'bottom' in items:
                return 'male'  # Traditional male outfit (sherwani)
        
        # If only 'top' and 'bottom' detected, default to male (more common in dataset)
        if set(items) == {'top', 'bottom'}:
            return 'male'
        
        if female_score > male_score:
            return 'female'
        elif male_score > female_score:
            return 'male'
        else:
            return 'male'  # Default to male for ambiguous cases
    
    def generate_links(self, outfit_data: Dict, occasion: str = None) -> Dict[str, List[str]]:
        """
        Generate shopping links for outfit
        
        Args:
            outfit_data: Outfit analysis data
            occasion: Detected occasion type
        
        Returns:
            Dict with shopping links
        """
        colors = outfit_data.get('colors', [])
        items = outfit_data.get('items', [])
        
        # Detect gender
        gender = self.detect_gender(outfit_data)
        
        # Select appropriate keywords based on occasion
        if occasion and ('Traditional' in occasion or 'Wedding' in occasion):
            # Traditional/Wedding occasion
            if gender == 'male':
                item_keywords = {
                    'top': 'mens sherwani kurta traditional wear',
                    'bottom': 'mens dhoti pants traditional',
                    'dress': 'mens sherwani kurta',
                    'jacket': 'mens traditional jacket',
                    'shoes': 'mens traditional shoes',
                    'accessories': 'mens traditional accessories',
                    'hoodie': 'mens traditional wear',
                    'tshirt': 'mens kurta',
                    'jeans': 'mens traditional pants',
                    'shirt': 'mens kurta sherwani',
                    'sneakers': 'mens traditional footwear',
                    'watch': 'mens traditional watch',
                    'cap': 'mens traditional cap',
                    'belt': 'mens traditional belt'
                }
            else:
                item_keywords = {
                    'top': 'womens lehenga saree traditional wear',
                    'bottom': 'womens traditional wear',
                    'dress': 'womens lehenga saree',
                    'jacket': 'womens traditional jacket',
                    'shoes': 'womens traditional shoes',
                    'accessories': 'womens traditional accessories',
                    'hoodie': 'womens traditional wear',
                    'tshirt': 'womens traditional wear',
                    'jeans': 'womens traditional wear',
                    'shirt': 'womens traditional wear',
                    'sneakers': 'womens traditional footwear',
                    'watch': 'womens traditional watch',
                    'cap': 'womens traditional accessories',
                    'belt': 'womens traditional accessories'
                }
        elif occasion == 'Casual':
            # Casual occasion - use casual keywords
            if gender == 'female':
                item_keywords = {
                    'top': 'womens casual tops t-shirts',
                    'bottom': 'womens casual jeans pants',
                    'dress': 'womens casual dresses',
                    'jacket': 'womens casual jackets',
                    'shoes': 'womens casual shoes sneakers',
                    'accessories': 'womens casual accessories',
                    'hoodie': 'womens casual hoodies',
                    'tshirt': 'womens casual t-shirts',
                    'jeans': 'womens casual jeans',
                    'shirt': 'womens casual shirts',
                    'sneakers': 'womens casual sneakers',
                    'watch': 'womens casual watches',
                    'cap': 'womens casual caps',
                    'belt': 'womens casual belts'
                }
            elif gender == 'male':
                item_keywords = {
                    'top': 'mens casual shirts t-shirts',
                    'bottom': 'mens casual jeans pants',
                    'dress': 'mens casual wear',
                    'jacket': 'mens casual jackets',
                    'shoes': 'mens casual shoes sneakers',
                    'accessories': 'mens casual accessories',
                    'hoodie': 'mens casual hoodies',
                    'tshirt': 'mens casual t-shirts',
                    'jeans': 'mens casual jeans',
                    'shirt': 'mens casual shirts',
                    'sneakers': 'mens casual sneakers',
                    'watch': 'mens casual watches',
                    'cap': 'mens casual caps',
                    'belt': 'mens casual belts'
                }
            else:
                item_keywords = {
                    'top': 'casual shirts t-shirts',
                    'bottom': 'casual jeans pants',
                    'dress': 'casual dresses',
                    'jacket': 'casual jackets',
                    'shoes': 'casual shoes sneakers',
                    'accessories': 'casual accessories',
                    'hoodie': 'casual hoodies',
                    'tshirt': 'casual t-shirts',
                    'jeans': 'casual jeans',
                    'shirt': 'casual shirts',
                    'sneakers': 'casual sneakers',
                    'watch': 'casual watches',
                    'cap': 'casual caps',
                    'belt': 'casual belts'
                }
        else:
            # Other occasions (Formal, Party, etc.)
            if gender == 'female':
                item_keywords = self.item_keywords_female
            elif gender == 'male':
                item_keywords = self.item_keywords_male
            else:
                item_keywords = {k: v.replace('mens ', '').replace('womens ', '') for k, v in self.item_keywords_male.items()}
        
        links = {}
        
        # Generate query for each item
        for item in items:
            item_keyword = item_keywords.get(item.lower(), item)
            
            # Add color if available
            if colors:
                color_query = f"{colors[0]} {item_keyword}"
            else:
                color_query = item_keyword
            
            # Add occasion to query for better results
            if occasion:
                # Don't repeat Traditional/Wedding or Casual in query if already in keyword
                if 'Traditional' not in item_keyword and 'Wedding' not in item_keyword and 'casual' not in item_keyword.lower():
                    query = f"{occasion} {color_query}"
                else:
                    query = color_query
            else:
                query = color_query
            
            # Generate links for each platform
            item_links = {}
            for platform, base_url in self.base_urls.items():
                encoded_query = urllib.parse.quote(query)
                item_links[platform] = base_url.format(query=encoded_query)
            
            links[item] = item_links
        
        return links
    
    def get_shopping_suggestions(self, outfit_data: Dict, occasion: str = None) -> List[str]:
        """Get shopping suggestions"""
        colors = outfit_data.get('colors', [])
        items = outfit_data.get('items', [])
        gender = self.detect_gender(outfit_data)
        
        suggestions = []
        
        if colors and items:
            primary_color = colors[0]
            gender_text = 'mens' if gender == 'male' else 'womens' if gender == 'female' else ''
            suggestions.append(f"Shop similar {gender_text} {primary_color} {items[0]} on major fashion platforms")
        
        if occasion:
            suggestions.append(f"Find {occasion.lower()} outfits with similar styling")
        
        suggestions.append("Explore trending fashion items matching your style")
        
        return suggestions


# Singleton instance
_shopping_instance = None

def get_shopping() -> ShoppingLinks:
    """Get singleton shopping instance"""
    global _shopping_instance
    if _shopping_instance is None:
        _shopping_instance = ShoppingLinks()
    return _shopping_instance

