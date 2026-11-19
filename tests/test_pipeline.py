import unittest
from cmc_agent import OmniAgentPipeline, CoinMarketCapClient
from cmc_agent.models import CryptoAsset, GlobalMarketMetrics

class TestOmniAgentPipeline(unittest.IsolatedAsyncioTestCase):

    async def test_client_listings_and_metrics(self):
        client = CoinMarketCapClient()
        listings = await client.get_latest_listings(limit=10)
        self.assertGreater(len(listings), 0)
        self.assertEqual(listings[0].symbol, "BTC")
        self.assertGreater(listings[0].price_usd, 0)
        self.assertGreater(listings[0].vol_to_mcap_ratio, 0)

        gm = await client.get_global_metrics()
        self.assertGreater(gm.total_market_cap_usd, 0)
        self.assertGreater(gm.btc_dominance, 0)

    async def test_multi_agent_pipeline_cycle(self):
        pipeline = OmniAgentPipeline()
        result = await pipeline.execute_cycle(limit=10)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertGreater(result["assets_tracked"], 0)
        self.assertIn("global_metrics", result)
        self.assertIn("signals", result)
        self.assertIn("alpha_rankings", result)
        self.assertGreater(len(result["alpha_rankings"]), 0)

        top_pick = result["alpha_rankings"][0]
        self.assertIn("symbol", top_pick)
        self.assertIn("alpha_score", top_pick)
        self.assertGreaterEqual(top_pick["alpha_score"], 0)

    def test_copilot_agent_queries(self):
        pipeline = OmniAgentPipeline()
        pipeline._cached_assets = [
            CryptoAsset(1, "Bitcoin", "BTC", "bitcoin", 94000.0, 4e10, 1.8e12, 0.5, 3.2, 8.1, 1.9e7, "")
        ]
        pipeline._cached_global = GlobalMarketMetrics(3.2e12, 1.4e11, 58.4, 14.2, 10000, 700)
        pipeline._cached_signals = []

        # Query 1: Overview
        ans_macro = pipeline.chat_with_copilot("What is the current market overview and BTC dominance?")
        self.assertIn("Global Crypto Market Brief", ans_macro["response"])
        self.assertEqual(ans_macro["intent"], "GLOBAL_MARKET_OVERVIEW")

        # Query 2: Asset specific
        ans_asset = pipeline.chat_with_copilot("Give me an analysis on BTC")
        self.assertIn("Bitcoin (BTC)", ans_asset["response"])
        self.assertEqual(ans_asset["intent"], "ASSET_DEEP_DIVE")

if __name__ == "__main__":
    unittest.main()
