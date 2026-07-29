# ARCHITECTURE.md

## Cel projektu

Opierdalator Engine (OE) jest silnikiem generowania identyfikacji wizualnej i layoutów na podstawie opisu marki.

Podstawowym celem jest wygenerowanie wielu spójnych wizualnie interpretacji tej samej marki. Aktualnie pierwszym rendererem jest renderer PNG wykorzystywany do szybkiego testowania koncepcji.

Projekt rozwijany jest zgodnie z zasadą:

- AI podejmuje decyzje projektowe.
- Python wykonuje deterministyczny rendering.
- Wyniki oceniane są wizualnie.

---

# Architektura

Aktualna struktura projektu:

```text
oe/
│
├── __init__.py
├── version.py
│
├── theme/
│   ├── __init__.py
│   └── theme_dna.py
│
├── variation/
│   ├── __init__.py
│   └── variation_engine.py
│
└── renderer/
    ├── __init__.py
    ├── png_renderer.py
    │
    └── sections/
        ├── __init__.py
        ├── title.py
        ├── palette.py
        ├── typography.py
        ├── button.py
        ├── card.py
        ├── hero.py
        └── variation.py
```

---

# Przepływ danych

```
ThemeDNA
        ↓
VariationEngine
        ↓
ThemeVariation
        ↓
PNGRenderer
        ↓
Theme Board (PNG)
```

Renderer nie podejmuje decyzji projektowych.

Renderer wyłącznie wizualizuje dane otrzymane z wcześniejszych etapów.

---

# ThemeDNA

ThemeDNA opisuje estetykę marki.

Każda cecha zawiera:

- wartość docelową
- dopuszczalne odchylenie

Aktualne cechy:

- softness
- contrast
- rhythm
- geometry
- elegance

ThemeDNA jest wejściem dla Variation Engine.

---

# Variation Engine

Variation Engine generuje konkretną wariację ThemeDNA.

Każda wygenerowana wartość mieści się w zakresie określonym przez ThemeDNA.

Generator wykorzystuje ziarno (`seed`), dzięki czemu wyniki mogą być powtarzalne.

---

# Renderer

Aktualnie dostępny jest renderer PNG.

Jego odpowiedzialnością jest wyłącznie wygenerowanie planszy prezentującej aktualny stan projektu.

Renderer nie powinien zawierać logiki projektowej.

---

# Renderer PNG

Renderer składa się z:

- orkiestratora (`png_renderer.py`)
- niezależnych modułów sekcji (`renderer/sections`)

Każda sekcja odpowiada za narysowanie jednego fragmentu Theme Board.

Aktualne sekcje:

- Title
- Palette
- Typography
- Button
- Card
- Hero
- Variation

Każda sekcja posiada własny moduł.

---

# Publiczne API

## ThemeDNA

Tworzenie opisu marki.

## VariationEngine.generate()

Wejście:

- ThemeDNA

Wyjście:

- ThemeVariation

## PNGRenderer.render()

Wejście:

- ThemeDNA
- ThemeVariation
- nazwa pliku

Wyjście:

- plik PNG

---

# Theme Board

Theme Board jest planszą służącą do oceny wizualnej.

Aktualnie zawiera:

- tytuł
- paletę kolorów
- próbkę typografii
- przykładowy przycisk
- przykładową kartę
- uproszczony Hero
- wartości Variation

Theme Board jest podstawowym artefaktem wykorzystywanym podczas testów wizualnych.

---

# Zależności

ThemeDNA

↓

Variation Engine

↓

ThemeVariation

↓

PNG Renderer

↓

Theme Board

Każdy moduł zna wyłącznie poprzedni etap przetwarzania danych.

Renderer nie powinien znać logiki Variation Engine.