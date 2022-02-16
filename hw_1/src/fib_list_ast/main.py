import ast
import inspect
import networkx


def fib_list(n):
    res = [1, 1]
    for i in range(2, n):
        res.append(res[i - 1] + res[i - 2])
    return res


class AstVisitor(ast.NodeVisitor):
    __operations_dict = {"Sub": "-", "Add": "+"}

    def __init__(self):
        self.graph = networkx.DiGraph()

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_FunctionDef(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="function " + node.name)
        for arg in self.visit(node.args):
            self.graph.add_edge(node_str, arg, label="arg")
        for item in node.body:
            self.graph.add_edge(node_str, self.visit(item), label="body")
        return node_str

    def visit_arguments(self, node):
        for item in node.args:
            self.graph.add_node(str(item), label="arg " + item.arg)
        return list(map(str, node.args))

    def visit_Assign(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="assign")
        for target in node.targets:
            self.graph.add_edge(node_str, self.visit(target), label="target")
        self.graph.add_edge(node_str, self.visit(node.value), label="value")
        return node_str

    def visit_List(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="list")
        for item in node.elts:
            self.graph.add_edge(node_str, self.visit(item), label="elem")
        return node_str

    def visit_For(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="for")
        self.graph.add_edge(node_str, self.visit(node.target), label="target")
        self.graph.add_edge(node_str, self.visit(node.iter), label="iter")
        for item in node.body:
            self.graph.add_edge(str(node), self.visit(item), label="body")
        return node_str

    def visit_Expr(self, node):
        self.graph.add_node(str(node), label="expr")
        self.graph.add_edge(str(node), self.visit(node.value))
        return str(node)

    def visit_Name(self, node):
        self.graph.add_node(str(node), label="name " + node.id)
        return str(node)

    def visit_Call(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="Call")
        self.graph.add_edge(node_str, self.visit(node.func), labale="func")
        for item in node.args:
            self.graph.add_edge(node_str, self.visit(item), label="arg")
        return node_str

    def visit_Attribute(self, node):
        self.graph.add_node(str(node), label="Attribute")
        self.graph.add_edge(str(node), self.visit(node.value), label="value")
        self.graph.add_node(node.attr)
        self.graph.add_edge(str(node), node.attr, label="attr")
        return str(node)

    def visit_BinOp(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="bin op " + AstVisitor.__operations_dict[node.op.__class__.__name__])
        self.graph.add_edge(node_str, self.visit(node.left), label="left")
        self.graph.add_edge(node_str, self.visit(node.right), label="right")
        return str(node)

    def visit_Subscript(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="subscript")
        self.graph.add_edge(node_str, self.visit(node.slice), label="slice")
        self.graph.add_edge(node_str, self.visit(node.value), label="value")
        return node_str

    def visit_Index(self, node):
        self.graph.add_node(str(node), label="index")
        self.graph.add_edge(str(node), self.visit(node.value))
        return str(node)

    def visit_Num(self, node):
        self.graph.add_node(str(node), label="Num " + str(node.n))
        return str(node)

    def visit_Return(self, node):
        node_str = str(node)
        self.graph.add_node(node_str, label="return")
        self.graph.add_edge(node_str, self.visit(node.value))
        return node_str


def generate_ast(path_to_save_file):
    ast_object = ast.parse(inspect.getsource(fib_list))
    visitor = AstVisitor()
    visitor.visit(ast_object)
    networkx.drawing.nx_pydot.to_pydot(visitor.graph).write_png(path_to_save_file)

if __name__ == "__main__":
    generate_ast("artifacts/res.png")
