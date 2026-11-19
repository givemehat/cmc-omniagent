async function runCycle() {
    try {
        const res = await fetch('/api/cycle?limit=50');
        const data = await res.json();
        renderDashboard(data);
    } catch (err) {
        console.error("Cycle failed", err);
    }
}

function renderDashboard(data) {
    // 1. Global Metrics
    const gm = data.global_metrics;
    document.getElementById('totalMcap').innerText = '$' + (gm.total_market_cap / 1e12).toFixed(2) + 'T';
    document.getElementById('totalVol').innerText = '$' + (gm.total_volume_24h / 1e9).toFixed(1) + 'B';
    document.getElementById('btcDom').innerText = gm.btc_dominance.toFixed(1) + '%';
    document.getElementById('ethDom').innerText = gm.eth_dominance.toFixed(1) + '%';

    // 2. Signals
    const signals = data.signals || [];
    document.getElementById('signalCountBadge').innerText = `${signals.length} Signals`;
    const sc = document.getElementById('signalsContainer');
    sc.innerHTML = '';

    if (signals.length === 0) {
        sc.innerHTML = '<div class="text-center py-10 text-gray-500 text-xs">No active breakout anomalies in current cycle.</div>';
    } else {
        signals.forEach(s => {
            const card = document.createElement('div');
            card.className = "p-3.5 rounded-xl bg-cmcCard border border-cmcBorder hover:border-gray-700 transition flex flex-col space-y-2";
            
            let badgeColor = "bg-blue-500/10 text-blue-400 border-blue-500/20";
            if (s.signal_type === "BREAKOUT") badgeColor = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
            if (s.signal_type === "UNUSUAL_VOLUME") badgeColor = "bg-amber-500/10 text-amber-400 border-amber-500/20";

            card.innerHTML = `
                <div class="flex items-center justify-between">
                    <span class="font-bold text-sm text-white">${s.token_symbol}</span>
                    <span class="text-[10px] uppercase font-bold px-2 py-0.5 rounded border ${badgeColor}">${s.signal_type.replace('_', ' ')}</span>
                </div>
                <p class="text-xs text-gray-200 font-semibold">${s.headline}</p>
                <p class="text-[11px] text-gray-400 leading-relaxed">${s.rationale}</p>
                <div class="flex items-center justify-between text-[10px] text-gray-500 pt-1 border-t border-cmcBorder/60">
                    <span>Confidence: <strong class="text-white">${Math.round(s.confidence * 100)}%</strong></span>
                    <span>${s.timestamp.split(' ')[1] || 'Just now'}</span>
                </div>
            `;
            sc.appendChild(card);
        });
    }

    // 3. Alpha Table
    const tableBody = document.getElementById('alphaTableBody');
    tableBody.innerHTML = '';
    (data.alpha_rankings || []).slice(0, 15).forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-gray-800/40 transition";

        let riskBadge = "text-emerald-400 bg-emerald-500/10";
        if (item.risk_level === "HIGH") riskBadge = "text-rose-400 bg-rose-500/10";
        if (item.risk_level === "MODERATE") riskBadge = "text-amber-400 bg-amber-500/10";

        tr.innerHTML = `
            <td class="p-3">
                <div class="flex items-center space-x-2">
                    <span class="text-gray-500 text-xs">#${index + 1}</span>
                    <span class="font-bold text-white">${item.symbol}</span>
                    <span class="text-gray-400 text-[11px] truncate max-w-[80px]">${item.name}</span>
                </div>
            </td>
            <td class="p-3 text-white font-mono">$${item.price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 4})}</td>
            <td class="p-3">
                <span class="font-bold text-cmcBlue">${item.alpha_score}</span>
            </td>
            <td class="p-3">
                <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${riskBadge}">${item.risk_level}</span>
            </td>
            <td class="p-3">
                <button onclick="askCopilot('Deep dive analysis on ${item.symbol}')" class="text-xs text-cmcBlue hover:underline">Inspect</button>
            </td>
        `;
        tableBody.appendChild(tr);
    });
}

async function handleChat(e) {
    e.preventDefault();
    const input = document.getElementById('chatInput');
    const query = input.value.trim();
    if (!query) return;

    input.value = '';
    const container = document.getElementById('chatMessages');

    // Append user message
    const uMsg = document.createElement('div');
    uMsg.className = "p-2.5 rounded-lg bg-cmcBlue/15 border border-cmcBlue/30 text-white ml-4 text-xs font-medium";
    uMsg.innerText = query;
    container.appendChild(uMsg);
    container.scrollTop = container.scrollHeight;

    // Loading indicator
    const loadMsg = document.createElement('div');
    loadMsg.className = "p-2.5 rounded-lg bg-gray-900 border border-cmcBorder text-gray-400 mr-4 text-xs";
    loadMsg.innerText = "Synthesizing CoinMarketCap data...";
    container.appendChild(loadMsg);

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query})
        });
        const ans = await res.json();
        loadMsg.innerHTML = ans.response.replace(/\n/g, '<br/>');
        loadMsg.className = "p-2.5 rounded-lg bg-gray-900/90 border border-cmcBorder text-gray-200 mr-4 text-xs leading-relaxed";
    } catch (err) {
        loadMsg.innerText = "Error analyzing query. Please retry.";
    }
    container.scrollTop = container.scrollHeight;
}

function askCopilot(text) {
    document.getElementById('chatInput').value = text;
    document.querySelector('form').dispatchEvent(new Event('submit'));
}

// Initial load
window.addEventListener('DOMContentLoaded', runCycle);
