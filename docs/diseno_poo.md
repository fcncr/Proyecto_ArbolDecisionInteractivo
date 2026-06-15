# Documento de Diseño Orientado a Objetos

## Nombre del proyecto

Árbol de Decisión Interactivo

## Descripción general

Este proyecto consiste en una aplicación gráfica desarrollada en Python que utiliza un árbol binario de decisión para simular un juego de preguntas y respuestas.

El usuario piensa en un elemento y la aplicación intenta adivinarlo realizando preguntas cuya respuesta debe ser únicamente Sí o No. Según cada respuesta, el programa avanza por una rama del árbol hasta llegar a una posible respuesta final.

Si la aplicación no logra adivinar correctamente, solicita al usuario una nueva respuesta correcta, una pregunta diferenciadora y si para esa nueva respuesta la contestación sería Sí o No. Con esta información, el árbol se actualiza y se guarda automáticamente en un archivo JSON para conservar el aprendizaje entre ejecuciones.

## Objetivo del diseño

El objetivo del diseño es separar las responsabilidades principales del sistema para evitar concentrar toda la lógica dentro de la interfaz gráfica.

Aunque el proyecto se trabaja principalmente en un solo archivo `main.py`, se organiza mediante clases para cumplir con Programación Orientada a Objetos.

Las responsabilidades principales se dividen en:

* Representación de nodos.
* Lógica del árbol.
* Manejo de archivos.
* Control del juego.
* Interfaz gráfica.

## Clases principales

El proyecto utiliza las siguientes clases:

* `DecisionNode`
* `DecisionTree`
* `TreeStorage`
* `GameController`
* `AppWindow`

---

## Clase DecisionNode

### Responsabilidad

La clase `DecisionNode` representa un nodo dentro del árbol binario de decisión.

Un nodo puede funcionar como:

* Nodo de pregunta: contiene una pregunta y tiene dos hijos.
* Nodo de respuesta: contiene una posible respuesta final y no tiene hijos.

### Atributos principales

* `text`: almacena el texto del nodo. Puede ser una pregunta o una respuesta.
* `yes_child`: referencia al nodo hijo que se recorre cuando el usuario responde Sí.
* `no_child`: referencia al nodo hijo que se recorre cuando el usuario responde No.

### Métodos principales

* `__init__()`: inicializa el nodo con su texto y sus hijos.
* `is_leaf()`: verifica si el nodo es una hoja. Si no tiene hijos, se considera una respuesta final.

---

## Clase DecisionTree

### Responsabilidad

La clase `DecisionTree` administra la lógica del árbol de decisión.

Se encarga de mantener la raíz del árbol, controlar el nodo actual, recorrer el árbol según las respuestas del usuario, reiniciar partidas y modificar el árbol cuando el sistema aprende una nueva respuesta.

### Atributos principales

* `root`: almacena el nodo raíz del árbol.
* `current_node`: almacena el nodo actual donde se encuentra la partida.

### Métodos principales

* `__init__()`: recibe la raíz del árbol e inicializa el nodo actual.
* `reset()`: reinicia la partida colocando el nodo actual en la raíz.
* `get_current_text()`: devuelve el texto del nodo actual.
* `is_current_leaf()`: indica si el nodo actual es una respuesta final.
* `answer_yes()`: avanza hacia la rama Sí del nodo actual.
* `answer_no()`: avanza hacia la rama No del nodo actual.
* `learn()`: reemplaza una respuesta incorrecta por una nueva pregunta y dos posibles respuestas.
* `node_to_dict()`: convierte un nodo del árbol en un diccionario.
* `to_dict()`: convierte todo el árbol en un diccionario para poder guardarlo en JSON.

---

## Clase TreeStorage

### Responsabilidad

La clase `TreeStorage` administra el manejo de archivos del árbol de decisión.

Su función principal es guardar y cargar el árbol usando archivos JSON. También controla errores relacionados con archivos inexistentes, vacíos, dañados o con una estructura incorrecta.

### Atributos principales

* `file_path`: ruta del archivo JSON utilizado para cargar o guardar el árbol.
* `last_load_success`: indica si la última carga fue exitosa.
* `last_load_message`: almacena un mensaje descriptivo del resultado de la última carga.
* `used_default_tree`: indica si fue necesario usar el árbol inicial por defecto.

### Métodos principales

* `__init__()`: inicializa el manejador con la ruta del archivo.
* `ensure_data_folder()`: crea la carpeta necesaria si no existe.
* `save_tree()`: guarda el árbol actual en un archivo JSON.
* `set_load_status()`: guarda el estado del último intento de carga.
* `load_tree()`: carga el árbol desde un archivo JSON. Si ocurre un error, devuelve el árbol inicial por defecto.

---

## Clase GameController

### Responsabilidad

La clase `GameController` funciona como intermediaria entre la interfaz gráfica, la lógica del árbol y el manejo de archivos.

