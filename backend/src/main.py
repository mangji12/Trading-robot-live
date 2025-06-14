import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.trading import db, Robot, Trade, Portfolio, StockUniverse, MarketCondition
from src.services.stock_data_service import StockDataService
from src.routes.robots import robots_bp
from src.routes.trades import trades_bp
from src.routes.predictions import predictions_bp
from datetime import datetime, date
import random
import json

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# CORS 설정 - 모든 도메인에서 접근 허용
CORS(app)

# 블루프린트 등록
app.register_blueprint(robots_bp, url_prefix='/api')
app.register_blueprint(trades_bp, url_prefix='/api')
app.register_blueprint(predictions_bp, url_prefix='/api')

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 주식 데이터 서비스 초기화
stock_service = StockDataService()

def init_stock_universe():
    """미국 상장기업 전체 목록 초기화"""
    if StockUniverse.query.count() > 0:
        return
    
    print("Initializing stock universe...")
    tickers = stock_service.get_all_tickers(limit=500)  # 500개 종목으로 제한
    
    for ticker_data in tickers:
        try:
            # 섹터 결정
            symbol = ticker_data.get("ticker", "")
            sector = "Technology"  # 기본값
            for sec, stocks in stock_service.sector_stocks.items():
                if symbol in stocks:
                    sector = sec
                    break
            
            # 시가총액 결정 (랜덤)
            market_cap = random.choice(["large", "mid", "small", "micro"])
            
            stock = StockUniverse(
                symbol=symbol,
                name=ticker_data.get("name", f"{symbol} Inc."),
                exchange=ticker_data.get("primary_exchange", "NASDAQ"),
                sector=sector,
                industry=f"{sector} Industry",
                market_cap=market_cap,
                is_active=ticker_data.get("active", True)
            )
            db.session.add(stock)
        except Exception as e:
            print(f"Error adding stock {ticker_data.get('ticker', 'Unknown')}: {e}")
            continue
    
    try:
        db.session.commit()
        print(f"Added {StockUniverse.query.count()} stocks to universe")
    except Exception as e:
        print(f"Error committing stock universe: {e}")
        db.session.rollback()

def init_market_conditions():
    """시장 상황 데이터 초기화"""
    today = date.today()
    if MarketCondition.query.filter_by(date=today).first():
        return
    
    market_data = stock_service.get_market_condition()
    
    market_condition = MarketCondition(
        date=today,
        overall_sentiment=market_data["overall_sentiment"],
        vix_level=market_data["vix_level"],
        sp500_change=market_data["market_changes"]["sp500"],
        nasdaq_change=market_data["market_changes"]["nasdaq"],
        dow_change=market_data["market_changes"]["dow"],
        volume_trend=market_data["volume_trend"],
        sector_rotation=json.dumps(market_data["sector_rotation"]),
        news_sentiment=market_data["news_sentiment"]
    )
    
    db.session.add(market_condition)
    db.session.commit()

