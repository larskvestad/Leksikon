import streamlit as st
import pandas as pd

# Konfigurasjon
st.set_page_config(page_title="Eigedomsretts-leksikon", layout="wide")

# LENKER - Hugs å byte ut desse med dine eigne!
# For å få CSV-lenka: Google Sheets -> Fil -> Del -> Publiser på Internett -> Vel 'Svar' og '.csv'
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3_o1k4DyG3BvBL6OI_WbQVV8BwCeDGABEg5BzeKvuGD0q1a3ZzK-nv7XH9FwnkGJZs0lRSbOIbLOj/pub?gid=1953725999&single=true&output=csv"
FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSft-iCsGIh5aagM_9EuFebWRXo51dKWQUwI40A9KBG7WdXIIA/viewform?usp=header"

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

# --- HOVUDSIDE: LEKSIKON ---
if val == "Leksikon":
    st.title("📜 Retthistorisk Leksikon")
    
    if df.empty:
        st.warning("Fann ingen data. Sjekk at CSV-lenka er rett.")
    else:
        # VIKTIG: Vi vaskar kolonnenamna for å fjerne mellomrom og rart rusk
        df.columns = [c.strip() for c in df.columns]
        
        # Her definerer vi kva kolonnar vi leitar etter. 
        # Sjekk at desse namna er IDENTISKE med overskriftene i Google Sheets!
        term_col = 'Term'
        def_col = 'Forståing/Definisjon'
        tid_col = 'Tidsperiode'
        sted_col = 'Geografisk område'
        kjelde_col = 'Kjelde'
        status_col = 'Status'

        # Sjekk om Status-kolonnen finst, viss ikkje viser vi alt
        if status_col in df.columns:
            godkjende = df[df[status_col].str.contains('Godkjent', na=False, case=False)]
        else:
            st.error(f"Fann ikkje kolonnen '{status_col}'. Sjekk overskriftene i Sheets.")
            godkjende = df

        sok = st.text_input("🔍 Søk i terminologien:", placeholder="T.ex. Skyldmark...")

        if not godkjende.empty:
            # Filtrer basert på søk i Term-kolonnen
            resultat = godkjende[godkjende[term_col].str.contains(sok, case=False, na=False)]

            for _, row in resultat.iterrows():
                with st.expander(f"**{row[term_col]}**"):
                    st.write(f"**Definisjon:** {row[def_col]}")
                    st.write(f"**Periode:** {row[tid_col]} | **Område:** {row[sted_col]}")
                    st.write(f"**Kjelde:** {row[kjelde_col]}")
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
