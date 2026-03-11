"""

Function document for MathObservers subprocess

January 2026, Skadi Wiesemann

"""

from Tools.i18n.pygettext import safe_eval
from FaustBot import logger

formel = input()
try:
    lösung = float(safe_eval(formel))
    logger.info(lösung)

except SyntaxError:
    logger.error("Fehler: SyntaxError")
