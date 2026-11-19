from typing import List, Dict, Any
from ..models import CryptoAsset, RiskProfile

class AlphaSynthesizerAgent:
    """Quantitative agent synthesizing multi-factor alpha scores for optimal asset selection."""

    def compute_alpha_rankings(
        self, assets: List[CryptoAsset], risk_profiles: Dict[str, RiskProfile]
    ) -> List[Dict[str, Any]]:
        rankings = []

        for asset in assets:
            risk = risk_profiles.get(asset.symbol)
            vol_score = risk.volatility_score if risk else 50.0

            # Factor 1: Momentum (0-100)
            mom_component = max(0.0, min(100.0, 50.0 + (asset.percent_change_24h * 3.0) + (asset.percent_change_7d * 0.5)))

            # Factor 2: Volume Quality (0-100)
            vol_component = min(100.0, asset.vol_to_mcap_ratio * 500.0)

            # Factor 3: Risk / Volatility penalty
            stability_component = max(0.0, 100.0 - (vol_score * 0.6))

            # Composite Alpha Score
            composite_alpha = round(
                (mom_component * 0.40) + (vol_component * 0.35) + (stability_component * 0.25), 1
            )

            rankings.append({
                "symbol": asset.symbol,
                "name": asset.name,
                "price": asset.price_usd,
                "alpha_score": composite_alpha,
                "momentum_score": round(mom_component, 1),
                "volume_quality": round(vol_component, 1),
                "risk_level": risk.risk_level if risk else "MODERATE",
                "recommendation": self._get_recommendation(composite_alpha)
            })

        rankings.sort(key=lambda x: x["alpha_score"], reverse=True)
        return rankings

    def _get_recommendation(self, score: float) -> str:
        if score >= 75.0:
            return "STRONG OVERWEIGHT (High Conviction Alpha)"
        elif score >= 60.0:
            return "OVERWEIGHT (Accumulate on Dips)"
        elif score >= 45.0:
            return "NEUTRAL (Market Weight)"
        else:
            return "UNDERWEIGHT (Elevated Risk / Drag)"
