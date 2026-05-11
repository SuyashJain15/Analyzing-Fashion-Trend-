import os
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify, session
from flask_cors import CORS

from src.bootstrap import ensure_artifacts
from src.image_analyzer import analyze_image
from src.models import load_models, predict_text
from src.chatbot import get_chatbot
from src.history import get_history_manager
from src.recommendations import get_recommender
from src.trend_explainer import get_explainer
from src.occasion_detector import get_detector
from src.shopping_links import get_shopping


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

UPLOAD_DIR.mkdir(exist_ok=True)
ARTIFACTS_DIR.mkdir(exist_ok=True)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    
    # Enable CORS for API endpoints
    CORS(app)
    
    # Initialize managers
    chatbot = get_chatbot()
    history_manager = get_history_manager()
    recommender = get_recommender()
    explainer = get_explainer()
    detector = get_detector()
    shopping = get_shopping()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze():
        if 'image' not in request.files:
            flash('Please upload an image file.')
            return redirect(url_for('index'))

        file = request.files['image']
        if file.filename == '':
            flash('No selected file.')
            return redirect(url_for('index'))

        save_path = UPLOAD_DIR / file.filename
        file.save(str(save_path))

        # Ensure artifacts exist (download+train on first run)
        ensure_artifacts()

        # Analyze image to produce a lightweight textual description
        img_report = analyze_image(str(save_path))

        # Load models and predict trendiness using synthesized text
        models = load_models()
        synthesized_text = img_report['synthesized_text']
        lr_pred, lr_prob, rf_pred, rf_prob, ensemble_pred = predict_text(models, synthesized_text)

        def reason_line(pred: int, prob: float) -> str:
            if pred == 1:
                return "Trending: High confidence in current fashion trends"
            return "Outdated: Pattern analysis suggests outdated style elements"

        lr_reason = reason_line(lr_pred, lr_prob)
        rf_reason = reason_line(rf_pred, rf_prob)
        ensemble_reason = (
            "Final Verdict: TRENDING – Your outfit follows current fashion trends"
            if ensemble_pred == 1
            else "Final Verdict: OUTDATED – Consider updating one or two key pieces"
        )

        # Load trends for suggestions
        trends_path = ARTIFACTS_DIR / 'top_trends.json'
        if trends_path.exists():
            top_trends = json.loads(trends_path.read_text(encoding='utf-8'))
        else:
            top_trends = {"colors": [], "items": []}

        # Build personalized suggestions based on detection + trend status
        suggestions: List[str] = []

        detected_items = set(img_report.get('items', []))
        detected_colors = set(img_report.get('colors', []))
        trending_item = (top_trends.get('items') or ['jacket'])[0]
        trending_color = (top_trends.get('colors') or ['black'])[0]

        if ensemble_pred == 1:
            suggestions.append("Your outfit shows good taste – try experimenting with different silhouettes")
            # Color nudge if not in trending palette
            if trending_color not in detected_colors:
                suggestions.append(f"Try popular color this season: {trending_color}")
        else:
            # If outdated, be more prescriptive
            if 'top' in detected_items:
                suggestions.append(f"Update your top – consider a modern {trending_item}")
            if 'bottom' in detected_items:
                suggestions.append("Switch to tapered or relaxed-fit trending jeans")
            if trending_color not in detected_colors:
                suggestions.append(f"Introduce trending color: {trending_color}")
            suggestions.append("Consider layering for added depth")

        trend_status = 'Trending' if ensemble_pred == 1 else 'Outdated'
        
        # Get outfit recommendations
        outfit_recommendations = recommender.generate_outfit_recommendations(img_report, trend_status)
        
        # Get trend explanation
        trend_explanation = explainer.generate_explanation(img_report, trend_status)
        
        # Detect occasion
        occasion_data = detector.detect_occasion(img_report)
        occasion_suggestions = detector.get_occasion_suggestions(occasion_data['occasion'])
        
        # Generate shopping links
        shopping_links = shopping.generate_links(img_report, occasion_data['occasion'])
        shopping_suggestions = shopping.get_shopping_suggestions(img_report, occasion_data['occasion'])

        context: Dict[str, Any] = {
            'filename': file.filename,
            'img_report': img_report,
            'lr_pred': int(lr_pred),
            'lr_prob': float(lr_prob),
            'lr_reason': lr_reason,
            'rf_pred': int(rf_pred),
            'rf_prob': float(rf_prob),
            'rf_reason': rf_reason,
            'ensemble_pred': int(ensemble_pred),
            'ensemble_reason': ensemble_reason,
            'trend_status': trend_status,
            'suggestions': suggestions,
            'recommendations': outfit_recommendations,
            'trend_explanation': trend_explanation,
            'occasion': occasion_data['occasion'],
            'occasion_confidence': occasion_data['confidence'],
            'occasion_suggestions': occasion_suggestions,
            'shopping_links': shopping_links,
            'shopping_suggestions': shopping_suggestions,
        }
        
        # Save to history
        history_data = {
            'filename': file.filename,
            'trend_status': trend_status,
            'ensemble_pred': int(ensemble_pred),
            'ensemble_prob': float((lr_prob + rf_prob) / 2),
            'colors': img_report.get('colors', []),
            'items': img_report.get('items', []),
        }
        analysis_id = history_manager.save_analysis(history_data)
        context['analysis_id'] = analysis_id

        return render_template('results.html', **context)

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename: str):
        return send_from_directory(str(UPLOAD_DIR), filename)
    
    @app.route('/chat', methods=['POST'])
    def chat():
        """Chatbot endpoint"""
        try:
            data = request.get_json()
            user_message = data.get('message', '')
            outfit_context = data.get('outfit_context', None)
            
            if not user_message:
                return jsonify({
                    'response': 'Please ask me a question about fashion! 💬',
                    'timestamp': __import__('datetime').datetime.now().isoformat()
                })
            
            response = chatbot.get_response(user_message, outfit_context)
            
            return jsonify({
                'response': response,
                'timestamp': __import__('datetime').datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({
                'response': f'I encountered an error: {str(e)}. Please try again!',
                'timestamp': __import__('datetime').datetime.now().isoformat()
            }), 500
    
    @app.route('/compare', methods=['POST'])
    def compare():
        """Compare two outfits"""
        if 'image1' not in request.files or 'image2' not in request.files:
            flash('Please upload both images.')
            return redirect(url_for('index'))
        
        file1 = request.files['image1']
        file2 = request.files['image2']
        
        if file1.filename == '' or file2.filename == '':
            flash('Please select both files.')
            return redirect(url_for('index'))
        
        # Save files
        save_path1 = UPLOAD_DIR / file1.filename
        save_path2 = UPLOAD_DIR / file2.filename
        file1.save(str(save_path1))
        file2.save(str(save_path2))
        
        # Ensure artifacts exist
        ensure_artifacts()
        
        # Analyze both images
        img_report1 = analyze_image(str(save_path1))
        img_report2 = analyze_image(str(save_path2))
        
        # Load models and predict
        models = load_models()
        synthesized_text1 = img_report1['synthesized_text']
        synthesized_text2 = img_report2['synthesized_text']
        
        lr_pred1, lr_prob1, rf_pred1, rf_prob1, ensemble_pred1 = predict_text(models, synthesized_text1)
        lr_pred2, lr_prob2, rf_pred2, rf_prob2, ensemble_pred2 = predict_text(models, synthesized_text2)
        
        # Determine winner
        ensemble_prob1 = float((lr_prob1 + rf_prob1) / 2)
        ensemble_prob2 = float((lr_prob2 + rf_prob2) / 2)
        
        if ensemble_prob1 > ensemble_prob2:
            winner = 1
            winner_filename = file1.filename
        elif ensemble_prob2 > ensemble_prob1:
            winner = 2
            winner_filename = file2.filename
        else:
            winner = 0  # Tie
            winner_filename = "Both"
        
        # Get trend explanations
        trend_explanation1 = explainer.generate_explanation(img_report1, 'Trending' if ensemble_pred1 == 1 else 'Outdated')
        trend_explanation2 = explainer.generate_explanation(img_report2, 'Trending' if ensemble_pred2 == 1 else 'Outdated')
        
        # Detect occasions
        occasion1 = detector.detect_occasion(img_report1)
        occasion2 = detector.detect_occasion(img_report2)
        
        context = {
            'filename1': file1.filename,
            'filename2': file2.filename,
            'img_report1': img_report1,
            'img_report2': img_report2,
            'ensemble_pred1': int(ensemble_pred1),
            'ensemble_prob1': ensemble_prob1,
            'ensemble_pred2': int(ensemble_pred2),
            'ensemble_prob2': ensemble_prob2,
            'trend_explanation1': trend_explanation1,
            'trend_explanation2': trend_explanation2,
            'occasion1': occasion1['occasion'],
            'occasion2': occasion2['occasion'],
            'winner': winner,
            'winner_filename': winner_filename,
        }
        
        return render_template('compare_results.html', **context)
    
    @app.route('/history')
    def history():
        """View analysis history"""
        recent = history_manager.get_recent(limit=20)
        return render_template('history.html', analyses=recent)
    
    @app.route('/analysis/<analysis_id>')
    def view_analysis(analysis_id: str):
        """View specific analysis"""
        analysis = history_manager.get_analysis(analysis_id)
        if not analysis:
            flash('Analysis not found')
            return redirect(url_for('history'))
        return render_template('analysis_detail.html', analysis=analysis)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)


