import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Button } from './components/ui/button'
import { Badge } from './components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { Progress } from './components/ui/progress'
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  DollarSign, 
  Users, 
  Trophy,
  BarChart3,
  Clock,
  Target,
  AlertTriangle,
  Brain,
  Globe,
  Zap,
  Info
} from 'lucide-react'
import './App.css'

// API 기본 URL (향상된 백엔드)
const API_BASE_URL = 'https://g8h3ilc7vokm.manus.space/api'

// API 호출 함수들
const fetchRobots = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/robots`)
    const data = await response.json()
    return data.success ? data.data : []
  } catch (error) {
    console.error('Error fetching robots:', error)
    return []
  }
}

const fetchDetailedTrades = async (limit = 20) => {
  try {
    const response = await fetch(`${API_BASE_URL}/trades/recent?details=true&limit=${limit}`)
    const data = await response.json()
    return data.success ? data.data : []
  } catch (error) {
    console.error('Error fetching detailed trades:', error)
    return []
  }
}

const fetchLiveTrades = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/trades/live`)
    const data = await response.json()
    return data.success ? data.data : []
  } catch (error) {
    console.error('Error fetching live trades:', error)
    return []
  }
}

const fetchMarketCondition = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/market/condition`)
    const data = await response.json()
    return data.success ? data.data : {}
  } catch (error) {
    console.error('Error fetching market condition:', error)
    return {}
  }
}

const fetchSectorPerformance = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/trades/sectors`)
    const data = await response.json()
    return data.success ? data.data : []
  } catch (error) {
    console.error('Error fetching sector performance:', error)
    return []
  }
}

const fetchTrendingStocks = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/market/trending`)
    const data = await response.json()
    return data.success ? data.data : []
  } catch (error) {
    console.error('Error fetching trending stocks:', error)
    return []
  }
}

const fetchPredictions = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/predictions/leaderboard`)
    const data = await response.json()
    return data.success ? data.data : []
  } catch (error) {
    console.error('Error fetching predictions:', error)
    return []
  }
}

