# Árbol de Decisión Interactivo

## Descripción del proyecto

Este proyecto consiste en una aplicación gráfica desarrollada en Python que implementa un árbol binario de decisión para simular un juego de preguntas y respuestas.

El usuario piensa en un elemento y la aplicación intenta adivinarlo haciendo preguntas cuya respuesta debe ser únicamente Sí o No. Según cada respuesta, el programa avanza por el árbol hasta llegar a una posible respuesta final.

Si la aplicación no logra adivinar correctamente, permite que el usuario agregue una nueva respuesta y una nueva pregunta para diferenciarla de la respuesta incorrecta anterior. De esta forma, el árbol aprende y mejora en futuras partidas.

## Tecnologías utilizadas

* Python
* Tkinter
* Programación Orientada a Objetos
* Archivos JSON
* Árbol binario de decisión

## Archivos principales

* `main.py`: contiene el código principal de la aplicación.
* `data/arbol_guardado.json`: archivo principal donde se guarda el árbol aprendido.
* `data/animales.json`: árbol de ejemplo con al menos 10 respuestas.
* `data/objetos.json`: árbol de ejemplo con al menos 10 respuestas.
* `data/comidas.json`: árbol de ejemplo con al menos 10 respuestas.
* `data/deportes.json`: árbol de ejemplo con al menos 10 respuestas.
* `data/transportes.json`: árbol de ejemplo con al menos 10 respuestas.
* `docs/diseno_poo.txt`: documento de diseño orientado a objetos.

## Cómo ejecutar el proyecto

1. Tener Python instalado.
2. Abrir una terminal en la carpeta del proyecto.
3. Ejecutar el siguiente comando:

```bash
python main.py
```

## Funcionamiento general

1. El usuario abre la aplicación.
2. La aplicación muestra una pantalla inicial.
3. El usuario puede iniciar una partida o cargar un árbol desde archivo.
4. La aplicación muestra preguntas de Sí o No.
5. Según las respuestas, el sistema recorre el árbol.
6. Al llegar a una hoja, intenta adivinar la respuesta.
7. Si adivina correctamente, muestra un mensaje de victoria.
8. Si falla, solicita:

   * La respuesta correcta.
   * Una pregunta para diferenciar la nueva respuesta.
   * Si para la nueva respuesta la contestación sería Sí o No.
9. El árbol se actualiza.
10. El árbol actualizado se guarda automáticamente en el archivo correspondiente.

## Características principales

* Interfaz gráfica con Tkinter.
* Árbol binario de decisión.
* Nodos de pregunta y nodos de respuesta.
* Carga de árboles desde archivos JSON.
* Guardado automático después del aprendizaje.
* Validación de archivos vacíos, dañados o con formato incorrecto.
* Validación de campos vacíos en el formulario de aprendizaje.
* Posibilidad de jugar múltiples partidas sin cerrar la aplicación.

## Archivos de ejemplo

El proyecto incluye cinco archivos de ejemplo dentro de la carpeta `data`, cada uno con al menos 10 respuestas finales:

* `animales.json`
* `objetos.json`
* `comidas.json`
* `deportes.json`
* `transportes.json`

Estos archivos pueden cargarse desde la opción "Cargar árbol desde archivo" en la pantalla inicial.

## Autor
Fabián Cambronero Núñez - Proyecto desarrollado para el curso Taller de Programación.

