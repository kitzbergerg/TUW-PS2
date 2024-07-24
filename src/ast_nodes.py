class Node(object):
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children or []
        self.value = value


class AssignmentNode(Node):
    def __init__(self, name, new_val):
        super().__init__('assignment', children=[name, new_val])


class FunctionCallNode(Node):
    def __init__(self, name, args):
        super().__init__('function_call', children=[name, args])


class FunctionDefinitionNode(Node):
    def __init__(self, name, params, body):
        super().__init__('function_definition', children=[name, params, body])


class IntegerNode(Node):
    def __init__(self, value):
        super().__init__('integer', value=value)


class ListNode(Node):
    def __init__(self, elements):
        super().__init__('list', children=elements)

# Define other AST node classes for your language elements
