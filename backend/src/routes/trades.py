from flask import Blueprint, jsonify, request
from src.models.trading import db, Trade, Robot, MarketData, StockUniverse, MarketCondition
from src.services.stock_data_service import StockDataService
from datetime import datetime, timedelta, date
import random

trades_bp = Blueprint('trades', __name__)
stock_service = StockDataService()

@trades_bp.route('/trades/recent', methods=['GET'])
def get_recent_trades():
    """최근 거래 내역 조회 (상세 정보 포함)"""
    try:
        limit = request.args.get('limit', 20, type=int)
        include_details = request.args.get('details', 'true').lower() == 'true'
        
        trades = Trade.query.order_by(Trade.trade_date.desc()).limit(limit).all()
        
        if include_details:
            trades_data = [trade.to_dict() for trade in trades]
        else:
            trades_data = []
            for trade in trades:
                trades_data.append({
                    'id': trade.id,
                    'robot_name': trade.robot.name if trade.robot else None,
                    'symbol': trade.symbol,
                    'company_name': trade.company_name,
                    'trade_type': trade.trade_type,
                    'quantity': trade.quantity,
                    'price': trade.price,
                    'total_amount': trade.total_amount,
                    'trade_date': trade.trade_date.isoformat() if trade.trade_date else None,
                    'sector': trade.sector,
                    'confidence_score': trade.confidence_score
                })
        
        return jsonify({
            'success': True,
            'data': trades_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trades_bp.route('/trades/detailed/<int:trade_id>', methods=['GET'])
def get_trade_details(trade_id):
    """특정 거래의 상세 정보 조회"""
    try:
        trade = Trade.query.get_or_404(trade_id)
        return jsonify({
            'success': True,
            'data': trade.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trades_bp.route('/trades/live', methods=['GET'])
def get_live_trades():
    """실시간 거래 현황 (향상된 버전)"""
    try:
        # 실시간 거래 데이터 시뮬레이션 (더 많은 종목 포함)
        robots = Robot.query.filter_by(is_active=True).all()
        
        live_trades = []
        for i in range(15):  # 15개의 최근 거래
            robot = random.choice(robots)
            symbol = stock_service.get_random_stock_for_trading()
            trade_type = random.choice(['BUY', 'SELL'])
            
            # 상세한 거래 데이터 생성
            trade_data = stock_service.generate_detailed_trade_data(symbol, trade_type, robot.name)
            
            # 시간을 몇 분 전으로 설정
            minutes_ago = random.randint(1, 120)
            trade_time = datetime.now() - timedelta(minutes=minutes_ago)
            
            quantity = random.randint(10, 500)
            
            live_trades.append({
                'symbol': symbol,
                'company_name': trade_data['company_name'],
                'trade_type': trade_type,
                'price': trade_data['price'],
                'quantity': quantity,
                'total_amount': round(trade_data['price'] * quantity, 2),
                'robot_name': robot.name,
                'robot_id': robot.id,
                'time_ago': f"{minutes_ago}분 전" if minutes_ago < 60 else f"{minutes_ago//60}시간 전",
                'trade_time': trade_time.isoformat(),
                'sector': trade_data['sector'],
                'confidence_score': trade_data['confidence_score'],
                'market_condition': trade_data['market_condition'],
                'reason': trade_data['reason'][:50] + "..." if len(trade_data['reason']) > 50 else trade_data['reason']
            })
        
        # 시간순으로 정렬
        live_trades.sort(key=lambda x: x['trade_time'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': live_trades
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trades_bp.route('/trades/by-sector', methods=['GET'])
def get_trades_by_sector():
    """섹터별 거래 현황"""
    try:
        # 최근 24시간 거래 데이터
        yesterday = datetime.now() - timedelta(days=1)
        trades = Trade.query.filter(Trade.trade_date >= yesterday).all()
        
        sector_stats = {}
        for trade in trades:
            sector = trade.sector or 'Unknown'
            if sector not in sector_stats:
                sector_stats[sector] = {
                    'sector': sector,
                    'total_trades': 0,
                    'buy_trades': 0,
                    'sell_trades': 0,
                    'total_volume': 0,
                    'avg_confidence': 0,
                    'top_stocks': {}
                }
            
            sector_stats[sector]['total_trades'] += 1
            if trade.trade_type == 'BUY':
                sector_stats[sector]['buy_trades'] += 1
            else:
                sector_stats[sector]['sell_trades'] += 1
            
            sector_stats[sector]['total_volume'] += trade.total_amount
            
            if trade.confidence_score:
                sector_stats[sector]['avg_confidence'] += trade.confidence_score
            
            # 인기 종목 추적
            symbol = trade.symbol
            if symbol not in sector_stats[sector]['top_stocks']:
                sector_stats[sector]['top_stocks'][symbol] = 0
            sector_stats[sector]['top_stocks'][symbol] += 1
        
        # 평균 신뢰도 계산 및 상위 종목 정리
        for sector in sector_stats:
            if sector_stats[sector]['total_trades'] > 0:
                sector_stats[sector]['avg_confidence'] /= sector_stats[sector]['total_trades']
                sector_stats[sector]['avg_confidence'] = round(sector_stats[sector]['avg_confidence'], 1)
            
            # 상위 3개 종목만 유지
            top_stocks = sorted(
                sector_stats[sector]['top_stocks'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            sector_stats[sector]['top_stocks'] = [{'symbol': k, 'trades': v} for k, v in top_stocks]
        
        return jsonify({
            'success': True,
            'data': list(sector_stats.values())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trades_bp.route('/trades/simulate', methods=['POST'])
def simulate_trade():
    """거래 시뮬레이션 (향상된 버전)"""
    try:
        data = request.get_json()
        
        robot_id = data.get('robot_id')
        symbol = data.get('symbol')
        trade_type = data.get('trade_type')
        quantity = data.get('quantity')
        
        if not all([robot_id, symbol, trade_type, quantity]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        robot = Robot.query.get(robot_id)
        if not robot:
            return jsonify({
                'success': False,
                'error': 'Robot not found'
            }), 404
        
        # 상세한 거래 데이터 생성
        trade_data = stock_service.generate_detailed_trade_data(symbol, trade_type, robot.name)
        price = trade_data['price']
        total_amount = price * quantity
        
        # 거래 기록 생성
        trade = Trade(
            robot_id=robot_id,
            symbol=symbol,
            company_name=trade_data['company_name'],
            trade_type=trade_type,
            quantity=quantity,
            price=price,
            total_amount=total_amount,
            reason=trade_data['reason'],
            confidence_score=trade_data['confidence_score'],
            market_condition=trade_data['market_condition'],
            sector=trade_data['sector'],
            market_cap=trade_data['market_cap'],
            rsi=trade_data['technical_indicators']['rsi'],
            macd=trade_data['technical_indicators']['macd'],
            moving_avg_20=trade_data['technical_indicators']['moving_avg_20'],
            moving_avg_50=trade_data['technical_indicators']['moving_avg_50'],
            volume_ratio=trade_data['technical_indicators']['volume_ratio'],
            market_price_at_trade=trade_data['market_data']['market_price_at_trade'],
            day_high=trade_data['market_data']['day_high'],
            day_low=trade_data['market_data']['day_low'],
            day_open=trade_data['market_data']['day_open'],
            prev_close=trade_data['market_data']['prev_close'],
            expected_return=trade_data['trade_strategy']['expected_return'],
            stop_loss=trade_data['trade_strategy']['stop_loss'],
            take_profit=trade_data['trade_strategy']['take_profit'],
            holding_period=trade_data['trade_strategy']['holding_period'],
            position_size_pct=trade_data['trade_strategy']['position_size_pct'],
            risk_score=trade_data['trade_strategy']['risk_score']
        )
        
        db.session.add(trade)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': trade.to_dict(),
            'message': f'Successfully simulated {trade_type} order for {quantity} shares of {symbol}'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trades_bp.route('/market/quote/<symbol>', methods=['GET'])
def get_market_quote(symbol):
    """실시간 주식 시세 (실제 API 연동)"""
    try:
        quote_data = stock_service.get_stock_quote(symbol)
        
        # 추가 정보 포함
        stock_info = StockUniverse.query.filter_by(symbol=symbol).first()
        if stock_info:
            quote_data.update({
                'company_name': stock_info.name,
                'sector': stock_info.sector,
                'exchange': stock_info.exchange,
                'market_cap_category': stock_info.market_cap
            })
        
        return jsonify({
            'success': True,
            'data': quote_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trades_bp.route('/market/trending', methods=['GET'])
def get_trending_stocks():
    """인기 종목 조회 (실제 거래 데이터 기반)"""
    try:
        # 최근 24시간 거래량 기준 인기 종목
        yesterday = datetime.now() - timedelta(days=1)
        
        # 거래량이 많은 종목들 조회
        popular_stocks = db.session.query(
            Trade.symbol,
            Trade.company_name,
            Trade.sector,
            db.func.count(Trade.id).label('trade_count'),
            db.func.sum(Trade.total_amount).label('total_volume'),
            db.func.avg(Trade.confidence_score).label('avg_confidence')
        ).filter(
            Trade.trade_date >= yesterday
        ).group_by(
            Trade.symbol
        ).order_by(
            db.func.count(Trade.id).desc()
        ).limit(10).all()
        
        trending_data = []
        for stock in popular_stocks:
            # 현재 시세 가져오기
            quote = stock_service.get_stock_quote(stock.symbol)
            
            trending_data.append({
                'symbol': stock.symbol,
                'company_name': stock.company_name or f"{stock.symbol} Inc.",
                'sector': stock.sector,
                'current_price': quote['close'],
                'change_percent': round(random.uniform(-5, 5), 2),  # 실제로는 전일 대비 계산
                'trade_count': stock.trade_count,
                'total_volume': round(stock.total_volume, 2),
                'avg_confidence': round(stock.avg_confidence or 0, 1),
                'volume': quote['volume']
            })
        
        return jsonify({
            'success': True,
            'data': trending_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trades_bp.route('/market/sectors', methods=['GET'])
def get_sector_performance():
    """섹터별 성과 분석"""
    try:
        # 현재 시장 상황 가져오기
        today = date.today()
        market_condition = MarketCondition.query.filter_by(date=today).first()
        
        if market_condition and market_condition.sector_rotation:
            sector_data = market_condition.to_dict()['sector_rotation']
        else:
            # 기본 섹터 성과 데이터
            sector_data = stock_service._generate_sector_performance()
        
        # 섹터별 거래 활동 추가
        yesterday = datetime.now() - timedelta(days=1)
        sector_trades = db.session.query(
            Trade.sector,
            db.func.count(Trade.id).label('trade_count'),
            db.func.avg(Trade.confidence_score).label('avg_confidence')
        ).filter(
            Trade.trade_date >= yesterday,
            Trade.sector.isnot(None)
        ).group_by(Trade.sector).all()
        
        sector_activity = {trade.sector: {
            'trade_count': trade.trade_count,
            'avg_confidence': round(trade.avg_confidence or 0, 1)
        } for trade in sector_trades}
        
        # 결합된 섹터 데이터
        combined_data = []
        for sector, performance in sector_data.items():
            activity = sector_activity.get(sector, {'trade_count': 0, 'avg_confidence': 0})
            combined_data.append({
                'sector': sector,
                'performance': performance,
                'trade_count': activity['trade_count'],
                'avg_confidence': activity['avg_confidence'],
                'trend': 'up' if performance > 0 else 'down' if performance < 0 else 'neutral'
            })
        
        # 성과순으로 정렬
        combined_data.sort(key=lambda x: x['performance'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': combined_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

