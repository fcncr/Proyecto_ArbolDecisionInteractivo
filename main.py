#INSTITUTO TECNOLÓGICO DE COSTA RICA
#PROYECTO  3 TALLER DE PROGRAMACIÓN 
#Fabián Cambronero Núñez
#2026079420 

# =========================
# IMPORTS
# =========================

import os
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


# =========================
# CONSTANTES DEL PROYECTO
# =========================

DATA_FOLDER = "data"
DEFAULT_TREE_FILE = os.path.join(DATA_FOLDER, "arbol_guardado.json")


# =========================
# MODELO: NODO DEL ÁRBOL
# =========================

class DecisionNode:

    # Inicializa un nodo del árbol de decisión.
    # Entradas: texto del nodo, hijo para Sí y hijo para No.
    # Salidas: ninguna; crea un objeto DecisionNode.
    def __init__(self, text, yes_child=None, no_child=None):
        self.text = text
        self.yes_child = yes_child
        self.no_child = no_child

    # Indica si el nodo actual es una respuesta final.
    # Entradas: ninguna.
    # Salidas: True si no tiene hijos; False si tiene al menos un hijo.
    def is_leaf(self):
        return self.yes_child is None and self.no_child is None


# =========================
# LÓGICA DEL ÁRBOL
# =========================

class DecisionTree:

    # Inicializa el árbol de decisión con una raíz.
    # Entradas: nodo raíz del árbol.
    # Salidas: ninguna; crea un objeto DecisionTree.
    def __init__(self, root):
        self.root = root
        self.current_node = root

    # Reinicia la partida colocando el nodo actual en la raíz.
    # Entradas: ninguna.
    # Salidas: ninguna; actualiza el nodo actual.
    def reset(self):
        self.current_node = self.root

    # Obtiene el texto del nodo actual.
    # Entradas: ninguna.
    # Salidas: texto de la pregunta o respuesta actual.
    def get_current_text(self):
        return self.current_node.text

    # Verifica si el nodo actual es una respuesta final.
    # Entradas: ninguna.
    # Salidas: True si el nodo actual es hoja; False si es pregunta.
    def is_current_leaf(self):
        return self.current_node.is_leaf()

    # Avanza el árbol hacia la rama Sí del nodo actual.
    # Entradas: ninguna.
    # Salidas: True si avanzó correctamente; False si no existe rama Sí.
    def answer_yes(self):
        if self.current_node.yes_child is not None:
            self.current_node = self.current_node.yes_child
            return True

        return False

    # Avanza el árbol hacia la rama No del nodo actual.
    # Entradas: ninguna.
    # Salidas: True si avanzó correctamente; False si no existe rama No.
    def answer_no(self):
        if self.current_node.no_child is not None:
            self.current_node = self.current_node.no_child
            return True

        return False

    # Reemplaza una respuesta incorrecta por una nueva pregunta.
    # Entradas: respuesta correcta, nueva pregunta y respuesta esperada para la correcta.
    # Salidas: ninguna; modifica el nodo actual del árbol.
    def learn(self, correct_answer, new_question, answer_for_correct):
        old_answer = self.current_node.text

        new_correct_node = DecisionNode(correct_answer)
        old_answer_node = DecisionNode(old_answer)

        self.current_node.text = new_question

        if answer_for_correct == "si":
            self.current_node.yes_child = new_correct_node
            self.current_node.no_child = old_answer_node
        else:
            self.current_node.yes_child = old_answer_node
            self.current_node.no_child = new_correct_node

    # Convierte un nodo del árbol en un diccionario.
    # Entradas: nodo del árbol o None.
    # Salidas: diccionario con text, yes y no; o None si no hay nodo.
    def node_to_dict(self, node):
        if node is None:
            return None

        return {
            "text": node.text,
            "yes": self.node_to_dict(node.yes_child),
            "no": self.node_to_dict(node.no_child)
        }

    # Convierte todo el árbol en un diccionario desde la raíz.
    # Entradas: ninguna.
    # Salidas: diccionario que representa el árbol completo.
    def to_dict(self):
        return self.node_to_dict(self.root)


# =========================
# CONVERSIÓN DE DICCIONARIO A ÁRBOL
# =========================

