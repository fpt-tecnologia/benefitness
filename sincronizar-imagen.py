"""Baja la imagen de OneDrive, la optimiza y la guarda como promo.jpg.

Lo corre solo la GitHub Action de este repositorio, cada hora.
También se puede correr a mano desde esta carpeta:

    python sincronizar-imagen.py

Por qué existe: la liga de OneDrive solo entrega el JPG si el navegador acepta sus
cookies, y Safari en iPhone las bloquea por ser de otro sitio. Por eso la imagen se
copia al repositorio y se sirve desde el mismo dominio que la página.
"""

import io
import sys
from pathlib import Path

import requests
from PIL import Image

LIGA = (
    "https://fitnessparatodoss-my.sharepoint.com/:i:/g/personal/marketing_fpt_com_mx/"
    "IQB8zY5HrNBASLpwdS5jQ-98Ab-Y3E9keh01VoyFBFVrjPM?download=1"
)
DESTINO = Path(__file__).parent / "promo.jpg"
ANCHO_MAX = 1080
CALIDAD = 82

NAVEGADOR = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    )
}


def main():
    sesion = requests.Session()  # la sesión guarda las cookies que pide SharePoint
    r = sesion.get(LIGA, headers=NAVEGADOR, timeout=300)
    r.raise_for_status()

    if "image" not in r.headers.get("Content-Type", ""):
        sys.exit(
            "OneDrive no devolvio una imagen. Revisa que la liga para compartir siga activa "
            "y que PF_BC_ALIANZAS_01.jpg siga en la carpeta QR BENEFITNESS."
        )

    im = Image.open(io.BytesIO(r.content))
    if im.mode != "RGB":
        im = im.convert("RGB")
    if im.width > ANCHO_MAX:
        alto = round(im.height * ANCHO_MAX / im.width)
        im = im.resize((ANCHO_MAX, alto), Image.LANCZOS)

    im.save(DESTINO, "JPEG", quality=CALIDAD, optimize=True, progressive=True)
    print(f"Publicada: {im.width}x{im.height}, {DESTINO.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
