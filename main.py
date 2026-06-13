import os

def mainscreen(lang):
    if lang == "en":
        print("------ You VS Teacher ------")
        print("- 1. Play                  -")
        print("- 2. Settings              -")
        print("- 3. Quit                  -")
        print("------ -------------- ------")
        chosen = input("Choose an option: ")
        if chosen == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            game("en")
        elif chosen == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            config("en")
        else:
            return
        
        
    elif lang == "es":
        print("------ Tú VS Profesor ------")
        print("- 1. Jugar                 -")
        print("- 2. Configuracion         -")
        print("- 3. Salir                 -")
        print("------ -------------- ------")
        chosen = input("Escoje una opción: ")
        if chosen == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            game("es")
        elif chosen == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            config("es")
        elif chosen == "3":
            return

#--------------------------------------------------------

def config(lang):
    if lang == "en":
        print("--------- Settings ---------")
        print("- 1. Change Language       -")
        print("- 2. Blind Mode            -")
        print("- 3. Back                  -")
        print("------ -------------- ------")
        chosen = input("Choose an option: ")
        if chosen == "1":
            choosen = input("Choose a language (en/es): ")

        elif chosen == "2":
            print("Blind mode activated.")
        else:
            return
        
        
    elif lang == "es":
        print("------ Configuracion -------")
        print("- 1. Jugar                 -")
        print("- 2. Configuracion         -")
        print("- 3. Salir                 -")
        print("------ -------------- ------")
        chosen = input("Escoje una opción: ")
        if chosen == "1":
            print("Empezando juego...")
        elif chosen == "2":
                os.system('cls' if os.name == 'nt' else 'clear')
                config("es")
        elif chosen == "3":
            return

#--------------------------------------------------------

def game(lang):
    if lang == "en":
        print("--------- Gamemode ---------")
        print("- 1. Math                  -")
        print("- 2. Geography             -")
        print("- 3. English               -")
        print("------ -------------- ------")
        chosen = input("Choose an option: ")
        if chosen == "1":
           a
        
        
    elif lang == "es":
        print("------ Configuracion -------")
        print("- 1. Jugar                 -")
        print("- 2. Configuracion         -")
        print("- 3. Salir                 -")
        print("------ -------------- ------")
        chosen = input("Escoje una opción: ")
        if chosen == "1":
            print("Empezando juego...")
        elif chosen == "2":
                os.system('cls' if os.name == 'nt' else 'clear')
                config("es")
        elif chosen == "3":
            return
        
    i = 0
    while i < 10:
        if lang=="en":
            os.system('cls' if os.name == 'nt' else 'clear')
            question("en")
        elif lang=="es":
            os.system('cls' if os.name == 'nt' else 'clear')
            question("es")
        i += 1



#--------------------------------------------------------

def question_geography(lang):
    if lang == "en":
        print("Question: ")
        print("A. Answer 1")
        print("B. Answer 2")
        print("C. Answer 3")
        print("D. Answer 4")