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
# ESTILOS VISUALES
# =========================
BACKGROUND_COLOR = "#100B24"
CARD_COLOR = "#201238"
CARD_DARK_COLOR = "#160C2B"
CARD_LIGHT_COLOR = "#2B1A4A"

PRIMARY_COLOR = "#F4C542"
PRIMARY_HOVER_COLOR = "#DFAE24"

SUCCESS_COLOR = "#22C55E"
SUCCESS_HOVER_COLOR = "#16A34A"

SECONDARY_COLOR = "#7C3AED"
SECONDARY_HOVER_COLOR = "#6D28D9"

DANGER_COLOR = "#EF4444"
DANGER_HOVER_COLOR = "#DC2626"

NEUTRAL_COLOR = "#3B2B5B"
NEUTRAL_HOVER_COLOR = "#4C3A72"

TEXT_COLOR = "#F8FAFC"
SECONDARY_TEXT_COLOR = "#C9BFE8"
MUTED_TEXT_COLOR = "#9A8FBD"

INPUT_COLOR = "#F8F5EF"
INPUT_TEXT_COLOR = "#1C1630"
BORDER_COLOR = "#59487A"

FONT_TITLE = ("Arial", 27, "bold")
FONT_SECTION_TITLE = ("Arial", 21, "bold")
FONT_SUBTITLE = ("Arial", 12)
FONT_LABEL = ("Arial", 12, "bold")
FONT_TEXT = ("Arial", 11)
FONT_QUESTION = ("Arial", 21, "bold")
FONT_BUTTON = ("Arial", 12, "bold")
FONT_SMALL = ("Arial", 10)

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


