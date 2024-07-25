from src.interpreter.function_executor import FunctionExecutor
from src.interpreter.types import EvaluationResult, Type


def f_mult(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value * params[1].value
    return EvaluationResult(Type.INTEGER, result)


def f_eq(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].type == params[1].type and params[0].value == params[1].value
    return EvaluationResult(Type.BOOLEAN, result)


def f_not(params: list[EvaluationResult]) -> EvaluationResult:
    result = not params[0].value
    return EvaluationResult(Type.BOOLEAN, result)


def f_and(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value and params[1].value
    return EvaluationResult(Type.BOOLEAN, result)


def f_or(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value and params[1].value
    return EvaluationResult(Type.BOOLEAN, result)


def f_less(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value < params[1].value
    return EvaluationResult(Type.BOOLEAN, result)


def f_greater(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value > params[1].value
    return EvaluationResult(Type.BOOLEAN, result)


def f_plus(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value + params[1].value
    return EvaluationResult(Type.INTEGER, result)


def f_minus(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value - params[1].value
    return EvaluationResult(Type.INTEGER, result)


def f_div(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value // params[1].value
    return EvaluationResult(Type.INTEGER, result)


def f_mod(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value % params[1].value
    return EvaluationResult(Type.INTEGER, result)


def f_head(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value[0]
    return EvaluationResult(result.type, result)


def f_tail(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[1:]
    return EvaluationResult(Type.LIST, result)


def f_is_empty(params: list[EvaluationResult]) -> EvaluationResult:
    result = len(params[0].value) == 0
    return EvaluationResult(Type.BOOLEAN, result)


def f_concat(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[0].value + params[1].value
    return EvaluationResult(Type.LIST, result)


def f_if(params: list[EvaluationResult]) -> EvaluationResult:
    result = params[1] if params[0].value else params[2]
    return EvaluationResult(result.type, result)


def f_print(params: list[EvaluationResult]) -> EvaluationResult:
    print(params[0].value)
    return EvaluationResult(Type.UNIT, None)


class FunctionRegistry:
    def __init__(self):
        self.functions = {
            "eq": FunctionExecutor("eq", [Type.BOOLEAN, Type.BOOLEAN], f_eq),
            "not": FunctionExecutor("not", [Type.BOOLEAN], f_not),
            "and": FunctionExecutor("and", [Type.BOOLEAN, Type.BOOLEAN], f_and),
            "or": FunctionExecutor("or", [Type.BOOLEAN, Type.BOOLEAN], f_or),
            "less": FunctionExecutor("less", [Type.INTEGER, Type.INTEGER], f_less),
            "greater": FunctionExecutor("greater", [Type.INTEGER, Type.INTEGER], f_greater),

            "plus": FunctionExecutor("plus", [Type.INTEGER, Type.INTEGER], f_plus),
            "minus": FunctionExecutor("minus", [Type.INTEGER, Type.INTEGER], f_minus),
            "mult": FunctionExecutor("mult", [Type.INTEGER, Type.INTEGER], f_mult),
            "div": FunctionExecutor("div", [Type.INTEGER, Type.INTEGER], f_div),
            "mod": FunctionExecutor("mod", [Type.INTEGER, Type.INTEGER], f_mod),

            "head": FunctionExecutor("head", [Type.LIST], f_head),
            "tail": FunctionExecutor("tail", [Type.LIST], f_tail),
            "is_empty": FunctionExecutor("is_empty", [Type.LIST], f_is_empty),
            "concat": FunctionExecutor("concat", [Type.LIST, Type.LIST], f_concat),

            "if": FunctionExecutor("if", [Type.BOOLEAN, None, None], f_if),
            "print": FunctionExecutor("print", [None], f_print),
        }

    def get_function(self, name) -> FunctionExecutor:
        return self.functions.get(name)
