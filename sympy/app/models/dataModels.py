from fractions import Fraction
from typing import List, Optional
import sympy as sp
from sympy.printing.latex import LatexPrinter
latex = LatexPrinter(dict(order='none')).doprint

class DualInequalityParams:
    def __init__(self, left, inequality_op1, expression, inequality_op2, right, double_dollar=False):
        self.left = left
        self.inequality_op1 = inequality_op1
        self.expression = expression
        self.inequality_op2 = inequality_op2
        self.right = right
        self.double_dollar = double_dollar

class LatexConverter:
    def convert_expr_to_latex(self, expr):
        if isinstance(expr, sp.Eq):
            lhs = self.convert_expr_to_latex(expr.lhs)
            rhs = self.convert_expr_to_latex(expr.rhs)
            return f"{lhs} = {rhs}"

        if isinstance(expr, sp.Lt):
            lhs = self.convert_expr_to_latex(expr.lhs)
            rhs = self.convert_expr_to_latex(expr.rhs)
            return f"{lhs} < {rhs}"

        if isinstance(expr, sp.Gt):
            lhs = self.convert_expr_to_latex(expr.lhs)
            rhs = self.convert_expr_to_latex(expr.rhs)
            return f"{lhs} > {rhs}"

        if isinstance(expr, sp.Le):
            lhs = self.convert_expr_to_latex(expr.lhs)
            rhs = self.convert_expr_to_latex(expr.rhs)
            return f"{lhs} \\leq {rhs}"

        if isinstance(expr, sp.Ge):
            lhs = self.convert_expr_to_latex(expr.lhs)
            rhs = self.convert_expr_to_latex(expr.rhs)
            return f"{lhs} \\geq {rhs}"

        if isinstance(expr, sp.Add):
            # Handle addition (e.g., if the equation contains a sum)
            terms = []
            for arg in expr.args:
                term_latex = self.convert_expr_to_latex(arg)
                if arg.could_extract_minus_sign():
                    term_latex = f"{term_latex}"
                terms.append(term_latex)
            # Join terms and handle proper placement of '+' and '-' signs
            result = terms[0]
            for term in terms[1:]:
                if term.startswith('-'):
                    result += f" {term}"
                else:
                    result += f" + {term}"
            return result

        if isinstance(expr, sp.Mul):
            fractions = [arg for arg in expr.args if isinstance(arg, sp.Rational)]
            variables = [arg for arg in expr.args if arg.is_symbol]

            if fractions and variables:
                fraction_latex = latex(fractions[0])
                variable_latex = latex(variables[0])
                return f"{fraction_latex} {variable_latex}"

        # Default LaTeX conversion for other cases
        return latex(expr)

    def convert_double_inequality_in_latex(self, params: DualInequalityParams, double_dollar=False):
        dollar_sign = '$$' if double_dollar else '$'
        if isinstance(params.left, Fraction):
            params.left = sp.Rational(params.left.numerator, params.left.denominator)
        if isinstance(params.expression, Fraction):
            params.expression = sp.Rational(params.expression.numerator, params.expression.denominator)
        if isinstance(params.right, Fraction):
            params.right = sp.Rational(params.right.numerator, params.right.denominator)
        if isinstance(params.left, sp.Basic):
            params.left = self.convert_expr_to_latex(params.left)
        else:
            params.left = latex(params.left)
        if isinstance(params.expression, sp.Basic):
            params.expression = self.convert_expr_to_latex(params.expression)
        else:
            params.expression = latex(params.expression)
        if isinstance(params.right, sp.Basic):
            params.right = self.convert_expr_to_latex(params.right)
        else:
            params.right = latex(params.right)

        if params.inequality_op1 == '<=':
            inequality_1 = "\\leq"
        else:
            inequality_1 = params.inequality_op1

        if params.inequality_op2 == '<=':
            inequality_2 = "\\leq"
        else:
            inequality_2 = params.inequality_op2
        return f"{dollar_sign} {params.left} {inequality_1} {params.expression} {inequality_2} {params.right} {dollar_sign}"

class LatexObject:
    value: any
    is_in_latex_format: bool
    is_double_dollar_required: bool

    def __init__(self, value: any, is_in_latex_format: bool = False, is_double_dollar_required: bool = False):
        self.value = value
        self.is_in_latex_format = is_in_latex_format
        self.is_double_dollar_required = is_double_dollar_required


class LatexStringModel():
    # placeholders are the list of sympy equation values
    placeholders: List[LatexObject]
    string_value: str
    latex_converter = LatexConverter()

    def __init__(self, string_value: str, placeholders: List[LatexObject]):
        self.placeholders = placeholders
        self.string_value = string_value

    def convert_to_latex(self):
        converted_placeholders = []

        for expr in self.placeholders:
            if expr.is_in_latex_format:
                converted_placeholders.append(expr.value)
                continue
            dollar_sign = '$$' if expr.is_double_dollar_required else '$'
            latex_expr = self.latex_converter.convert_expr_to_latex(expr.value)
            converted_placeholders.append(f"{dollar_sign}{latex_expr}{dollar_sign}")

        formatted_string = self.string_value.format(*converted_placeholders)
        return formatted_string


class ServiceResponce():
    question: str
    graph_img: Optional[str]= None
    correct_solution: str
    other_solutions: Optional[List[str]]

    def __init__(self, question: str, correct_solution: str, other_solutions: Optional[List[str]] = None,graph_img:Optional[str]=None):
        self.question = question
        self.correct_solution = correct_solution
        self.other_solutions = other_solutions
        self.graph_img =graph_img