Esta clase evita que la lógica del proyecto quede concentrada dentro de los botones de la interfaz gráfica.

### Atributos principales

* `storage`: objeto encargado de guardar y cargar archivos.
* `tree`: objeto que contiene el árbol de decisión actual.

### Métodos principales

* `__init__()`: inicializa el controlador y carga el árbol desde archivo.
* `start_game()`: reinicia la partida desde la raíz del árbol.
* `get_current_text()`: devuelve la pregunta o respuesta actual.
* `is_current_leaf()`: indica si el nodo actual es una hoja.
* `answer_question()`: procesa una respuesta Sí o No y avanza en el árbol.
* `validate_learning_data()`: valida los datos ingresados durante el aprendizaje.
* `learn()`: actualiza el árbol con una nueva pregunta y respuesta, y guarda automáticamente.
* `save_game()`: guarda el árbol actual.
* `load_tree_from_file()`: carga un árbol desde un archivo seleccionado por el usuario.
* `get_last_load_message()`: devuelve el mensaje del último intento de carga.

---

## Clase AppWindow

### Responsabilidad

La clase `AppWindow` representa la interfaz gráfica de la aplicación.

Se encarga de mostrar la pantalla inicial, las preguntas, los botones de Sí y No, los mensajes de resultado, los errores y el formulario de aprendizaje.

### Atributos principales

* `controller`: objeto `GameController` que administra la lógica del juego.
* `game_mode`: indica si el usuario está respondiendo una pregunta o una adivinanza final.
* `last_wrong_answer`: almacena la última respuesta incorrecta del sistema.

### Métodos principales

* `__init__()`: configura la ventana principal.
* `clear_window()`: elimina los elementos visuales actuales.
* `build_home_screen()`: construye la pantalla inicial.
* `load_tree_file()`: permite seleccionar y cargar un archivo JSON.
* `start_game()`: inicia una nueva partida.
* `build_game_screen()`: construye la pantalla de preguntas.
* `update_game_text()`: actualiza el texto mostrado según el nodo actual.
* `answer_yes_click()`: procesa el clic del botón Sí.
* `answer_no_click()`: procesa el clic del botón No.
* `process_answer()`: decide cómo procesar la respuesta según el modo actual.
* `handle_question_answer()`: procesa respuestas a nodos de pregunta.
* `handle_guess_answer()`: procesa respuestas a una adivinanza final.
* `build_learning_screen()`: construye el formulario de aprendizaje.
* `save_learning_click()`: guarda los datos ingresados en el formulario de aprendizaje.
* `show_end_options()`: muestra opciones después de ganar o aprender.

---

## Relación entre clases

La relación entre clases se organiza de la siguiente manera:

```text
AppWindow
   ↓
GameController
   ↓
DecisionTree
   ↓
DecisionNode
```

Además, `GameController` utiliza `TreeStorage` para guardar y cargar archivos:

```text
GameController
   ↓
TreeStorage
   ↓
Archivo JSON
```

La interfaz gráfica no modifica directamente el árbol ni los archivos. En su lugar, llama al controlador. El controlador decide qué acciones realizar sobre el árbol y cuándo guardar los cambios.

---

## Representación del árbol

El árbol se representa internamente mediante objetos de la clase `DecisionNode`.

Cada nodo contiene:

* Un texto.
* Una rama para Sí.
* Una rama para No.

Si un nodo tiene hijos, representa una pregunta.

Si un nodo no tiene hijos, representa una respuesta final.

Ejemplo de árbol inicial:

```text
¿Es un animal?
Sí -> perro
No -> computadora
```

Representación interna:

```python
DecisionNode(
    "¿Es un animal?",
    DecisionNode("perro"),
    DecisionNode("computadora")
)
```

---

## Recorrido del árbol

El recorrido inicia desde la raíz del árbol.

Cuando el usuario responde Sí, el programa avanza hacia `yes_child`.

Cuando el usuario responde No, el programa avanza hacia `no_child`.

El proceso continúa hasta que el nodo actual sea una hoja. Cuando se llega a una hoja, la aplicación intenta adivinar preguntando si el usuario estaba pensando en esa respuesta.

Ejemplo:

```text
Pregunta: ¿Es un animal?
Usuario: Sí
Avance: rama Sí
Nodo actual: perro
```

Como `perro` es una hoja, el sistema pregunta:

```text
¿Estabas pensando en perro?
```

---

## Diferencia entre nodos de pregunta y nodos de respuesta

Un nodo de pregunta tiene dos hijos:

* `yes_child`
* `no_child`

Un nodo de respuesta no tiene hijos.

La diferencia se determina con el método `is_leaf()`.

Si `is_leaf()` devuelve `True`, el nodo es una respuesta final.

Si `is_leaf()` devuelve `False`, el nodo es una pregunta.

---

## Proceso de aprendizaje

Cuando el sistema falla al adivinar, se activa el proceso de aprendizaje.

El sistema solicita al usuario:

