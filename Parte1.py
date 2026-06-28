import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# =========================
# MEDIOS
# =========================

urls = {
    "Ojo": "https://ojo.pe/",
    "El Comercio": "https://elcomercio.pe/",
    "Correo": "https://diariocorreo.pe/",
    "La República": "https://larepublica.pe/",
}


# =========================
# CATEGORÍAS POR PALABRAS CLAVE
# =========================

alarmistas = [
    "fraude", "presunto fraude", "denuncian", "denuncia",
    "irregularidades", "presuntas irregularidades",
    "cuestiona", "cuestionan", "rechaza", "rechazan",
    "manipulación", "manipulado", "manipular",
    "ilegitimidad", "ilegal", "ilegalidad",
    "crisis", "escándalo", "polémica", "polémicas",
    "sospecha", "sospechas", "alerta", "alertan",
    "protesta", "protestas"
]

informativas = [
    "onpe", "jne", "reniec",
    "elecciones", "electoral", "proceso electoral",
    "resultados", "resultados preliminares",
    "conteo", "conteo rápido", "conteo oficial",
    "actas", "actas procesadas", "actas observadas",
    "sufragio", "votación", "segunda vuelta",
    "mesa de sufragio", "centro de votación",
    "avance del conteo", "cómputo oficial"
]

politicos = [
    "keiko", "fujimori",
    "pedro castillo", "castillo",
    "rafael lopez aliaga", "lopez aliaga",
    "hernando de soto",
    "veronika mendoza",
    "candidata", "candidato",
    "presidente", "presidencial",
    "congreso", "parlamento",
    "ministro", "gobierno"
]
otros = []

# =========================
# DATA FINAL
# =========================

datos = []

# =========================
# SCRAPING
# =========================

for fuente, url in urls.items():

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        titulares = soup.find_all(["h1", "h2", "h3"])

        for t in titulares:

            texto = t.get_text(strip=True)

            if len(texto) < 20:
                continue

            texto_low = texto.lower()

            # =========================
            # CLASIFICACIÓN
            # =========================

            if any(p in texto_low for p in alarmistas):
                categoria = "🚨 Alarmista"

            elif any(p in texto_low for p in informativas):
                categoria = "🗳️ Informativa electoral"

            elif any(p in texto_low for p in politicos):
                categoria = "👤 Política"

            else:
                categoria = "📌 Otros"

            datos.append({
                "Fuente": fuente,
                "Titular": texto,
                "Categoria": categoria,
                "Fecha": datetime.now()
            })

    except Exception as e:
        print(f"Error en {fuente}: {e}")

# =========================
# DATAFRAME FINAL
# =========================

df = pd.DataFrame(datos)

# =========================
# RESULTADOS
# =========================

print(df)

# guardar CSV
df.to_csv("clasificacion_titulares_electorales.csv", index=False)

print("\nArchivo guardado: clasificacion_titulares_electorales.csv")

#Dataframe
df = df[df["Categoria"] != "📌 Otros"]
df

# =========================
# LIMPIEZA PARA GRÁFICOS
# =========================

import plotly.express as px

# Copia del dataframe original
df_grafico = df.copy()

# Quitamos "Otros" solo para enfocar el análisis electoral
df_grafico = df_grafico[df_grafico["Categoria"] != "📌 Otros"]

# Total de titulares por cada medio
total_por_fuente = (
    df_grafico.groupby("Fuente")
    .size()
    .reset_index(name="Total_medio")
)

# Cantidad por fuente y categoría
resumen = (
    df_grafico.groupby(["Fuente", "Categoria"])
    .size()
    .reset_index(name="Cantidad")
)

# Unimos con el total de cada medio
resumen = resumen.merge(total_por_fuente, on="Fuente")

# Porcentaje dentro de cada medio
resumen["Porcentaje_medio"] = (
    resumen["Cantidad"] / resumen["Total_medio"] * 100
).round(1)

resumen
