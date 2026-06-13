import os
import pyttsx3

engine = pyttsx3.init()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def hablar(texto, lang):
    voices = engine.getProperty('voices')

    if lang == "es":
        for voice in voices:
            if "spanish" in voice.name.lower() or "es" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
    else:
        for voice in voices:
            if "english" in voice.name.lower() or "en" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break

    engine.say(texto)
    engine.runAndWait()

BANCO_PREGUNTAS = {
    "math": [
        {
            "en": {"q": "What is 7 * 8?", "a": "56", "b": "64", "c": "48", "d": "54"},
            "es": {"q": "¿Cuánto es 7 * 8?", "a": "56", "b": "64", "c": "48", "d": "54"}
        },
        {
            "en": {"q": "Solve: 15 - (3 * 4)", "a": "3", "b": "12", "c": "48", "d": "6"},
            "es": {"q": "Resuelve: 15 - (3 * 4)", "a": "3", "b": "12", "c": "48", "d": "6"}
        },
        {
            "en": {"q": "What is the square root of 81?", "a": "9", "b": "7", "c": "8", "d": "10"},
            "es": {"q": "¿Cuál es la raíz cuadrada de 81?", "a": "9", "b": "7", "c": "8", "d": "10"}
        },
        {
            "en": {"q": "Which number is prime?", "a": "13", "b": "4", "c": "9", "d": "15"},
            "es": {"q": "¿Qué número es primo?", "a": "13", "b": "4", "c": "9", "d": "15"}
        },
        {
            "en": {"q": "What is 120 / 4?", "a": "30", "b": "25", "c": "40", "d": "20"},
            "es": {"q": "¿Cuánto es 120 / 4?", "a": "30", "b": "25", "c": "40", "d": "20"}
        }
    ],
    "geography": [
        {
            "en": {"q": "What is the capital of France?", "a": "Paris", "b": "London", "c": "Madrid", "d": "Berlin"},
            "es": {"q": "¿Cuál es la capital de Francia?", "a": "París", "b": "Londres", "c": "Madrid", "d": "Berlín"}
        },
        {
            "en": {"q": "Which is the largest ocean on Earth?", "a": "Pacific Ocean", "b": "Atlantic Ocean", "c": "Indian Ocean", "d": "Arctic Ocean"},
            "es": {"q": "¿Cuál es el océano más grande de la Tierra?", "a": "Océano Pacífico", "b": "Océano Atlántico", "c": "Océano Índico", "d": "Océano Ártico"}
        },
        {
            "en": {"q": "In which continent is Egypt located?", "a": "Africa", "b": "Asia", "c": "Europe", "d": "America"},
            "es": {"q": "¿En qué continente se encuentra Egipto?", "a": "África", "b": "Asia", "c": "Europa", "d": "América"}
        },
        {
            "en": {"q": "What is the longest river in the world?", "a": "Amazon River", "b": "Nile", "c": "Mississippi", "d": "Yangtze"},
            "es": {"q": "¿Cuál es el río más largo del mundo?", "a": "Río Amazonas", "b": "Nilo", "c": "Misisipi", "d": "Yangtsé"}
        },
        {
            "en": {"q": "Which country has the most population?", "a": "India", "b": "China", "c": "USA", "d": "Russia"},
            "es": {"q": "¿Qué país tiene mayor población?", "a": "India", "b": "China", "c": "EE.UU.", "d": "Rusia"}
        }
    ],
    "english": [
        {
            "en": {"q": "What is the past tense of 'GO'?", "a": "Went", "b": "Goed", "c": "Gone", "d": "Going"},
            "es": {"q": "¿Cuál es el pasado del verbo 'GO'?", "a": "Went", "b": "Goed", "c": "Gone", "d": "Going"}
        },
        {
            "en": {"q": "Choose the plural of 'Child':", "a": "Children", "b": "Childs", "c": "Childrens", "d": "Childes"},
            "es": {"q": "Elige el plural de 'Child':", "a": "Children", "b": "Childs", "c": "Childrens", "d": "Childes"}
        },
        {
            "en": {"q": "Complete: She ___ a doctor.", "a": "is", "b": "are", "c": "am", "d": "be"},
            "es": {"q": "Completa: She ___ a doctor.", "a": "is", "b": "are", "c": "am", "d": "be"}
        },
        {
            "en": {"q": "What is the antonym of 'Beautiful'?", "a": "Ugly", "b": "Pretty", "c": "Smart", "d": "Short"},
            "es": {"q": "¿Cuál es el antónimo de 'Beautiful'?", "a": "Ugly", "b": "Pretty", "c": "Smart", "d": "Short"}
        },
        {
            "en": {"q": "Which word is a noun?", "a": "Table", "b": "Run", "c": "Beautifully", "d": "Under"},
            "es": {"q": "¿Qué palabra es un sustantivo?", "a": "Table", "b": "Run", "c": "Beautifully", "d": "Under"}
        }
    ]
}