# Convierte un diccionario en un nodo del árbol de decisión.
# Entradas: diccionario con las llaves text, yes y no; o None.
# Salidas: objeto DecisionNode reconstruido; o None si no hay datos.
def dict_to_node(data):
    if data is None:
        return None

    if not isinstance(data, dict):
        raise ValueError("El dato del nodo debe ser un diccionario.")

    if "text" not in data:
        raise ValueError("El nodo no contiene la llave obligatoria 'text'.")

    if "yes" not in data:
        raise ValueError("El nodo no contiene la llave obligatoria 'yes'.")

    if "no" not in data:
        raise ValueError("El nodo no contiene la llave obligatoria 'no'.")

    text = data["text"]

    if not isinstance(text, str) or text.strip() == "":
        raise ValueError("El texto del nodo no puede estar vacío.")

    has_yes = data["yes"] is not None
    has_no = data["no"] is not None

    if has_yes != has_no:
        raise ValueError("Un nodo de pregunta debe tener rama Sí y rama No.")

    yes_child = dict_to_node(data["yes"])
    no_child = dict_to_node(data["no"])

    return DecisionNode(text.strip(), yes_child, no_child)


# =========================
# CREACIÓN DEL ÁRBOL INICIAL
# =========================

# Crea el árbol inicial por defecto del juego.
# Entradas: ninguna.
# Salidas: nodo raíz del árbol de decisión.
def create_default_tree():
    root = DecisionNode(
        "¿Es un animal?",
        DecisionNode("perro"),
        DecisionNode("computadora")
    )

    return root


# =========================
# MANEJO DE ARCHIVOS
# =========================

class TreeStorage:

    # Inicializa el manejador de archivos del árbol.
    # Entradas: ruta del archivo JSON donde se guardará o cargará el árbol.
    # Salidas: ninguna; crea un objeto TreeStorage.
    def __init__(self, file_path=DEFAULT_TREE_FILE):
        self.file_path = file_path
        self.last_load_success = False
        self.last_load_message = ""
        self.used_default_tree = False

    # Crea la carpeta donde se guardará el archivo si todavía no existe.
    # Entradas: ninguna.
    # Salidas: ninguna; asegura la existencia de la carpeta del archivo.
    def ensure_data_folder(self):
        folder_path = os.path.dirname(self.file_path)

        if folder_path != "" and not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Guarda el árbol de decisión en un archivo JSON.
    # Entradas: objeto DecisionTree que será guardado.
    # Salidas: True si se guardó correctamente; False si ocurrió un error.
    def save_tree(self, tree):
        try:
            self.ensure_data_folder()

            tree_data = tree.to_dict()

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(tree_data, file, indent=4, ensure_ascii=False)

            return True

        except OSError as error:
            print("Error al guardar el árbol:", error)
            return False

    # Guarda el estado del último intento de carga.
    # Entradas: éxito, mensaje y si se usó el árbol por defecto.
    # Salidas: ninguna; actualiza atributos internos del almacenamiento.
    def set_load_status(self, success, message, used_default_tree):
        self.last_load_success = success
        self.last_load_message = message
        self.used_default_tree = used_default_tree

    # Carga el árbol de decisión desde un archivo JSON.
    # Entradas: ninguna.
    # Salidas: objeto DecisionTree cargado; si falla, devuelve árbol por defecto.
    def load_tree(self):
        try:
            if not os.path.exists(self.file_path):
                self.set_load_status(
                    False,
                    "El archivo no existe. Se usó el árbol inicial por defecto.",
                    True
                )
                return DecisionTree(create_default_tree())

            if os.path.getsize(self.file_path) == 0:
                self.set_load_status(
                    False,
                    "El archivo está vacío. Se usó el árbol inicial por defecto.",
                    True
                )
                return DecisionTree(create_default_tree())

            with open(self.file_path, "r", encoding="utf-8") as file:
                tree_data = json.load(file)

            root = dict_to_node(tree_data)

            self.set_load_status(
                True,
                "El árbol se cargó correctamente desde el archivo seleccionado.",
                False
            )

            return DecisionTree(root)

        except json.JSONDecodeError:
            self.set_load_status(
                False,
                "El archivo no tiene un formato JSON válido. Se usó el árbol inicial por defecto.",
                True
            )
            return DecisionTree(create_default_tree())

        except ValueError as error:
            self.set_load_status(
                False,
                f"El archivo no tiene una estructura válida: {error}. Se usó el árbol inicial por defecto.",
                True
            )
            return DecisionTree(create_default_tree())

        except OSError as error:
            self.set_load_status(
                False,
                f"No se pudo leer el archivo: {error}. Se usó el árbol inicial por defecto.",
                True
            )
            return DecisionTree(create_default_tree())


# =========================
# CONTROLADOR DEL JUEGO
# =========================

