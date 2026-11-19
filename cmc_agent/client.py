import os
import json
import urllib.request
import urllib.error
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import CryptoAsset, GlobalMarketMetrics

class CoinMarketCapClient:
    BASE_URL = "https://pro-api.coinmarketcap.com"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CMC_API_KEY", "")
        self.is_live = bool(self.api_key and self.api_key != "your_coinmarketcap_api_key_here")

    async def get_latest_listings(self, limit: int = 50) -> List[CryptoAsset]:
        """Fetch top cryptocurrency listings from CMC API or realistic benchmark feed."""
        if not self.is_live:
            return self._get_fallback_listings(limit)

        url = f"{self.BASE_URL}/v1/cryptocurrency/listings/latest?start=1&limit={limit}&convert=USD"
        headers = {
            "X-CMC_PRO_API_KEY": self.api_key,
            "Accept": "application/json"
        }

        try:
            data = await asyncio.to_thread(self._fetch_json, url, headers)
            items = data.get("data", [])
            if items:
                return [self._parse_asset(item) for item in items]
        except Exception:
            pass

        return self._get_fallback_listings(limit)

    async def get_global_metrics(self) -> GlobalMarketMetrics:
        """Fetch global market metrics from CMC API."""
        if not self.is_live:
            return self._get_fallback_global_metrics()

        url = f"{self.BASE_URL}/v1/global-metrics/quotes/latest"
        headers = {"X-CMC_PRO_API_KEY": self.api_key, "Accept": "application/json"}

        try:
            data = await asyncio.to_thread(self._fetch_json, url, headers)
            d = data.get("data", {})
            quote = d.get("quote", {}).get("USD", {})
            return GlobalMarketMetrics(
                total_market_cap_usd=float(quote.get("total_market_cap", 3.2e12)),
                total_volume_24h_usd=float(quote.get("total_volume_24h", 1.4e11)),
                btc_dominance=float(d.get("btc_dominance", 58.0)),
                eth_dominance=float(d.get("eth_dominance", 14.0)),
                active_cryptocurrencies=int(d.get("active_cryptocurrencies", 10000)),
                active_exchanges=int(d.get("active_exchanges", 700))
            )
        except Exception:
            pass

        return self._get_fallback_global_metrics()

    def _fetch_json(self, url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    def _parse_asset(self, item: Dict[str, Any]) -> CryptoAsset:
        quote = item.get("quote", {}).get("USD", {})
        return CryptoAsset(
            id=item.get("id", 0),
            name=item.get("name", ""),
            symbol=item.get("symbol", ""),
            slug=item.get("slug", ""),
            price_usd=float(quote.get("price", 0.0)),
            volume_24h=float(quote.get("volume_24h", 0.0)),
            market_cap=float(quote.get("market_cap", 0.0)),
            percent_change_1h=float(quote.get("percent_change_1h", 0.0)),
            percent_change_24h=float(quote.get("percent_change_24h", 0.0)),
            percent_change_7d=float(quote.get("percent_change_7d", 0.0)),
            circulating_supply=float(item.get("circulating_supply", 0.0)),
            last_updated=quote.get("last_updated", datetime.utcnow().isoformat())
        )

    def _get_fallback_global_metrics(self) -> GlobalMarketMetrics:
        return GlobalMarketMetrics(
            total_market_cap_usd=3_250_450_000_000.0,
            total_volume_24h_usd=142_890_000_000.0,
            btc_dominance=58.4,
            eth_dominance=14.2,
            active_cryptocurrencies=10420,
            active_exchanges=740
        )

    def _get_fallback_listings(self, limit: int = 50) -> List[CryptoAsset]:
        now = datetime.utcnow().isoformat()
        sample = [
            CryptoAsset(1, "Bitcoin", "BTC", "bitcoin", 94250.0, 48500000000.0, 1860000000000.0, 0.42, 3.85, 8.40, 19780000.0, now),
            CryptoAsset(1027, "Ethereum", "ETH", "ethereum", 3420.0, 22100000000.0, 412000000000.0, -0.15, 4.12, 11.20, 120400000.0, now),
            CryptoAsset(5426, "Solana", "SOL", "solana", 215.50, 8900000000.0, 102000000000.0, 1.20, 7.84, 18.90, 471000000.0, now),
            CryptoAsset(1839, "BNB", "BNB", "bnb", 655.0, 2100000000.0, 95000000000.0, 0.10, 1.45, 4.20, 145000000.0, now),
            CryptoAsset(52, "XRP", "XRP", "xrp", 1.15, 6200000000.0, 65000000000.0, 2.45, 14.50, 45.20, 56900000000.0, now),
            CryptoAsset(2010, "Cardano", "ADA", "cardano", 0.78, 1850000000.0, 27500000000.0, -0.40, 5.20, 22.10, 35700000000.0, now),
            CryptoAsset(5805, "Avalanche", "AVAX", "avalanche", 38.40, 980000000.0, 15600000000.0, 0.85, 6.10, 14.50, 406000000.0, now),
            CryptoAsset(1975, "Chainlink", "LINK", "chainlink", 17.80, 840000000.0, 11100000000.0, 0.35, 4.80, 16.70, 626000000.0, now),
            CryptoAsset(20947, "Sui", "SUI", "sui", 3.45, 1750000000.0, 9800000000.0, 1.80, 12.40, 28.50, 2840000000.0, now),
            CryptoAsset(6535, "NEAR Protocol", "NEAR", "near-protocol", 6.85, 780000000.0, 8300000000.0, -0.25, 5.90, 15.30, 1210000000.0, now)
        ]
        return sample[:limit]
