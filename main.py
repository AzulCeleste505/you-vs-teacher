import pygame
import pyttsx3
import threading
import random
import sys
import json
import os

from questions import QUESTIONS

pygame.init()

# ================= CONFIGURACIÓN VISUAL (MODERNA Y ACCESIBLE) =================
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You VS Teacher")
CLOCK = pygame.time.Clock()

# Fuentes
FONT_BIG = pygame.font.SysFont("comicsansms" if "comicsansms" in pygame.font.get_fonts() else "arial", 52, bold=True)
FONT_MEDIUM = pygame.font.SysFont("arial", 36, bold=True)
FONT = pygame.font.SysFont("arial", 28)
FONT_SMALL = pygame.font.SysFont("arial", 22)

# Paleta de colores de alto contraste y descanso visual
BG_COLOR = (18, 24, 38)        # Azul oscuro profundo
CARD_COLOR = (30, 41, 59)      # Gris azulado para componentes
TEXT_COLOR = (248, 250, 252)   # Blanco brillante texturas
ACCENT_COLOR = (99, 102, 241)  # Violeta eléctrico para selección
GREEN = (34, 197, 94)          # Verde éxito
RED = (239, 68, 68)            # Rojo error
GRAY = (71, 85, 105)           # Gris neutro

# ================= ARCHIVOS =================
STATS_FILE = "stats.json"
RANK_FILE = "ranking.json"


def load_json(file, default):
    try:
        if not os.path.exists(file):
            return default
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if data else default
    except (json.JSONDecodeError, IOError):
        return default


def save_json(file, data):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError:
        print(f"Error guardando {file}")


# ================= SISTEMA TTS MEJORADO =================
class TTS:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            # Configurar una velocidad de lectura ligeramente más natural
            self.engine.setProperty('rate', 180)
        except Exception as e:
            print(f"No se pudo inicializar el motor TTS: {e}")
            self.engine = None
            
        self.enabled = True  # Activado por defecto para mejorar accesibilidad inicial
        self.lang = "es"

    def set_language(self, lang):
        self.lang = lang

    def speak(self, text):
        if not self.enabled or not self.engine:
            return

        def run():
            try:
                # Detener lecturas previas si es posible para evitar solapamientos violentos
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error en hilo de TTS: {e}")

        threading.Thread(target=run, daemon=True).start()


tts = TTS()


# ================= AUXILIAR: ENVOLVER TEXTO LARGO =================
def draw_text_wrapped(surface, text, x, y, max_width, font, color):
    """Divide un texto largo en múltiples líneas para que no se salga de la pantalla"""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = font.render(line.strip(), True, color)
        surface.blit(text_surface, (x, y + i * (font.get_linesize() + 5)))
    
    return len(lines) * (font.get_linesize() + 5)


# ================= BOTONES MEJORADOS =================
class Button:
    def __init__(self, x, y, w, h, text, base_color=CARD_COLOR):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = base_color

    def draw(self):
        # Efecto Hover visualmente más marcado
        is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = ACCENT_COLOR if is_hovered else self.base_color
        
        # Dibujar botón con bordes redondeados y sombra sutil
        pygame.draw.rect(SCREEN, color, self.rect, border_radius=16)
        if is_hovered:
            pygame.draw.rect(SCREEN, TEXT_COLOR, self.rect, width=2, border_radius=16)

        # Renderizar texto centrado
        label = FONT.render(self.text, True, TEXT_COLOR)
        SCREEN.blit(label, (
            self.rect.centerx - label.get_width() // 2,
            self.rect.centery - label.get_height() // 2
        ))

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos)
        )


