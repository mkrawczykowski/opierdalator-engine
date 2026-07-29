# PROJECT_STATE.md

## Aktualny sprint

Sprint 05.0

### Cel

Zbudowanie pierwszego zestawu komponentów sterowanych przez Design Tokens.

Ocena projektu odbywa się wyłącznie na podstawie wygenerowanych PNG.

---

# Ukończone

## Inicjalizacja projektu

Projekt posiada podstawową strukturę katalogów.

---

## ThemeDNA

Zaimplementowano model ThemeDNA.

---

## Variation Engine

Variation Engine generuje powtarzalne wariacje.

---

## PNG Renderer

Renderer generuje obraz PNG.

---

## Eksperymenty wizualne

Zweryfikowano eksperymentalnie wpływ parametrów:

- boldness
- elegance
- softness

na odbiór projektu.

Eksperymenty wykazały, że pojedyncze cechy powinny wpływać na wiele parametrów wizualnych jednocześnie.

---

# Aktualny sprint

Pierwszym celem nie jest jeszcze budowanie stron.

Pierwszym celem jest stworzenie systemu Design Tokens.

Powstaną podstawowe komponenty:

- Section
- Container
- Heading
- Paragraph
- Button

Każdy komponent będzie sterowany wyłącznie przez wartości liczbowe.

---

# Zakres sprintu

Renderer wygeneruje jeden PNG.

PNG będzie zawierał:

- dwie sekcje
- nagłówek
- akapit
- przycisk

bez:

- kolumn
- zdjęć
- kart
- ikon
- formularzy

---

# Znane problemy

Brakuje jeszcze warstwy Design Tokens.

Komponenty są nadal zbyt mocno związane z rendererem.

---

# Następny logiczny krok

Stworzyć TokenGenerator, który będzie tłumaczył cechy takie jak:

- boldness
- elegance
- softness

na konkretne wartości liczbowe używane przez komponenty.