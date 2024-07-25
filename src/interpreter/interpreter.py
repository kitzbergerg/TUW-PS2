from typing import Optional

from src.ast_nodes import Node, BlockNode, AssignmentNode, FunctionDefinitionNode
from src.interpreter.function_registry import FunctionRegistry
from src.interpreter.types import EvaluationResult, Type, Environment


def execute_if_builtin(node: Node, params: list[EvaluationResult]) -> Optional[EvaluationResult]:
    function = FunctionRegistry().get_function(node.children[0])
    if function is not None:
        return function(*params)
    else:
        return None


def create_new_function(function: EvaluationResult, parameter_values: list[any]):
    # Create a new function like:
    #   my_func = |a,b| {
    #       mult(plus(a,b),b)
    #   }
    #   my_func(2) -> |b| {
    #       a = 2
    #       mult(plus(a,b),b)
    #   }
    parameter_names, function_body, environment = function
    assert isinstance(function_body, BlockNode)
    assert len(parameter_names) > len(parameter_values)

    new_params = parameter_names[len(parameter_values):]
    assignments = []
    for i, value in enumerate(parameter_values):
        assignments.append(AssignmentNode(parameter_names[i], value))
    values, return_val = function_body.children
    new_body = BlockNode(assignments + values, return_val)
    new_function = FunctionDefinitionNode(new_params, new_body)

    return EvaluationResult(Type.FUNCTION, new_function.children, environment=environment.copy_stack())


class Interpreter:
    def __init__(self, stack: list[Environment] = None):
        self.stack = []
        if stack is not None:
            self.stack = stack

    def visit(self, node: Node | str):
        if isinstance(node, str):
            variable = self.find_in_env(node)
            return variable

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

                if len(parameter_values) < len(parameter_names):
                    return create_new_function(function, parameter_values)
                elif len(parameter_values) == len(parameter_names):
                    parameter_env = Environment()
                    for i, param in enumerate(parameter_values):
                        parameter_env.set_variable(parameter_names[i], param)
                    function.stack.append(parameter_env)
                    result = Interpreter(function.stack).visit(function_body)
                else:
                    raise Exception(
                        f"Invalid parameter count for function call. Expected {len(parameter_names)}, got {len(parameter_values)}")
            return result

        if node.type == "function_definition":
            return EvaluationResult(Type.FUNCTION, node.children, environment=self.copy_stack())

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

    def copy_stack(self) -> list[Environment]:
        return [Environment(x.variables.copy()) for x in self.stack]

    def interpret(self, ast):
        self.visit(ast)
