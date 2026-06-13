import pygame
import pyttsx3
import requests
import threading
import random
import sys

pygame.init()

# =====================================
# CONFIG
# =====================================

WIDTH = 1200
HEIGHT = 700

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You VS Teacher")

CLOCK = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("arial", 48)
FONT = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)

WHITE = (255,255,255)
BLACK = (20,20,20)
GRAY = (50,50,50)
LIGHT_GRAY = (90,90,90)
GREEN = (50,180,80)
RED = (220,60,60)
BLUE = (50,120,220)

API_GET = "https://jsonplaceholder.typicode.com/todos/1"
API_POST = "https://jsonplaceholder.typicode.com/posts"

# =====================================
# TEXTS
# =====================================

TEXTS = {

    "es": {

        "title": "Tú VS Profesor",

        "play": "Jugar",

        "settings": "Configuración",

        "stats": "Estadísticas",

        "quit": "Salir",

        "language": "Idioma",

        "blind": "Modo Ciego",

        "back": "Volver",

        "math": "Matemáticas",

        "geo": "Geografía",

        "english": "Inglés",

        "correct": "Correcto",

        "wrong": "Incorrecto",

        "score": "Puntuación",

        "choose": "Elige una respuesta",

        "finalscore": "Puntuación Final",

        "send": "Enviar Resultado"

    },

    "en": {

        "title": "You VS Teacher",

        "play": "Play",

        "settings": "Settings",

        "stats": "Statistics",

        "quit": "Quit",

        "language": "Language",

        "blind": "Blind Mode",

        "back": "Back",

        "math": "Math",

        "geo": "Geography",

        "english": "English",

        "correct": "Correct",

        "wrong": "Wrong",

        "score": "Score",

        "choose": "Choose an answer",

        "finalscore": "Final Score",

        "send": "Send Score"

    }
}

# =====================================
# QUESTIONS
# =====================================

QUESTIONS = {

    "math":[

        {
            "correct":"A",

            "es":{
                "q":"¿Cuánto es 7 x 8?",
                "A":"56",
                "B":"64",
                "C":"72",
                "D":"54"
            },

            "en":{
                "q":"What is 7 x 8?",
                "A":"56",
                "B":"64",
                "C":"72",
                "D":"54"
            }
        },

        {
            "correct":"D",

            "es":{
                "q":"¿Cuánto es 25 / 5?",
                "A":"4",
                "B":"6",
                "C":"10",
                "D":"5"
            },

            "en":{
                "q":"What is 25 / 5?",
                "A":"4",
                "B":"6",
                "C":"10",
                "D":"5"
            }
        },

        {
            "correct":"B",

            "es":{
                "q":"Raíz cuadrada de 81",
                "A":"8",
                "B":"9",
                "C":"10",
                "D":"11"
            },

            "en":{
                "q":"Square root of 81",
                "A":"8",
                "B":"9",
                "C":"10",
                "D":"11"
            }
        }

    ],

    "geo":[

        {
            "correct":"A",

            "es":{
                "q":"Capital de Francia",
                "A":"París",
                "B":"Madrid",
                "C":"Roma",
                "D":"Berlín"
            },

            "en":{
                "q":"Capital of France",
                "A":"Paris",
                "B":"Madrid",
                "C":"Rome",
                "D":"Berlin"
            }
        },

        {
            "correct":"C",

            "es":{
                "q":"Océano más grande",
                "A":"Atlántico",
                "B":"Índico",
                "C":"Pacífico",
                "D":"Ártico"
            },

            "en":{
                "q":"Largest ocean",
                "A":"Atlantic",
                "B":"Indian",
                "C":"Pacific",
                "D":"Arctic"
            }
        }

    ],

    "english":[

        {
            "correct":"A",

            "es":{
                "q":"Pasado de GO",
                "A":"Went",
                "B":"Goed",
                "C":"Gone",
                "D":"Going"
            },

            "en":{
                "q":"Past tense of GO",
                "A":"Went",
                "B":"Goed",
                "C":"Gone",
                "D":"Going"
            }
        },

        {
            "correct":"B",

            "es":{
                "q":"Plural de Child",
                "A":"Childs",
                "B":"Children",
                "C":"Childrens",
                "D":"Childes"
            },

            "en":{
                "q":"Plural of Child",
                "A":"Childs",
                "B":"Children",
                "C":"Childrens",
                "D":"Childes"
            }
        }

    ]
}

