# 🎮 You VS Teacher - Quiz Game

Un juego educativo de preguntas y respuestas en Pygame con soporte para múltiples idiomas y categorías.

## 📸 Características

- ✅ **Juego de Preguntas**: 4 opciones múltiples por pregunta
- ✅ **3 Categorías**: Matemáticas, Geografía, Inglés
- ✅ **Bilingüe**: Español e Inglés
- ✅ **Text-to-Speech**: Lee las preguntas en voz alta (opcional)
- ✅ **Estadísticas**: Guarda tu progreso y ranking
- ✅ **Rankings**: Visualiza tu Top 10
- ✅ **Sin Crashes**: Código robusto con manejo de errores
- ✅ **Interfaz Intuitiva**: Menú fácil de usar

---

## 🚀 Instalación Rápida

### 1️⃣ Requiere Python 3.7+

### 2️⃣ Instala las dependencias

```bash
pip install pygame pyttsx3
```

### 3️⃣ Estructura de carpetas

```
tu_proyecto/
├── main.py                  # Archivo principal (NUEVO)
├── questions.py             # Tus preguntas (crea basándote en questions_EJEMPLO.py)
├── stats.json              # Se crea automáticamente
└── ranking.json            # Se crea automáticamente
```

### 4️⃣ Crea tu archivo questions.py

Copia el contenido de `questions_EJEMPLO.py` y personalizalo con tus preguntas.

### 5️⃣ Ejecuta el juego

```bash
python main.py
```

---

## 🎮 Cómo Jugar

1. **Menú Principal**: Selecciona "Jugar"
2. **Elige Categoría**: Math, Geography o English
3. **Responde Preguntas**: Click en A, B, C o D
4. **Ve tu Puntuación**: Al final ves tu score
5. **Estadísticas**: Consulta tu progreso en cualquier momento

---

## ⚙️ Configuración

### Cambiar Idioma
1. Click en "Configuración" desde el menú
2. Selecciona "Español" o "English"
3. Las preguntas y menús cambian al instante

### Activar Text-to-Speech
1. Click en "Configuración"
2. Click en "Leer preguntas (TTS)"
3. Las preguntas se leerán en voz alta
4. Requiere altavoces/auriculares

---

## 📊 Estadísticas

El juego guarda automáticamente:
- **games_played**: Total de juegos jugados
- **games_won**: Juegos ganados (con 50%+ de respuestas correctas)
- **ranking.json**: Tu Top 10 de puntuaciones

Archivo: `stats.json`
```json
{
    "games_played": 5,
    "games_won": 3
}
```

---

## 🎯 Estructura de Preguntas

Cada pregunta debe tener esta estructura:

```python
{
    "es": {
        "q": "¿Pregunta en español?",
        "A": "Opción A",
        "B": "Opción B",
        "C": "Opción C",
        "D": "Opción D"
    },
    "en": {
        "q": "Question in English?",
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
    },
    "correct": "B"  # La respuesta correcta
}
```

---

## 🔧 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'pygame'"
**Solución**: Instala pygame
```bash
pip install pygame
```

### Problema: "ModuleNotFoundError: No module named 'questions'"
**Solución**: Crea un archivo `questions.py` en la misma carpeta que `main.py`

### Problema: El TTS no funciona
**Solución**: En algunos sistemas requiere configuración adicional
- En Windows: Generalmente funciona sin configuración
- En Mac: `pip install --upgrade pyttsx3`
- En Linux: `apt-get install espeak` (para español)

### Problema: El juego se ve pequeño/grande
**Solución**: Modifica estas líneas en `main.py`:
```python
WIDTH, HEIGHT = 1200, 700  # Cambia estos valores
```

---

## 📝 Personalización

### Agregar una Nueva Categoría

1. En `questions.py`, agrega:
```python
QUESTIONS = {
    "math": [...],
    "geo": [...],
    "english": [...],
    "history": [...]  # NUEVA CATEGORÍA
}
```

2. En `main.py`, agrega un botón en `category()`:
```python
self.history_btn = Button(400, 480, 400, 60, "History")
self.history_btn.draw()
```

3. En `handle()`, agrega el evento:
```python
elif self.history_btn.clicked(event):
    self.start("history")
```

### Cambiar Colores

En `main.py`, modifica estas líneas:
```python
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (50, 50, 50)
LIGHT_GRAY = (90, 90, 90)
GREEN = (50, 180, 80)
RED = (200, 50, 50)
```

---

## 🐛 Reporte de Bugs

Si encuentras un error:
1. Revisa que `questions.py` esté bien formateado
2. Verifica que todas las preguntas tengan la estructura correcta
3. Comprueba que `correct` sea "A", "B", "C" o "D"

---

## 📚 Archivos Incluidos

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Código principal del juego (CORREGIDO) |
| `questions_EJEMPLO.py` | Ejemplo de estructura de preguntas |
| `CAMBIOS.md` | Detalles de las correcciones realizadas |
| `README.md` | Este archivo |
| `stats.json` | Se crea automáticamente |
| `ranking.json` | Se crea automáticamente |

---

## 💡 Tips para Mejorar el Juego

1. **Agrega más preguntas**: Más contenido = más diversidad
2. **Crea más categorías**: Expand the game with new topics
3. **Aumenta la dificultad**: Preguntas progresivas
4. **Cambia los colores**: Hazlo más atractivo visualmente
5. **Agrega sonidos**: Usa pygame.mixer para efectos

---

## 📄 Licencia

Este código es de código abierto. ¡Úsalo, modifícalo y mejóralo!

---

## 🎓 Créditos

Creado como herramienta educativa para estudiantes y profesores.

---

## 🚀 Versión

**v2.0** - Versión corregida sin crashes
- ✅ Fixed settings crash
- ✅ Added settings screen
- ✅ Better title display
- ✅ Improved error handling
- ✅ Full bilingual support

---

## ¡Disfruta el juego! 🎮

**¿Preguntas?** Revisa los ejemplos en `questions_EJEMPLO.py` y `CAMBIOS.md`
