# Datos ficticios

Los vídeos demo enseñan el producto con datos inventados. Nunca aparecen personas, empresas, correos o cifras reales, tampoco de clientes ni del propio equipo.

## Personas

- **Nombres variados y verosímiles**, de orígenes distintos, sin coincidir con alguien famoso o conocido del sector.
- **Nunca repetir el relleno de Figma.** Si en el diseño la misma persona de ejemplo aparece en todas las filas, en el vídeo cada fila es alguien distinto, con su propio cargo.
- **Trayectorias coherentes**: si una persona tiene dos experiencias, en dos empresas distintas; cargo, ubicación y empresa encajan con el tema del vídeo.
- **El usuario que maneja la app** (el que aparece en la barra lateral) también es ficticio y lleva foto o iniciales, igual que el resto.

## Empresas y logos

- Nombres inventados que suenen reales ("Bruma Foods", "Telar Labs"). Comprobar con una búsqueda rápida que no son una empresa conocida.
- **Logos**: por defecto, el componente `LogoBadge` dibuja un monograma de color derivado del nombre: cero imágenes, sin riesgo de parecerse a una marca real.
- Nunca el logo de una empresa real.

## Fotos de personas

Opciones, de menos a más realista:

1. **Iniciales sobre color** (por defecto, componente `Avatar` sin `avatarUrl`). Siempre correcto, cero trabajo.
2. **Avatares ilustrados** de un servicio de avatares generados (p. ej. DiceBear). Revisa la licencia del estilo que elijas.
3. **Fotos realistas generadas por IA** de personas que no existen. Encuadre recomendado para avatares circulares: de pecho para arriba, con aire por encima de la cabeza, fondo liso, ropa de oficina sencilla, sonrisa natural. Si usas un servicio de pago, Claude te pregunta antes de generar una tanda.

Guarda las imágenes en `renderer/public/personas/` y los logos en `renderer/public/logos/`, con un `FUENTE.md` al lado que diga de dónde salen y cómo se regeneran. Nunca en `.tmp/`.

Si no te gusta cómo queda un estilo, lo normal es comparar dos opciones renderizadas una al lado de la otra. Por eso las fotos van en el guion (`avatarUrl`) y no dentro de los componentes: cambiar de estilo es cambiar rutas en el JSON.

## Textos

- Nada del texto de relleno de Figma ("Lorem ipsum", "Label", "Nombre Apellido", palabras a medio escribir).
- Sin guiones largos ni medios (— –).
- Cifras y fechas verosímiles y coherentes entre escenas.