# =====================================
# TTS
# =====================================

class TTS:

    def __init__(self):

        self.engine = pyttsx3.init()
        self.enabled = False
        self.lang = "es"

    def set_language(self, lang):

        self.lang = lang

        for voice in self.engine.getProperty("voices"):

            name = voice.name.lower()
            vid = voice.id.lower()

            if lang == "es":

                if "spanish" in name or "es" in vid:
                    self.engine.setProperty("voice", voice.id)
                    return

            else:

                if "english" in name or "en" in vid:
                    self.engine.setProperty("voice", voice.id)
                    return

    def speak(self,text):

        if not self.enabled:
            return

        def run():

            self.engine.say(text)
            self.engine.runAndWait()

        threading.Thread(
            target=run,
            daemon=True
        ).start()

tts = TTS()

# =====================================
# API
# =====================================

def get_online_stats():

    try:

        r = requests.get(
            API_GET,
            timeout=5
        )

        return r.json()

    except:

        return {
            "title":"Offline"
        }

def post_score(score):

    payload = {
        "player":"Anonymous",
        "score":score
    }

    try:

        r = requests.post(
            API_POST,
            json=payload,
            timeout=5
        )

        return r.status_code

    except:
        return 0

# =====================================
# BUTTON
# =====================================

class Button:

    def __init__(
        self,
        x,
        y,
        w,
        h,
        text
    ):

        self.rect = pygame.Rect(
            x,
            y,
            w,
            h
        )

        self.text = text

    def draw(self):

        mouse = pygame.mouse.get_pos()

        color = GRAY

        if self.rect.collidepoint(mouse):
            color = LIGHT_GRAY

        pygame.draw.rect(
            SCREEN,
            color,
            self.rect,
            border_radius=12
        )

        label = FONT.render(
            self.text,
            True,
            WHITE
        )

        SCREEN.blit(
            label,
            (
                self.rect.centerx -
                label.get_width()//2,

                self.rect.centery -
                label.get_height()//2
            )
        )

    def clicked(self,event):

        return (

            event.type == pygame.MOUSEBUTTONDOWN

            and

            event.button == 1

            and

            self.rect.collidepoint(
                event.pos
            )

        )

# =====================================
# GAME
# =====================================

