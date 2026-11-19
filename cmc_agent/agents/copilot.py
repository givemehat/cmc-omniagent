import re
from typing import List, Dict, Any
from ..models import CryptoAsset, GlobalMarketMetrics, MarketSignal

class CopilotAgent:
    """Natural language AI agent that answers analytical queries using CoinMarketCap telemetry."""

    def answer_query(
        self,
        query: str,
        assets: List[CryptoAsset],
        global_metrics: GlobalMarketMetrics,
        signals: List[MarketSignal]
    ) -> Dict[str, Any]:
        query_lower = query.lower().strip()
        asset_map = {a.symbol.lower(): a for a in assets}
        asset_name_map = {a.name.lower(): a for a in assets}

        # 1. Market Overview / Macro questions
        if any(w in query_lower for w in ["market", "overview", "btc dominance", "macro", "total", "dominance"]):
            return {
                "intent": "GLOBAL_MARKET_OVERVIEW",
                "response": (
                    f"**Global Crypto Market Brief:**\n"
                    f"- Total Market Cap: ${global_metrics.total_market_cap_usd:,.0f}\n"
                    f"- 24h Volume: ${global_metrics.total_volume_24h_usd:,.0f}\n"
                    f"- Bitcoin Dominance: {global_metrics.btc_dominance:.1f}%\n"
                    f"- Ethereum Dominance: {global_metrics.eth_dominance:.1f}%\n"
                    f"- Active Cryptocurrencies Tracked: {global_metrics.active_cryptocurrencies:,}\n\n"
                    f"*Synthesized Outlook:* Market breadth is currently led by BTC dominance at {global_metrics.btc_dominance:.1f}%, "
                    f"while total 24h liquidity throughput remains active at ${global_metrics.total_volume_24h_usd / 1e9:.1f}B."
                ),
                "data": {
                    "total_market_cap": global_metrics.total_market_cap_usd,
                    "btc_dominance": global_metrics.btc_dominance
                }
            }

        # 2. Breakouts / Signals / Best tokens
        if any(w in query_lower for w in ["breakout", "signal", "buy", "trending", "top", "gainer"]):
            top_gainers = sorted(assets, key=lambda x: x.percent_change_24h, reverse=True)[:3]
            gainers_str = "\n".join([f"- **{a.symbol}**: ${a.price_usd:,.2f} (+{a.percent_change_24h:.2f}%) | Vol/MCap: {a.vol_to_mcap_ratio:.2%}" for a in top_gainers])
            active_signals = len(signals)

            return {
                "intent": "MOMENTUM_SIGNALS",
                "response": (
                    f"**AI Agent Breakout & Momentum Scan:**\n"
                    f"The Market Scout has generated **{active_signals} active signals** across the tracked universe.\n\n"
                    f"**Top 24h Momentum Leaders:**\n{gainers_str}\n\n"
                    f"*Alpha Insight:* Breakout velocity is strongest on assets exhibiting both double-digit 24h price expansion and sustained volume-to-market-cap ratios above 12%."
                ),
                "data": [{"symbol": a.symbol, "gain_24h": a.percent_change_24h} for a in top_gainers]
            }

        # 3. Specific asset lookup (e.g. "SOL", "Bitcoin", "ETH vs SOL")
        mentioned_assets = []
        for symbol, asset in asset_map.items():
            if re.search(r'\b' + re.escape(symbol) + r'\b', query_lower) or re.search(r'\b' + re.escape(asset.name.lower()) + r'\b', query_lower):
                mentioned_assets.append(asset)

        if mentioned_assets:
            details = []
            for a in mentioned_assets:
                details.append(
                    f"**{a.name} ({a.symbol}) Telemetry:**\n"
                    f"- Price: ${a.price_usd:,.2f}\n"
                    f"- 24h Change: {a.percent_change_24h:+.2f}%\n"
                    f"- 7d Change: {a.percent_change_7d:+.2f}%\n"
                    f"- 24h Volume: ${a.volume_24h:,.0f}\n"
                    f"- Market Cap: ${a.market_cap:,.0f}\n"
                    f"- Vol/MCap Ratio: {a.vol_to_mcap_ratio:.2%}"
                )
            return {
                "intent": "ASSET_DEEP_DIVE",
                "response": "\n\n".join(details),
                "data": [{"symbol": a.symbol, "price": a.price_usd, "change_24h": a.percent_change_24h} for a in mentioned_assets]
            }

        # 4. Default fallback synthesis
        return {
            "intent": "GENERAL_INQUIRY",
            "response": (
                f"I analyzed your request against real-time CoinMarketCap feeds. "
                f"Currently tracking {len(assets)} major assets with {len(signals)} autonomous signals active.\n\n"
                f"You can ask me:\n"
                f"- *'Show global market overview and BTC dominance'*\n"
                f"- *'Which tokens have active volume breakouts?'*\n"
                f"- *'Analyze SOL or BTC price and liquidity risk'*"
            ),
            "data": {}
        }
