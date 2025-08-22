import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="YT Analyzer", page_icon="📈")

st.title("📊 Yield Token Analyzer")

implied_apy = st.number_input("Implied APY (e.g. 13.25% → 0.1325)", format="%.6f")
underlying_apy = st.number_input("Underlying APY (e.g. 13.25% → 0.1325)", format="%.6f")
pt_price = st.number_input("Principal Token Price (PT)", format="%.6f")
d = st.number_input("Days Until Maturity", min_value=1, max_value=365, step=1)
yt_now = st.number_input("Yield Token Current Price (YT)", format="%.6f")

if all(x > 0 for x in [implied_apy, underlying_apy, pt_price, d, yt_now]):
    fair_yt = pt_price * ((implied_apy + 1) ** (d/365) - 1)
    percentage = abs((fair_yt / yt_now - 1) * 100)
    percentage_apy = abs((implied_apy / underlying_apy - 1) * 100)

    st.markdown(f"### 🎯 YT Fair Price: `${fair_yt:.4f}`")
    st.markdown(f"- Difference from current price: `{percentage:.2f}%`")
    st.markdown(f"- Implied vs Underlying APY difference: `{percentage_apy:.2f}%`")

    st.divider()

    if (implied_apy > underlying_apy) and (yt_now > fair_yt) and percentage_apy > 1 and percentage > 1:
        st.warning("🔻 Implied APY is unattractive and YT is expensive.")
        st.error("💡 SHORT YIELD → Consider buying PT")
    elif (implied_apy < underlying_apy) and (yt_now < fair_yt) and percentage_apy > 1 and percentage > 1:
        st.success("✅ Implied APY is attractive and YT is cheap.")
        st.info("💡 LONG YIELD → Consider buying YT")
    elif abs(implied_apy - underlying_apy) < 1e-5 and abs(yt_now - fair_yt) < 1e-5:
        st.info("⚖️ Fair price. No significant deviation.")
    else:
        st.warning("😐 Mixed or weak signals.")
        if (implied_apy < underlying_apy) and (yt_now > fair_yt) and percentage_apy > 1 and percentage > 1:
            st.info(f"Implied APY is attractive (`{percentage_apy:.2f}%` lower than Underlying APY) but YT's price is expensive (`{percentage:.2f}%` higher than its fair price based on the maturity curve).")
        elif (implied_apy > underlying_apy) and (yt_now < fair_yt) and percentage_apy > 1 and percentage > 1:
            st.info(f"Implied APY is unattractive (`{percentage_apy:.2f}%` higher than Underlying APY) but YT's price is cheap (`{percentage:.2f}%` lower than its fair price based on the maturity curve).")
        
        if percentage < 1:
            if implied_apy > underlying_apy:
                st.info(f"Implied APY is unattractive (`{percentage_apy:.2f}%` higher than Underlying APY), but YT price is fair.")
            elif implied_apy < underlying_apy:
                st.info(f"Implied APY is attractive (`{percentage_apy:.2f}%` lower than Underlying APY), but YT price is fair.")
        if percentage_apy < 1:
            if yt_now < fair_yt:
                st.info(f"Implied APY is nearly equal to Underlying APY, but YT price is cheap (`{percentage:.2f}%` lower than its fair price based on the maturity curve).")
            elif yt_now > fair_yt:
                st.info(f"Implied APY is nearly equal to Underlying APY, but YT price is expensive (`{percentage:.2f}%` higher than its fair price based on the maturity curve).")

    st.divider()

    # -------------------------
    # Gráfico do preço justo
    # -------------------------
    n = 365  # capitalização diária
    dias_since = st.number_input("Days Since Launch", min_value=1, max_value=365, step=1)
    dias = np.arange(0, d + dias_since + 1)
    
    # usa underlying como yield "fundamental"
    i = (1 + underlying_apy)**(1/n) - 1
    fair_curve = 1 - (1 + i)**(-dias)
    
    df = pd.DataFrame({
        "Dia": dias,
        "Preço Justo (Underlying APY)": fair_curve,
        "Preço Atual YT": [yt_now] * len(dias)
    }).set_index("Dia")
    
    st.subheader("📉 Curva de Preço Justo do YT")
    st.line_chart(df)

    qt = st.number_input("How many YT tokens are you buying?", min_value=0.0, step=1.0, format="%.2f")
    if qt > 0:
        profit = (underlying_apy * qt) * d/365
        cost = qt * yt_now

        st.markdown(f"### 💰 At maturity, your investment will be worth: `{profit:.2f}`")

st.divider()

st.link_button("Follow @zuka_defi on X", "https://x.com/zuka_defi")

        



