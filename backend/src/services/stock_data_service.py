import requests
import random
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import json

class StockDataService:
    """실제 주식 데이터를 가져오는 서비스"""
    
    def __init__(self, polygon_api_key: str = None):
        self.polygon_api_key = polygon_api_key or "demo"  # 데모 키 사용
        self.base_url = "https://api.polygon.io"
        
        # 주요 섹터별 대표 종목들
        self.sector_stocks = {
            "Technology": ["AAPL", "MSFT", "GOOGL", "NVDA", "META", "TSLA", "NFLX", "ADBE", "CRM", "ORCL"],
            "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "TMO", "DHR", "BMY", "AMGN", "GILD", "BIIB"],
            "Financial": ["JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "BLK", "SCHW", "USB"],
            "Consumer Discretionary": ["AMZN", "HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "TJX", "F", "GM"],
            "Consumer Staples": ["PG", "KO", "PEP", "WMT", "COST", "CL", "KMB", "GIS", "K", "HSY"],
            "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "MPC", "OXY", "HAL"],
            "Industrials": ["BA", "CAT", "GE", "MMM", "HON", "UPS", "RTX", "LMT", "DE", "EMR"],
            "Materials": ["LIN", "APD", "SHW", "ECL", "FCX", "NEM", "DOW", "DD", "PPG", "IFF"],
            "Utilities": ["NEE", "DUK", "SO", "D", "AEP", "EXC", "XEL", "SRE", "PEG", "ED"],
            "Real Estate": ["AMT", "PLD", "CCI", "EQIX", "PSA", "WELL", "DLR", "O", "SBAC", "EXR"],
            "Communication": ["VZ", "T", "CMCSA", "DIS", "CHTR", "TMUS", "NFLX", "GOOGL", "META", "TWTR"]
        }
        
        # 시가총액별 분류
        self.market_cap_ranges = {
            "large": 10000000000,  # 100억 이상
            "mid": 2000000000,     # 20억 이상
            "small": 300000000,    # 3억 이상
            "micro": 0             # 3억 미만
        }
    
    def get_all_tickers(self, limit: int = 1000) -> List[Dict]:
        """모든 활성 주식 티커 목록 가져오기"""
        try:
            url = f"{self.base_url}/v3/reference/tickers"
            params = {
                "market": "stocks",
                "active": "true",
                "limit": limit,
                "apikey": self.polygon_api_key
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            else:
                # API 호출 실패 시 샘플 데이터 반환
                return self._get_sample_tickers()
        except Exception as e:
            print(f"Error fetching tickers: {e}")
            return self._get_sample_tickers()
    
    def _get_sample_tickers(self) -> List[Dict]:
        """샘플 티커 데이터 생성"""
        sample_tickers = []
        for sector, stocks in self.sector_stocks.items():
            for stock in stocks:
                sample_tickers.append({
                    "ticker": stock,
                    "name": f"{stock} Inc.",
                    "market": "stocks",
                    "primary_exchange": random.choice(["NYSE", "NASDAQ"]),
                    "type": "CS",
                    "active": True,
                    "currency_name": "usd"
                })
        
        # 추가 랜덤 종목들
        additional_stocks = [
            "ROKU", "ZOOM", "SHOP", "SQ", "PYPL", "UBER", "LYFT", "SNAP", "TWTR", "PINS",
            "DOCU", "ZM", "CRWD", "OKTA", "SNOW", "PLTR", "RBLX", "COIN", "HOOD", "RIVN"
        ]
        
        for stock in additional_stocks:
            sample_tickers.append({
                "ticker": stock,
                "name": f"{stock} Corporation",
                "market": "stocks",
                "primary_exchange": "NASDAQ",
                "type": "CS",
                "active": True,
                "currency_name": "usd"
            })
        
        return sample_tickers
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """실시간 주식 시세 가져오기"""
        try:
            url = f"{self.base_url}/v2/aggs/ticker/{symbol}/prev"
            params = {"apikey": self.polygon_api_key}
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    result = data["results"][0]
                    return {
                        "symbol": symbol,
                        "open": result.get("o"),
                        "high": result.get("h"),
                        "low": result.get("l"),
                        "close": result.get("c"),
                        "volume": result.get("v"),
                        "timestamp": result.get("t")
                    }
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
        
        # API 호출 실패 시 모의 데이터 반환
        return self._generate_mock_quote(symbol)
    
    def _generate_mock_quote(self, symbol: str) -> Dict:
        """모의 주식 시세 생성"""
        base_prices = {
            "AAPL": 175.23, "MSFT": 378.45, "GOOGL": 142.67, "NVDA": 489.12,
            "TSLA": 248.89, "AMZN": 145.32, "META": 298.76, "NFLX": 456.78
        }
        
        base_price = base_prices.get(symbol, random.uniform(50, 500))
        change_pct = random.uniform(-5, 5)
        current_price = base_price * (1 + change_pct / 100)
        
        return {
            "symbol": symbol,
            "open": round(base_price * random.uniform(0.98, 1.02), 2),
            "high": round(current_price * random.uniform(1.01, 1.05), 2),
            "low": round(current_price * random.uniform(0.95, 0.99), 2),
            "close": round(current_price, 2),
            "volume": random.randint(1000000, 50000000),
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
    
    def get_market_condition(self) -> Dict:
        """현재 시장 상황 분석"""
        # 실제로는 여러 지표를 종합하여 분석
        market_conditions = ["bullish", "bearish", "neutral"]
        sentiment = random.choice(market_conditions)
        
        return {
            "date": date.today().isoformat(),
            "overall_sentiment": sentiment,
            "vix_level": round(random.uniform(15, 35), 2),
            "market_changes": {
                "sp500": round(random.uniform(-2, 2), 2),
                "nasdaq": round(random.uniform(-3, 3), 2),
                "dow": round(random.uniform(-2, 2), 2)
            },
            "volume_trend": random.choice(["high", "normal", "low"]),
            "sector_rotation": self._generate_sector_performance(),
            "news_sentiment": round(random.uniform(-0.5, 0.5), 2)
        }
    
    def _generate_sector_performance(self) -> Dict:
        """섹터별 성과 생성"""
        sector_performance = {}
        for sector in self.sector_stocks.keys():
            sector_performance[sector] = round(random.uniform(-3, 3), 2)
        return sector_performance
    
    def generate_detailed_trade_data(self, symbol: str, trade_type: str, robot_name: str) -> Dict:
        """상세한 거래 데이터 생성"""
        quote = self.get_stock_quote(symbol)
        market_condition = self.get_market_condition()
        
        # 섹터 결정
        sector = "Technology"  # 기본값
        for sec, stocks in self.sector_stocks.items():
            if symbol in stocks:
                sector = sec
                break
        
        # 시가총액 결정
        market_cap = random.choice(["large", "mid", "small"])
        
        # 기술적 지표 생성
        price = quote["close"]
        technical_indicators = {
            "rsi": round(random.uniform(20, 80), 2),
            "macd": round(random.uniform(-2, 2), 3),
            "moving_avg_20": round(price * random.uniform(0.95, 1.05), 2),
            "moving_avg_50": round(price * random.uniform(0.90, 1.10), 2),
            "volume_ratio": round(random.uniform(0.5, 2.0), 2)
        }
        
        # 거래 이유 생성
        reasons = {
            "BUY": [
                f"RSI 지표가 {technical_indicators['rsi']}로 과매도 구간 진입",
                f"20일 이동평균선 돌파로 상승 모멘텀 확인",
                f"거래량이 평균 대비 {technical_indicators['volume_ratio']}배 증가",
                f"{sector} 섹터 강세로 인한 매수 신호",
                f"MACD 골든크로스 발생으로 상승 전환 신호"
            ],
            "SELL": [
                f"RSI 지표가 {technical_indicators['rsi']}로 과매수 구간 진입",
                f"20일 이동평균선 하향 이탈로 하락 모멘텀 확인",
                f"거래량 감소로 상승 동력 약화",
                f"{sector} 섹터 약세로 인한 매도 신호",
                f"MACD 데드크로스 발생으로 하락 전환 신호"
            ]
        }
        
        return {
            "symbol": symbol,
            "company_name": f"{symbol} Inc.",
            "trade_type": trade_type,
            "price": price,
            "reason": random.choice(reasons[trade_type]),
            "confidence_score": round(random.uniform(70, 95), 1),
            "market_condition": market_condition["overall_sentiment"],
            "sector": sector,
            "market_cap": market_cap,
            "technical_indicators": technical_indicators,
            "market_data": {
                "market_price_at_trade": price,
                "day_high": quote["high"],
                "day_low": quote["low"],
                "day_open": quote["open"],
                "prev_close": round(price * random.uniform(0.98, 1.02), 2)
            },
            "trade_strategy": {
                "expected_return": round(random.uniform(5, 20), 1),
                "stop_loss": round(price * (0.95 if trade_type == "BUY" else 1.05), 2),
                "take_profit": round(price * (1.15 if trade_type == "BUY" else 0.85), 2),
                "holding_period": random.randint(1, 30),
                "position_size_pct": round(random.uniform(2, 8), 1),
                "risk_score": round(random.uniform(3, 8), 1)
            }
        }
    
    def get_random_stock_for_trading(self) -> str:
        """거래할 랜덤 주식 선택"""
        all_stocks = []
        for stocks in self.sector_stocks.values():
            all_stocks.extend(stocks)
        
        # 추가 종목들도 포함
        additional_stocks = [
            "ROKU", "ZOOM", "SHOP", "SQ", "PYPL", "UBER", "LYFT", "SNAP", "TWTR", "PINS",
            "DOCU", "ZM", "CRWD", "OKTA", "SNOW", "PLTR", "RBLX", "COIN", "HOOD", "RIVN",
            "AMD", "INTC", "QCOM", "AVGO", "TXN", "MU", "LRCX", "KLAC", "MCHP", "XLNX"
        ]
        all_stocks.extend(additional_stocks)
        
        return random.choice(all_stocks)

