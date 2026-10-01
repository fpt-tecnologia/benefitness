# Benefitness — página del QR

Página que abre el código QR de Benefitness. Muestra la imagen promocional que está en
OneDrive (Marketing Team / 2026 / DISEÑO / QR BENEFITNESS) y lleva a planetfitness.mx.

La página es un carrusel: muestra todas las imágenes de esa carpeta, en orden alfabético por
nombre de archivo, y se desliza con el dedo o con las flechas. Las imágenes se publican aquí
como `promo-1.jpg`, `promo-2.jpg`... y `imagenes.json` dice cuáles son.

No se jalan directo de OneDrive porque esa liga necesita cookies de otro sitio y Safari en
iPhone las bloquea: la imagen no cargaba.

## Cómo se actualiza la promoción

1. Marketing agrega, quita o reemplaza imágenes en la carpeta de OneDrive. Para controlar el
   orden, conviene nombrarlas `01_`, `02_`, `03_`...
2. Una GitHub Action revisa OneDrive **cada hora**, baja las imágenes, las reduce a 1080 px de
   ancho y las publica. No hay que hacer nada más.

Para no esperar la hora: pestaña **Actions** -> "Actualizar las imagenes de la promocion" ->
**Run workflow**. A mano también se puede, con `python sincronizar-imagenes.py` y un push.

Mantenimiento: Infraestructura y Servicios TI, Fitness Para Todos.
