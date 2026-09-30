# Benefitness — página del QR

Página que abre el código QR de Benefitness. Muestra la imagen promocional que está en
OneDrive (Marketing Team / 2026 / DISEÑO / QR BENEFITNESS) y lleva a planetfitness.mx.

La imagen se publica aquí como `promo.jpg`. No se jala directo de OneDrive porque esa liga
necesita cookies de otro sitio y Safari en iPhone las bloquea: la imagen no cargaba.

## Cómo se actualiza la promoción

1. Marketing reemplaza `PF_BC_ALIANZAS_01.jpg` en OneDrive, con el mismo nombre.
2. Una GitHub Action revisa OneDrive **cada hora**, baja la imagen, la reduce a 1080 px de
   ancho y la publica aqui como `promo.jpg`. No hay que hacer nada mas.

Para no esperar la hora: pestana **Actions** -> "Actualizar la imagen de la promocion" ->
**Run workflow**. A mano tambien se puede, con `python sincronizar-imagen.py` y un push.

Mantenimiento: Infraestructura y Servicios TI, Fitness Para Todos.
