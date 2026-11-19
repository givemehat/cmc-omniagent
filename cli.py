import asyncio
import sys
from cmc_agent import OmniAgentPipeline

async def main():
    print("\n" + "="*70)
    print(" ⚡ CMC-OmniAgent: Autonomous Crypto Intelligence & Alpha Scanner")
    print(" Built for CoinMarketCap API Hackathon Round 2 on DoraHacks")
    print("="*70 + "\n")

    pipeline = OmniAgentPipeline()
    print("🔍 Fetching live CoinMarketCap market feeds and initiating agent cycle...\n")
    data = await pipeline.execute_cycle(limit=50)

    # 1. Global Metrics
    gm = data["global_metrics"]
    print(f"🌐 [GLOBAL TELEMETRY]")
    print(f"   • Total Market Cap : ${gm['total_market_cap']:,.0f}")
    print(f"   • 24h Global Volume: ${gm['total_volume_24h']:,.0f}")
    print(f"   • BTC Dominance    : {gm['btc_dominance']:.1f}%")
    print(f"   • ETH Dominance    : {gm['eth_dominance']:.1f}%\n")

    # 2. Autonomous Signals
    signals = data["signals"]
    print(f"📡 [AUTONOMOUS SIGNALS DETECTED ({len(signals)})]")
    for s in signals:
        print(f"   [{s['signal_type']}] {s['token_symbol']} (Conf: {int(s['confidence']*100)}%) - {s['headline']}")
        print(f"     ↳ {s['rationale']}\n")

    # 3. Top Alpha Rankings
    rankings = data["alpha_rankings"][:10]
    print("🏆 [QUANTITATIVE ALPHA LEADERBOARD (Top 10)]")
    print(f"   {'Rank':<5} {'Symbol':<8} {'Price ($)':<12} {'Alpha Score':<14} {'Risk Level':<12} {'Recommendation'}")
    print("   " + "-"*65)
    for i, r in enumerate(rankings, 1):
        price_str = f"${r['price']:,.2f}"
        print(f"   #{i:<4} {r['symbol']:<8} {price_str:<12} {r['alpha_score']:<14} {r['risk_level']:<12} {r['recommendation']}")

    print("\n" + "="*70)
    print(" ✅ Scan complete. Run `python app.py` to launch the interactive Web Dashboard.")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