class GameController:

    # Inicializa el controlador principal del juego.
    # Entradas: objeto TreeStorage opcional para cargar y guardar el árbol.
    # Salidas: ninguna; crea un controlador con árbol cargado.
    def __init__(self, storage=None):
        if storage is None:
            self.storage = TreeStorage()
        else:
            self.storage = storage

        self.tree = self.storage.load_tree()

    # Inicia o reinicia una partida desde la raíz del árbol.
    # Entradas: ninguna.
    # Salidas: texto del nodo inicial del árbol.
    def start_game(self):
        self.tree.reset()
        return self.tree.get_current_text()

    # Obtiene el texto del nodo actual de la partida.
    # Entradas: ninguna.
    # Salidas: pregunta o respuesta actual.
    def get_current_text(self):
        return self.tree.get_current_text()

    # Verifica si el nodo actual es una respuesta final.
    # Entradas: ninguna.
    # Salidas: True si el nodo actual es una hoja; False si es pregunta.
    def is_current_leaf(self):
        return self.tree.is_current_leaf()

    # Procesa una respuesta Sí o No y avanza en el árbol.
    # Entradas: respuesta normalizada "si" o "no".
    # Salidas: texto del nuevo nodo actual.
    def answer_question(self, answer):
        if answer == "si":
            self.tree.answer_yes()
        elif answer == "no":
            self.tree.answer_no()
        else:
            raise ValueError("La respuesta debe ser 'si' o 'no'.")

        return self.tree.get_current_text()

    # Valida los datos necesarios para el aprendizaje.
    # Entradas: respuesta correcta, nueva pregunta y respuesta Sí/No para la correcta.
    # Salidas: ninguna; lanza ValueError si algún dato es inválido.
    def validate_learning_data(self, correct_answer, new_question, answer_for_correct):
        if correct_answer.strip() == "":
            raise ValueError("La respuesta correcta no puede estar vacía.")

        if new_question.strip() == "":
            raise ValueError("La nueva pregunta no puede estar vacía.")

        if answer_for_correct not in ["si", "no"]:
            raise ValueError("Debe indicar si para la nueva respuesta la contestación es Sí o No.")

        current_wrong_answer = self.tree.get_current_text().strip().lower()
        normalized_correct_answer = correct_answer.strip().lower()

        if normalized_correct_answer == current_wrong_answer:
            raise ValueError("La respuesta correcta no puede ser igual a la respuesta incorrecta anterior.")

    # Aprende una nueva respuesta, actualiza el árbol y guarda automáticamente.
    # Entradas: respuesta correcta, nueva pregunta y respuesta esperada para la correcta.
    # Salidas: True si guardó correctamente; False si ocurrió error al guardar.
    def learn(self, correct_answer, new_question, answer_for_correct):
        correct_answer = correct_answer.strip()
        new_question = new_question.strip()

        self.validate_learning_data(correct_answer, new_question, answer_for_correct)

        if not new_question.endswith("?"):
            new_question = new_question + "?"

        self.tree.learn(correct_answer, new_question, answer_for_correct)

        return self.save_game()
    
    # Guarda el árbol actual en el archivo configurado.
    # Entradas: ninguna.
    # Salidas: True si guardó correctamente; False si ocurrió error.
    def save_game(self):
        return self.storage.save_tree(self.tree)

    # Carga un nuevo árbol desde una ruta seleccionada por el usuario.
    # Entradas: ruta del archivo JSON seleccionado.
    # Salidas: True si cargó correctamente; False si usó árbol por defecto.
    def load_tree_from_file(self, file_path):
        self.storage = TreeStorage(file_path)
        self.tree = self.storage.load_tree()

        return self.storage.last_load_success

    # Obtiene el mensaje del último intento de carga.
    # Entradas: ninguna.
    # Salidas: mensaje descriptivo sobre la última carga de archivo.
    def get_last_load_message(self):
        return self.storage.last_load_message


# =========================
# INTERFAZ GRÁFICA
# =========================

