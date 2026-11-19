from typing import Dict, Any, Optional
from datetime import datetime
from .client import CoinMarketCapClient
from .agents.scout import MarketScoutAgent
from .agents.sentinel import VolatilitySentinelAgent
from .agents.alpha import AlphaSynthesizerAgent
from .agents.copilot import CopilotAgent

class OmniAgentPipeline:
    """Orchestrator managing multi-agent execution cycle and state persistence."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = CoinMarketCapClient(api_key=api_key)
        self.scout = MarketScoutAgent()
        self.sentinel = VolatilitySentinelAgent()
        self.alpha = AlphaSynthesizerAgent()
        self.copilot = CopilotAgent()

        self._cached_assets = []
        self._cached_global = None
        self._cached_signals = []
        self._cached_risks = {}
        self._cached_alpha = []
        self._last_run = None

    async def execute_cycle(self, limit: int = 50) -> Dict[str, Any]:
        """Run an autonomous analysis cycle across all 4 agents."""
        assets = await self.client.get_latest_listings(limit=limit)
        global_metrics = await self.client.get_global_metrics()

        signals = self.scout.analyze(assets)
        risks = self.sentinel.evaluate_risks(assets)
        alpha_rankings = self.alpha.compute_alpha_rankings(assets, risks)

        self._cached_assets = assets
        self._cached_global = global_metrics
        self._cached_signals = signals
        self._cached_risks = risks
        self._cached_alpha = alpha_rankings
        self._last_run = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        return {
            "status": "SUCCESS",
            "timestamp": self._last_run,
            "assets_tracked": len(assets),
            "signals_detected": len(signals),
            "top_alpha_pick": alpha_rankings[0] if alpha_rankings else None,
            "global_metrics": {
                "total_market_cap": global_metrics.total_market_cap_usd,
                "total_volume_24h": global_metrics.total_volume_24h_usd,
                "btc_dominance": global_metrics.btc_dominance,
                "eth_dominance": global_metrics.eth_dominance
            },
            "signals": [s.__dict__ for s in signals],
            "alpha_rankings": alpha_rankings,
            "risks": {k: v.__dict__ for k, v in risks.items()}
        }

    def chat_with_copilot(self, user_query: str) -> Dict[str, Any]:
        """Query the Copilot Agent using the latest market state."""
        return self.copilot.answer_query(
            query=user_query,
            assets=self._cached_assets,
            global_metrics=self._cached_global,
            signals=self._cached_signals
        )