1. La respuesta correcta.
2. Una pregunta que diferencie la respuesta correcta de la respuesta incorrecta.
3. Si para la respuesta correcta la contestación a esa pregunta sería Sí o No.

Luego, el nodo de respuesta incorrecta se transforma en una nueva pregunta.

Ejemplo:

Antes del aprendizaje:

```text
¿Es un animal?
Sí -> perro
No -> computadora
```

Si el usuario pensaba en `gato`, el sistema solicita una pregunta diferenciadora:

```text
Respuesta correcta: gato
Pregunta diferenciadora: ¿Maúlla?
Para gato: Sí
```

Después del aprendizaje:

```text
¿Es un animal?
Sí -> ¿Maúlla?
      Sí -> gato
      No -> perro
No -> computadora
```

La respuesta incorrecta anterior no se elimina; queda en la rama opuesta a la nueva respuesta correcta.

---

## Guardado del árbol

El árbol se guarda en formato JSON.

Como Python no puede guardar directamente objetos `DecisionNode` en un archivo JSON, primero se convierte el árbol a un diccionario.

El proceso de guardado es:

```text
Árbol de objetos -> Diccionario -> JSON
```

El método `to_dict()` convierte el árbol completo en diccionario.

Luego, `TreeStorage.save_tree()` escribe ese diccionario en un archivo `.json`.

Ejemplo de JSON:

```json
{
    "text": "¿Es un animal?",
    "yes": {
        "text": "perro",
        "yes": null,
        "no": null
    },
    "no": {
        "text": "computadora",
        "yes": null,
        "no": null
    }
}
```

---

## Carga del árbol

Para cargar un árbol desde archivo se realiza el proceso inverso:

```text
JSON -> Diccionario -> Árbol de objetos
```

Primero, Python lee el archivo JSON y lo convierte en un diccionario.

Después, la función `dict_to_node()` reconstruye los objetos `DecisionNode` de forma recursiva.

Si el archivo no existe, está vacío, tiene formato JSON incorrecto o no tiene una estructura válida, el sistema muestra un mensaje claro y utiliza el árbol inicial por defecto.

---

## Árbol inicial por defecto

Si el usuario no carga ningún archivo válido, el programa inicia con un árbol básico por defecto:

```text
¿Es un animal?
Sí -> perro
No -> computadora
```

Este árbol permite iniciar partidas aunque no exista ningún archivo guardado.

---

## Validaciones implementadas

El proyecto incluye validaciones para evitar errores durante la ejecución.

### Validaciones de aprendizaje

* La respuesta correcta no puede estar vacía.
* La nueva pregunta no puede estar vacía.
* La respuesta correcta no puede ser igual a la respuesta incorrecta anterior.
* El usuario debe indicar si para la nueva respuesta la contestación sería Sí o No.
* Si la pregunta no termina en signo de pregunta, el sistema agrega `?` automáticamente.

### Validaciones de archivo

* Se valida que el archivo exista.
* Se valida que el archivo no esté vacío.
* Se valida que el archivo tenga formato JSON válido.
* Se valida que cada nodo tenga la llave `text`.
* Se valida que cada nodo tenga las llaves `yes` y `no`.
* Se valida que el texto del nodo no esté vacío.
* Se valida que un nodo de pregunta tenga ambas ramas: Sí y No.

---

## Manejo de errores

Cuando ocurre un error al cargar un archivo, la aplicación no se cierra inesperadamente.

En lugar de eso:

1. Muestra un mensaje claro al usuario.
2. Usa el árbol inicial por defecto.
3. Permite seguir jugando normalmente.

Esto permite cumplir con el requisito de evitar cierres inesperados por errores de archivo.

---

## Interfaz gráfica

La interfaz gráfica fue desarrollada con Tkinter.

Incluye:

* Pantalla inicial.
* Título del juego.
* Instrucciones breves.
* Botón para iniciar partida.
* Botón para cargar árbol desde archivo.
* Botón para salir.
* Pantalla de preguntas.
* Botones Sí y No.
* Mensajes de victoria.
* Formulario de aprendizaje.
* Mensajes de error y confirmación.

---

## Archivos de ejemplo

El proyecto incluye cinco archivos de ejemplo dentro de la carpeta `data`.

Cada archivo contiene un árbol con al menos 10 respuestas finales:

* `animales.json`
* `objetos.json`
* `comidas.json`
* `deportes.json`
* `transportes.json`

Estos archivos permiten probar el sistema con diferentes temas.

---

## Separación de responsabilidades

Aunque el proyecto se mantiene principalmente en un solo archivo Python, la lógica se divide en clases.

Esta separación evita que toda la lógica quede dentro de la interfaz gráfica.

La división es la siguiente:

* `DecisionNode`: representa nodos.
* `DecisionTree`: controla el árbol.
* `TreeStorage`: maneja archivos.
* `GameController`: conecta la lógica con la interfaz.
* `AppWindow`: maneja la interfaz gráfica.

---

