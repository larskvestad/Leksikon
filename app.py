import streamlit as st
import pandas as pd

# 1. OPPSETT
st.set_page_config(page_title="Eigedomsretts-leksikon", layout="wide")

# LENKER - Hugs å sjekke at desse er rett
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3_o1k4DyG3BvBL6OI_WbQVV8BwCeDGABEg5BzeKvuGD0q1a3ZzK-nv7XH9FwnkGJZs0lRSbOIbLOj/pub?gid=1953725999&single=true&output=csv"
FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSft-iCsGIh5aagM_9EuFebWRXo51dKWQUwI40A9KBG7WdXIIA/viewform?usp=header"

# 2. FUNKSJON FOR Å HENTE DATA
def last_data():
    try:
        # Hentar data og tvingar pandas til å lese alt som tekst for å unngå feil
        df = pd.read_csv(f"{SHEET_URL}&cache={pd.Timestamp.now().timestamp()}", dtype=str)
        # Fjernar ekstra mellomrom i kolonnenamn
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Kunne ikkje hente data frå Google Sheets. Feil: {e}")
        return pd.DataFrame()

df = last_data()

# 3. DEFINER KOLONNENAMN (Må vere like som i Sheets)
TERM_COL = 'Term'
DEF_COL = 'Forståing/Definisjon'
TID_COL = 'Tidsperiode'
STED_COL = 'Geografisk område'
KJELDE_COL = 'Kjelde'
STATUS_COL = 'Status'

# 4. MENY
with st.sidebar:
    st.title("Navigasjon")
    val = st.radio("Vel side:", ["Leksikon", "Foreslå nytt", "Admin"])

# --- SIDE: LEKSIKON ---
if val == "Leksikon":
    st.title("📜 Retthistorisk Leksikon")
    
    if df.empty:
        st.info("Leksikonet er førebels tomt.")
    else:
        # Sjekk kva kolonnar som faktisk finst i Sheets
        eksisterande_kolonnar = df.columns.tolist()
        
        # Filter: Vis berre godkjende viss Status-kolonnen finst
        if STATUS_COL in eksisterande_kolonnar:
            # Vi gjer filteret robust: sjekkar om det står "Godkjent" (uavhengig av store/små bokstavar)
            godkjende = df[df[STATUS_COL].str.contains('Godkjent', na=False, case=False)]
        else:
            st.warning(f"Fann ikkje kolonnen '{STATUS_COL}'. Viser alle rader førebels.")
            godkjende = df

        sok = st.text_input("🔍 Søk i terminologien:", placeholder="T.ex. Skyldmark...")

        if not godkjende.empty:
            # Sjekk om Term-kolonnen finst før vi søker
            if TERM_COL in eksisterande_kolonnar:
                resultat = godkjende[godkjende[TERM_COL].str.contains(sok, case=False, na=False)]
                
                for _, row in resultat.iterrows():
                    # Vi brukar .get() for å unngå kræsj viss ein kolonne manglar
                    term = row.get(TERM_COL, "Mangler tittel")
                    definisjon = row.get(DEF_COL, "Ingen definisjon lagt inn.")
                    tid = row.get(TID_COL, "Ukjent tid")
                    sted = row.get(STED_COL, "Heile landet")
                    kjelde = row.get(KJELDE_COL, "Ingen kjelde")
                    
                    with st.expander(f"**{term}**"):
                        st.write(f"**Definisjon:** {definisjon}")
                        st.write(f"**Periode:** {tid} | **Område:** {sted}")
                        st.write(f"**Kjelde:** {kjelde}")
            else:
                st.error(f"Fann ikkje kolonnen '{TERM_COL}'. Sjekk overskrifta i Sheets.")
        else:
            st.info("Ingen godkjende ord i databasen ennå.")

# --- SIDE: FORESLÅ NYTT ---
elif val == "Foreslå nytt":
    st.title("💡 Bidra til leksikonet")
    st.write("Her kan du sende inn forslag til ein term eller ei alternativ forståing.")
    st.link_button("Opne innsendingsskjema", FORMS_URL)

# --- SIDE: ADMIN ---
elif val == "Admin":
    st.title("🔐 Admin-panel")
    passord = st.text_input("Passord:", type="password")
    
    if passord == "historie2024":
        st.subheader("Rådata frå Google Sheets")
        st.write("Her ser du alle innsendingar, inkludert dei som ikkje er godkjende ennå.")
        st.dataframe(df)
        st.info("For å godkjenne: Gå til Google Sheets og skriv 'Godkjent' i Status-kolonnen.")
