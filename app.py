import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Asistente de activos financieros", page_icon="📈")

st.title("📈 Asistente de Activos Financieros")
st.write("Ingresá un ticker para obtener información básica del activo.")
st.caption("Uso educativo. No constituye asesoramiento financiero profesional.")

ticker_input = st.text_input("Ticker", value="AAPL").strip().upper()

descripciones = {
    "AAPL": "Apple Inc. es una empresa tecnológica de Estados Unidos.",
    "MSFT": "Microsoft es una empresa tecnológica enfocada en software, nube y productividad.",
    "TSLA": "Tesla es una empresa vinculada a autos eléctricos, energía y tecnología.",
    "SPY": "SPY es un ETF que replica el índice S&P 500.",
    "VOO": "VOO es un ETF que sigue al S&P 500.",
    "QQQ": "QQQ es un ETF vinculado al Nasdaq-100."
}

def explicar_activo(ticker: str, info: dict) -> str:
    if ticker in descripciones:
        return descripciones[ticker]

    quote_type = str(info.get("quoteType", "")).lower()
    sector = info.get("sector")
    industry = info.get("industry")

    if quote_type == "etf":
        return f"{ticker} es un ETF. Un ETF es un fondo que cotiza en bolsa y suele seguir un índice o una cesta de activos."
    if quote_type == "equity":
        if sector and industry:
            return f"{ticker} es una acción de una empresa del sector {sector}, industria {industry}."
        if sector:
            return f"{ticker} es una acción de una empresa del sector {sector}."
        return f"{ticker} es una acción de una empresa que cotiza en bolsa."

    return f"{ticker} es un activo financiero cotizado. Esta respuesta es educativa e informativa."

if st.button("Consultar"):
    if not ticker_input:
        st.warning("Ingresá un ticker.")
    else:
        try:
            activo = yf.Ticker(ticker_input)
            info = activo.info

            precio = info.get("currentPrice") or info.get("regularMarketPrice")
            cambio = info.get("regularMarketChangePercent")
            nombre = info.get("shortName") or info.get("longName") or ticker_input
            moneda = info.get("currency", "")

            if precio is None:
                st.error("No encontré datos para ese ticker.")
            else:
                st.subheader(nombre)
                st.metric(
                    label=f"Precio actual ({moneda})" if moneda else "Precio actual",
                    value=f"{precio}",
                    delta=f"{cambio:.2f}%" if isinstance(cambio, (int, float)) else None
                )

                st.write("### Explicación")
                st.write(explicar_activo(ticker_input, info))

                st.write("### Conceptos útiles")
                st.write("- **Acción**: representa una parte de la propiedad de una empresa.")
                st.write("- **ETF**: fondo que cotiza en bolsa y suele seguir un índice.")
                st.write("- **Riesgo**: posibilidad de que el valor de la inversión baje.")
                st.write("- **Volatilidad**: cuánto cambia el precio de un activo en el tiempo.")

                st.info("La información mostrada es de carácter educativo y no sustituye asesoramiento financiero profesional.")
        except Exception as e:
            st.error(f"Ocurrió un error al consultar el ticker: {e}")