# -------------------
# INTERFAZ GRÁFICA
# ------------------
class AppWindow(tk.Tk):

    # Inicializa la ventana principal de la aplicación.
    # Entradas: ninguna.
    # Salidas: ninguna; crea la ventana y muestra la pantalla inicial.
    def __init__(self):
        super().__init__()

        self.controller = GameController()
        self.game_mode = "question"
        self.last_wrong_answer = ""

        self.title("Árbol de Decisión Interactivo")
        self.geometry("860x700")
        self.resizable(False, False)
        self.configure(bg=BACKGROUND_COLOR)

        self.build_home_screen()

    # Elimina todos los elementos actuales de la ventana.
    # Entradas: ninguna.
    # Salidas: ninguna; limpia la interfaz.
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Crea la tarjeta principal de cada pantalla.
    # Entradas: ancho y alto opcionales de la tarjeta.
    # Salidas: frame central con borde y fondo configurado.
    def create_card(self, width=790, height=635):
        card = tk.Frame(
            self,
            bg=CARD_COLOR,
            width=width,
            height=height,
            highlightbackground=BORDER_COLOR,
            highlightthickness=2
        )
        card.pack_propagate(False)
        card.pack(expand=True)

        return card

    # Crea el encabezado principal de la aplicación.
    # Entradas: contenedor donde se agregará el encabezado.
    # Salidas: ninguna; agrega título y línea decorativa.
    def create_header(self, parent):
        header = tk.Frame(parent, bg=CARD_COLOR)
        header.pack(fill="x", pady=(22, 12))

        title = tk.Label(
            header,
            text="Genio Adivinador",
            font=FONT_TITLE,
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        title.pack()

        divider_frame = tk.Frame(header, bg=CARD_COLOR)
        divider_frame.pack(pady=(12, 0))

        left_line = tk.Frame(divider_frame, bg=PRIMARY_COLOR, width=110, height=2)
        left_line.grid(row=0, column=0, padx=12)

        center_mark = tk.Label(
            divider_frame,
            text="◇",
            font=("Arial", 16, "bold"),
            bg=CARD_COLOR,
            fg=PRIMARY_COLOR
        )
        center_mark.grid(row=0, column=1)

        right_line = tk.Frame(divider_frame, bg=PRIMARY_COLOR, width=110, height=2)
        right_line.grid(row=0, column=2, padx=12)

    # Crea una etiqueta reutilizable para la interfaz.
    # Entradas: contenedor, texto, fuente, color y separación vertical.
    # Salidas: objeto Label agregado al contenedor.
    def create_label(self, parent, text, font, color=TEXT_COLOR, pady=5):
        label = tk.Label(
            parent,
            text=text,
            font=font,
            bg=CARD_COLOR,
            fg=color,
            wraplength=640,
            justify="center"
        )
        label.pack(pady=pady)

        return label

    # Crea un botón reutilizable con estilo visual.
    # Entradas: contenedor, texto, comando, color, color activo, color de texto y ancho.
    # Salidas: objeto Button agregado al contenedor.
    def create_button(self, parent, text, command, bg_color, active_color, fg_color=TEXT_COLOR, width=24):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            height=2,
            bg=bg_color,
            fg=fg_color,
            activebackground=active_color,
            activeforeground=fg_color,
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=4
        )
        button.pack(pady=8)

        return button

    # Crea un campo de entrada con etiqueta.
    # Entradas: contenedor y texto de la etiqueta.
    # Salidas: objeto Entry creado para capturar información.
    def create_input_field(self, parent, label_text):
        label = tk.Label(
            parent,
            text=label_text,
            font=FONT_LABEL,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            anchor="w"
        )
        label.pack(fill="x", padx=68, pady=(14, 6))

        entry = tk.Entry(
            parent,
            width=58,
            font=FONT_TEXT,
            bg=INPUT_COLOR,
            fg=INPUT_TEXT_COLOR,
            relief="flat",
            insertbackground=INPUT_TEXT_COLOR
        )
        entry.pack(ipady=9)

        return entry

    # Construye la pantalla inicial de la aplicación.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra título, descripción mínima y botones principales.
    # Construye la pantalla inicial de la aplicación.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra título, descripción mínima y botones principales.
    def build_home_screen(self):
        self.clear_window()

        card = self.create_card()
        self.create_header(card)

        content = tk.Frame(card, bg=CARD_COLOR)
        content.pack(expand=True)

        buttons_frame = tk.Frame(content, bg=CARD_COLOR)
        buttons_frame.pack(pady=22)

        self.create_button(
            buttons_frame,
            "Iniciar partida",
            self.start_game,
            SUCCESS_COLOR,
            SUCCESS_HOVER_COLOR,
            "#052E16",
            36
        )

        self.create_button(
            buttons_frame,
            "Cargar árbol desde archivo",
            self.load_tree_file,
            SECONDARY_COLOR,
            SECONDARY_HOVER_COLOR,
            TEXT_COLOR,
            36
        )

        self.create_button(
            buttons_frame,
            "Salir",
            self.destroy,
            DANGER_COLOR,
            DANGER_HOVER_COLOR,
            TEXT_COLOR,
            36
        )

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

    # Construye la pantalla principal de preguntas.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra pregunta actual y botones de respuesta.
    def build_game_screen(self):
        self.clear_window()

        card = self.create_card()
        self.create_header(card)

        body = tk.Frame(card, bg=CARD_COLOR)
        body.pack(expand=True, fill="both")

        self.status_label = tk.Label(
            body,
            text="",
            font=FONT_SUBTITLE,
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT_COLOR
        )
        self.status_label.pack(pady=(16, 8))

        question_box = tk.Frame(
            body,
            bg=CARD_DARK_COLOR,
            highlightbackground=PRIMARY_COLOR,
            highlightthickness=1
        )
        question_box.pack(fill="x", padx=62, pady=20)

        self.question_label = tk.Label(
            question_box,
            text="",
            font=FONT_QUESTION,
            bg=CARD_DARK_COLOR,
            fg=TEXT_COLOR,
            wraplength=590,
            justify="center",
            pady=34
        )
        self.question_label.pack(fill="x")

        answer_frame = tk.Frame(body, bg=CARD_COLOR)
        answer_frame.pack(pady=18)

        yes_button = tk.Button(
            answer_frame,
            text="Sí",
            width=18,
            height=2,
            command=self.answer_yes_click,
            bg="#22C55E",
            fg="#1C1630",
            activebackground=NEUTRAL_HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0
        )
        yes_button.grid(row=0, column=0, padx=12)

        no_button = tk.Button(
            answer_frame,
            text="No",
            width=18,
            height=2,
            command=self.answer_no_click,
            bg="#EF4444",
            fg=TEXT_COLOR,
            activebackground=NEUTRAL_HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0
        )
        no_button.grid(row=0, column=1, padx=12)

        bottom_frame = tk.Frame(body, bg=CARD_COLOR)
        bottom_frame.pack(pady=12)

        self.create_button(
            bottom_frame,
            "Volver al inicio",
            self.build_home_screen,
            NEUTRAL_COLOR,
            NEUTRAL_HOVER_COLOR,
            TEXT_COLOR,
            22
        )

        self.update_game_text()

    # Actualiza el texto mostrado según el nodo actual.
    # Entradas: ninguna.
    # Salidas: ninguna; cambia entre modo pregunta y modo adivinanza.
    def update_game_text(self):
        current_text = self.controller.get_current_text()

        if self.controller.is_current_leaf():
            self.game_mode = "guess"
            self.status_label.config(text="Creo que ya sé la respuesta")
            self.question_label.config(text=f"¿Estabas pensando en {current_text}?")
        else:
            self.game_mode = "question"
            self.status_label.config(text="Pregunta")
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
    # Salidas: ninguna; avanza en el juego o finaliza la adivinanza.
    def process_answer(self, answer):
        if self.game_mode == "question":
            self.handle_question_answer(answer)
        elif self.game_mode == "guess":
            self.handle_guess_answer(answer)

    # Procesa una respuesta dada a una pregunta del árbol.
    # Entradas: respuesta normalizada "si" o "no".
    # Salidas: ninguna; avanza por el árbol y actualiza la pantalla.
    def handle_question_answer(self, answer):
        self.controller.answer_question(answer)
        self.update_game_text()

    # Procesa una respuesta dada a una adivinanza final.
    # Entradas: respuesta normalizada "si" o "no".
    # Salidas: ninguna; muestra pantalla final o formulario de aprendizaje.
    def handle_guess_answer(self, answer):
        if answer == "si":
            self.show_end_options("Adiviné correctamente")
        else:
            self.last_wrong_answer = self.controller.get_current_text()
            self.build_learning_screen()

    # Construye la pantalla de aprendizaje.
    # Entradas: ninguna.
    # Salidas: ninguna; muestra el formulario para agregar una nueva respuesta.
    def build_learning_screen(self):
        self.clear_window()

        card = self.create_card(height=650)
        self.create_header(card)

        body = tk.Frame(card, bg=CARD_COLOR)
        body.pack(fill="both", expand=True, padx=30)

        title_label = tk.Label(
            body,
            text="Nuevo aprendizaje",
            font=FONT_SECTION_TITLE,
            bg=CARD_COLOR,
            fg=PRIMARY_COLOR
        )
        title_label.pack(pady=(4, 5))

        underline = tk.Frame(body, bg=PRIMARY_COLOR, width=70, height=3)
        underline.pack(pady=(0, 10))

        previous_frame = tk.Frame(
            body,
            bg=CARD_LIGHT_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        previous_frame.pack(pady=(0, 10))

        previous_label = tk.Label(
            previous_frame,
            text=f"Respuesta anterior: {self.last_wrong_answer}",
            font=FONT_SUBTITLE,
            bg=CARD_LIGHT_COLOR,
            fg=SECONDARY_TEXT_COLOR,
            padx=20,
            pady=8
        )
        previous_label.pack()

        form_frame = tk.Frame(body, bg=CARD_COLOR)
        form_frame.pack(fill="x")

        self.correct_answer_entry = self.create_input_field(
            form_frame,
            "Respuesta correcta"
        )

        self.new_question_entry = self.create_input_field(
            form_frame,
            "Pregunta diferenciadora"
        )

        option_label = tk.Label(
            form_frame,
            text="Para la respuesta correcta, la respuesta a esa pregunta es:",
            font=FONT_LABEL,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            anchor="w"
        )
        option_label.pack(fill="x", padx=68, pady=(14, 8))

        self.answer_for_correct_var = tk.StringVar(value="si")

        options_frame = tk.Frame(form_frame, bg=CARD_COLOR)
        options_frame.pack(fill="x", padx=68, pady=(0, 12))

        yes_option = tk.Radiobutton(
            options_frame,
            text="Sí",
            variable=self.answer_for_correct_var,
            value="si",
            font=FONT_BUTTON,
            bg=CARD_DARK_COLOR,
            fg=PRIMARY_COLOR,
            selectcolor=CARD_DARK_COLOR,
            activebackground=CARD_DARK_COLOR,
            activeforeground=PRIMARY_COLOR,
            width=20,
            height=2,
            indicatoron=True,
            relief="flat"
        )
        yes_option.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        no_option = tk.Radiobutton(
            options_frame,
            text="No",
            variable=self.answer_for_correct_var,
            value="no",
            font=FONT_BUTTON,
            bg=CARD_DARK_COLOR,
            fg=TEXT_COLOR,
            selectcolor=CARD_DARK_COLOR,
            activebackground=CARD_DARK_COLOR,
            activeforeground=TEXT_COLOR,
            width=20,
            height=2,
            indicatoron=True,
            relief="flat"
        )
        no_option.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)

        footer = tk.Frame(
            card,
            bg=CARD_DARK_COLOR,
            height=96,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        footer.pack_propagate(False)
        footer.pack(side="bottom", fill="x")

        actions_frame = tk.Frame(footer, bg=CARD_DARK_COLOR)
        actions_frame.pack(expand=True)

        cancel_button = tk.Button(
            actions_frame,
            text="Cancelar",
            width=22,
            height=2,
            command=self.build_home_screen,
            bg=NEUTRAL_COLOR,
            fg=TEXT_COLOR,
            activebackground=NEUTRAL_HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=6
        )
        cancel_button.grid(row=0, column=0, padx=12)

        save_button = tk.Button(
            actions_frame,
            text="Guardar aprendizaje",
            width=26,
            height=2,
            command=self.save_learning_click,
            bg=PRIMARY_COLOR,
            fg="#1C1630",
            activebackground=PRIMARY_HOVER_COLOR,
            activeforeground="#1C1630",
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=6
        )
        save_button.grid(row=0, column=1, padx=12)

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
                    "Aprendizaje guardado correctamente."
                )
            else:
                messagebox.showwarning(
                    "Aprendizaje parcial",
                    "El árbol aprendió, pero ocurrió un error al guardar."
                )

            self.show_end_options("Aprendizaje guardado")

        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error))

    # Muestra opciones después de ganar o aprender.
    # Entradas: mensaje final que se mostrará.
    # Salidas: ninguna; muestra opciones para continuar o salir.
    def show_end_options(self, result_message):
        self.clear_window()

        card = self.create_card()
        self.create_header(card)

        content = tk.Frame(card, bg=CARD_COLOR)
        content.pack(expand=True)

        self.create_label(
            content,
            result_message,
            FONT_SECTION_TITLE,
            PRIMARY_COLOR,
            20
        )

        buttons_frame = tk.Frame(content, bg=CARD_COLOR)
        buttons_frame.pack(pady=28)

        new_game_button = tk.Button(
            buttons_frame,
            text="Nueva partida",
            width=28,
            height=2,
            command=self.start_game,
            bg=SUCCESS_COLOR,
            fg="#052E16",
            activebackground=SUCCESS_HOVER_COLOR,
            activeforeground="#052E16",
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=5
        )
        new_game_button.pack(pady=9)

        home_button = tk.Button(
            buttons_frame,
            text="Volver al inicio",
            width=28,
            height=2,
            command=self.build_home_screen,
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR,
            activebackground=SECONDARY_HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=5
        )
        home_button.pack(pady=9)

        exit_button = tk.Button(
            buttons_frame,
            text="Salir",
            width=28,
            height=2,
            command=self.destroy,
            bg=DANGER_COLOR,
            fg=TEXT_COLOR,
            activebackground=DANGER_HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=5
        )
        exit_button.pack(pady=9)

# -----
# MAIN
# -----

# Ejecuta la aplicación gráfica principal.
# Entradas: ninguna.
# Salidas: ninguna; inicia el ciclo principal de Tkinter.
def main():
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()