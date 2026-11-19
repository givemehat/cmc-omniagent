from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class CryptoAsset:
    id: int
    name: str
    symbol: str
    slug: str
    price_usd: float
    volume_24h: float
    market_cap: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    circulating_supply: float
    last_updated: str
    vol_to_mcap_ratio: float = 0.0

    def __post_init__(self):
        if self.market_cap > 0:
            self.vol_to_mcap_ratio = round(self.volume_24h / self.market_cap, 4)

@dataclass
class MarketSignal:
    token_symbol: str
    token_name: str
    signal_type: str  # BREAKOUT, VOLATILITY_SPIKE, UNUSUAL_VOLUME, ACCUMULATION
    confidence: float # 0.0 to 1.0
    severity: str     # HIGH, MEDIUM, LOW
    headline: str
    rationale: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""

@dataclass
class RiskProfile:
    token_symbol: str
    volatility_score: float # 0 to 100
    liquidity_score: float  # 0 to 100
    risk_level: str         # LOW, MODERATE, HIGH, CRITICAL
    drawdown_risk: str
    warning_notes: List[str] = field(default_factory=list)

@dataclass
class GlobalMarketMetrics:
    total_market_cap_usd: float
    total_volume_24h_usd: float
    btc_dominance: float
    eth_dominance: float
    active_cryptocurrencies: int
    active_exchanges: int
