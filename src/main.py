from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser


def run_on_file(file_path):
    # Read the code from a file
    with open(file_path, 'r') as file:
        code = file.read()

    lexer = Lexer()
    lexer.build()
    lexer.test(code)

    parser = Parser()
    parser.build()
    ast = parser.parser.parse(code, lexer=lexer.lexer)
    print(ast)

    # Create an instance of the interpreter
    # interpreter = Interpreter()

    # Parse and execute the code
    # result = interpreter.parse_and_execute(code)

    # Print the result
    # print(result)


if __name__ == '__main__':
    run_on_file('../test/list_at_index.lang')
    run_on_file('../test/list_map.lang')
    run_on_file('../test/list_reduce.lang')
    run_on_file('../test/plus.lang')
