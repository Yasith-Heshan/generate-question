import sympy as sp
import random

from sympy.core.random import choice

from app.models.dataModels import LatexStringModel, LatexObject
from app.services.mcqRuleService import generateCustomeAnswerList, Rule
from app.utils.helpers import randint_exclude_list, generate_general_constant_without_sqrt, exp_hack


def generate_difficulty_level_2_type_1_equations(variable, other_sol_generator_var):
    terms_count = random.choice([i for i in range(1, 6)])
    polynomial = 0
    selected_powers = sorted([generate_general_constant_without_sqrt(-15, 15) for i in range(terms_count)])
    for i in selected_powers:
        coefficient = generate_general_constant_without_sqrt(-5, 5)
        polynomial += coefficient * variable ** (i + other_sol_generator_var)
    return polynomial

def generate_difficulty_level_4_equations(variable, other_sol_generator_var, terms_count_limit = 6):
    terms_count = random.choice([i for i in range(1, terms_count_limit)])
    polynomial = 0
    selected_terms = sorted(random.sample([i for i in range(1, 11)], k=terms_count))
    for i in selected_terms:
        coefficient = randint_exclude_list(-5, 5)
        polynomial += coefficient * variable ** (i + other_sol_generator_var)
    return polynomial

def get_answer_for_difficulty_2(f, g, variable):
    return sp.diff(f, variable) * g.as_expr() + f.as_expr() * sp.diff(g, variable)

def get_answer_for_difficulty_4(f, g, variable):
    return sp.Mul(sp.diff(f, variable) * g.as_expr() - f.as_expr() * sp.diff(g, variable), 1/(g**2), evaluate=False)

def generate_changed_equation(equation):
    return equation + randint_exclude_list(-15, 16)

def get_answer_for_difficulty_5_type_1(f, g, h, variable, other_sol_generator_var):
    other_solutions = []
    eq1_sol = f.subs(other_sol_generator_var, 0)
    eq2_sol = g.subs(other_sol_generator_var, 0)
    eq3_sol = h.subs(other_sol_generator_var, 0)

    intermediate_solution = get_answer_for_difficulty_2(eq1_sol, eq2_sol, variable)
    solution = (intermediate_solution * eq3_sol - eq1_sol * eq2_sol * sp.diff(eq3_sol,
                                                                              variable).as_expr()) / eq3_sol ** 2
    for m in [-1, 1, 3, 4]:
        eq1_m = f.subs(other_sol_generator_var, m)
        eq2_m = g.subs(other_sol_generator_var, m)
        eq3_m = eq3_sol
        intermediate_solution = get_answer_for_difficulty_2(eq1_m, eq2_m, variable)
        other_solutions.append((intermediate_solution * eq3_m - eq1_m * eq2_m * sp.diff(eq3_m, variable).as_expr()) / eq3_m ** 2)
    return solution, other_solutions

def get_answer_for_difficulty_5_type_2(f, g, h, variable, other_sol_generator_var):
    other_solutions = []
    eq1_sol = f.subs(other_sol_generator_var, 0)
    eq2_sol = g.subs(other_sol_generator_var, 0)
    eq3_sol = h.subs(other_sol_generator_var, 0)

    intermediate_solution = get_answer_for_difficulty_2(eq2_sol, eq3_sol, variable)
    solution = (sp.diff(eq1_sol, variable) * eq2_sol * eq3_sol - eq1_sol * intermediate_solution) / (
                eq2_sol * eq3_sol) ** 2

    for m in [-1, 1, 3, 4]:
        eq1_m = f.subs(other_sol_generator_var, m)
        eq2_m = eq2_sol
        eq3_m = eq3_sol
        intermediate_solution = get_answer_for_difficulty_2(eq2_m, eq3_m, variable)
        other_solutions.append((sp.diff(eq1_m, variable) * eq2_m * eq3_m - eq1_m * intermediate_solution) / (
                    eq2_m * eq3_m) ** 2)
    return solution, other_solutions

