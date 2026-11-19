from typing import List, Dict
from ..models import CryptoAsset, RiskProfile

class VolatilitySentinelAgent:
    """Autonomous agent analyzing market risk, drawdown vulnerability, and volatility dispersion."""

    def evaluate_risks(self, assets: List[CryptoAsset]) -> Dict[str, RiskProfile]:
        profiles: Dict[str, RiskProfile] = {}

        for asset in assets:
            warnings = []
            # Calculate volatility score (0-100) based on multi-timeframe range
            abs_24h = abs(asset.percent_change_24h)
            abs_7d = abs(asset.percent_change_7d)
            vol_score = min(100.0, round((abs_24h * 3.5) + (abs_7d * 1.2), 1))

            # Liquidity score (higher market cap + healthy volume = higher liquidity safety)
            liq_score = min(100.0, round((asset.vol_to_mcap_ratio * 400.0) + (min(asset.market_cap / 1e10, 50.0)), 1))

            if abs_24h > 12.0:
                warnings.append(f"Elevated 24h tail volatility ({asset.percent_change_24h:+.1f}%)")
            if asset.vol_to_mcap_ratio < 0.02:
                warnings.append("Illiquid order book: low volume relative to capital base")
            if asset.percent_change_7d > 40.0:
                warnings.append("Extended weekly impulse; high mean-reversion risk")

            # Risk classification
            if vol_score > 65.0:
                risk_level = "HIGH"
                drawdown = "Severe downside sensitivity in market-wide pullbacks"
            elif vol_score > 40.0:
                risk_level = "MODERATE"
                drawdown = "Normal trading range volatility"
            else:
                risk_level = "LOW"
                drawdown = "Defensive market resilience"

            profiles[asset.symbol] = RiskProfile(
                token_symbol=asset.symbol,
                volatility_score=vol_score,
                liquidity_score=liq_score,
                risk_level=risk_level,
                drawdown_risk=drawdown,
                warning_notes=warnings
            )

        return profiles
