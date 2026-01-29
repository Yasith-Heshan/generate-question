import random
import sympy as sp
from app.models.dataModels import LatexStringModel, LatexObject
from app.utils.helpers import  generate_general_constant_number,generate_general_constant_without_sqrt
from app.services.mcqRuleService import generateCustomeAnswerList, Rule

x, y,z,t,u,v,w, k = sp.symbols('x y z t u v w k')


def generate_equestion(difficulty: int, variable = x):
    if difficulty == 1:
        return generate_difficulty_level_1_equations(variable)
    elif difficulty == 2:
        return generate_difficulty_level_2_equations(variable)
    elif difficulty == 3:
        return generate_difficulty_level_3_equations(variable)
    elif difficulty == 4:
        return generate_difficulty_level_4_equations(variable)
    else:
        return generate_difficulty_level_5_equations(variable)

def generate_difficulty_level_1_equations(variable):
    expression = generate_general_constant_number(-10, 10)
    constant = generate_general_constant_number(-10, 10)
    limit = sp.Limit(expression, variable, constant, dir='+-')
    solution = sp.limit(expression, variable, constant, dir='+-')
    return limit, solution, None

def generate_difficulty_level_2_equations(variable):
    a = generate_general_constant_without_sqrt(-10, 10)
    b = generate_general_constant_without_sqrt(-10, 10)
    constant = generate_general_constant_without_sqrt(-10, 10)
    expression = a*variable + b
    limit = sp.Limit(expression, variable, constant, dir='+-')
    solution = sp.limit(expression, variable, constant, dir='+-')
    return limit, solution, None

def generate_difficulty_level_3_equations(variable):
    degree = random.choice([2, 3, 4, 5,6])
    polynomial = 0
    for i in range(degree):
        if(degree==2):
            coefficient = generate_general_constant_without_sqrt(-10,10)
        else:
            coefficient = random.choice([i for i in range(-10, 11) if i != 0])
        polynomial += coefficient * variable**i
    constant = generate_general_constant_without_sqrt(-10, 10)
    limit = sp.Limit(polynomial, variable, constant, dir='+-')
    solution = sp.limit(polynomial, variable, constant, dir='+-')
    return limit, solution, None

def generate_difficulty_level_4_equations(variable):
    
    # Define possible limit numbers with higher probability for specific trigonometric values
    trig_values = [0, sp.pi/6, sp.pi/4, sp.pi/3, sp.pi/2, 5*sp.pi/6, 3*sp.pi/4, 2*sp.pi/3, sp.pi, 3*sp.pi/2, 2*sp.pi]
    # Define possible functions
    functions = [
        sp.Abs(variable),
        sp.sin(variable),
        sp.cos(variable),
        sp.tan(variable),
        sp.exp(variable),
        sp.log(variable)
    ]
    
    # Randomly select a combination of functions
    selected_functions = random.sample(functions, k=random.randint(2, 3))
    if(sp.sin(variable) in selected_functions or sp.cos(variable) in selected_functions or sp.tan(variable) in selected_functions):
        limit_number = random.choice(trig_values)
    else:
        limit_number = generate_general_constant_number(-10, 10)   
    
    # Create the expression by combining the selected functions
    expression = selected_functions[0]
    for func in selected_functions[1:]:
        expression += func
    
    # Create the limit and solution
    limit = sp.Limit(expression, variable, limit_number, dir='+-')
    lhs_solution = sp.limit(expression, variable, limit_number, dir='-')
    rhs_solution = sp.limit(expression, variable, limit_number, dir='+')
    solution = lhs_solution if lhs_solution == rhs_solution else "no_solutions"
    return limit, solution, None

def generate_difficulty_level_5_equations(variable):
    # Generate coefficients for the linear, quadratic, and constant functions
    def generate_piece(degree):
        if degree == 0:  # Constant
            return generate_general_constant_without_sqrt(-10, 10)
        elif degree == 1:  # Linear
            a = generate_general_constant_without_sqrt(-10, 10)
            b = generate_general_constant_without_sqrt(-10, 10)
            return a * variable + b
        elif degree == 2:  # Quadratic
            a = generate_general_constant_without_sqrt(-10, 10)
            b = generate_general_constant_without_sqrt(-10, 10)
            c = generate_general_constant_without_sqrt(-10, 10)
            return a * variable**2 + b * variable + c

    # Randomly choose breakpoints and corresponding pieces
    breakpoint = generate_general_constant_without_sqrt(-10, 10)
    left_piece = generate_piece(random.choice([0, 1, 2]))
    right_piece = generate_piece(random.choice([0, 1, 2]))
    
    # Define the piecewise function
   
    
    # Define the limit at the breakpoint
    limit = sp.Limit(k, variable, breakpoint, dir='+-')
    lhs_solution = sp.limit(left_piece, variable, breakpoint, dir='-')
    rhs_solution = sp.limit(right_piece, variable, breakpoint, dir='+')
    solution_exist = random.choice([True, False])
    right_piece = right_piece+(lhs_solution-rhs_solution) if solution_exist else right_piece
    rhs_solution = sp.limit(right_piece, variable, breakpoint, dir='+')
    piecewise_function =  sp.Piecewise(
        (left_piece, variable <= breakpoint),
        (right_piece, variable > breakpoint),Evaluate=False
    )
    solution = lhs_solution if lhs_solution == rhs_solution else "no_solutions"

    return limit, solution, piecewise_function


def generate_problem_22_E_3__3_01_questions(difficulty: int,
                                    questions_count: int):
    equations_and_solutions = []

    for _ in range(questions_count):
        letter = random.choice(["x", "y", "z", "t", "u", "v", "w"])
        variable = sp.Symbol(letter)
        limit, solution, pf = generate_equestion(difficulty,variable)
        if(solution != sp.oo and solution != -sp.oo and solution != "no_solutions"):
            other_solutions = generateCustomeAnswerList(Rule.MULTIPLY.value,solution,4)
        else:
            other_solutions = generateCustomeAnswerList(Rule.MULTIPLY.value,random.randint(1,10),4)
        if(difficulty == 5 and solution != "no_solutions"):
            other_solutions = other_solutions[:3]
        if(pf):
            pf_str = LatexStringModel(
                string_value="{}",
                placeholders=[LatexObject(sp.Eq(sp.Function("f")(x),pf), False, True)],
                ).convert_to_latex()
            question = (LatexStringModel(
                string_value="Evaluate the following limit: {}",
                placeholders=[LatexObject(limit, False, True)],
            ).convert_to_latex().replace("k",f"f({letter})")+f" where "+pf_str)
        else:
            question = LatexStringModel(
                placeholders=[LatexObject(limit, False, True)],
                string_value="Evaluate the following limit: {}",
            ).convert_to_latex()
        other_solution_latex = [LatexStringModel(
                placeholders=[LatexObject(x, False, False)],
                string_value="{}"
                ).convert_to_latex() for x in other_solutions]
        if(difficulty == 5 and solution != "no_solutions"):
            other_solution_latex = other_solution_latex + ["Do not exist."]
        equations_and_solutions.append({
            "question": question,
            "solution": LatexStringModel(
                placeholders=[LatexObject(solution, False, False)],
                string_value="{}"
                ).convert_to_latex() if solution != "no_solutions" else "Do not exist.",
            "other_solutions": other_solution_latex
        })
    return equations_and_solutions

