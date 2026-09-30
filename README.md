# Benefitness — página del QR

Página que abre el código QR de Benefitness. Muestra la imagen promocional que está en
OneDrive (Marketing Team / 2026 / DISEÑO / QR BENEFITNESS) y lleva a planetfitness.mx.

La imagen se publica aquí como `promo.jpg`. No se jala directo de OneDrive porque esa liga
necesita cookies de otro sitio y Safari en iPhone las bloquea: la imagen no cargaba.

## Cómo se actualiza la promoción

1. Marketing reemplaza `PF_BC_ALIANZAS_01.jpg` en OneDrive, con el mismo nombre.
2. En `Claude\qr` se corre `python actualizar-imagen.py`, que la baja, la reduce a 1080 px
   de ancho y la deja en esta carpeta como `promo.jpg`.
3. `git add -A`, `git commit` y `git push origin main`.

Mantenimiento: Infraestructura y Servicios TI, Fitness Para Todos.