class AppWindow(tk.Tk):

    # Inicializa la ventana principal de la aplicación.
    # Entradas: ninguna.
    # Salidas: ninguna; crea la ventana y muestra pantalla inicial.
    def __init__(self):
        super().__init__()

        self.controller = GameController()
        self.game_mode = "question"
        self.last_wrong_answer = ""

        self.title("Árbol de Decisión Interactivo")
        self.geometry("650x500")
        self.resizable(False, False)

        self.build_home_screen()

    # Elimina todos los elementos visuales actuales de la ventana.
    # Entradas: ninguna.
    # Salidas: ninguna; limpia la interfaz.
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Construye la pantalla inicial de la aplicación.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra título, instrucciones y botones principales.
    def build_home_screen(self):
        self.clear_window()

        title_label = tk.Label(
            self,
            text="Adivina en qué estoy pensando",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=25)

        instructions_label = tk.Label(
            self,
            text="Piensa en un elemento y responde únicamente con Sí o No.\n"
                 "El sistema intentará adivinarlo usando un árbol de decisión.\n"
                 "Si falla, puedes enseñarle una nueva respuesta.",
            font=("Arial", 12),
            justify="center"
        )
        instructions_label.pack(pady=15)

        start_button = tk.Button(
            self,
            text="Iniciar partida",
            width=28,
            command=self.start_game
        )
        start_button.pack(pady=8)

        load_button = tk.Button(
            self,
            text="Cargar árbol desde archivo",
            width=28,
            command=self.load_tree_file
        )
        load_button.pack(pady=8)

        exit_button = tk.Button(
            self,
            text="Salir",
            width=28,
            command=self.destroy
        )
        exit_button.pack(pady=8)

    # Permite seleccionar un archivo JSON y cargar un árbol.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra si la carga fue correcta o si hubo error.
    def load_tree_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de árbol",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )

        if file_path == "":
            return

        loaded_successfully = self.controller.load_tree_from_file(file_path)
        message = self.controller.get_last_load_message()

        if loaded_successfully:
            messagebox.showinfo("Archivo cargado", message)
        else:
            messagebox.showwarning("Error al cargar archivo", message)

    # Inicia una partida nueva desde la raíz del árbol.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra la pantalla de juego.
    def start_game(self):
        self.controller.start_game()
        self.game_mode = "question"
        self.build_game_screen()

    # Construye la pantalla principal de preguntas y respuestas.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra el texto actual y botones Sí/No.
    def build_game_screen(self):
        self.clear_window()

        self.status_label = tk.Label(
            self,
            text="Responde la siguiente pregunta:",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=20)

        self.question_label = tk.Label(
            self,
            text="",
            font=("Arial", 18, "bold"),
            wraplength=560,
            justify="center"
        )
        self.question_label.pack(pady=25)

        yes_button = tk.Button(
            self,
            text="Sí",
            width=18,
            command=self.answer_yes_click
        )
        yes_button.pack(pady=5)

        no_button = tk.Button(
            self,
            text="No",
            width=18,
            command=self.answer_no_click
        )
        no_button.pack(pady=5)

        home_button = tk.Button(
            self,
            text="Volver al inicio",
            width=18,
            command=self.build_home_screen
        )
        home_button.pack(pady=20)

        self.update_game_text()

    # Actualiza el texto mostrado según el nodo actual del árbol.
    # Entradas: ninguna.
    # Salidas: ninguna; actualiza etiquetas y modo de juego.
    def update_game_text(self):
        current_text = self.controller.get_current_text()

        if self.controller.is_current_leaf():
            self.game_mode = "guess"
            self.status_label.config(text="Creo que ya sé la respuesta:")
            self.question_label.config(text=f"¿Estabas pensando en {current_text}?")
        else:
            self.game_mode = "question"
            self.status_label.config(text="Responde la siguiente pregunta:")
            self.question_label.config(text=current_text)

    # Procesa el clic del botón Sí.
    # Entradas: ninguna.
    # Salidas: ninguna; procesa la respuesta positiva.
    def answer_yes_click(self):
        self.process_answer("si")

    # Procesa el clic del botón No.
    # Entradas: ninguna.
    # Salidas: ninguna; procesa la respuesta negativa.
    def answer_no_click(self):
        self.process_answer("no")

    # Decide cómo procesar la respuesta según el modo actual.
    # Entradas: respuesta normalizada "si" o "no".
    # Salidas: ninguna; avanza, gana o muestra formulario de aprendizaje.
    def process_answer(self, answer):
        if self.game_mode == "question":
            self.handle_question_answer(answer)
        elif self.game_mode == "guess":
            self.handle_guess_answer(answer)

    # Procesa una respuesta dada a un nodo de pregunta.
    # Entradas: respuesta normalizada "si" o "no".
    # Salidas: ninguna; avanza en el árbol y actualiza la pantalla.
    def handle_question_answer(self, answer):
        self.controller.answer_question(answer)
        self.update_game_text()

    # Procesa una respuesta dada a una adivinanza final.
    # Entradas: respuesta normalizada "si" o "no".
    # Salidas: ninguna; muestra victoria o formulario de aprendizaje.
    def handle_guess_answer(self, answer):
        if answer == "si":
            messagebox.showinfo("Resultado", "¡Gané! Adiviné correctamente.")
            self.show_end_options("¡Gané! Adiviné correctamente.")
        else:
            self.last_wrong_answer = self.controller.get_current_text()
            self.build_learning_screen()

    # Construye el formulario de aprendizaje cuando el sistema falla.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra campos para enseñar una nueva respuesta.
    def build_learning_screen(self):
        self.clear_window()

        title_label = tk.Label(
            self,
            text="Ayúdame a aprender",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)

        info_label = tk.Label(
            self,
            text=f"No logré adivinar. Mi respuesta incorrecta fue: {self.last_wrong_answer}",
            font=("Arial", 11),
            wraplength=560,
            justify="center"
        )
        info_label.pack(pady=10)

        correct_label = tk.Label(
            self,
            text="¿Cuál era la respuesta correcta?",
            font=("Arial", 11)
        )
        correct_label.pack(pady=5)

        self.correct_answer_entry = tk.Entry(self, width=50)
        self.correct_answer_entry.pack(pady=5)

        question_label = tk.Label(
            self,
            text="Escribe una pregunta que diferencie ambas respuestas:",
            font=("Arial", 11)
        )
        question_label.pack(pady=5)

        self.new_question_entry = tk.Entry(self, width=50)
        self.new_question_entry.pack(pady=5)

        option_label = tk.Label(
            self,
            text="Para la respuesta correcta, ¿la respuesta a esa pregunta sería Sí o No?",
            font=("Arial", 11),
            wraplength=560,
            justify="center"
        )
        option_label.pack(pady=10)

        self.answer_for_correct_var = tk.StringVar(value="si")

        yes_radio = tk.Radiobutton(
            self,
            text="Sí",
            variable=self.answer_for_correct_var,
            value="si"
        )
        yes_radio.pack()

        no_radio = tk.Radiobutton(
            self,
            text="No",
            variable=self.answer_for_correct_var,
            value="no"
        )
        no_radio.pack()

        learn_button = tk.Button(
            self,
            text="Guardar aprendizaje",
            width=25,
            command=self.save_learning_click
        )
        learn_button.pack(pady=15)

        cancel_button = tk.Button(
            self,
            text="Cancelar y volver al inicio",
            width=25,
            command=self.build_home_screen
        )
        cancel_button.pack(pady=5)

    # Guarda la información ingresada en el formulario de aprendizaje.
    # Entradas: ninguna.
    # Salidas: ninguna; valida, aprende, guarda y muestra resultado.
    def save_learning_click(self):
        correct_answer = self.correct_answer_entry.get()
        new_question = self.new_question_entry.get()
        answer_for_correct = self.answer_for_correct_var.get()

        try:
            saved = self.controller.learn(correct_answer, new_question, answer_for_correct)

            if saved:
                messagebox.showinfo(
                    "Aprendizaje guardado",
                    "¡Gracias! Aprendí algo nuevo y el árbol se guardó correctamente."
                )
            else:
                messagebox.showwarning(
                    "Aprendizaje parcial",
                    "Aprendí la nueva respuesta, pero ocurrió un error al guardar el archivo."
                )

            self.show_end_options("Aprendizaje completado.")

        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error))

    # Muestra opciones después de ganar o aprender.
    # Entradas: mensaje que se mostrará como resultado final.
    # Salidas: ninguna; muestra botones para nueva partida, inicio o salir.
    def show_end_options(self, result_message):
        self.clear_window()

        result_label = tk.Label(
            self,
            text=result_message,
            font=("Arial", 18, "bold"),
            wraplength=560,
            justify="center"
        )
        result_label.pack(pady=40)

        new_game_button = tk.Button(
            self,
            text="Nueva partida",
            width=22,
            command=self.start_game
        )
        new_game_button.pack(pady=10)

        home_button = tk.Button(
            self,
            text="Volver al inicio",
            width=22,
            command=self.build_home_screen
        )
        home_button.pack(pady=10)

        exit_button = tk.Button(
            self,
            text="Salir",
            width=22,
            command=self.destroy
        )
        exit_button.pack(pady=10)


# =========================
# MAIN
# =========================

# Ejecuta la aplicación gráfica principal.
# Entradas: ninguna.
# Salidas: ninguna; inicia el ciclo principal de Tkinter.
def main():
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()