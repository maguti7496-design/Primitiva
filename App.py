import streamlit as st
import pandas as pd
from collections import Counter
import random
from datetime import datetime

st.set_page_config(page_title="Primitiva Analyzer", layout="centered")
st.title("🎰 Analizador Estadístico La Primitiva")
st.markdown("**Análisis automático de +15 años** • Sugerencias con valor estadístico")

@st.cache_data(ttl=3600)  # Cachea 1 hora
def load_data():
    with st.spinner("📥 Cargando histórico completo..."):
        try:
            url1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTov1BuA0nkVGTS48arpPFkc9cG7B40Xi3BfY6iqcWTrMwCBg5b50-WwvnvaR6mxvFHbDBtYFKg5IsJ/pub?gid=0&single=true&output=csv"
            url2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTov1BuA0nkVGTS48arpPFkc9cG7B40Xi3BfY6iqcWTrMwCBg5b50-WwvnvaR6mxvFHbDBtYFKg5IsJ/pub?gid=1&single=true&output=csv"
            df1 = pd.read_csv(url1)
            df2 = pd.read_csv(url2)
            df = pd.concat([df1, df2], ignore_index=True)
            st.success(f"✅ {len(df):,} sorteos cargados")
            return df
        except:
            st.error("Error al cargar datos. Inténtalo más tarde.")
            return None

df = load_data()

if df is not None:
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        years = st.slider("Años a analizar", 5, 25, 15)
    with col2:
        n_combos = st.slider("Combinaciones a generar", 5, 20, 10)

    # Preprocesado
    date_col = next((col for col in df.columns if 'fecha' in str(col).lower() or 'date' in str(col).lower()), None)
    num_cols = [col for col in df.columns if any(str(i) in str(col).lower() for i in range(1,7))]

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        cutoff = datetime.now() - pd.Timedelta(days=365 * years)
        recent = df[df[date_col] >= cutoff].copy()
    else:
        recent = df.tail(int(len(df) * 0.6))

    # Análisis
    all_nums = []
    for col in num_cols[:6]:
        nums = pd.to_numeric(recent[col], errors='coerce').dropna().astype(int)
        all_nums.extend(nums.tolist())

    freq = Counter(all_nums)
    total = len(recent)

    st.subheader(f"🔥 Estadísticas últimos {years} años ({total} sorteos)")

    col_hot, col_cold = st.columns(2)
    with col_hot:
        st.write("**🏆 Números más frecuentes (Hot)**")
        hot = freq.most_common(15)
        for n, c in hot:
            st.write(f"{n:2d} → {c} veces ({c/total*100:.1f}%)")

    with col_cold:
        st.write("**❄️ Números menos frecuentes**")
        cold = freq.most_common()[-10:]
        for n, c in cold:
            st.write(f"{n:2d} → {c} veces")

    # Generar combinaciones
    if st.button("🎲 Generar combinaciones recomendadas", type="primary"):
        st.subheader("📊 Tus sugerencias estadísticas")
        hot_numbers = [n for n, _ in freq.most_common(35)]
        
        for i in range(n_combos):
            combo = sorted(random.sample(hot_numbers, 6))
            reintegro = random.randint(0, 9)
            st.success(f"**{i+1:2d}.** {combo}  +  **Reintegro: {reintegro}**")

    st.info("💡 Recuerda: Cada sorteo es aleatorio. Este análisis solo ayuda a elegir con criterio estadístico histórico.")

    st.caption("Datos de lotoideas.com • Actualizados automáticamente")
