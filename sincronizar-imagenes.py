"""Baja todas las imágenes de la carpeta de OneDrive y las deja listas para el carrusel.

Lo corre la GitHub Action de este repositorio cada hora. También se puede a mano:

    python sincronizar-imagenes.py

Qué hace:
  1. Abre la liga para compartir de la carpeta, que deja las cookies que pide SharePoint.
  2. Lista los archivos de la carpeta y se queda con las imágenes.
  3. Baja cada una, la reduce a 1080 px de ancho y la guarda como promo-1.jpg, promo-2.jpg...
     en el orden alfabético del nombre del archivo.
  4. Escribe imagenes.json, que es lo que lee la página.
  5. Borra las imágenes que ya no estén en OneDrive.

Por qué se copian aquí en vez de jalarlas de OneDrive: esa liga solo entrega el archivo si el
navegador acepta sus cookies, y Safari en iPhone las bloquea por ser de otro sitio.
"""

import base64
import io
import json
import sys
from pathlib import Path

import requests
from PIL import Image

LIGA_CARPETA = (
    "https://fitnessparatodoss-my.sharepoint.com/:f:/g/personal/marketing_fpt_com_mx/"
    "IgCg4DLwOQxlTrzDwaSr_XAXAS2oe-QpzvVlpBol7Tn2XOc"
)
API = "https://fitnessparatodoss-my.sharepoint.com/personal/marketing_fpt_com_mx/_api/v2.0"

AQUI = Path(__file__).parent
MANIFIESTO = AQUI / "imagenes.json"
FONDO = AQUI / "fondo.jpg"
# El archivo de la carpeta cuyo nombre empiece con FONDO se usa como fondo de la página,
# no como una promoción más del carrusel.
PREFIJO_FONDO = "FONDO"
ANCHO_MAX = 1080
CALIDAD = 82
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}

NAVEGADOR = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    )
}


def listar(sesion):
    """Devuelve las imágenes de la carpeta, ordenadas por nombre."""
    sesion.get(LIGA_CARPETA, timeout=300).raise_for_status()  # canjea la liga: deja cookies
    token = "u!" + base64.urlsafe_b64encode(LIGA_CARPETA.encode()).decode().rstrip("=")
    r = sesion.get(
        f"{API}/shares/{token}/driveItem/children",
        headers={"Accept": "application/json"},
        timeout=300,
    )
    r.raise_for_status()

    archivos = [
        it
        for it in r.json().get("value", [])
        if Path(it["name"]).suffix.lower() in EXTENSIONES and it.get("@content.downloadUrl")
    ]
    return sorted(archivos, key=lambda it: it["name"].lower())


def guardar(sesion, archivo, destino):
    """Baja una imagen, la reduce a 1080 px de ancho y la guarda como JPG."""
    datos = sesion.get(archivo["@content.downloadUrl"], timeout=600).content
    im = Image.open(io.BytesIO(datos))
    if im.mode != "RGB":
        im = im.convert("RGB")
    if im.width > ANCHO_MAX:
        im = im.resize((ANCHO_MAX, round(im.height * ANCHO_MAX / im.width)), Image.LANCZOS)
    im.save(destino, "JPEG", quality=CALIDAD, optimize=True, progressive=True)
    return im.width, im.height, destino.stat().st_size / 1024


def main():
    sesion = requests.Session()
    sesion.headers.update(NAVEGADOR)

    todos = listar(sesion)
    fondo = next((a for a in todos if a["name"].upper().startswith(PREFIJO_FONDO)), None)
    archivos = [a for a in todos if a is not fondo]
    if not archivos:
        sys.exit(
            "La carpeta QR BENEFITNESS no tiene imágenes, o la liga para compartir dejó de "
            "funcionar. No se toca lo que ya está publicado."
        )

    # El fondo solo se reemplaza cuando hay un archivo FONDO en la carpeta. Si no lo hay,
    # se deja el que ya está publicado: así una carpeta sin fondo no deja la página sin él.
    if fondo:
        guardar(sesion, fondo, FONDO)
        print(f"{fondo['name']} -> fondo.jpg")
    elif FONDO.exists():
        print("Sin archivo FONDO en OneDrive: se conserva el fondo publicado.")

    publicadas = []
    for numero, archivo in enumerate(archivos, start=1):
        nombre = f"promo-{numero}.jpg"
        ancho, alto, peso = guardar(sesion, archivo, AQUI / nombre)
        publicadas.append(nombre)
        print(f"{archivo['name']} -> {nombre}  {ancho}x{alto}, {peso:.0f} KB")

    manifiesto = {"imagenes": publicadas}
    if FONDO.exists():
        manifiesto["fondo"] = FONDO.name
    MANIFIESTO.write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Limpia las que sobraron de una sincronización anterior con más imágenes.
    for viejo in AQUI.glob("promo-*.jpg"):
        if viejo.name not in publicadas:
            viejo.unlink()
            print(f"Quitada: {viejo.name}")

    print(f"Total publicadas: {len(publicadas)}")


if __name__ == "__main__":
    main()
