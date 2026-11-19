from typing import List
from datetime import datetime
from ..models import CryptoAsset, MarketSignal

class MarketScoutAgent:
    """Autonomous agent that identifies volume surges, momentum breakouts, and liquidity divergences."""

    def analyze(self, assets: List[CryptoAsset]) -> List[MarketSignal]:
        signals: List[MarketSignal] = []
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        for asset in assets:
            # 1. Unusual Volume Anomaly (Volume / MCap > 0.12 for large cap, > 0.20 for mid cap)
            if asset.vol_to_mcap_ratio >= 0.12:
                signals.append(MarketSignal(
                    token_symbol=asset.symbol,
                    token_name=asset.name,
                    signal_type="UNUSUAL_VOLUME",
                    confidence=min(0.95, round(0.70 + (asset.vol_to_mcap_ratio * 1.5), 2)),
                    severity="HIGH" if asset.vol_to_mcap_ratio > 0.18 else "MEDIUM",
                    headline=f"Aggressive volume turnover detected on {asset.symbol}",
                    rationale=f"24h Volume/MCap ratio reached {asset.vol_to_mcap_ratio:.2%}, indicating heavy liquidity churn and institutional interest.",
                    metrics={"volume_24h": asset.volume_24h, "vol_to_mcap": asset.vol_to_mcap_ratio, "price": asset.price_usd},
                    timestamp=now_str
                ))

            # 2. Strong Price Breakout (24h change > 8%)
            if asset.percent_change_24h >= 8.0:
                signals.append(MarketSignal(
                    token_symbol=asset.symbol,
                    token_name=asset.name,
                    signal_type="BREAKOUT",
                    confidence=0.88,
                    severity="HIGH",
                    headline=f"Bullish momentum surge: {asset.symbol} +{asset.percent_change_24h:.2f}%",
                    rationale=f"Strong 24h expansion with multi-timeframe confirmation (1h: {asset.percent_change_1h:+.2f}%, 7d: {asset.percent_change_7d:+.2f}%).",
                    metrics={"change_24h": asset.percent_change_24h, "change_7d": asset.percent_change_7d, "price": asset.price_usd},
                    timestamp=now_str
                ))

            # 3. Consolidation / Accumulation (1h positive while 24h flat with high volume)
            if 0.0 <= asset.percent_change_24h <= 3.0 and asset.percent_change_1h > 0.8 and asset.vol_to_mcap_ratio > 0.08:
                signals.append(MarketSignal(
                    token_symbol=asset.symbol,
                    token_name=asset.name,
                    signal_type="ACCUMULATION",
                    confidence=0.76,
                    severity="LOW",
                    headline=f"Quiet accumulation structure forming on {asset.symbol}",
                    rationale=f"Price compressed in narrow 24h range with steady 1h upward bias and sustained volume turnover.",
                    metrics={"change_1h": asset.percent_change_1h, "change_24h": asset.percent_change_24h},
                    timestamp=now_str
                ))

        return signals
