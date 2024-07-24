from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser


def run_on_file(file_path):
    print(f"Running on {file_path}...")

    # Read the code from a file
    with open(file_path, 'r') as file:
        code = file.read()

    lexer = Lexer()
    lexer.build()
    # lexer.test(code)

    parser = Parser()
    parser.build()
    ast = parser.parser.parse(code, lexer=lexer.lexer)
    print(ast)

    # Create an instance of the interpreter
    interpreter = Interpreter()
    # Parse and execute the code
    interpreter.interpret(ast)


if __name__ == '__main__':
    run_on_file('../test/plus.lang')
    run_on_file('../test/func_no_params.lang')
    run_on_file('../test/list_map.lang')
    #run_on_file('../test/list_at_index.lang')
    #run_on_file('../test/list_reduce.lang')
