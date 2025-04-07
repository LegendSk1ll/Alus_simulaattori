import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Aluksen Simulaattori", layout="wide")

# --- Otsikko ja tyyli ---
st.markdown("""
    <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
        }
        .status-box {
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-font'>🛳️ Aluksen Sensorisimulaattori</div>", unsafe_allow_html=True)

# --- Alustetaan historia ---
if 'historia' not in st.session_state:
    st.session_state.historia = []

# --- Simuloidaan sensoridata ---
moottorin_lampotila = random.uniform(50, 120)
polttoainetaso = random.uniform(0, 100)
nopeus = random.uniform(0, 30)

# --- Tallennetaan historia ---
st.session_state.historia.append({
    'aika': datetime.now().strftime("%H:%M:%S"),
    'lampo': moottorin_lampotila,
    'polttoaine': polttoainetaso,
    'nopeus': nopeus
})

# --- Tilamääritykset ---
def tila_vari(arvo, vihrea, keltainen):
    if arvo < vihrea:
        return '🟢', 'success'
    elif arvo < keltainen:
        return '🟡', 'warning'
    else:
        return '🔴', 'error'

# --- UI elementit riveissä ---
col1, col2, col3 = st.columns(3)

# Moottorin lämpötila
emoji, tyyppi = tila_vari(moottorin_lampotila, 90, 100)
with col1:
    st.metric("Moottorin lämpötila", f"{moottorin_lampotila:.1f} °C", delta=None)
    getattr(st, tyyppi)(f"{emoji} Tila")

# Polttoainetaso
emoji, tyyppi = tila_vari(100 - polttoainetaso, 50, 85)
with col2:
    st.metric("Polttoainetaso", f"{polttoainetaso:.1f} %")
    getattr(st, tyyppi)(f"{emoji} Tila")

# Nopeus
emoji, tyyppi = tila_vari(nopeus, 5, 2)
with col3:
    st.metric("Nopeus", f"{nopeus:.1f} kn")
    getattr(st, tyyppi)(f"{emoji} Tila")

# --- Klikattavat ratkaisut ---
st.divider()
st.subheader("🔧 Ehdotetut ratkaisut")

if moottorin_lampotila > 100:
    if st.button("Näytä ratkaisu: Moottorin ylikuumeneminen"):
        st.info("Tarkista jäähdytysjärjestelmä. Varmista, että tuuletus toimii ja nesteet ovat kunnossa.")

if polttoainetaso < 15:
    if st.button("Näytä ratkaisu: Matala polttoainetaso"):
        st.info("Suunnittele välitön tankkaus. Vältä pitkiä matkoja ennen tankkausta.")

# --- Historia ---
st.divider()
st.subheader("📜 Sensorihistoria")
with st.expander("Näytä/ Piilota historia"):
    for rivi in st.session_state.historia[::-1][-10:]:
        st.write(f"{rivi['aika']} | Lämpötila: {rivi['lampo']:.1f}°C | Polttoaine: {rivi['polttoaine']:.1f}% | Nopeus: {rivi['nopeus']:.1f} kn")