def init_enhanced_sample_data():
    """향상된 샘플 데이터 초기화"""
    # 기존 데이터 확인
    if Robot.query.count() > 0:
        return
    
    # 투자 로봇 샘플 데이터
    robots_data = [
        {
            'name': 'Momentum Master',
            'strategy_type': '모멘텀 투자',
            'description': '기술적 분석과 모멘텀 지표를 활용한 단기 투자 전략. RSI, MACD 등을 종합 분석하여 상승 모멘텀이 강한 종목을 선별합니다.',
            'risk_level': '중간',
            'initial_capital': 100000,
            'current_capital': 125800,
            'total_return': 15.8,
            'win_rate': 68.5,
            'max_drawdown': 12.3,
            'sharpe_ratio': 1.45
        },
        {
            'name': 'Value Hunter',
            'strategy_type': '가치 투자',
            'description': '기본적 분석을 통해 내재가치 대비 저평가된 우량주를 발굴하는 장기 투자 전략. PER, PBR, ROE 등을 종합 평가합니다.',
            'risk_level': '낮음',
            'initial_capital': 100000,
            'current_capital': 112300,
            'total_return': 12.3,
            'win_rate': 72.1,
            'max_drawdown': 8.7,
            'sharpe_ratio': 1.62
        },
        {
            'name': 'Growth Seeker',
            'strategy_type': '성장주 투자',
            'description': '높은 성장 잠재력을 가진 기업에 투자하는 전략. 매출 성장률, 시장 점유율 확대 등을 중점 분석합니다.',
            'risk_level': '높음',
            'initial_capital': 100000,
            'current_capital': 122700,
            'total_return': 22.7,
            'win_rate': 61.3,
            'max_drawdown': 18.5,
            'sharpe_ratio': 1.28
        },
        {
            'name': 'Dividend Collector',
            'strategy_type': '배당 투자',
            'description': '안정적인 배당 수익을 추구하는 보수적 투자 전략. 배당 수익률과 배당 성장률을 중시합니다.',
            'risk_level': '낮음',
            'initial_capital': 100000,
            'current_capital': 108900,
            'total_return': 8.9,
            'win_rate': 78.4,
            'max_drawdown': 5.2,
            'sharpe_ratio': 1.78
        },
        {
            'name': 'AI Quant',
            'strategy_type': 'AI 퀀트',
            'description': '머신러닝과 빅데이터 분석을 활용한 알고리즘 투자 전략. 시장 패턴과 이상 징후를 실시간 감지합니다.',
            'risk_level': '중간',
            'initial_capital': 100000,
            'current_capital': 118500,
            'total_return': 18.5,
            'win_rate': 65.7,
            'max_drawdown': 14.8,
            'sharpe_ratio': 1.52
        }
    ]
    
    # 로봇 데이터 삽입
    for robot_data in robots_data:
        robot = Robot(**robot_data)
        db.session.add(robot)
    
    db.session.commit()
    
    # 향상된 거래 데이터 생성
    robots = Robot.query.all()
    
    for _ in range(100):  # 100개의 상세한 거래 데이터
        robot = random.choice(robots)
        symbol = stock_service.get_random_stock_for_trading()
        trade_type = random.choice(['BUY', 'SELL'])
        
        # 상세한 거래 데이터 생성
        trade_data = stock_service.generate_detailed_trade_data(symbol, trade_type, robot.name)
        
        # 거래량과 가격 계산
        quantity = random.randint(10, 500)
        price = trade_data["price"]
        total_amount = quantity * price
        
        trade = Trade(
            robot_id=robot.id,
            symbol=symbol,
            company_name=trade_data["company_name"],
            trade_type=trade_type,
            quantity=quantity,
            price=price,
            total_amount=total_amount,
            trade_date=datetime.now(),
            reason=trade_data["reason"],
            confidence_score=trade_data["confidence_score"],
            market_condition=trade_data["market_condition"],
            sector=trade_data["sector"],
            market_cap=trade_data["market_cap"],
            rsi=trade_data["technical_indicators"]["rsi"],
            macd=trade_data["technical_indicators"]["macd"],
            moving_avg_20=trade_data["technical_indicators"]["moving_avg_20"],
            moving_avg_50=trade_data["technical_indicators"]["moving_avg_50"],
            volume_ratio=trade_data["technical_indicators"]["volume_ratio"],
            market_price_at_trade=trade_data["market_data"]["market_price_at_trade"],
            day_high=trade_data["market_data"]["day_high"],
            day_low=trade_data["market_data"]["day_low"],
            day_open=trade_data["market_data"]["day_open"],
            prev_close=trade_data["market_data"]["prev_close"],
            expected_return=trade_data["trade_strategy"]["expected_return"],
            stop_loss=trade_data["trade_strategy"]["stop_loss"],
            take_profit=trade_data["trade_strategy"]["take_profit"],
            holding_period=trade_data["trade_strategy"]["holding_period"],
            position_size_pct=trade_data["trade_strategy"]["position_size_pct"],
            risk_score=trade_data["trade_strategy"]["risk_score"]
        )
        db.session.add(trade)
    
    db.session.commit()
    print(f"Added {Trade.query.count()} enhanced trades")

with app.app_context():
    db.create_all()
    init_stock_universe()
    init_market_conditions()
    init_enhanced_sample_data()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """API 상태 확인"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'features': {
            'enhanced_trading_logs': True,
            'real_market_data': True,
            'comprehensive_stock_universe': True,
            'market_condition_analysis': True
        }
    }

@app.route('/api/market/condition', methods=['GET'])
def get_current_market_condition():
    """현재 시장 상황 조회"""
    today = date.today()
    condition = MarketCondition.query.filter_by(date=today).first()
    
    if not condition:
        # 새로운 시장 상황 데이터 생성
        init_market_conditions()
        condition = MarketCondition.query.filter_by(date=today).first()
    
    return {
        'success': True,
        'data': condition.to_dict() if condition else {}
    }

@app.route('/api/stocks/universe', methods=['GET'])
def get_stock_universe():
    """전체 주식 목록 조회"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    sector = request.args.get('sector')
    market_cap = request.args.get('market_cap')
    search = request.args.get('search')
    
    query = StockUniverse.query.filter_by(is_active=True)
    
    if sector:
        query = query.filter(StockUniverse.sector == sector)
    if market_cap:
        query = query.filter(StockUniverse.market_cap == market_cap)
    if search:
        query = query.filter(
            db.or_(
                StockUniverse.symbol.contains(search.upper()),
                StockUniverse.name.contains(search)
            )
        )
    
    stocks = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'success': True,
        'data': {
            'stocks': [stock.to_dict() for stock in stocks.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': stocks.total,
                'pages': stocks.pages
            }
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

