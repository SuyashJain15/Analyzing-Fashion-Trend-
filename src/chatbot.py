"""
AI Chatbot for Fashion Outfit Suggestions
Uses OpenAI API or local intelligent responses
"""
import os
import json
from typing import Dict, List, Optional
from pathlib import Path

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class FashionChatbot:
    """AI-powered fashion advisor chatbot"""
    
    def __init__(self):
        self.use_openai = OPENAI_AVAILABLE and os.environ.get('OPENAI_API_KEY')
        if self.use_openai:
            openai.api_key = os.environ.get('OPENAI_API_KEY')
        
        # Load fashion knowledge base
        self.trends_path = Path(__file__).parent.parent / 'artifacts' / 'top_trends.json'
        self.load_trends()
    
    def load_trends(self):
        """Load current fashion trends"""
        try:
            if self.trends_path.exists():
                with open(self.trends_path, 'r', encoding='utf-8') as f:
                    self.trends = json.load(f)
            else:
                self.trends = {"colors": ["black", "navy", "beige"], "items": ["jacket", "sneakers"]}
        except Exception as e:
            # Fallback if loading fails
            self.trends = {"colors": ["black", "navy", "beige"], "items": ["jacket", "sneakers"]}
    
    def get_response(self, user_message: str, outfit_context: Optional[Dict] = None) -> str:
        """
        Get chatbot response
        
        Args:
            user_message: User's question
            outfit_context: Current outfit analysis context
        
        Returns:
            AI-generated response
        """
        user_message_lower = user_message.lower()
        
        # Check for specific fashion-related queries
        if any(word in user_message_lower for word in ['color', 'change color', 'different color']):
            return self._suggest_color(user_message, outfit_context)
        
        elif any(word in user_message_lower for word in ['watch', 'accessor', 'add', 'wear']):
            return self._suggest_accessories(user_message, outfit_context)
        
        elif any(word in user_message_lower for word in ['trend', 'trending', 'style', 'fashion']):
            return self._suggest_trends()
        
        elif any(word in user_message_lower for word in ['outfit', 'look', 'appearance']):
            return self._analyze_outfit(user_message, outfit_context)
        
        elif self.use_openai:
            return self._openai_response(user_message, outfit_context)
        else:
            return self._local_response(user_message, outfit_context)
    
    def _suggest_color(self, message: str, context: Optional[Dict]) -> str:
        """Suggest color changes"""
        suggestions = []
        
        if context:
            current_colors = context.get('colors', [])
            trending_colors = self.trends.get('colors', ['black', 'navy', 'beige', 'white'])
            
            for color in trending_colors:
                if color not in current_colors:
                    suggestions.append(color)
            
            if suggestions:
                return f"💡 Consider these trending colors: {', '.join(suggestions[:3])}. " \
                       f"These work great for a modern, sophisticated look!"
            else:
                return "Your current color palette is already on-trend! 🎨 Consider experimenting with complementary shades."
        
        return "The trending colors this season are: black, navy, beige, and soft pastels. " \
               "These create an elegant, timeless look! ✨"
    
    def _suggest_accessories(self, message: str, context: Optional[Dict]) -> str:
        """Suggest accessories and additions"""
        accessories = [
            "⌚ A minimalist watch adds sophistication",
            "👔 A statement scarf can elevate your look",
            "🕶️ Sunglasses are always a classic touch",
            "🧢 A baseball cap for casual vibes",
            "💼 A leather belt to define your waist",
            "🎒 A stylish backpack or tote bag",
            "💍 Minimalist jewelry for elegance",
            "🧦 Statement socks for personality"
        ]
        
        import random
        selected = random.sample(accessories, 3)
        
        response = "Complete your outfit with these trendy accessories:\n\n"
        response += "\n".join(f"• {acc}" for acc in selected)
        response += "\n\n✨ Tip: Choose 1-2 accessories max to avoid over-accessorizing!"
        
        return response
    
    def _suggest_trends(self) -> str:
        """Suggest current fashion trends"""
        colors = ', '.join(self.trends.get('colors', ['black', 'navy', 'beige']))
        items = ', '.join(self.trends.get('items', ['jacket', 'sneakers']))
        
        return f"🔥 Current Fashion Trends:\n\n" \
               f"🎨 Colors: {colors}\n" \
               f"👕 Items: {items}\n\n" \
               f"💡 Pro tip: Mix trendy colors with classic pieces for a balanced, timeless look!"
    
    def _analyze_outfit(self, message: str, context: Optional[Dict]) -> str:
        """Analyze and provide outfit feedback"""
        if not context:
            return "Upload an outfit photo for personalized analysis! 📸"
        
        status = context.get('trend_status', 'Unknown')
        items = context.get('items', [])
        colors = context.get('colors', [])
        
        if status == 'Trending':
            return f"Your outfit is on-trend! ✨ Your {', '.join(colors)} color scheme works great. " \
                   f"Keep experimenting with different silhouettes and textures."
        else:
            return f"Your outfit could use some updates. Try incorporating trending colors like " \
                   f"{self.trends.get('colors', ['navy', 'beige'])[0]} or updating your {items[0] if items else 'top'} " \
                   f"with modern cuts."
    
    def _openai_response(self, message: str, context: Optional[Dict]) -> str:
        """Get response from OpenAI"""
        try:
            prompt = self._build_prompt(message, context)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly fashion advisor. Provide helpful, trendy outfit suggestions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return self._local_response(message, context)
    
    def _local_response(self, message: str, context: Optional[Dict]) -> str:
        """Fallback intelligent responses"""
        greetings = ['hi', 'hello', 'hey', 'greetings']
        thanks = ['thank', 'thanks', 'appreciate']
        
        if any(word in message.lower() for word in greetings):
            return "Hello! 👋 I'm your fashion advisor. Ask me about colors, accessories, trends, or outfit suggestions!"
        
        elif any(word in message.lower() for word in thanks):
            return "You're welcome! Happy to help you look your best! 💫"
        
        elif 'help' in message.lower():
            return "I can help you with:\n\n" \
                   "• 🎨 Color suggestions\n" \
                   "• ⌚ Accessory recommendations\n" \
                   "• 🔥 Current fashion trends\n" \
                   "• 👔 Outfit analysis\n\n" \
                   "Just ask me anything!"
        
        else:
            return "Interesting question! 🤔 For fashion advice, try asking about:\n\n" \
                   "• 'What colors should I wear?'\n" \
                   "• 'What accessories match my outfit?'\n" \
                   "• 'What's trending this season?'\n\n" \
                   "Or upload an outfit photo for personalized analysis!"
    
    def _build_prompt(self, message: str, context: Optional[Dict]) -> str:
        """Build prompt for OpenAI"""
        prompt = f"User question: {message}\n\n"
        
        if context:
            prompt += f"Current outfit: {context.get('colors', [])} colors, {context.get('items', [])} items, "
            prompt += f"Status: {context.get('trend_status', 'Unknown')}\n\n"
        
        prompt += "Provide a helpful, friendly fashion advice response."
        return prompt


# Singleton instance
_chatbot_instance = None

def get_chatbot() -> FashionChatbot:
    """Get singleton chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = FashionChatbot()
    return _chatbot_instance