const fetchMetaModel = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/meta-model/performance`)
    const data = await response.json()
    return data.success ? data.data : {}
  } catch (error) {
    console.error('Error fetching meta model:', error)
    return {}
  }
}

// 거래 상세 정보 모달 컴포넌트
const TradeDetailModal = ({ trade, onClose }) => {
  if (!trade) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">거래 상세 정보</h2>
            <Button variant="outline" onClick={onClose}>닫기</Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* 기본 거래 정보 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <DollarSign className="h-5 w-5" />
                  거래 정보
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">종목:</span>
                  <span className="font-semibold">{trade.symbol} - {trade.company_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">거래 유형:</span>
                  <Badge variant={trade.trade_type === 'BUY' ? 'default' : 'destructive'}>
                    {trade.trade_type}
                  </Badge>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">수량:</span>
                  <span>{trade.quantity.toLocaleString()}주</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">가격:</span>
                  <span>${trade.price}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">총 금액:</span>
                  <span className="font-semibold">${trade.total_amount.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">로봇:</span>
                  <span>{trade.robot_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">섹터:</span>
                  <span>{trade.sector}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">신뢰도:</span>
                  <span>{trade.confidence_score}%</span>
                </div>
              </CardContent>
            </Card>

            {/* 거래 이유 및 전략 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5" />
                  거래 분석
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <span className="text-gray-600 block mb-1">거래 이유:</span>
                  <p className="text-sm bg-gray-50 p-2 rounded">{trade.reason}</p>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">시장 상황:</span>
                  <Badge variant={
                    trade.market_condition === 'bullish' ? 'default' : 
                    trade.market_condition === 'bearish' ? 'destructive' : 'secondary'
                  }>
                    {trade.market_condition}
                  </Badge>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">예상 수익률:</span>
                  <span className="text-green-600">{trade.trade_strategy?.expected_return}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">손절가:</span>
                  <span className="text-red-600">${trade.trade_strategy?.stop_loss}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">익절가:</span>
                  <span className="text-green-600">${trade.trade_strategy?.take_profit}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">예상 보유기간:</span>
                  <span>{trade.trade_strategy?.holding_period}일</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">포지션 크기:</span>
                  <span>{trade.trade_strategy?.position_size_pct}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">리스크 점수:</span>
                  <span>{trade.trade_strategy?.risk_score}/10</span>
                </div>
              </CardContent>
            </Card>

            {/* 기술적 지표 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  기술적 지표
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">RSI:</span>
                  <span>{trade.technical_indicators?.rsi}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">MACD:</span>
                  <span>{trade.technical_indicators?.macd}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">20일 이평:</span>
                  <span>${trade.technical_indicators?.moving_avg_20}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">50일 이평:</span>
                  <span>${trade.technical_indicators?.moving_avg_50}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">거래량 비율:</span>
                  <span>{trade.technical_indicators?.volume_ratio}x</span>
                </div>
              </CardContent>
            </Card>

            {/* 시장 데이터 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5" />
                  시장 데이터
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">시가:</span>
                  <span>${trade.market_data?.day_open}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">고가:</span>
                  <span>${trade.market_data?.day_high}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">저가:</span>
                  <span>${trade.market_data?.day_low}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">전일 종가:</span>
                  <span>${trade.market_data?.prev_close}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">거래 시점 가격:</span>
                  <span className="font-semibold">${trade.market_data?.market_price_at_trade}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

function App() {
  const [robots, setRobots] = useState([])
  const [detailedTrades, setDetailedTrades] = useState([])
  const [liveTrades, setLiveTrades] = useState([])
  const [marketCondition, setMarketCondition] = useState({})
  const [sectorPerformance, setSectorPerformance] = useState([])
  const [trendingStocks, setTrendingStocks] = useState([])
  const [predictions, setPredictions] = useState([])
  const [metaModel, setMetaModel] = useState({})
  const [selectedTrade, setSelectedTrade] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  // 데이터 로딩 함수
  const loadData = async () => {
    try {
      const [
        robotsData,
        detailedTradesData,
        liveTradesData,
        marketData,
        sectorData,
        trendingData,
        predictionsData,
        metaModelData
      ] = await Promise.all([
        fetchRobots(),
        fetchDetailedTrades(20),
        fetchLiveTrades(),
        fetchMarketCondition(),
        fetchSectorPerformance(),
        fetchTrendingStocks(),
        fetchPredictions(),
        fetchMetaModel()
      ])

      setRobots(robotsData)
      setDetailedTrades(detailedTradesData)
      setLiveTrades(liveTradesData)
      setMarketCondition(marketData)
      setSectorPerformance(sectorData)
      setTrendingStocks(trendingData)
      setPredictions(predictionsData)
      setMetaModel(metaModelData)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Error loading data:', error)
    }
  }

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000) // 30초마다 업데이트
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* 헤더 */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Activity className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AI Trading Robots Arena</h1>
                <p className="text-sm text-gray-600">투자 로봇 거래 플랫폼</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">
                  {new Date().toLocaleDateString('ko-KR')} {new Date().toLocaleTimeString('ko-KR')}
                </p>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-xs text-green-600">실시간 거래 중</span>
                </div>
              </div>
              <Button onClick={loadData} variant="outline" size="sm">
                <Zap className="h-4 w-4 mr-1" />
                새로고침
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 시장 상황 대시보드 */}
        {marketCondition && Object.keys(marketCondition).length > 0 && (
          <Card className="mb-8 bg-gradient-to-r from-purple-500 to-pink-500 text-white">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-6 w-6" />
                현재 시장 상황
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <p className="text-sm opacity-90">전체 심리</p>
                  <Badge variant={
                    marketCondition.overall_sentiment === 'bullish' ? 'default' : 
                    marketCondition.overall_sentiment === 'bearish' ? 'destructive' : 'secondary'
                  } className="mt-1">
                    {marketCondition.overall_sentiment}
                  </Badge>
                </div>
                <div className="text-center">
                  <p className="text-sm opacity-90">VIX 지수</p>
                  <p className="text-lg font-bold">{marketCondition.vix_level}</p>
                </div>
                <div className="text-center">
                  <p className="text-sm opacity-90">S&P 500</p>
                  <p className={`text-lg font-bold ${marketCondition.market_changes?.sp500 >= 0 ? 'text-green-300' : 'text-red-300'}`}>
                    {marketCondition.market_changes?.sp500 >= 0 ? '+' : ''}{marketCondition.market_changes?.sp500}%
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-sm opacity-90">NASDAQ</p>
                  <p className={`text-lg font-bold ${marketCondition.market_changes?.nasdaq >= 0 ? 'text-green-300' : 'text-red-300'}`}>
                    {marketCondition.market_changes?.nasdaq >= 0 ? '+' : ''}{marketCondition.market_changes?.nasdaq}%
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* 메인 컨텐츠 */}
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">AI 투자 로봇들의 실시간 거래 경쟁</h2>
          <p className="text-xl text-gray-600 mb-6">
            검증된 알고리즘으로 만들어진 {robots.length}개의 투자 로봇이 미국 전체 상장기업을 대상으로 실시간 경쟁합니다
          </p>
          <div className="flex justify-center space-x-4">
            <Button size="lg" className="bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600">
              <TrendingUp className="mr-2 h-5 w-5" />
              실시간 거래 보기
            </Button>
            <Button size="lg" variant="outline">
              <Users className="mr-2 h-5 w-5" />
              예측 게임 참여
            </Button>
          </div>
        </div>

        {/* 메타 모델 카드 */}
        {metaModel && Object.keys(metaModel).length > 0 && (
          <Card className="mb-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <Trophy className="h-8 w-8" />
                Meta Model - 통합 AI 투자 모델
              </CardTitle>
              <CardDescription className="text-blue-100">
                {robots.length}개 로봇의 장점을 결합한 최적화된 투자 전략
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <p className="text-3xl font-bold text-yellow-300">+{metaModel.total_return || '15.64'}%</p>
                  <p className="text-sm text-blue-100">총 수익률</p>
                </div>
                <div className="text-center">
                  <p className="text-3xl font-bold">{metaModel.win_rate || '69.2'}%</p>
                  <p className="text-sm text-blue-100">승률</p>
                </div>
                <div className="text-center">
                  <p className="text-3xl font-bold">${(metaModel.current_capital || 117640).toLocaleString()}</p>
                  <p className="text-sm text-blue-100">현재 자산</p>
                </div>
                <div className="text-center">
                  <p className="text-3xl font-bold">{metaModel.sharpe_ratio || '1.53'}</p>
                  <p className="text-sm text-blue-100">샤프 비율</p>
                </div>
                <div className="text-center">
                  <p className="text-3xl font-bold">{metaModel.max_drawdown || '18.5'}%</p>
                  <p className="text-sm text-blue-100">최대 손실</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* 탭 컨텐츠 */}
        <Tabs defaultValue="robots" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="robots">투자 로봇</TabsTrigger>
            <TabsTrigger value="trades">실시간 거래</TabsTrigger>
            <TabsTrigger value="market">시장 분석</TabsTrigger>
            <TabsTrigger value="predictions">예측 게임</TabsTrigger>
          </TabsList>

          {/* 투자 로봇 탭 */}
          <TabsContent value="robots">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {robots.map((robot) => (
                <Card key={robot.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <Brain className="h-5 w-5 text-blue-600" />
                        </div>
                        {robot.name}
                      </CardTitle>
                      <Badge variant={robot.risk_level === '높음' ? 'destructive' : robot.risk_level === '중간' ? 'default' : 'secondary'}>
                        {robot.risk_level}
                      </Badge>
                    </div>
                    <CardDescription>{robot.strategy_type}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-gray-600">{robot.description}</p>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">수익률</span>
                        <span className={`font-semibold ${robot.total_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {robot.total_return >= 0 ? '+' : ''}{robot.total_return}%
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">승률</span>
                        <span className="font-semibold">{robot.win_rate}%</span>
                      </div>
                      <Progress value={robot.win_rate} className="h-2" />
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">승률 진행도</span>
                        <span className="text-sm text-gray-500">{robot.win_rate}%</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">현재 자산</span>
                        <span className="font-semibold">${robot.current_capital?.toLocaleString()}</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">샤프 비율</span>
                        <span className="font-semibold">{robot.sharpe_ratio}</span>
                      </div>
                    </div>
                    
                    <Button className="w-full" variant="outline">
                      <BarChart3 className="mr-2 h-4 w-4" />
                      상세 보기
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* 실시간 거래 탭 */}
          <TabsContent value="trades">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 실시간 거래 현황 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="h-5 w-5" />
                    실시간 거래 현황
                  </CardTitle>
                  <CardDescription>
                    최근 거래 내역 (자동 업데이트)
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {liveTrades.map((trade, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`p-2 rounded-full ${trade.trade_type === 'BUY' ? 'bg-green-100' : 'bg-red-100'}`}>
                            {trade.trade_type === 'BUY' ? 
                              <TrendingUp className={`h-4 w-4 text-green-600`} /> : 
                              <TrendingDown className={`h-4 w-4 text-red-600`} />
                            }
                          </div>
                          <div>
                            <p className="font-semibold">{trade.symbol}</p>
                            <p className="text-sm text-gray-600">{trade.robot_name}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">${trade.price}</p>
                          <p className="text-sm text-gray-600">{trade.time_ago}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* 상세 거래 로그 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Info className="h-5 w-5" />
                    상세 거래 로그
                  </CardTitle>
                  <CardDescription>
                    거래 이유와 기술적 분석 포함
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {detailedTrades.slice(0, 10).map((trade) => (
                      <div 
                        key={trade.id} 
                        className="p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                        onClick={() => setSelectedTrade(trade)}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <Badge variant={trade.trade_type === 'BUY' ? 'default' : 'destructive'}>
                              {trade.trade_type}
                            </Badge>
                            <span className="font-semibold">{trade.symbol}</span>
                            <span className="text-sm text-gray-600">{trade.sector}</span>
                          </div>
                          <span className="text-sm text-gray-500">신뢰도: {trade.confidence_score}%</span>
                        </div>
                        <p className="text-sm text-gray-600 mb-1">{trade.robot_name}</p>
                        <p className="text-xs text-gray-500 truncate">{trade.reason}</p>
                        <div className="flex justify-between items-center mt-2">
                          <span className="text-sm font-semibold">${trade.price} × {trade.quantity}</span>
                          <span className="text-xs text-gray-500">
                            {new Date(trade.trade_date).toLocaleTimeString('ko-KR')}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* 인기 종목 */}
            {trendingStocks.length > 0 && (
              <Card className="mt-6">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5" />
                    인기 거래 종목
                  </CardTitle>
                  <CardDescription>
                    최근 24시간 거래량 기준
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {trendingStocks.slice(0, 6).map((stock, index) => (
                      <div key={index} className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-semibold">{stock.symbol}</span>
                          <Badge variant="outline">{stock.sector}</Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{stock.company_name}</p>
                        <div className="flex justify-between items-center">
                          <span className="text-lg font-bold">${stock.current_price}</span>
                          <span className={`text-sm ${stock.change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent}%
                          </span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          거래 횟수: {stock.trade_count} | 신뢰도: {stock.avg_confidence}%
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* 시장 분석 탭 */}
          <TabsContent value="market">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 섹터별 성과 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    섹터별 성과
                  </CardTitle>
                  <CardDescription>
                    오늘의 섹터별 수익률과 거래 활동
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {sectorPerformance.map((sector, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-semibold">{sector.sector}</p>
                          <p className="text-sm text-gray-600">거래 {sector.trade_count}회 | 신뢰도 {sector.avg_confidence}%</p>
                        </div>
                        <div className="text-right">
                          <span className={`text-lg font-bold ${sector.performance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {sector.performance >= 0 ? '+' : ''}{sector.performance}%
                          </span>
                          <div className="flex items-center">
                            {sector.trend === 'up' ? 
                              <TrendingUp className="h-4 w-4 text-green-600" /> : 
                              sector.trend === 'down' ? 
                              <TrendingDown className="h-4 w-4 text-red-600" /> :
                              <div className="h-4 w-4" />
                            }
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* 시장 지표 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5" />
                    주요 시장 지표
                  </CardTitle>
                  <CardDescription>
                    실시간 시장 상황 분석
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <h4 className="font-semibold mb-2">변동성 지수 (VIX)</h4>
                      <p className="text-2xl font-bold text-blue-600">{marketCondition.vix_level || '22.5'}</p>
                      <p className="text-sm text-gray-600">시장 불안감 수준</p>
                    </div>
                    
                    <div className="p-4 bg-green-50 rounded-lg">
                      <h4 className="font-semibold mb-2">거래량 트렌드</h4>
                      <p className="text-lg font-bold text-green-600">{marketCondition.volume_trend || 'Normal'}</p>
                      <p className="text-sm text-gray-600">평균 대비 거래량</p>
                    </div>
                    
                    <div className="p-4 bg-purple-50 rounded-lg">
                      <h4 className="font-semibold mb-2">뉴스 감정 지수</h4>
                      <p className="text-lg font-bold text-purple-600">
                        {marketCondition.news_sentiment ? 
                          (marketCondition.news_sentiment > 0 ? '긍정적' : marketCondition.news_sentiment < 0 ? '부정적' : '중립적') : 
                          '중립적'
                        }
                      </p>
                      <p className="text-sm text-gray-600">시장 뉴스 분석 결과</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* 예측 게임 탭 */}
          <TabsContent value="predictions">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5" />
                    주가 예측 게임
                  </CardTitle>
                  <CardDescription>
                    내일의 주가 방향을 예측하고 포인트를 획득하세요
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg">
                      <h4 className="font-semibold mb-2">오늘의 예측 종목: AAPL</h4>
                      <p className="text-sm text-gray-600 mb-3">현재가: $175.23 (+1.2%)</p>
                      <div className="flex space-x-2">
                        <Button className="flex-1 bg-green-600 hover:bg-green-700">
                          <TrendingUp className="mr-2 h-4 w-4" />
                          상승 예측
                        </Button>
                        <Button className="flex-1 bg-red-600 hover:bg-red-700">
                          <TrendingDown className="mr-2 h-4 w-4" />
                          하락 예측
                        </Button>
                      </div>
                    </div>
                    
                    <div className="text-center p-4 bg-yellow-50 rounded-lg">
                      <Trophy className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                      <p className="font-semibold">내 예측 점수</p>
                      <p className="text-2xl font-bold text-yellow-600">1,250 점</p>
                      <p className="text-sm text-gray-600">정확도: 68%</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Trophy className="h-5 w-5" />
                    예측 순위표
                  </CardTitle>
                  <CardDescription>
                    이번 주 최고 예측자들
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {predictions.map((user, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                            index === 0 ? 'bg-yellow-500' : index === 1 ? 'bg-gray-400' : index === 2 ? 'bg-orange-500' : 'bg-blue-500'
                          }`}>
                            {index + 1}
                          </div>
                          <div>
                            <p className="font-semibold">{user.user_name}</p>
                            <p className="text-sm text-gray-600">정확도: {user.accuracy}%</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">{user.points} 점</p>
                          <p className="text-sm text-gray-600">{user.predictions_count}회 예측</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* 거래 상세 정보 모달 */}
      {selectedTrade && (
        <TradeDetailModal 
          trade={selectedTrade} 
          onClose={() => setSelectedTrade(null)} 
        />
      )}

      {/* 푸터 */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">마지막 업데이트: {lastUpdate.toLocaleTimeString('ko-KR')}</p>
            <p className="text-sm">
              실시간 데이터는 30초마다 자동 업데이트됩니다. 
              총 {robots.length}개 로봇이 미국 전체 상장기업을 대상으로 거래 중입니다.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

