# Design tokens de tu producto

Este documento es la **única fuente** de colores, tipografía, radios, espaciados y sombras que usan las escenas. Se rellena en la fase 5 (`fases/5-sistema-visual.md`) y después se traslada a `renderer/src/tokens/tokens.json`. Ningún valor aparece en el JSON o en un componente sin estar antes aquí.

Mientras esté vacío, el kit usa los valores neutros de ejemplo que trae `tokens.json`.

## Etiquetas de confianza

Cada valor lleva una etiqueta que dice de dónde sale:

- `[figma-variable]`: variable o estilo definido en Figma (leído con `get_variable_defs`). Máxima confianza.
- `[code]`: leído del código que genera Figma para una pantalla (`get_design_context`).
- `[png-estimated]`: estimado mirando una captura, ajustado al valor confirmado más cercano. Nunca un valor inventado desde cero.
- `[devtools]`: medido en el producto real en el navegador (ver `fases/extras/medir-animaciones-en-el-navegador.md`).

## Reglas

- **Un token con dos valores**: distinguir si es **por contexto** (p. ej. texto sobre fondo claro vs. oscuro: documentar ambos con su contexto) o una **ambigüedad real** (mismo contexto, valor distinto sin explicación: documentar ambos como abiertos, nunca quedarse con uno sin decirlo).
- **Un valor nuevo solo como último recurso**: primero buscar el token existente más cercano.
- Si una fuente secundaria (una guía de marca antigua, un mockup de marketing) contradice lo que dice Figma o el código del producto, manda el producto.

---

## 1. Color

| Token | Valor | Uso | Fuente |
|---|---|---|---|
| canvas | | fondo general de la app | |
| surface | | tarjetas y paneles | |
| border | | bordes por defecto | |
| textPrimary | | texto principal | |
| textSecondary | | texto secundario, iconos secundarios | |
| accent | | botón principal, enlaces, elemento activo | |

### 1.1 Valores por contexto

### 1.2 Ambigüedades sin resolver

## 2. Tipografía

Familia: 

| Token | Tamaño | Peso | Interlineado | Uso | Fuente |
|---|---|---|---|---|---|

## 3. Radios

| Token | Valor | Uso | Fuente |
|---|---|---|---|

## 4. Espaciados

| Token | Valor | Uso | Fuente |
|---|---|---|---|

## 5. Sombras y elevación

## 6. Estructura de pantalla

Anchura de la barra lateral, altura de la cabecera, tamaño de referencia de las pantallas (p. ej. 1440×900), paneles fijos.
