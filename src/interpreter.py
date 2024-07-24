from enum import Enum
from typing import Optional

from src.ast_nodes import Node


class Type(Enum):
    # has value of True/False
    BOOLEAN = 0
    # has value of 0,1,...
    INTEGER = 1
    # has value of (params[], code)
    FUNCTION = 2
    # has value of values[]
    LIST = 3
    # use for functions with side effects like print (as they have no return values)
    UNIT = 4


class EvaluationResult:
    def __init__(self, type: Type, value: any, environment: Optional[dict] = None):
        self.type = type
        self.value = value
        # self.environment = environment


class Environment:
    def __init__(self):
        self.variables = {}

    def get_variable(self, name: str) -> Optional[EvaluationResult]:
        if name in self.variables:
            return self.variables[name]
        return None

    def set_variable(self, name: str, result: EvaluationResult):
        self.variables[name] = result


def execute_if_builtin(node: Node, params: list[EvaluationResult]) -> Optional[EvaluationResult]:
    # TODO: allow less params and return new function

    if node.children[0] == "eq":
        assert len(params) == 2
        result = params[0].type and params[1].type and params[0].value == params[0].value
        return EvaluationResult(Type.BOOLEAN, result)
    if node.children[0] == "not":
        assert len(params) == 1 and params[0].type == Type.BOOLEAN
        result = not params[0].value
        return EvaluationResult(Type.BOOLEAN, result)
    if node.children[0] == "and":
        assert len(params) == 2 and params[0].type == Type.BOOLEAN and params[1].type == Type.BOOLEAN
        result = params[0].value and params[1].value
        return EvaluationResult(Type.BOOLEAN, result)
    if node.children[0] == "or":
        assert len(params) == 2 and params[0].type == Type.BOOLEAN and params[1].type == Type.BOOLEAN
        result = params[0].value and params[1].value
        return EvaluationResult(Type.BOOLEAN, result)
    if node.children[0] == "less":
        assert len(params) == 2 and params[0].type == Type.INTEGER and params[1].type == Type.INTEGER
        result = params[0].value < params[1].value
        return EvaluationResult(Type.BOOLEAN, result)
    if node.children[0] == "greater":
        assert len(params) == 2 and params[0].type == Type.INTEGER and params[1].type == Type.INTEGER
        result = params[0].value > params[1].value
        return EvaluationResult(Type.BOOLEAN, result)

    if node.children[0] == "plus":
        assert len(params) == 2 and params[0].type == Type.INTEGER and params[1].type == Type.INTEGER
        result = params[0].value + params[1].value
        return EvaluationResult(Type.INTEGER, result)
    if node.children[0] == "minus":
        assert len(params) == 2 and params[0].type == Type.INTEGER and params[1].type == Type.INTEGER
        result = params[0].value - params[1].value
        return EvaluationResult(Type.INTEGER, result)
    if node.children[0] == "mult":
        assert len(params) == 2 and params[0].type == Type.INTEGER and params[1].type == Type.INTEGER
        result = params[0].value * params[1].value
        return EvaluationResult(Type.INTEGER, result)
    if node.children[0] == "div":
        assert len(params) == 2 and params[0].type == Type.INTEGER and params[1].type == Type.INTEGER
        result = params[0].value // params[1].value
        return EvaluationResult(Type.INTEGER, result)
    if node.children[0] == "mod":
        assert len(params) == 2 and params[0].type == Type.INTEGER and params[1].type == Type.INTEGER
        result = params[0].value % params[1].value
        return EvaluationResult(Type.INTEGER, result)

    if node.children[0] == "head":
        assert len(params) == 1 and params[0].type == Type.LIST
        result = params[0][0]
        return EvaluationResult(result.type, result)
    if node.children[0] == "tail":
        assert len(params) == 1 and params[0].type == Type.LIST
        result = params[1:]
        return EvaluationResult(Type.LIST, result)
    if node.children[0] == "is_empty":
        assert len(params) == 1 and params[0].type == Type.LIST
        result = len(params[0].value) == 0
        return EvaluationResult(Type.BOOLEAN, result)
    if node.children[0] == "concat":
        assert len(params) == 2 and params[0].type == Type.LIST and params[1].type == Type.LIST
        result = params[0].value + params[1].value
        return EvaluationResult(Type.LIST, result)

    if node.children[0] == "if":
        assert len(params) == 3 and params[0].type == Type.BOOLEAN
        result = params[1] if params[0].value else params[2]
        return EvaluationResult(result.type, result)
    if node.children[0] == "print":
        assert len(params) == 1
        print(params[0].value)
        return EvaluationResult(Type.UNIT, Node)

    return None


class Interpreter():
    def __init__(self):
        self.stack = []

    def visit(self, node: Node):
        if node.type == "program":
            self.stack.append(Environment())
            for child in node.children:
                self.visit(child)
            self.stack.pop()
            return

        if node.type == "assignment":
            result = self.visit(node.children[1])
            self.stack[-1].set_variable(node.children[0], result)
            return

        if node.type == "function_call":
            parameter_values = []
            for i, child in enumerate(node.children[1]):
                parameter_values.append(self.visit(child))

            result = execute_if_builtin(node, parameter_values)
            if result is None:
                function = self.find_in_env(node.children[0])
                assert function.type == Type.FUNCTION
                parameter_names, function_body = function.value
                environment = Environment()
                for i, param in enumerate(parameter_values):
                    environment.set_variable(parameter_names[i], param)
                self.stack.append(environment)
                result = self.visit(function_body)
                self.stack.pop()
            return result

        if node.type == "function_definition":
            return EvaluationResult(Type.FUNCTION, node.children)

        if node.type == "block":
            self.stack.append(Environment())
            for child in node.children[0]:
                self.visit(child)
            result = self.visit(node.children[1])
            self.stack.pop()
            return result

        if node.type == "integer":
            return EvaluationResult(Type.INTEGER, node.value)

        if node.type == "list":
            return EvaluationResult(Type.LIST, node.children)

        raise Exception(f"Cannot evaluate type {node.type}")

    def find_in_env(self, name: str) -> EvaluationResult:
        for scope in reversed(self.stack):
            result = scope.get_variable(name)
            if result:
                return result
        raise Exception(f"Variable {name} not found!")

    def interpret(self, ast):
        self.visit(ast)