def mainscreen(lang):
    limpiar_pantalla()

    if lang == "en":
        print("------ You VS Teacher ------")
        print("- 1. Play                  -")
        print("- 2. Settings              -")
        print("- 3. Quit                  -")
        print("------ -------------- ------")

        hablar(
            "You VS Teacher. One, Play. Two, Settings. Three, Quit. Choose an option.",
            lang
        )
        chosen = input("Choose an option: ")
    else:
        print("------ Tú VS Profesor ------")
        print("- 1. Jugar                 -")
        print("- 2. Configuración         -")
        print("- 3. Salir                 -")
        print("------ -------------- ------")

        hablar(
            "Tú contra Profesor. Uno, Jugar. Dos, Configuración. Tres, Salir. Escoge una opción.",
            lang
        )
        chosen = input("Escoge una opción: ")

    if chosen == "1":
        return "game", lang
    elif chosen == "2":
        return "config", lang
    elif chosen == "3":
        return "quit", lang

    return "menu", lang

def config(lang):
    limpiar_pantalla()

    if lang == "en":
        print("--------- Settings ---------")
        print("- 1. Change Language       -")
        print("- 2. Blind Mode            -")
        print("- 3. Back                  -")
        print("------ -------------- ------")

        hablar(
            "Settings. One, Change Language. Two, Blind Mode. Three, Back. Choose an option.",
            lang
        )

        chosen = input("Choose an option: ")

        if chosen == "1":
            hablar("Choose a language: en or es", lang)
            new_lang = input("Choose a language (en/es): ").strip().lower()

            if new_lang in ["en", "es"]:
                return new_lang

        elif chosen == "2":
            print("Blind mode activated.")
            hablar("Blind mode activated.", lang)
            input("\nPress Enter to continue...")
    else:
        print("------ Configuración -------")
        print("- 1. Cambiar Idioma        -")
        print("- 2. Modo Ciego            -")
        print("- 3. Volver                -")
        print("------ -------------- ------")

        hablar(
            "Configuración. Uno, Cambiar Idioma. Dos, Modo Ciego. Tres, Volver. Escoge una opción.",
            lang
        )

        chosen = input("Escoge una opción: ")

        if chosen == "1":
            hablar("Elige un idioma: en o es", lang)
            new_lang = input("Elige un idioma (en/es): ").strip().lower()

            if new_lang in ["en", "es"]:
                return new_lang

        elif chosen == "2":
            print("Modo ciego activado.")
            hablar("Modo ciego activado.", lang)
            input("\nPresiona Enter para continuar...")

    return lang

def game(lang):
    limpiar_pantalla()

    if lang == "en":
        print("--------- Gamemode ---------")
        print("- 1. Math                  -")
        print("- 2. Geography             -")
        print("- 3. English               -")
        print("- 4. Back                  -")
        print("------ -------------- ------")

        hablar(
            "Gamemode. One, Math. Two, Geography. Three, English. Four, Back. Choose an option.",
            lang
        )

        chosen = input("Choose an option: ")
    else:
        print("------ Modo de Juego -------")
        print("- 1. Matemáticas           -")
        print("- 2. Geografía             -")
        print("- 3. Inglés                -")
        print("- 4. Volver                -")
        print("------ -------------- ------")

        hablar(
            "Modo de juego. Uno, Matemáticas. Dos, Geografía. Tres, Inglés. Cuatro, Volver. Escoge una opción.",
            lang
        )

        chosen = input("Escoge una opción: ")

    categorias = {
        "1": "math",
        "2": "geography",
        "3": "english"
    }

    if chosen in categorias:
        categoria_seleccionada = categorias[chosen]
        preguntas = BANCO_PREGUNTAS[categoria_seleccionada]

        for i, pregunta in enumerate(preguntas):
            limpiar_pantalla()

            datos_idioma = pregunta[lang]

            print(
                f"--- {lang.upper()} - Question {i+1}/5 ---"
                if lang == "en"
                else f"--- {lang.upper()} - Pregunta {i+1}/5 ---"
            )

            print(f"\n{datos_idioma['q']}\n")
            print(f"A) {datos_idioma['a']}")
            print(f"B) {datos_idioma['b']}")
            print(f"C) {datos_idioma['c']}")
            print(f"D) {datos_idioma['d']}")

            texto_a_leer = (
                f"{datos_idioma['q']}. "
                f"Option A: {datos_idioma['a']}. "
                f"Option B: {datos_idioma['b']}. "
                f"Option C: {datos_idioma['c']}. "
                f"Option D: {datos_idioma['d']}."
            )

            hablar(texto_a_leer, lang)

            hablar(
                "Choose A, B, C or D"
                if lang == "en"
                else "Elige A, B, C o D",
                lang
            )

            input(
                "\nChoose A, B, C or D: "
                if lang == "en"
                else "\nElige A, B, C o D: "
            )

def main():
    idioma_actual = "es"

    while True:
        estado, idioma_actual = mainscreen(idioma_actual)

        if estado == "quit":
            print("Goodbye!" if idioma_actual == "en" else "¡Adiós!")
            hablar(
                "Goodbye!"
                if idioma_actual == "en"
                else "¡Adiós!",
                idioma_actual
            )
            break

        elif estado == "config":
            idioma_actual = config(idioma_actual)

        elif estado == "game":
            game(idioma_actual)

if __name__ == "__main__":
    main()