class Game:

    def __init__(self):

        self.lang = "es"
        self.state = "menu"

        self.score = 0
        self.current_category = None
        self.current_question = 0
        self.questions = []
        self.stats_data = None

        # ========================
        # BUTTONS (INIT ONCE)
        # ========================
        self.play_btn = Button(450,180,300,60,"")
        self.settings_btn = Button(450,270,300,60,"")
        self.stats_btn = Button(450,360,300,60,"")
        self.quit_btn = Button(450,450,300,60,"")

        self.lang_btn = Button(400,200,400,60,"")
        self.blind_btn = Button(400,300,400,60,"")
        self.back_btn = Button(400,450,400,60,"")

        self.math_btn = Button(400,180,400,60,"")
        self.geo_btn = Button(400,280,400,60,"")
        self.eng_btn = Button(400,380,400,60,"")

        self.answerA = Button(250,250,700,60,"")
        self.answerB = Button(250,340,700,60,"")
        self.answerC = Button(250,430,700,60,"")
        self.answerD = Button(250,520,700,60,"")

        self.back_menu_btn = Button(400,500,400,60,"")

    # ==========================
    # TRANSLATION
    # ==========================
    def T(self, key):
        return TEXTS[self.lang][key]

    # ==========================
    # DRAW TITLE
    # ==========================
    def draw_title(self):

        title = FONT_BIG.render(self.T("title"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 50))

    # ==========================
    # MENU
    # ==========================
    def menu(self):

        SCREEN.fill(BLACK)
        self.draw_title()

        self.play_btn.text = self.T("play")
        self.settings_btn.text = self.T("settings")
        self.stats_btn.text = self.T("stats")
        self.quit_btn.text = self.T("quit")

        self.play_btn.draw()
        self.settings_btn.draw()
        self.stats_btn.draw()
        self.quit_btn.draw()

    # ==========================
    # SETTINGS
    # ==========================
    def settings(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("settings"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        blind_text = "ON" if tts.enabled else "OFF"

        self.lang_btn.text = f"{self.T('language')}: {self.lang.upper()}"
        self.blind_btn.text = f"{self.T('blind')}: {blind_text}"
        self.back_btn.text = self.T("back")

        self.lang_btn.draw()
        self.blind_btn.draw()
        self.back_btn.draw()

    # ==========================
    # STATS
    # ==========================
    def stats(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("stats"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        if self.stats_data is None:
            self.stats_data = get_online_stats()

        y = 180
        for k, v in self.stats_data.items():
            txt = FONT.render(f"{k}: {v}", True, WHITE)
            SCREEN.blit(txt, (120, y))
            y += 50

        self.back_btn.text = self.T("back")
        self.back_btn.draw()

    # ==========================
    # CATEGORY
    # ==========================
    def choose_category(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("play"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        self.math_btn.text = self.T("math")
        self.geo_btn.text = self.T("geo")
        self.eng_btn.text = self.T("english")
        self.back_btn.text = self.T("back")

        self.math_btn.draw()
        self.geo_btn.draw()
        self.eng_btn.draw()
        self.back_btn.draw()

    # ==========================
    # START GAME
    # ==========================
    def start_category(self, category):

        self.current_category = category
        self.questions = QUESTIONS[category][:]
        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0

        self.state = "question"
        self.read_current_question()

    # ==========================
    # QUESTION SCREEN
    # ==========================
    def question_screen(self):

        SCREEN.fill(BLACK)

        qdata = self.questions[self.current_question]
        q = qdata[self.lang]

        self.answerA.text = f"A) {q['A']}"
        self.answerB.text = f"B) {q['B']}"
        self.answerC.text = f"C) {q['C']}"
        self.answerD.text = f"D) {q['D']}"

        title = FONT.render(
            f"{self.current_question+1}/{len(self.questions)}",
            True,
            WHITE
        )
        SCREEN.blit(title, (50, 30))

        score_text = FONT.render(
            f"{self.T('score')}: {self.score}",
            True,
            GREEN
        )
        SCREEN.blit(score_text, (900, 30))

        question = FONT.render(q["q"], True, WHITE)
        SCREEN.blit(question, (WIDTH//2 - question.get_width()//2, 120))

        self.answerA.draw()
        self.answerB.draw()
        self.answerC.draw()
        self.answerD.draw()

    # ==========================
    # READ QUESTION (TTS)
    # ==========================
    def read_current_question(self):

        if not tts.enabled:
            return

        q = self.questions[self.current_question][self.lang]

        text = (
            f"{q['q']}. "
            f"A. {q['A']}. "
            f"B. {q['B']}. "
            f"C. {q['C']}. "
            f"D. {q['D']}."
        )

        tts.speak(text)

    # ==========================
    # ANSWER CHECK
    # ==========================
    def answer(self, letter):

        correct = self.questions[self.current_question]["correct"]

        if letter == correct:
            self.score += 1
            tts.speak(self.T("correct"))
        else:
            tts.speak(self.T("wrong"))

        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.state = "results"
            post_score(self.score)
        else:
            self.read_current_question()

    # ==========================
    # RESULTS
    # ==========================
    def results(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("finalscore"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        result = FONT_BIG.render(
            f"{self.score}/{len(self.questions)}",
            True,
            GREEN
        )
        SCREEN.blit(result, (WIDTH//2 - result.get_width()//2, 250))

        percent = int(self.score / len(self.questions) * 100)

        ptxt = FONT.render(f"{percent}%", True, WHITE)
        SCREEN.blit(ptxt, (WIDTH//2 - ptxt.get_width()//2, 350))

        self.back_menu_btn.text = self.T("back")
        self.back_menu_btn.draw()

    # ==========================
    # EVENTS
    # ==========================
    def handle_event(self, event):

        if self.state == "menu":

            if self.play_btn.clicked(event):
                self.state = "category"

            elif self.settings_btn.clicked(event):
                self.state = "settings"

            elif self.stats_btn.clicked(event):
                self.stats_data = get_online_stats()
                self.state = "stats"

            elif self.quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        elif self.state == "settings":

            if self.lang_btn.clicked(event):

                self.lang = "en" if self.lang == "es" else "es"
                tts.set_language(self.lang)

            elif self.blind_btn.clicked(event):

                tts.enabled = not tts.enabled
                if tts.enabled:
                    tts.set_language(self.lang)

            elif self.back_btn.clicked(event):
                self.state = "menu"

        elif self.state == "stats":

            if self.back_btn.clicked(event):
                self.state = "menu"

        elif self.state == "category":

            if self.math_btn.clicked(event):
                self.start_category("math")

            elif self.geo_btn.clicked(event):
                self.start_category("geo")

            elif self.eng_btn.clicked(event):
                self.start_category("english")

            elif self.back_btn.clicked(event):
                self.state = "menu"

        elif self.state == "question":

            if self.answerA.clicked(event):
                self.answer("A")
            elif self.answerB.clicked(event):
                self.answer("B")
            elif self.answerC.clicked(event):
                self.answer("C")
            elif self.answerD.clicked(event):
                self.answer("D")

        elif self.state == "results":

            if self.back_menu_btn.clicked(event):
                self.state = "menu"

    # ==========================
    # DRAW ROUTER
    # ==========================s
    def draw(self):

        if self.state == "menu":
            self.menu()

        elif self.state == "settings":
            self.settings()

        elif self.state == "stats":
            self.stats()

        elif self.state == "category":
            self.choose_category()

        elif self.state == "question":
            self.question_screen()

        elif self.state == "results":
            self.results()

    def __init__(self):

        self.lang = "es"
        self.state = "menu"

        self.score = 0
        self.current_category = None
        self.current_question = 0
        self.questions = []
        self.stats_data = None

        # ========================
        # BUTTONS (INIT ONCE)
        # ========================
        self.play_btn = Button(450,180,300,60,"")
        self.settings_btn = Button(450,270,300,60,"")
        self.stats_btn = Button(450,360,300,60,"")
        self.quit_btn = Button(450,450,300,60,"")

        self.lang_btn = Button(400,200,400,60,"")
        self.blind_btn = Button(400,300,400,60,"")
        self.back_btn = Button(400,450,400,60,"")

        self.math_btn = Button(400,180,400,60,"")
        self.geo_btn = Button(400,280,400,60,"")
        self.eng_btn = Button(400,380,400,60,"")

        self.answerA = Button(250,250,700,60,"")
        self.answerB = Button(250,340,700,60,"")
        self.answerC = Button(250,430,700,60,"")
        self.answerD = Button(250,520,700,60,"")

        self.back_menu_btn = Button(400,500,400,60,"")

    # ==========================
    # TRANSLATION
    # ==========================
    def T(self,key):
        return TEXTS[self.lang][key]

    # ==========================
    # MENU
    # ==========================
    def menu(self):

        SCREEN.fill(BLACK)
        self.draw_title()

        self.play_btn.text = self.T("play")
        self.settings_btn.text = self.T("settings")
        self.stats_btn.text = self.T("stats")
        self.quit_btn.text = self.T("quit")

        self.play_btn.draw()
        self.settings_btn.draw()
        self.stats_btn.draw()
        self.quit_btn.draw()

    # ==========================
    # SETTINGS
    # ==========================
    def settings(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("settings"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        blind_text = "ON" if tts.enabled else "OFF"

        self.lang_btn.text = f"{self.T('language')}: {self.lang.upper()}"
        self.blind_btn.text = f"{self.T('blind')}: {blind_text}"
        self.back_btn.text = self.T("back")

        self.lang_btn.draw()
        self.blind_btn.draw()
        self.back_btn.draw()

def handle_event(self, event):

    if self.state == "menu":

        if self.play_btn.clicked(event):
            self.state = "category"

        elif self.settings_btn.clicked(event):
            self.state = "settings"

        elif self.stats_btn.clicked(event):
            self.stats_data = get_online_stats()
            self.state = "stats"

        elif self.quit_btn.clicked(event):
            pygame.quit()
            sys.exit()

    elif self.state == "settings":

        if self.lang_btn.clicked(event):

            self.lang = "en" if self.lang == "es" else "es"
            tts.set_language(self.lang)

        elif self.blind_btn.clicked(event):

            tts.enabled = not tts.enabled
            if tts.enabled:
                tts.set_language(self.lang)

        elif self.back_btn.clicked(event):
            self.state = "menu"

    elif self.state == "stats":

        if self.back_btn.clicked(event):
            self.state = "menu"

    elif self.state == "category":

        if self.math_btn.clicked(event):
            self.start_category("math")

        elif self.geo_btn.clicked(event):
            self.start_category("geo")

        elif self.eng_btn.clicked(event):
            self.start_category("english")

        elif self.back_btn.clicked(event):
            self.state = "menu"

    elif self.state == "question":

        if self.answerA.clicked(event):
            self.answer("A")
        elif self.answerB.clicked(event):
            self.answer("B")
        elif self.answerC.clicked(event):
            self.answer("C")
        elif self.answerD.clicked(event):
            self.answer("D")

    elif self.state == "results":

        if self.back_menu_btn.clicked(event):
            self.state = "menu"

    # ==========================
    # STATS
    # ==========================
    def stats(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("stats"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        if self.stats_data is None:
            self.stats_data = get_online_stats()

        y = 180
        for k,v in self.stats_data.items():
            txt = FONT.render(f"{k}: {v}", True, WHITE)
            SCREEN.blit(txt,(120,y))
            y += 50

        self.back_btn.text = self.T("back")
        self.back_btn.draw()

    # ==========================
    # CATEGORY
    # ==========================
    def choose_category(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("play"), True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        self.math_btn.text = self.T("math")
        self.geo_btn.text = self.T("geo")
        self.eng_btn.text = self.T("english")
        self.back_btn.text = self.T("back")

        self.math_btn.draw()
        self.geo_btn.draw()
        self.eng_btn.draw()
        self.back_btn.draw()

    # ==========================
    # GAME START
    # ==========================
    def start_category(self, category):

        self.current_category = category
        self.questions = QUESTIONS[category][:]
        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0

        self.state = "question"
        self.read_current_question()

    # ==========================
    # QUESTION
    # ==========================
    def question_screen(self):

        SCREEN.fill(BLACK)

        qdata = self.questions[self.current_question]
        q = qdata[self.lang]

        self.answerA.text = f"A) {q['A']}"
        self.answerB.text = f"B) {q['B']}"
        self.answerC.text = f"C) {q['C']}"
        self.answerD.text = f"D) {q['D']}"

        title = FONT.render(f"{self.current_question+1}/{len(self.questions)}", True, WHITE)
        SCREEN.blit(title,(50,30))

        score_text = FONT.render(f"{self.T('score')}: {self.score}", True, GREEN)
        SCREEN.blit(score_text,(900,30))

        question = FONT.render(q["q"], True, WHITE)
        SCREEN.blit(question,(WIDTH//2 - question.get_width()//2,120))

        self.answerA.draw()
        self.answerB.draw()
        self.answerC.draw()
        self.answerD.draw()

    # ==========================
    # ANSWER CHECK
    # ==========================
    def answer(self, letter):

        correct = self.questions[self.current_question]["correct"]

        if letter == correct:
            self.score += 1
            tts.speak(self.T("correct"))
        else:
            tts.speak(self.T("wrong"))

        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.state = "results"
            post_score(self.score)
        else:
            self.read_current_question()

    # ==========================
    # RESULTS
    # ==========================
    def results(self):

        SCREEN.fill(BLACK)

        title = FONT_BIG.render(self.T("finalscore"), True, WHITE)
        SCREEN.blit(title,(WIDTH//2 - title.get_width()//2,120))

        result = FONT_BIG.render(f"{self.score}/{len(self.questions)}", True, GREEN)
        SCREEN.blit(result,(WIDTH//2 - result.get_width()//2,250))

        percent = int(self.score/len(self.questions)*100)

        ptxt = FONT.render(f"{percent}%", True, WHITE)
        SCREEN.blit(ptxt,(WIDTH//2 - ptxt.get_width()//2,350))

        self.back_menu_btn.text = self.T("back")
        self.back_menu_btn.draw()


# =====================================
# MAIN
# =====================================

game = Game()

tts.set_language("es")

while True:

    CLOCK.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        game.handle_event(event)

    game.draw()

    pygame.display.flip()