"""
History tracking for fashion analyses
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class HistoryManager:
    """Manages analysis history"""
    
    def __init__(self, history_file: Path):
        self.history_file = history_file
        self.history_file.parent.mkdir(exist_ok=True)
        self._ensure_history_exists()
    
    def _ensure_history_exists(self):
        """Create history file if it doesn't exist"""
        if not self.history_file.exists():
            self.history_file.write_text('[]', encoding='utf-8')
    
    def save_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """
        Save analysis to history
        
        Args:
            analysis_data: Complete analysis data
        
        Returns:
            Analysis ID
        """
        history = self.load_history()
        
        # Generate unique ID
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add timestamp and ID
        analysis_data['id'] = analysis_id
        analysis_data['timestamp'] = datetime.now().isoformat()
        
        # Add to history
        history.append(analysis_data)
        
        # Keep only last 50 analyses
        if len(history) > 50:
            history = history[-50:]
        
        # Save to file
        self.history_file.write_text(
            json.dumps(history, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        return analysis_id
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load all history"""
        try:
            return json.loads(self.history_file.read_text(encoding='utf-8'))
        except:
            return []
    
    def get_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Get specific analysis by ID"""
        history = self.load_history()
        for analysis in history:
            if analysis.get('id') == analysis_id:
                return analysis
        return {}
    
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analyses"""
        history = self.load_history()
        return history[-limit:]
    
    def clear_history(self):
        """Clear all history"""
        self.history_file.write_text('[]', encoding='utf-8')


# Singleton instance
_history_manager = None

def get_history_manager() -> HistoryManager:
    """Get singleton history manager"""
    global _history_manager
    if _history_manager is None:
        history_file = Path(__file__).parent.parent / 'artifacts' / 'history.json'
        _history_manager = HistoryManager(history_file)
    return _history_manager






