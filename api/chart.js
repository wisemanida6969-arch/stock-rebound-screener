/**
 * Vercel Serverless — Yahoo 차트 JSON 그대로 전달 (CORS 허용)
 * GET /api/chart?ticker=AAPL&range=1d&interval=1m
 */
module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();

  const rawT = String(req.query.ticker || "AAPL");
  const ticker = rawT.replace(/[^A-Za-z0-9^.^\-]/g, "").slice(0, 16) || "AAPL";
  const range = String(req.query.range || "1d").replace(/[^0-9a-z]/gi, "").slice(0, 10) || "1d";
  const interval = String(req.query.interval || "1m").replace(/[^0-9a-z]/gi, "").slice(0, 5) || "1m";

  const yahoo =
    "https://query1.finance.yahoo.com/v8/finance/chart/" +
    encodeURIComponent(ticker) +
    "?range=" +
    encodeURIComponent(range) +
    "&interval=" +
    encodeURIComponent(interval);

  try {
    const r = await fetch(yahoo, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (compatible; ChartProxy/1.0)",
        Accept: "application/json,text/plain,*/*",
      },
    });
    const text = await r.text();
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.status(r.ok ? 200 : 502).send(text);
  } catch (e) {
    res.status(500).json({ error: String(e && e.message) });
  }
};
