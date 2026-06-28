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
