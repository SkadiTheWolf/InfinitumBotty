"""

Function document for MathObservers subprocess

January 2026, Skadi Wiesemann

"""
from Tools.i18n.pygettext import safe_eval

formel = input()
try:
    lösung =  float(safe_eval(formel))
    print(lösung)

except SyntaxError:
    print('Fehler: SyntaxError')