def get_answer_for_difficulty_5_type_3(f, g, h, variable, other_sol_generator_var):
    other_solutions = []
    eq1_sol = f.subs(other_sol_generator_var, 0)
    eq2_sol = g.subs(other_sol_generator_var, 0)
    eq3_sol = h.subs(other_sol_generator_var, 0)

    intermediate_solution = get_answer_for_difficulty_2(eq2_sol, eq3_sol, variable)
    solution = eq1_sol.as_expr() * intermediate_solution.as_expr() + sp.diff(eq1_sol,
                                                                             variable).as_expr() * eq2_sol.as_expr() * eq3_sol.as_expr()
    for m in [-1, 1, 3, 4]:
        eq1_m = f.subs(other_sol_generator_var, m)
        eq2_m = g.subs(other_sol_generator_var, m)
        eq3_m = h.subs(other_sol_generator_var, m)
        intermediate_solution = get_answer_for_difficulty_2(eq2_m, eq3_m, variable)
        other_solutions.append(eq1_m.as_expr() * intermediate_solution.as_expr() + sp.diff(eq1_m,
                                                                                             variable).as_expr() * eq2_m.as_expr() * eq3_m.as_expr())
    return solution, other_solutions

def generate_problem_22_E_3__3_07_questions(difficulty: int, question_count: int):
    equations_and_solutions = []

    for i in range(question_count):
        variable = sp.Symbol(random.choice(["x", "y", "z", "t", "u", "v", "w"]))
        function = sp.Function(random.choice(["f", "g", "h", "p", "q", "r"]))(variable)
        other_sol_generator_var = sp.Symbol("a")
        other_solutions = []
        solution, f, g, generic_equation = None, None, None, None

        if difficulty == 1:
            a = randint_exclude_list(-15, 15)
            b = randint_exclude_list(-15, 15)
            c = randint_exclude_list(-15, 15)
            d = randint_exclude_list(-15, 15)
            generic_equation = (a * variable ** other_sol_generator_var + b ) * (c * variable ** other_sol_generator_var + d)
            equation = generic_equation.subs(other_sol_generator_var, 1)
            function_equation = sp.Eq(function, equation)
        elif difficulty == 2:
            choice = random.choice([1, 2, 3])
            if choice == 1:
                f = generate_difficulty_level_2_type_1_equations(variable, other_sol_generator_var)
                g = generate_difficulty_level_2_type_1_equations(variable, other_sol_generator_var)
                generic_equation = sp.Mul(f, g, evaluate=False)
            elif choice == 2:
                f = generate_difficulty_level_2_type_1_equations(variable, other_sol_generator_var)
                g = generate_difficulty_level_4_equations(variable, other_sol_generator_var)
                generic_equation = sp.Mul(f, g, evaluate=False)
            elif choice == 3:
                f = generate_difficulty_level_4_equations(variable, other_sol_generator_var)
                g = generate_difficulty_level_2_type_1_equations(variable, other_sol_generator_var)
                generic_equation = sp.Mul(f, g, evaluate=False)
            else:
                f = generate_difficulty_level_4_equations(variable, other_sol_generator_var)
                g = generate_difficulty_level_4_equations(variable, other_sol_generator_var)
                generic_equation = sp.Mul(f, g, evaluate=False)
            equation = generic_equation.subs(other_sol_generator_var, 0)
            function_equation = sp.Eq(function, equation)
            f_sol = f.subs(other_sol_generator_var, 0)
            g_sol = g.subs(other_sol_generator_var, 0)
            solution = get_answer_for_difficulty_2(f_sol, g_sol, variable)
        elif difficulty == 3:
            a = randint_exclude_list(-15, 15)
            b = random.randint(-15, 15)
            c = randint_exclude_list(-15, 15)
            d = random.randint(-15, 15)
            generic_equation = (a * variable ** other_sol_generator_var + b)/ (c * variable + d)
            equation = generic_equation.subs(other_sol_generator_var, 1)
            function_equation = sp.Eq(function, equation)
        elif difficulty == 4:
            f = generate_difficulty_level_4_equations(variable, other_sol_generator_var) + randint_exclude_list(-15, 15)
            g = generate_difficulty_level_4_equations(variable, other_sol_generator_var)
            while sp.gcd(f.subs(other_sol_generator_var, 0), g.subs(other_sol_generator_var, 0)) != 1:
                g = generate_changed_equation(g)
            equation = f.subs(other_sol_generator_var, 0) / g.subs(other_sol_generator_var, 0)
            function_equation = sp.Eq(function, equation)
        elif difficulty == 5:
            eq1 = generate_difficulty_level_4_equations(variable, other_sol_generator_var, 3)
            eq2 = generate_difficulty_level_4_equations(variable, other_sol_generator_var, 3)
            while sp.gcd(eq1.subs(other_sol_generator_var, 0), eq2.subs(other_sol_generator_var, 0)) != 1:
                eq2 = generate_changed_equation(eq2)
            eq3 = generate_difficulty_level_4_equations(variable, other_sol_generator_var, 3)
            while sp.gcd(eq1.subs(other_sol_generator_var, 0) * eq2.subs(other_sol_generator_var, 0), eq3.subs(other_sol_generator_var, 0)) != 1:
                eq3 = generate_changed_equation(eq3)
            eq1_sol = eq1.subs(other_sol_generator_var, 0)
            eq2_sol = eq2.subs(other_sol_generator_var, 0)
            eq3_sol = eq3.subs(other_sol_generator_var, 0)
            choice = random.choice([1, 2, 3])
            if choice == 1:
                equation = (eq1_sol * eq2_sol) / eq3_sol
                solution, other_solutions = get_answer_for_difficulty_5_type_1(eq1, eq2, eq3, variable, other_sol_generator_var)
            elif choice == 2:
                equation = eq1_sol/ (eq2_sol * eq3_sol)
                solution, other_solutions = get_answer_for_difficulty_5_type_2(eq1, eq2, eq3, variable, other_sol_generator_var)
            else:
                equation = eq1_sol * eq2_sol * eq3_sol
                solution, other_solutions = get_answer_for_difficulty_5_type_3(eq1, eq2, eq3, variable, other_sol_generator_var)

            function_equation = sp.Eq(function, equation)
        else:
            raise ValueError('Unsupported difficulty level')

        question = LatexStringModel(
            placeholders=[LatexObject(function_equation, False, True)],
            string_value="Find the derivative of: {}",
        ).convert_to_latex()

        if difficulty == 1:
            solution = exp_hack(sp.diff(equation, variable))
            for m in [-1, 0, 3, 4]:
                other_solutions.append(exp_hack(sp.together(sp.diff(generic_equation.subs(other_sol_generator_var, m), variable))))
        elif difficulty == 2:
            f_sol = f.subs(other_sol_generator_var, 0)
            g_sol = g.subs(other_sol_generator_var, 0)
            solution = get_answer_for_difficulty_2(f_sol, g_sol, variable)
            other_solutions.append(
                get_answer_for_difficulty_2(f.subs(other_sol_generator_var, -2), g.subs(other_sol_generator_var, 0),
                                            variable))
            other_solutions.append(
                get_answer_for_difficulty_2(f.subs(other_sol_generator_var, -1), g.subs(other_sol_generator_var, 0),
                                            variable))
            other_solutions.append(
                get_answer_for_difficulty_2(f.subs(other_sol_generator_var, 1), g.subs(other_sol_generator_var, 0),
                                            variable))
            other_solutions.append(
                get_answer_for_difficulty_2(f.subs(other_sol_generator_var, 3), g.subs(other_sol_generator_var, 0),
                                            variable))

        elif difficulty == 3:
            solution = sp.together(sp.diff(equation, variable))
            for m in [-1, 0, 3, 4]:
                other_solutions.append(sp.together(sp.diff(generic_equation.subs(other_sol_generator_var, m), variable)))

        elif difficulty == 4:
            solution = get_answer_for_difficulty_4(f.subs(other_sol_generator_var, 0), g.subs(other_sol_generator_var, 0), variable)
            other_solutions.append(get_answer_for_difficulty_4(f.subs(other_sol_generator_var, -1), g.subs(other_sol_generator_var, 0), variable))
            other_solutions.append(
                get_answer_for_difficulty_4(f.subs(other_sol_generator_var, 1), g.subs(other_sol_generator_var, 0),
                                            variable))
            other_solutions.append(
                get_answer_for_difficulty_4(f.subs(other_sol_generator_var, 3), g.subs(other_sol_generator_var, 0),
                                            variable))
            other_solutions.append(
                get_answer_for_difficulty_4(f.subs(other_sol_generator_var, 4), g.subs(other_sol_generator_var, 0),
                                            variable))

        other_solution_latex = [LatexStringModel(
            placeholders=[LatexObject(x, False, False)],
            string_value="{}"
        ).convert_to_latex() for x in other_solutions]

        equations_and_solutions.append({
            'question': question,
            'solution': LatexStringModel(
                placeholders=[LatexObject(solution, False, False)],
                string_value="{}"
                ).convert_to_latex(),
            'other_solutions': other_solution_latex
        })
    return equations_and_solutions
