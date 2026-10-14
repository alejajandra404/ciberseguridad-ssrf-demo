# Nota de uso de Inteligencia Artificial

La rúbrica pide declarar el uso de IA, el prompt utilizado y los
resultados adaptados. Aquí está la declaración honesta de esta parte
(SSRF).

## Herramienta
Claude (Anthropic), usado como apoyo para preparar el laboratorio de demostración.

## Punto de partida (sin IA)
El código base **vulnerable** y **mitigado** proviene de la clase: 
el que se practicó previamente en una práctica. Esa parte no se generó con IA.

## Para qué se usó la IA
1. **Completar el laboratorio para la demo en vivo.** La IA ayudó a agregar un
   **servicio interno simulado** (`servicio_interno.py`) que entrega un
   "secreto" falso, para que el ataque sea visible frente al grupo.
2. **Organización y guía.** Ajuste de puertos (vulnerable 5000, mitigado
   5001, interno 8000).

## Prompt principal utilizado
> "Tengo una asignación de la materia de Ciberseguridad Aplicada, 
> se requiere presentar un exploit y su mitigación de la vulnerabilidad SSRF, 
> ejecutarlo en clase y explicarlo. Necesito que me ayudes a construir un laboratorio local y seguro, 
> partiendo del código base visto en clase (versión vulnerable y versión corregida), 
> que permita demostrar en vivo tanto el ataque como su bloqueo."

## Resultado adaptado
- Se conservó el código usado en la practica como núcleo de la parte vulnerable y
  mitigada.
- Se añadió el servicio interno simulado y se ajustaron los puertos para
  que la demostración sea visible.
- Se verificó que todo corre: el ataque al servidor vulnerable filtra el
  token secreto, y el mismo ataque al servidor mitigado responde `403`.
