"""
TokenVariator — losuje wariant DesignTokens na podstawie variability.

Zmieniane pola:
    ButtonToken:     padding_x, padding_y, radius, border_width
    TypographyToken: font_size, line_height (heading, body, button_text)

Zasady:
- Każda wartość int jest przesuwana o losowy offset z przedziału
  [-variability_pct%, +variability_pct%] tej wartości.
- Wynik jest zaokrąglany w dół (floor) do całkowitych pikseli.
- Wartości nie schodzą poniżej 1 (typografia) lub 0 (reszta).
- Różny seed → różny wynik → gwarantuje unikalność kolejnych plików PNG.
"""

import math
import random
from dataclasses import replace

from oe.design.tokens import DesignTokens, ButtonToken, TypographyToken


class TokenVariator:

    def vary(self, tokens: DesignTokens, variability_pct: float, seed: int) -> DesignTokens:
        """
        Wejście:  DesignTokens (bazowe), variability_pct (0–100), seed
        Wyjście:  nowe DesignTokens z losowo zmienionymi wartościami int

        Seed gwarantuje powtarzalność dla danej iteracji
        i unikalność między iteracjami.
        """
        if variability_pct == 0.0:
            return tokens

        rng = random.Random(seed)

        return replace(
            tokens,
            heading=self._vary_typography(tokens.heading, variability_pct, rng),
            body=self._vary_typography(tokens.body, variability_pct, rng),
            button_text=self._vary_typography(tokens.button_text, variability_pct, rng),
            button=self._vary_button(tokens.button, variability_pct, rng),
        )

    # ------------------------------------------------------------------

    def _vary_typography(
        self,
        token: TypographyToken,
        variability_pct: float,
        rng: random.Random,
    ) -> TypographyToken:
        font_size   = self._vary_int(token.font_size,   variability_pct, rng, min_val=1)
        line_height = self._vary_int(token.line_height, variability_pct, rng, min_val=1)
        return replace(token, font_size=font_size, line_height=line_height)

    def _vary_button(
        self,
        button: ButtonToken,
        variability_pct: float,
        rng: random.Random,
    ) -> ButtonToken:
        return replace(
            button,
            padding_x=self._vary_int(button.padding_x,    variability_pct, rng),
            padding_y=self._vary_int(button.padding_y,    variability_pct, rng),
            radius=self._vary_int(button.radius,           variability_pct, rng),
            border_width=self._vary_int(button.border_width, variability_pct, rng),
        )

    def _vary_int(
        self,
        value: int,
        variability_pct: float,
        rng: random.Random,
        min_val: int = 0,
    ) -> int:
        max_delta = value * (variability_pct / 100.0)
        delta = rng.uniform(-max_delta, max_delta)
        return max(min_val, math.floor(value + delta))
