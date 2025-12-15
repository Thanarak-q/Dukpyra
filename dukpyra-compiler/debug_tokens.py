from dukpyra.lexer import lexer

code = """
import dukpyra
app = dukpyra.app()

@app.get("/process-numbers")
def process_numbers(numbers: list):
    return [x * 2 for x in numbers]
"""

lexer.input(code)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
