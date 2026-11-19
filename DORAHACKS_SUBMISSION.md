# 🏆 DoraHacks Hackathon Submission Package
## Build with CMC: API Hackathon (Round 2)

Copy and paste the sections below directly into the **DoraHacks Project Submission Form**:

---

### 1. Basic Information
* **Project Name:** CMC-OmniAgent
* **Tagline / One-Liner:** Autonomous Multi-Agent Crypto Intelligence, Quantitative Risk & Alpha Copilot powered by CoinMarketCap API.
* **Track:** AI Agents and Automation
* **GitHub Repository:** [https://github.com/givemehat/cmc-omniagent](https://github.com/givemehat/cmc-omniagent)
* **Demo / Local URL:** `http://localhost:8000`
* **Lead Developer:** Rajnish Singh (`@givemehat`)
* **Contact Email:** `245ucs155@gbu.ac.in`
* **Payout Wallet (Base / EVM):** `0xFFE286685fB8C12c3d59728DA29E44a637C22d3d`

---

### 2. Project Description & Problem Statement
Crypto traders and research analysts face significant challenges:
1. **Information Fragmentation:** Critical data (volume surges, dominance shifts, order book churn) is scattered across disparate dashboards.
2. **Execution Latency:** By the time a human trader notices a 15% volume surge or an abnormal volume-to-market-cap ratio, the optimal trade window has passed.
3. **Emotional Bias:** Traders lack quantitative multi-factor discipline, often confusing high-volatility traps with sustainable breakouts.

### 3. Solution & Innovation
**CMC-OmniAgent** solves this by introducing a decentralized team of 4 autonomous software agents orchestrating live data from the **CoinMarketCap Developer API**:
* **Market Scout Agent:** Automatically flags volume anomalies (Volume/MCap > 12%), breakout velocity, and accumulation ranges with deterministic confidence scores.
* **Volatility & Risk Sentinel:** Evaluates tail volatility, liquidity depth, and downside drawdown vulnerability.
* **Quantitative Alpha Synthesizer:** Computes a composite multi-factor score:
  `Composite Alpha = (0.40 * Momentum) + (0.35 * Volume Quality) + (0.25 * Stability)`
  and issues actionable institutional ratings (Strong Overweight, Accumulate on Dips, Neutral, Underweight).
* **AI Copilot Agent:** Context-aware natural language assistant allowing users to query live token metrics, compare assets (e.g. *SOL vs ETH*), and inspect macro market health.

### 4. CoinMarketCap API Utilization
CMC-OmniAgent leverages:
* `GET /v1/cryptocurrency/listings/latest` (Universe prices, 24h volume, market cap, percentage changes across multiple windows).
* `GET /v1/global-metrics/quotes/latest` (Global market capitalization, 24h total volume, Bitcoin & Ethereum dominance).
* `GET /v1/cryptocurrency/quotes/latest` (Single and multi-asset real-time telemetry).

### 5. Tech Stack
* **Language:** Python 3.10+ (Standard Library + AsyncIO)
* **API Engine:** FastAPI / Uvicorn
* **Frontend:** Responsive Dark-Mode Terminal UI (Tailwind CSS, Vanilla JavaScript, Lucide Icons)
* **Testing:** Python `unittest` suite (100% test pass rate)

### 6. Roadmap
* **Phase 1 (Current):** Autonomous scanning, quantitative alpha synthesis, multi-factor scoring, and interactive web/CLI dashboard.
* **Phase 2:** Automated Telegram & Discord bot alerts triggered on high-confidence breakout signals.
* **Phase 3:** On-chain execution integration with DEX aggregators (Uniswap, Raydium) via smart contract vaults.
