#!/usr/bin/env python3
"""Transitional entry point.

The game now lives in the ``src/dice_game`` package. Until packaging is set up
(see action item 3 in ``improve_quality_todo.md``), this shim puts ``src`` on the
import path so ``python main.py`` keeps working. After ``pip install -e .`` you
can instead run ``dice-game`` or ``python -m dice_game`` and delete this file.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from dice_game.cli import main  # noqa: E402  (path tweak must precede import)

if __name__ == "__main__":
    main()
