from flask import Blueprint, jsonify, request
from src.models.trading import db, UserPrediction
from datetime import datetime, date, timedelta
import random

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/predictions', methods=['POST'])
def submit_prediction():
    """예측 제출"""
    try:
        data = request.get_json()
        
        user_name = data.get('user_name')
        symbol = data.get('symbol')
        predicted_direction = data.get('predicted_direction')
        predicted_price = data.get('predicted_price')
        
        if not all([user_name, symbol, predicted_direction]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # 내일 날짜를 타겟으로 설정
        target_date = date.today() + timedelta(days=1)
        
        prediction = UserPrediction(
            user_name=user_name,
            symbol=symbol,
            predicted_direction=predicted_direction,
            predicted_price=predicted_price,
            target_date=target_date
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': prediction.to_dict(),
            'message': 'Prediction submitted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@predictions_bp.route('/predictions/leaderboard', methods=['GET'])
def get_leaderboard():
    """예측 순위표"""
    try:
        # 모의 순위 데이터
        leaderboard = [
            {'rank': 1, 'user_name': '김투자', 'points': 2850, 'accuracy': 78.5, 'predictions': 45},
            {'rank': 2, 'user_name': '박트레이더', 'points': 2720, 'accuracy': 76.2, 'predictions': 42},
            {'rank': 3, 'user_name': '이퀀트', 'points': 2680, 'accuracy': 74.8, 'predictions': 38},
            {'rank': 4, 'user_name': '최애널', 'points': 2590, 'accuracy': 73.1, 'predictions': 41},
            {'rank': 5, 'user_name': '정로봇', 'points': 2510, 'accuracy': 71.9, 'predictions': 39},
            {'rank': 6, 'user_name': '한투자', 'points': 2450, 'accuracy': 70.5, 'predictions': 36},
            {'rank': 7, 'user_name': '윤예측', 'points': 2380, 'accuracy': 69.2, 'predictions': 34},
            {'rank': 8, 'user_name': '장분석', 'points': 2320, 'accuracy': 68.7, 'predictions': 37},
            {'rank': 9, 'user_name': '조주식', 'points': 2280, 'accuracy': 67.9, 'predictions': 33},
            {'rank': 10, 'user_name': '신전략', 'points': 2210, 'accuracy': 66.8, 'predictions': 35}
        ]
        
        return jsonify({
            'success': True,
            'data': leaderboard
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@predictions_bp.route('/predictions/accuracy', methods=['GET'])
def get_prediction_accuracy():
    """예측 정확도 통계"""
    try:
        user_name = request.args.get('user_name')
        
        if user_name:
            # 특정 사용자의 정확도
            predictions = UserPrediction.query.filter_by(user_name=user_name).all()
            
            if not predictions:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            total_predictions = len(predictions)
            correct_predictions = len([p for p in predictions if p.is_correct])
            accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0
            total_points = sum(p.points_earned for p in predictions)
            
            user_stats = {
                'user_name': user_name,
                'total_predictions': total_predictions,
                'correct_predictions': correct_predictions,
                'accuracy': round(accuracy, 2),
                'total_points': total_points,
                'rank': random.randint(1, 50)  # 모의 순위
            }
            
            return jsonify({
                'success': True,
                'data': user_stats
            })
        else:
            # 전체 통계
            overall_stats = {
                'total_users': 150,
                'total_predictions': 2847,
                'average_accuracy': 72.3,
                'top_accuracy': 85.7,
                'active_predictions': 45
            }
            
            return jsonify({
                'success': True,
                'data': overall_stats
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@predictions_bp.route('/predictions/current', methods=['GET'])
def get_current_predictions():
    """현재 진행 중인 예측 게임"""
    try:
        # 현재 예측 가능한 주식들
        current_predictions = [
            {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'current_price': 175.23,
                'deadline': (datetime.now() + timedelta(hours=2, minutes=15)).isoformat(),
                'participants': 127,
                'up_votes': 78,
                'down_votes': 49
            },
            {
                'symbol': 'MSFT',
                'name': 'Microsoft Corp.',
                'current_price': 378.45,
                'deadline': (datetime.now() + timedelta(hours=3, minutes=45)).isoformat(),
                'participants': 95,
                'up_votes': 52,
                'down_votes': 43
            },
            {
                'symbol': 'GOOGL',
                'name': 'Alphabet Inc.',
                'current_price': 142.67,
                'deadline': (datetime.now() + timedelta(hours=1, minutes=30)).isoformat(),
                'participants': 83,
                'up_votes': 45,
                'down_votes': 38
            }
        ]
        
        return jsonify({
            'success': True,
            'data': current_predictions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@predictions_bp.route('/predictions/history/<user_name>', methods=['GET'])
def get_user_prediction_history(user_name):
    """사용자 예측 기록"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        predictions = UserPrediction.query.filter_by(user_name=user_name)\
                                        .order_by(UserPrediction.prediction_date.desc())\
                                        .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'predictions': [prediction.to_dict() for prediction in predictions.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': predictions.total,
                    'pages': predictions.pages
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

