import streamlit as st
import pandas as pd

# Konfigurasjon
st.set_page_config(page_title="Eigedomsretts-leksikon", layout="wide")

# LENKER - Hugs å byte ut desse med dine eigne!
# For å få CSV-lenka: Google Sheets -> Fil -> Del -> Publiser på Internett -> Vel 'Svar' og '.csv'
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/DIN_ID_HER/pub?gid=DIN_GID_HER&single=true&output=csv"
FORMS_URL = "https://forms.gle/DIN_SKJEMA_LENKE"

def last_data():
    try:
        # Vi legg til ein tidsstempel-parameter for å unngå caching-problem i nettlesaren
        df = pd.read_csv(f"{SHEET_URL}&cache={pd.Timestamp.now().timestamp()}")
        return df
    except Exception as e:
        return pd.DataFrame()

df = last_data()

# --- MENY I MARGINEN ---
with st.sidebar:
    st.title("Navigasjon")
    val = st.radio("Vel side:", ["Leksikon", "Foreslå nytt", "Admin"])
    st.divider()
    st.info("Dette er eit verktøy for å lære terminologi i eigedomsrettshistorie.")

# --- SIDE 1: LEKSIKON ---
if val == "Leksikon":
    st.title("📜 Retthistorisk Leksikon")
    
    if df.empty:
        st.warning("Fann ingen data. Sjekk at CSV-lenka i koden er rett og at arket er publisert.")
    else:
        # Vi sjekkar kva kolonnar som faktisk finst (Google Sheets kan variere litt)
        # Vi antar: B=Term, C=Definisjon, D=Tid, E=Geografi, F=Kjelde, H=Status
        
        # Sørg for at vi berre viser godkjende
        if 'Status' in df.columns:
            godkjende = df[df['Status'].str.contains('Godkjent', na=False, case=False)]
        else:
            godkjende = df # Viss statuskolonnen manglar, viser vi alt førebels

        sok = st.text_input("🔍 Søk i terminologien:", placeholder="T.ex. Skyldmark...")

        if not godkjende.empty:
            # Filtermekanisme
            resultat = godkjende[godkjende.iloc[:, 1].str.contains(sok, case=False, na=False)] # Sjekkar kolonne B (Term)

            for _, row in resultat.iterrows():
                with st.expander(f"**{row.iloc[1]}**"): # Viser Term
                    st.write(f"**Definisjon:** {row.iloc[2]}")
                    st.write(f"**Periode:** {row.iloc[3]} | **Område:** {row.iloc[4]}")
                    st.write(f"**Kjelde:** {row.iloc[5]}")
        else:
            st.info("Ingen ord er godkjende i databasen ennå.")

# --- SIDE 2: FORESLÅ NYTT ---
elif val == "Foreslå nytt":
    st.title("💡 Bidra til leksikonet")
    st.write("Klikk på knappen under for å sende inn eit forslag til ein term eller ei alternativ forståing.")
    st.link_button("Opne innsendingsskjema", FORMS_URL)
    st.caption("Alle forslag vert vurderte av administrator før dei vert publiserte.")

# --- SIDE 3: ADMIN ---
elif val == "Admin":
    st.title("🔐 Admin-panel")
    passord = st.text_input("Passord:", type="password")
    
    if passord == "historie2024":
        if not df.empty:
            st.subheader("Alle registreringar (inkludert ventande)")
            st.dataframe(df)
            st.write("Endre status til 'Godkjent' i Google Sheets for å publisere.")
        else:
            st.error("Ingen data fann.")
