from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Robot(db.Model):
    __tablename__ = 'robots'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    strategy_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    risk_level = db.Column(db.String(20))
    initial_capital = db.Column(db.Float, default=100000)
    current_capital = db.Column(db.Float)
    total_return = db.Column(db.Float)
    win_rate = db.Column(db.Float)
    max_drawdown = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    trades = db.relationship('Trade', backref='robot', lazy=True)
    portfolios = db.relationship('Portfolio', backref='robot', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'strategy_type': self.strategy_type,
            'description': self.description,
            'risk_level': self.risk_level,
            'initial_capital': self.initial_capital,
            'current_capital': self.current_capital,
            'total_return': self.total_return,
            'win_rate': self.win_rate,
            'max_drawdown': self.max_drawdown,
            'sharpe_ratio': self.sharpe_ratio,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Trade(db.Model):
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(200))
    trade_type = db.Column(db.String(10), nullable=False)  # 'BUY' or 'SELL'
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    trade_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 상세 거래 정보
    reason = db.Column(db.Text)  # 거래 이유
    confidence_score = db.Column(db.Float)  # 신뢰도 점수 (0-100)
    market_condition = db.Column(db.String(50))  # 시장 상황 (bullish, bearish, neutral)
    sector = db.Column(db.String(100))  # 섹터
    market_cap = db.Column(db.String(50))  # 시가총액 구분 (large, mid, small)
    
    # 기술적 지표
    rsi = db.Column(db.Float)  # RSI 지표
    macd = db.Column(db.Float)  # MACD 지표
    moving_avg_20 = db.Column(db.Float)  # 20일 이동평균
    moving_avg_50 = db.Column(db.Float)  # 50일 이동평균
    volume_ratio = db.Column(db.Float)  # 거래량 비율
    
    # 시장 데이터
    market_price_at_trade = db.Column(db.Float)  # 거래 시점 시장가
    day_high = db.Column(db.Float)  # 당일 최고가
    day_low = db.Column(db.Float)  # 당일 최저가
    day_open = db.Column(db.Float)  # 당일 시가
    prev_close = db.Column(db.Float)  # 전일 종가
    
    # 거래 성과
    expected_return = db.Column(db.Float)  # 예상 수익률
    stop_loss = db.Column(db.Float)  # 손절가
    take_profit = db.Column(db.Float)  # 익절가
    holding_period = db.Column(db.Integer)  # 예상 보유 기간 (일)
    
    # 리스크 관리
    position_size_pct = db.Column(db.Float)  # 포지션 크기 (포트폴리오 대비 %)
    risk_score = db.Column(db.Float)  # 리스크 점수 (1-10)
    
    def to_dict(self):
        return {
            'id': self.id,
            'robot_id': self.robot_id,
            'robot_name': self.robot.name if self.robot else None,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'trade_type': self.trade_type,
            'quantity': self.quantity,
            'price': self.price,
            'total_amount': self.total_amount,
            'trade_date': self.trade_date.isoformat() if self.trade_date else None,
            'reason': self.reason,
            'confidence_score': self.confidence_score,
            'market_condition': self.market_condition,
            'sector': self.sector,
            'market_cap': self.market_cap,
            'technical_indicators': {
                'rsi': self.rsi,
                'macd': self.macd,
                'moving_avg_20': self.moving_avg_20,
                'moving_avg_50': self.moving_avg_50,
                'volume_ratio': self.volume_ratio
            },
            'market_data': {
                'market_price_at_trade': self.market_price_at_trade,
                'day_high': self.day_high,
                'day_low': self.day_low,
                'day_open': self.day_open,
                'prev_close': self.prev_close
            },
            'trade_strategy': {
                'expected_return': self.expected_return,
                'stop_loss': self.stop_loss,
                'take_profit': self.take_profit,
                'holding_period': self.holding_period,
                'position_size_pct': self.position_size_pct,
                'risk_score': self.risk_score
            }
        }

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False)
    avg_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float)
    market_value = db.Column(db.Float)
    unrealized_pnl = db.Column(db.Float)
    unrealized_pnl_pct = db.Column(db.Float)
    weight = db.Column(db.Float)
    sector = db.Column(db.String(100))
    market_cap = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'robot_id': self.robot_id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'quantity': self.quantity,
            'avg_price': self.avg_price,
            'current_price': self.current_price,
            'market_value': self.market_value,
            'unrealized_pnl': self.unrealized_pnl,
            'unrealized_pnl_pct': self.unrealized_pnl_pct,
            'weight': self.weight,
            'sector': self.sector,
            'market_cap': self.market_cap,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MarketData(db.Model):
    __tablename__ = 'market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    volume = db.Column(db.BigInteger)
    market_cap = db.Column(db.BigInteger)
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    exchange = db.Column(db.String(20))
    data_source = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('symbol', 'date', name='_symbol_date_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'date': self.date.isoformat() if self.date else None,
            'open_price': self.open_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'close_price': self.close_price,
            'volume': self.volume,
            'market_cap': self.market_cap,
            'sector': self.sector,
            'industry': self.industry,
            'exchange': self.exchange,
            'data_source': self.data_source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StockUniverse(db.Model):
    """미국 상장기업 전체 목록"""
    __tablename__ = 'stock_universe'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    exchange = db.Column(db.String(20))  # NYSE, NASDAQ, etc.
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    market_cap = db.Column(db.String(50))  # large, mid, small, micro
    is_active = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'exchange': self.exchange,
            'sector': self.sector,
            'industry': self.industry,
            'market_cap': self.market_cap,
            'is_active': self.is_active,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class MarketCondition(db.Model):
    """시장 상황 분석"""
    __tablename__ = 'market_conditions'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    overall_sentiment = db.Column(db.String(20))  # bullish, bearish, neutral
    vix_level = db.Column(db.Float)  # 변동성 지수
    sp500_change = db.Column(db.Float)  # S&P 500 변화율
    nasdaq_change = db.Column(db.Float)  # NASDAQ 변화율
    dow_change = db.Column(db.Float)  # DOW 변화율
    volume_trend = db.Column(db.String(20))  # high, normal, low
    sector_rotation = db.Column(db.Text)  # JSON 형태의 섹터별 성과
    economic_indicators = db.Column(db.Text)  # JSON 형태의 경제 지표
    news_sentiment = db.Column(db.Float)  # 뉴스 감정 점수 (-1 to 1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'overall_sentiment': self.overall_sentiment,
            'vix_level': self.vix_level,
            'market_changes': {
                'sp500': self.sp500_change,
                'nasdaq': self.nasdaq_change,
                'dow': self.dow_change
            },
            'volume_trend': self.volume_trend,
            'sector_rotation': json.loads(self.sector_rotation) if self.sector_rotation else {},
            'economic_indicators': json.loads(self.economic_indicators) if self.economic_indicators else {},
            'news_sentiment': self.news_sentiment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserPrediction(db.Model):
    __tablename__ = 'user_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    symbol = db.Column(db.String(20), nullable=False)
    predicted_direction = db.Column(db.String(10))  # 'UP' or 'DOWN'
    predicted_price = db.Column(db.Float)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.Date)
    is_correct = db.Column(db.Boolean)
    points_earned = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'symbol': self.symbol,
            'predicted_direction': self.predicted_direction,
            'predicted_price': self.predicted_price,
            'prediction_date': self.prediction_date.isoformat() if self.prediction_date else None,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'is_correct': self.is_correct,
            'points_earned': self.points_earned
        }

