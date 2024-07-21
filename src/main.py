from src import lexer
from src.interpreter import Interpreter

if __name__ == '__main__':
    # Read the code from a file
    with open('../test/list_map.lang', 'r') as file:
        code = file.read()

    lexer = lexer.Lexer()
    lexer.build()
    lexer.test(code)

    # Create an instance of the interpreter
    interpreter = Interpreter()

    # Parse and execute the code
    result = interpreter.parse_and_execute(code)

    # Print the result
    print(result)
