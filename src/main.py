from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser

if __name__ == '__main__':
    # Read the code from a file
    with open('../test/list_map.lang', 'r') as file:
        code = file.read()

    lexer = Lexer()
    lexer.build()
    lexer.test(code)

    parser = Parser()
    parser.build()
    ast = parser.parser.parse(code, lexer=lexer.lexer)
    print(ast)

    # Create an instance of the interpreter
    interpreter = Interpreter()

    # Parse and execute the code
    result = interpreter.parse_and_execute(code)

    # Print the result
    print(result)
