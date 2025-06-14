from flask import Blueprint, jsonify, request
from src.models.trading import db, Robot, Trade, Portfolio
from datetime import datetime
import random

robots_bp = Blueprint('robots', __name__)

@robots_bp.route('/robots', methods=['GET'])
def get_robots():
    """모든 투자 로봇 목록 조회"""
    try:
        robots = Robot.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'data': [robot.to_dict() for robot in robots]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@robots_bp.route('/robots/<int:robot_id>', methods=['GET'])
def get_robot(robot_id):
    """특정 로봇 상세 정보 조회"""
    try:
        robot = Robot.query.get_or_404(robot_id)
        return jsonify({
            'success': True,
            'data': robot.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@robots_bp.route('/robots/<int:robot_id>/performance', methods=['GET'])
def get_robot_performance(robot_id):
    """로봇 성과 데이터 조회"""
    try:
        robot = Robot.query.get_or_404(robot_id)
        
        # 최근 30일 성과 데이터 (모의 데이터)
        performance_data = []
        for i in range(30):
            date = datetime.now().date()
            date = date.replace(day=date.day - i)
            
            # 기본 수익률에 랜덤 변동 추가
            base_return = robot.total_return or 0
            daily_return = base_return + random.uniform(-2, 2)
            
            performance_data.append({
                'date': date.isoformat(),
                'return': round(daily_return, 2),
                'capital': round(robot.current_capital * (1 + daily_return/100), 2)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'robot': robot.to_dict(),
                'performance': performance_data
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@robots_bp.route('/robots/<int:robot_id>/trades', methods=['GET'])
def get_robot_trades(robot_id):
    """로봇 거래 기록 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        trades = Trade.query.filter_by(robot_id=robot_id)\
                          .order_by(Trade.trade_date.desc())\
                          .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'trades': [trade.to_dict() for trade in trades.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': trades.total,
                    'pages': trades.pages
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@robots_bp.route('/robots/<int:robot_id>/portfolio', methods=['GET'])
def get_robot_portfolio(robot_id):
    """로봇 포트폴리오 조회"""
    try:
        portfolios = Portfolio.query.filter_by(robot_id=robot_id).all()
        
        return jsonify({
            'success': True,
            'data': [portfolio.to_dict() for portfolio in portfolios]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@robots_bp.route('/meta-model/performance', methods=['GET'])
def get_meta_model_performance():
    """메타 모델 성과 조회"""
    try:
        # 모든 활성 로봇의 평균 성과 계산
        robots = Robot.query.filter_by(is_active=True).all()
        
        if not robots:
            return jsonify({
                'success': False,
                'error': 'No active robots found'
            }), 404
        
        # 메타 모델 성과 계산
        total_return = sum(robot.total_return or 0 for robot in robots) / len(robots)
        win_rate = sum(robot.win_rate or 0 for robot in robots) / len(robots)
        current_capital = sum(robot.current_capital or 0 for robot in robots) / len(robots)
        sharpe_ratio = sum(robot.sharpe_ratio or 0 for robot in robots) / len(robots)
        max_drawdown = max(robot.max_drawdown or 0 for robot in robots)
        
        meta_performance = {
            'name': 'Meta Model',
            'total_return': round(total_return, 2),
            'win_rate': round(win_rate, 2),
            'current_capital': round(current_capital, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_drawdown': round(max_drawdown, 2),
            'robot_count': len(robots)
        }
        
        return jsonify({
            'success': True,
            'data': meta_performance
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@robots_bp.route('/meta-model/allocation', methods=['GET'])
def get_meta_model_allocation():
    """메타 모델 자산 배분 현황"""
    try:
        robots = Robot.query.filter_by(is_active=True).all()
        
        allocations = []
        total_capital = sum(robot.current_capital or 0 for robot in robots)
        
        for robot in robots:
            weight = (robot.current_capital or 0) / total_capital * 100 if total_capital > 0 else 0
            allocations.append({
                'robot_id': robot.id,
                'robot_name': robot.name,
                'strategy_type': robot.strategy_type,
                'weight': round(weight, 2),
                'capital': robot.current_capital or 0,
                'return': robot.total_return or 0
            })
        
        return jsonify({
            'success': True,
            'data': {
                'allocations': allocations,
                'total_capital': total_capital,
                'last_updated': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

