"""
TextWrapper — łamanie tekstu na linie mieszczące się w zadanej szerokości.

Używany zarówno przez VerticalLayout (obliczanie wysokości)
jak i przez NodePainter (rysowanie), żeby obie fazy operowały
na identycznym podziale tekstu.
"""

from PIL import ImageFont


class TextWrapper:

    def wrap(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int,
    ) -> list[str]:
        """
        Dzieli tekst na listę linii, z których każda mieści się
        w max_width pikseli.

        Algorytm:
        - Iteruje po słowach.
        - Dodaje słowa do bieżącej linii dopóki mieszczą się w max_width.
        - Gdy słowo nie mieści się — zamyka bieżącą linię i zaczyna nową.
        - Pojedyncze słowo szersze niż max_width trafia na osobną linię
          (nie jest łamane w środku).
        """
        if not text.strip():
            return [""]

        words = text.split()
        lines: list[str] = []
        current_line = ""

        for word in words:
            candidate = f"{current_line} {word}".strip()
            if self._text_width(candidate, font) <= max_width:
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines if lines else [""]

    def total_height(self, line_count: int, line_height: int) -> int:
        """Łączna wysokość bloku tekstowego."""
        return line_count * line_height

    # ------------------------------------------------------------------

    def _text_width(self, text: str, font: ImageFont.FreeTypeFont) -> int:
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0]
