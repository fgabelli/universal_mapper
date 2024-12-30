import pandas as pd
import streamlit as st

def upload_file(label):
    """
    Gestisce il caricamento di un file utilizzando Streamlit.
    :param label: Etichetta mostrata all'utente.
    :return: Oggetto file caricato o None.
    """
    uploaded_file = st.file_uploader(label, type=["csv", "xls", "xlsx"])
    return uploaded_file

def preview_file(file):
    """
    Mostra un'anteprima del file caricato.
    :param file: File caricato.
    :return: DataFrame del file caricato o None in caso di errore.
    """
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        st.write(df.head())
        return df
    except Exception as e:
        st.error(f"Errore nella lettura del file: {e}")
        return None

def get_columns(file):
    """
    Recupera i nomi delle colonne dal file caricato.
    :param file: File caricato.
    :return: Lista dei nomi delle colonne.
    """
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, nrows=0)
        else:
            df = pd.read_excel(file, nrows=0)
        return list(df.columns)
    except Exception as e:
        st.error(f"Errore nel recupero delle colonne: {e}")
        return []

def generate_output(source_file, associations, output_format):
    """
    Genera un file di output basato sulle associazioni definite e il formato richiesto.
    :param source_file: File sorgente caricato dall'utente.
    :param associations: Lista di dizionari con associazioni tra colonne sorgente e record.
    :param output_format: Formato del file di output ("CSV", "XLS", "XLSX").
    :return: Percorso del file di output generato.
    """
    try:
        if source_file.name.endswith(".csv"):
            source_df = pd.read_csv(source_file)
        else:
            source_df = pd.read_excel(source_file)

        output_df = pd.DataFrame()
        for assoc in associations:
            record_col = assoc["record"]
            source_col = assoc["source"]
            if source_col is not None and source_col in source_df.columns:
                output_df[record_col] = source_df[source_col]
            else:
                output_df[record_col] = None

        output_path = f"output.{output_format.lower()}"
        if output_format == "CSV":
            output_df.to_csv(output_path, index=False)
        elif output_format in ["XLS", "XLSX"]:
            output_df.to_excel(output_path, index=False, engine="openpyxl")
        return output_path
    except Exception as e:
        raise ValueError(f"Errore nella generazione del file di output: {e}")