# ================= CLASE PRINCIPAL DEL JUEGO =================
class Game:
    def __init__(self):
        self.lang = "es"
        self.state = "menu"

        self.score = 0
        self.current_question = 0
        self.questions = []

        # Cargar configuraciones y datos
        self.stats_data = load_json(STATS_FILE, {"games_played": 0, "games_won": 0})
        self.ranking = load_json(RANK_FILE, [])

        if "games_played" not in self.stats_data: self.stats_data["games_played"] = 0
        if "games_won" not in self.stats_data: self.stats_data["games_won"] = 0

        # Posiciones estandarizadas de interfaz
        btn_w, btn_h = 400, 65
        cx = (WIDTH - btn_w) // 2

        # Inicialización de todos los botones
        self.play_btn = Button(cx, 220, btn_w, btn_h, "")
        self.settings_btn = Button(cx, 310, btn_w, btn_h, "")
        self.stats_btn = Button(cx, 400, btn_w, btn_h, "")
        self.quit_btn = Button(cx, 490, btn_w, btn_h, "", base_color=(64, 30, 30))

        self.math_btn = Button(cx, 220, btn_w, btn_h, "")
        self.geo_btn = Button(cx, 310, btn_w, btn_h, "")
        self.eng_btn = Button(cx, 400, btn_w, btn_h, "")
        self.back_btn = Button(cx, 550, btn_w, btn_h, "")

        self.spanish_btn = Button(cx, 220, btn_w, btn_h, "")
        self.english_btn = Button(cx, 310, btn_w, btn_h, "")
        self.tts_btn = Button(cx, 400, btn_w, btn_h, "")

        # Botones de juego optimizados para lectura de preguntas amplias
        self.a = Button(150, 260, 900, 60, "")
        self.b = Button(150, 340, 900, 60, "")
        self.c = Button(150, 420, 900, 60, "")
        self.d = Button(150, 500, 900, 60, "")

        # Ejecutar la primera locución al iniciar el juego
        self.announce_current_state()

    def set_state(self, new_state):
        """Cambia el estado de la aplicación y lee automáticamente la nueva pantalla"""
        self.state = new_state
        self.announce_current_state()

    def T(self, key):
        """Diccionario de traducciones integrado"""
        translations = {
            "es": {
                "title": "Tú VS Profesor",
                "play": "Jugar",
                "settings": "Configuración",
                "stats": "Estadísticas",
                "quit": "Salir",
                "back": "Volver al Menú",
                "score": "Puntuación",
                "final": "Resultado Final",
                "spanish": "Idioma: Español",
                "english": "Idioma: English",
                "tts_on": "Lectura de voz: ACTIVADA",
                "tts_off": "Lectura de voz: DESACTIVADA",
                "games_played": "Partidas completadas",
                "games_won": "Partidas ganadas",
                "select_cat": "Selecciona una Categoría",
                "top10": "Historial de mejores puntuaciones:",
                "pts": "puntos"
            },
            "en": {
                "title": "You VS Teacher",
                "play": "Play",
                "settings": "Settings",
                "stats": "Stats",
                "quit": "Quit",
                "back": "Back to Menu",
                "score": "Score",
                "final": "Final Score",
                "spanish": "Language: Español",
                "english": "Language: English",
                "tts_on": "Voice Reading: ENABLED",
                "tts_off": "Voice Reading: DISABLED",
                "games_played": "Games played",
                "games_won": "Games won",
                "select_cat": "Select a Category",
                "top10": "Top Scores History:",
                "pts": "points"
            }
        }
        return translations.get(self.lang, {}).get(key, key)

    # ================= NARRACIÓN TTS PARA CADA MENÚ =================
    def announce_current_state(self):
        """Genera dinámicamente un texto descriptivo completo de la pantalla actual para el TTS"""
        if self.state == "menu":
            texto = f"{self.T('title')}. {self.T('play')}, {self.T('settings')}, {self.T('stats')}, o {self.T('quit')}."
        elif self.state == "category":
            texto = f"{self.T('select_cat')}. Opciones disponibles: Matemáticas, Geografía, Inglés. O presiona Volver."
        elif self.state == "settings":
            status_tts = self.T("tts_on") if tts.enabled else self.T("tts_off")
            texto = f"{self.T('settings')}. Opciones: {self.T('spanish')}, {self.T('english')}, {status_tts}. O presiona Volver."
        elif self.state == "stats":
            texto = f"{self.T('stats')}. {self.T('games_played')}: {self.stats_data.get('games_played')}. {self.T('games_won')}: {self.stats_data.get('games_won')}."
            if self.ranking:
                texto += f" Tu mejor récord es de {max(self.ranking)} {self.T('pts')}."
        elif self.state == "question":
            self.read_question_payload()
            return
        elif self.state == "results":
            texto = f"{self.T('final')}. Conseguiste {self.score} puntos. Presiona Volver para regresar al menú."
        else:
            return

        tts.speak(texto)

    def read_question_payload(self):
        """Lee detalladamente la pregunta y sus 4 opciones correspondientes"""
        if not self.questions or self.current_question >= len(self.questions):
            return
        try:
            q = self.questions[self.current_question].get(self.lang)
            if q:
                texto = f"Pregunta: {q['q']}. Opción A: {q['A']}. Opción B: {q['B']}. Opción C: {q['C']}. Opción D: {q['D']}."
                tts.speak(texto)
        except Exception as e:
            print(f"Error procesando voz de la pregunta: {e}")

    # ================= MÉTODOS DE DIBUJADO DE INTERFAZ =================
    def menu(self):
        SCREEN.fill(BG_COLOR)
        title = FONT_BIG.render(self.T("title"), True, TEXT_COLOR)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        self.play_btn.text = self.T("play")
        self.settings_btn.text = self.T("settings")
        self.stats_btn.text = self.T("stats")
        self.quit_btn.text = self.T("quit")

        self.play_btn.draw()
        self.settings_btn.draw()
        self.stats_btn.draw()
        self.quit_btn.draw()

    def stats(self):
        SCREEN.fill(BG_COLOR)
        title = FONT_BIG.render(self.T("stats"), True, TEXT_COLOR)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Cuadro contenedor de estadísticas
        panel_rect = pygame.Rect(200, 150, 800, 380)
        pygame.draw.rect(SCREEN, CARD_COLOR, panel_rect, border_radius=20)

        p1 = FONT_MEDIUM.render(f"📊 {self.T('games_played')}: {self.stats_data['games_played']}", True, TEXT_COLOR)
        p2 = FONT_MEDIUM.render(f"🏆 {self.T('games_won')}: {self.stats_data['games_won']}", True, GREEN)
        SCREEN.blit(p1, (250, 180))
        SCREEN.blit(p2, (250, 240))

        # Historial/Ranking visual
        SCREEN.blit(FONT_MEDIUM.render(self.T("top10"), True, ACCENT_COLOR), (250, 320))
        if self.ranking:
            for i, score in enumerate(self.ranking[:5]):  # Mostramos los mejores 5 de forma más limpia
                txt = FONT.render(f"{i + 1}º Lugar: {score} {self.T('pts')}", True, TEXT_COLOR)
                SCREEN.blit(txt, (280, 370 + i * 32))
        else:
            txt = FONT.render("No hay registros aún", True, GRAY)
            SCREEN.blit(txt, (280, 370))

        self.back_btn.text = self.T("back")
        self.back_btn.draw()

    def settings(self):
        SCREEN.fill(BG_COLOR)
        title = FONT_BIG.render(self.T("settings"), True, TEXT_COLOR)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        self.spanish_btn.text = self.T("spanish")
        self.english_btn.text = self.T("english")
        self.tts_btn.text = self.T("tts_on") if tts.enabled else self.T("tts_off")

        # Cambiar de color el botón TTS si está activo o inactivo
        self.tts_btn.base_color = GREEN if tts.enabled else RED

        self.spanish_btn.draw()
        self.english_btn.draw()
        self.tts_btn.draw()
        
        self.back_btn.text = self.T("back")
        self.back_btn.draw()

    def category(self):
        SCREEN.fill(BG_COLOR)
        title = FONT_BIG.render(self.T("select_cat"), True, TEXT_COLOR)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        self.math_btn.text = "Math" if self.lang == "en" else "Matemáticas"
        self.geo_btn.text = "Geography" if self.lang == "en" else "Geografía"
        self.eng_btn.text = "English" if self.lang == "en" else "Inglés"
        self.back_btn.text = self.T("back")

        self.math_btn.draw()
        self.geo_btn.draw()
        self.eng_btn.draw()
        self.back_btn.draw()

    def start(self, cat):
        if cat not in QUESTIONS or not QUESTIONS[cat]:
            self.set_state("category")
            return

        self.questions = QUESTIONS[cat][:]
        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0
        self.set_state("question")

    def question(self):
        SCREEN.fill(BG_COLOR)

        if not self.questions or self.current_question >= len(self.questions):
            self.finish()
            self.set_state("results")
            return

        try:
            q = self.questions[self.current_question].get(self.lang)
            if not q:
                self.next_question()
                return

            # Cabecera de puntuación y progreso
            progreso = f"Pregunta {self.current_question + 1} de {len(self.questions)}"
            prog_surface = FONT_SMALL.render(progreso, True, GRAY)
            score_surface = FONT_MEDIUM.render(f"{self.T('score')}: {self.score}", True, GREEN)
            
            SCREEN.blit(prog_surface, (150, 30))
            SCREEN.blit(score_surface, (150, 60))

            # Dibujar la pregunta con el ajuste de línea automático
            draw_text_wrapped(SCREEN, q.get("q", ""), 150, 130, 900, FONT_MEDIUM, TEXT_COLOR)

            # Asignar textos a botones de respuestas
            self.a.text = f"A)  {q.get('A', '')}"
            self.b.text = f"B)  {q.get('B', '')}"
            self.c.text = f"C)  {q.get('C', '')}"
            self.d.text = f"D)  {q.get('D', '')}"

            self.a.draw()
            self.b.draw()
            self.c.draw()
            self.d.draw()

            # Leyenda informativa de accesibilidad de teclado en la zona inferior
            help_txt = "[Teclado]: Presiona A, B, C, D o los números 1, 2, 3, 4 para responder rápidamente"
            help_surf = FONT_SMALL.render(help_txt, True, GRAY)
            SCREEN.blit(help_surf, (WIDTH // 2 - help_surf.get_width() // 2, 620))

        except Exception as e:
            print(f"Error renderizando la pantalla de juego: {e}")
            self.next_question()

    def answer(self, letter):
        if not self.questions:
            return

        try:
            correct = self.questions[self.current_question].get("correct")
            if letter == correct:
                self.score += 1
        except IndexError:
            pass

        self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.finish()
            self.set_state("results")
        else:
            # Vuelve a ejecutar la lectura TTS automatizada por el cambio de pregunta
            self.announce_current_state()

    def finish(self):
        try:
            self.stats_data["games_played"] += 1
            if len(self.questions) > 0:
                if (self.score / len(self.questions)) >= 0.5:
                    self.stats_data["games_won"] += 1

            save_json(STATS_FILE, self.stats_data)

            self.ranking.append(self.score)
            self.ranking = sorted(self.ranking, reverse=True)[:10]
            save_json(RANK_FILE, self.ranking)
        except Exception as e:
            print(f"Error procesando finalización de juego: {e}")

    def results(self):
        SCREEN.fill(BG_COLOR)
        
        panel_rect = pygame.Rect(300, 120, 600, 320)
        pygame.draw.rect(SCREEN, CARD_COLOR, panel_rect, border_radius=24)

        title = FONT_BIG.render(self.T("final"), True, TEXT_COLOR)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))

        score_text = f"{self.score} / {len(self.questions)}" if self.questions else "0 / 0"
        score_surf = FONT_BIG.render(score_text, True, GREEN)
        SCREEN.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 260))

        self.back_btn.text = self.T("back")
        self.back_btn.draw()

    def draw(self):
        """Router centralizado de dibujado"""
        if self.state == "menu": self.menu()
        elif self.state == "stats": self.stats()
        elif self.state == "settings": self.settings()
        elif self.state == "category": self.category()
        elif self.state == "question": self.question()
        elif self.state == "results": self.results()

    # ================= MANEJO DE ENTRADAS Y EVENTOS =================
    def handle(self, event):
        # --- EVENTOS GENERALES DEL TECLADO PARA ACCESIBILIDAD ---
        if event.type == pygame.KEYDOWN:
            # Salida rápida con la tecla Escape desde cualquier menú (excepto jugando)
            if event.key == pygame.K_ESCAPE and self.state != "question":
                if self.state == "menu":
                    pygame.quit()
                    sys.exit()
                else:
                    self.set_state("menu")

            # --- CONTROL EXCLUSIVO POR TECLADO EN LAS PREGUNTAS ---
            if self.state == "question":
                if event.key in [pygame.K_a, pygame.K_1]: self.answer("A")
                elif event.key in [pygame.K_b, pygame.K_2]: self.answer("B")
                elif event.key in [pygame.K_c, pygame.K_3]: self.answer("C")
                elif event.key in [pygame.K_d, pygame.K_4]: self.answer("D")

        # --- EVENTOS DE CLIC DE RATÓN ---
        if self.state == "menu":
            if self.play_btn.clicked(event): self.set_state("category")
            elif self.settings_btn.clicked(event): self.set_state("settings")
            elif self.stats_btn.clicked(event): self.set_state("stats")
            elif self.quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        elif self.state == "settings":
            if self.spanish_btn.clicked(event):
                self.lang = "es"
                tts.set_language("es")
                self.announce_current_state()
            elif self.english_btn.clicked(event):
                self.lang = "en"
                tts.set_language("en")
                self.announce_current_state()
            elif self.tts_btn.clicked(event):
                tts.enabled = not tts.enabled
                self.announce_current_state()
            elif self.back_btn.clicked(event):
                self.set_state("menu")

        elif self.state == "stats":
            if self.back_btn.clicked(event): self.set_state("menu")

        elif self.state == "category":
            if self.math_btn.clicked(event): self.start("math")
            elif self.geo_btn.clicked(event): self.start("geo")
            elif self.eng_btn.clicked(event): self.start("english")
            elif self.back_btn.clicked(event): self.set_state("menu")

        elif self.state == "question":
            if self.a.clicked(event): self.answer("A")
            elif self.b.clicked(event): self.answer("B")
            elif self.c.clicked(event): self.answer("C")
            elif self.d.clicked(event): self.answer("D")

        elif self.state == "results":
            if self.back_btn.clicked(event): self.set_state("menu")


# ================= BUCLE PRINCIPAL =================
if __name__ == "__main__":
    game = Game()
    tts.set_language("es")

    running = True
    while running:
        CLOCK.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            game.handle(e)

        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()