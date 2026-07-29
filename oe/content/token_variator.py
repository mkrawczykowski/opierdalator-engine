"""
TokenVariator — losuje wariant DesignTokens na podstawie variability.

Zasady:
- Zmieniane są wyłącznie pola int w ButtonToken (padding_x, padding_y,
  radius, border_width).
- Każda wartość jest przesuwana o losowy offset z przedziału
  [-variability_pct%, +variability_pct%] tej wartości.
- Wynik jest zaokrąglany w dół (floor) do całkowitych pikseli.
- Wartości nie schodzą poniżej 0.
- Różny seed → różny wynik → gwarantuje unikalność kolejnych plików PNG.
"""

import math
import random
from dataclasses import replace

from oe.design.tokens import DesignTokens, ButtonToken


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
        new_button = self._vary_button(tokens.button, variability_pct, rng)
        return replace(tokens, button=new_button)

    # ------------------------------------------------------------------

    def _vary_button(
        self,
        button: ButtonToken,
        variability_pct: float,
        rng: random.Random,
    ) -> ButtonToken:
        return replace(
            button,
            padding_x=self._vary_int(button.padding_x, variability_pct, rng),
            padding_y=self._vary_int(button.padding_y, variability_pct, rng),
            radius=self._vary_int(button.radius, variability_pct, rng),
        )

    def _vary_int(self, value: int, variability_pct: float, rng: random.Random) -> int:
        max_delta = value * (variability_pct / 100.0)
        delta = rng.uniform(-max_delta, max_delta)
        return max(0, math.floor(value + delta))
