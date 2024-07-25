from interpreter.interpreter import Interpreter
from lexer import Lexer
from parser import Parser


def run(code):
    lexer = Lexer()
    lexer.build()
    # lexer.test(code)

    parser = Parser()
    parser.build()
    ast = parser.parser.parse(code, lexer=lexer.lexer)
    # print(ast)

    # Create an instance of the interpreter
    interpreter = Interpreter()
    # Parse and execute the code
    interpreter.interpret(ast)


if __name__ == '__main__':
    code = '''map = |list, op| if(is_empty(list)) list else {
  head_l = head(list)
  tail_l = tail(list)
  concat([op(head_l)], map(tail_l, op))
}
my_list = [1,2,3]
times_two = map(my_list, mult(2))
print(times_two)
    '''

    run(code)
