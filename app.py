code
Python
import streamlit as st
import pandas as pd

# Konfigurasjon av sida
st.set_page_config(page_title="Eigedomsretts-leksikon", layout="wide")

# Lenke til ditt Google Sheet (ERSTATT DENNE MED DIN EIGEN CSV-LENKE)
# For å finne denne: Fil -> Del -> Publiser på nett -> Vel fana 'Svar' og format 'CSV'.
SHEET_URL = "DIN_PUBLISERTE_CSV_LENKE_HER"

def last_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        st.error("Kunne ikkje hente data. Sjekk at arket er publisert på nett.")
        return pd.DataFrame()

df = last_data()

# --- SIDEBAR NAVIGASJON ---
st.sidebar.title("Meny")
val = st.sidebar.radio("Gå til:", ["Leksikon", "Foreslå nytt", "Admin"])

# --- HOVUDSIDE: LEKSIKON ---
if val == "Leksikon":
    st.title("📜 Retthistorisk Leksikon")
    st.write("Søk i terminologi for eigedomsrettshistorie.")

    # Filter for berre godkjende ord
    if not df.empty and 'Status' in df.columns:
        godkjende = df[df['Status'] == 'Godkjent']
        
        # Søkefelt
        sok = st.text_input("Søk på ord (t.ex. Almenning)", "")
        
        # Filtrering basert på søk
        resultat = godkjende[godkjende['Term'].str.contains(sok, case=False, na=False)]

        for index, row in resultat.iterrows():
            with st.expander(f"**{row['Term']}** ({row['Tidsperiode']})"):
                st.write(f"**Definisjon:** {row['Definisjon']}")
                st.write(f"**Område:** {row['Geografi']}")
                st.write(f"**Kjelde:** {row['Kjelde']}")
                st.caption(f"Innsendt av: {row['Innsendt av']}")
    else:
        st.info("Leksikonet er førebels tomt eller status-kolonnen manglar.")

# --- SIDE: FORESLÅ NYTT ---
elif val == "Foreslå nytt":
    st.title("💡 Foreslå ny terminologi")
    st.write("Her kan du legge inn nye ord eller alternative forståingar.")
    st.info("Nye forslag vert synlege for alle så snart lærar har godkjent dei.")
    
    # Her legg du inn lenka til Google Forms-skjemaet ditt
    st.markdown("[Klikk her for å opne innsendingsskjemaet](DIN_GOOGLE_FORMS_LENKE_HER)")

# --- SIDE: ADMIN ---
elif val == "Admin":
    st.title("🔐 Administrator")
    passord = st.text_input("Skriv inn passord for å sjå ventande forslag:", type="password")
    
    if passord == "historie2024": # Du kan bytte ut dette passordet
        st.subheader("Forslag som ventar på godkjenning")
        if not df.empty:
            ventande = df[df['Status'] != 'Godkjent']
            st.dataframe(ventande)
            st.write("Gå til Google Sheets for å endre status til 'Godkjent'.")
        else:
            st.write("Ingen ventande forslag.")
