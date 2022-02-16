import os
from typing import List
from fib_list_ast.main import generate_ast


def start_document() -> str:
    return "\\documentclass{article}\n" \
           "\\usepackage{graphicx}\n" \
           "\\begin{document}\n"


def end_document() -> str:
    return "\\end{document}\n"


def start_table(number_of_cols: int) -> str:
    return "\\begin{tabular}" + "{" + "|".join(["c"] * number_of_cols) + "}\n"


def end_table() -> str:
    return "\\end{tabular}\n"


def list_to_latex_row(lst: List) -> str:
    return " & ".join(map(str, lst)) + "\\\\\n"


def get_table(double_lst: List[List]) -> str:
    return start_table(len(double_lst[0])) + "".join(map(lambda lst: list_to_latex_row(lst), double_lst)) + end_table()


def get_picture(path_to_picture: str) -> str:
    return f"\\includegraphics[width=0.9\\linewidth]{{{path_to_picture}}}\n"


def get_table_with_picture_tex_document(double_lst: List[List], path_to_picture: str) -> str:
    return start_document() + get_table(double_lst) + get_picture(path_to_picture) + end_document()


if __name__ == "__main__":
    double_list_example = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    generate_ast("artifacts/tmp.png")
    with open("artifacts/res.tex", "w") as f:
        f.write(get_table_with_picture_tex_document(double_list_example, "artifacts/tmp.png"))
    os.system("pdflatex -output-directory=artifacts artifacts/res.tex")
    os.system("rm artifacts/res.aux artifacts/res.log artifacts/tmp.png")
