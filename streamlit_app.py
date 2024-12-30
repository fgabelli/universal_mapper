import streamlit as st
from utils.auth import login, register
from utils.file_processing import upload_file, preview_file, get_columns, generate_output
from utils.profiles import load_profile, save_profile, list_profiles, delete_profile

# Configurazione dell'app
st.set_page_config(page_title="Universal Mapper", layout="wide")

# Funzione per mostrare l'intestazione con logo e nome app
def show_header():
    col1, col2 = st.columns([1, 5])
    # URL del logo ospitato su GitHub
    logo_url = "https://raw.githubusercontent.com/fgabelli/universal_mapper/main/logo/logo_web.png"
    try:
        with col1:
            st.image(logo_url, width=80)  # Carica il logo dal link GitHub
        with col2:
            st.markdown(
                """
                <div style="margin-top: -10px;">
                    <h1 style="margin-bottom: 0; font-size: 24px; font-family: Arial, sans-serif; color: #333;">
                        Universal Mapper
                    </h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"Errore nel caricamento del logo: {e}")

# Mostra l'intestazione nella parte superiore di ogni pagina
show_header()

# Inizializza lo stato
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Caricamento File"
if "associations" not in st.session_state:
    st.session_state["associations"] = []

# Sidebar per la navigazione
with st.sidebar:
    if st.session_state["authenticated"]:
        st.title("Navigazione")
        page = st.radio(
            "Vai a:",
            options=["Caricamento File", "Gestione Profili", "Account", "Logout"],
            key="page_selector"
        )
        st.session_state["page"] = page
    else:
        st.title("Accesso richiesto")
        st.session_state["page"] = "login"

# Pagina di Login
if st.session_state["page"] == "login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state["authenticated"] = True
            st.session_state["page"] = "Caricamento File"
            st.success("Accesso effettuato!")
        else:
            st.error("Credenziali errate.")
    if st.button("Vai alla Registrazione"):
        st.session_state["page"] = "register"

# Pagina di Registrazione
elif st.session_state["page"] == "register":
    st.title("Registrazione")
    new_username = st.text_input("Nuovo Username")
    new_password = st.text_input("Nuova Password", type="password")
    if st.button("Registrati"):
        if register(new_username, new_password):
            st.success("Registrazione completata! Procedi con il login.")
            st.session_state["page"] = "login"
        else:
            st.error("Errore durante la registrazione.")
    if st.button("Torna al Login"):
        st.session_state["page"] = "login"

# Pagina di Caricamento File
elif st.session_state["page"] == "Caricamento File":
    st.title("Caricamento File")
    st.write(
        "Carica i file sorgente e il tracciato record. Se hai un profilo salvato, puoi caricarlo per autocompilare le associazioni."
    )
    uploaded_source = upload_file("Carica file sorgente (CSV/XLS/XLSX):")
    uploaded_record = upload_file("Carica file tracciato record (CSV/XLS/XLSX):")

    if uploaded_source and uploaded_record:
        st.subheader("Anteprima file sorgente:")
        source_df = preview_file(uploaded_source)

        st.subheader("Anteprima file tracciato record:")
        record_df = preview_file(uploaded_record)

        if source_df is not None and record_df is not None:
            source_columns = [""] + get_columns(uploaded_source)
            record_columns = get_columns(uploaded_record)

            st.subheader("Carica Profilo")
            profiles = list_profiles()
            if profiles:
                selected_profile = st.selectbox("Seleziona un profilo salvato", [""] + profiles)
                if selected_profile and selected_profile.strip() != "":
                    associations = load_profile(selected_profile)
                    st.session_state["associations"] = associations
                    st.success(f"Profilo '{selected_profile}' caricato!")
                else:
                    st.session_state["associations"] = []
            else:
                st.warning("Non ci sono profili salvati.")

            st.subheader("Associazione Colonne")
            associations = []
            for i, record_col in enumerate(record_columns):
                default_value = (
                    next(
                        (
                            assoc["source"]
                            for assoc in st.session_state["associations"]
                            if assoc["record"] == record_col
                        ),
                        "",
                    )
                )
                source_col = st.selectbox(
                    f"Colonna sorgente per '{record_col}' (opzionale)",
                    source_columns,
                    index=source_columns.index(default_value) if default_value in source_columns else 0,
                    key=f"assoc_{i}",
                )
                associations.append({"record": record_col, "source": source_col if source_col != "" else None})

            st.session_state["associations"] = associations

            profile_name = st.text_input("Nome del profilo", placeholder="Inserisci un nome per il profilo")
            if st.button("Salva Profilo"):
                if profile_name.strip():
                    save_profile(profile_name.strip(), associations)
                    st.success(f"Profilo '{profile_name}' salvato!")
                else:
                    st.error("Il nome del profilo non può essere vuoto.")

            output_format = st.selectbox("Formato del file di output", ["CSV", "XLS", "XLSX"])
            if st.button("Genera File"):
                try:
                    output_file = generate_output(uploaded_source, associations, output_format)
                    st.success("File generato con successo!")
                    st.download_button(
                        "Scarica file",
                        data=open(output_file, "rb"),
                        file_name=f"output.{output_format.lower()}",
                        mime="application/octet-stream",
                    )
                except ValueError as e:
                    st.error(str(e))

# Pagina di Gestione Profili
elif st.session_state["page"] == "Gestione Profili":
    st.title("Gestione Profili")
    st.write("Seleziona un profilo da eliminare.")
    profiles = list_profiles()
    if profiles:
        selected_profile = st.selectbox("Seleziona un profilo salvato", profiles)
        if st.button("Elimina Profilo"):
            delete_profile(selected_profile)
            st.success(f"Profilo '{selected_profile}' eliminato!")
    else:
        st.warning("Non ci sono profili salvati.")

# Pagina di Account
elif st.session_state["page"] == "Account":
    st.title("Impostazioni Account")
    st.write("Qui puoi gestire il tuo account.")
    new_password = st.text_input("Nuova Password", type="password")
    if st.button("Cambia Password"):
        # Simula il cambio password
        st.success("Password cambiata con successo!")

# Pagina di Logout
elif st.session_state["page"] == "Logout":
    st.session_state["authenticated"] = False
    st.session_state["page"] = "login"
    st.success("Disconnesso con successo!")
