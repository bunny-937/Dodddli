
import yfinance as yf
import pandas as pd
import streamlit as st

def main():
    st.set_page_config(page_title="Nifty 50 Stock Screener", layout="wide")
    st.title("📈 Nifty 50 Stock Screener (Above 50-day MA)")
    st.markdown("This app shows **Nifty 50 stocks trading above their 50-day Moving Average (MA)**.")

    symbols = [
        "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK", "LT", "BHARTIARTL", "HINDUNILVR",
        "ITC", "BAJFINANCE", "AXISBANK", "ASIANPAINT", "HCLTECH", "MARUTI", "NESTLEIND", "ULTRACEMCO", "WIPRO",
        "POWERGRID", "NTPC", "SUNPHARMA", "TITAN", "HDFCLIFE", "DIVISLAB", "TECHM", "JSWSTEEL", "GRASIM", "ONGC",
        "COALINDIA", "ADANIENT", "ADANIPORTS", "TATASTEEL", "SBILIFE", "BPCL", "HEROMOTOCO", "BAJAJFINSV",
        "BRITANNIA", "CIPLA", "EICHERMOT", "DRREDDY", "INDUSINDBK", "SHREECEM", "HINDALCO", "BAJAJ-AUTO",
        "TATACONSUM", "UPL", "HDFCAMC", "M&M", "ICICIPRULI"
    ]

    results = []

    with st.spinner("Fetching data..."):
        for symbol in symbols:
            try:
                data = yf.download(symbol + ".NS", period="3mo", interval="1d", progress=False)
                if data.empty or len(data) < 50:
                    continue
                data['50ma'] = data['Close'].rolling(window=50).mean()
                current_price = data['Close'].iloc[-1]
                current_50ma = data['50ma'].iloc[-1]

                if current_price > current_50ma:
                    results.append({
                        "Symbol": symbol,
                        "Current Price (₹)": round(current_price, 2),
                        "50-Day MA (₹)": round(current_50ma, 2)
                    })
            except:
                continue

    if results:
        df = pd.DataFrame(results).sort_values("Current Price (₹)", ascending=False)
        st.success(f"✅ {len(df)} stocks are trading above their 50-day MA.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No stocks are currently above their 50-day MA.")

main()
