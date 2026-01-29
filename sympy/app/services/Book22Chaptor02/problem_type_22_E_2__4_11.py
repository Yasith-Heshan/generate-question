import random
import sympy as sp
from fractions import Fraction
from app.models.dataModels import LatexStringModel, LatexObject
from app.utils.helpers import  generate_general_constant_number
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

def generate_difficulty_level_1_equations(variable,level_5=False):
    a = generate_general_constant_number(-100, 100)
    c=random.choice([1,2,3,4,5])
    if level_5:
        limit_type = "+-"
    else:
        limit_type = random.choice(["+","-"])
    limit_fn = a/(variable**c)
    goes_to = 0
    limit = sp.Limit(limit_fn, variable, goes_to, dir=limit_type)
    if level_5:
        r_solution = sp.limit(limit_fn, variable, goes_to, dir="+")
        l_solution = sp.limit(limit_fn, variable, goes_to, dir="-")
        if r_solution == l_solution:
            solution = r_solution
        else:
            solution = "no_solutions"
    else:
        solution = sp.limit(limit_fn, variable, goes_to, dir=limit_type)
    other_solutions = [i for i in [sp.oo, -sp.oo] if i!=solution]
    return limit, solution, other_solutions

def generate_difficulty_level_2_equations(variable,level_5=False):
    p = random.choice([i for i in range(-20,20)])
    q = random.choices( [i for i in range(-20, 0)]+[1]+[j for j in range(2,21)], weights=[1]*20 + [40]+[1]*19, k=1)[0]
    a = generate_general_constant_number(-100,100)
    c = random.choice([1,2,3,4,5])
    if level_5:
        limit_type = "+-"
    else:
        limit_type = random.choice(["+","-"])
    limit_fn = (a/(q*variable-p)**c)
    goes_to = Fraction(p,q)
    limit = sp.Limit(limit_fn, variable, goes_to, dir=limit_type)
    if level_5:
        r_solution = sp.limit(limit_fn, variable, goes_to, dir="+")
        l_solution = sp.limit(limit_fn, variable, goes_to, dir="-")
        if r_solution == l_solution:
            solution = r_solution
        else:
            solution = "no_solutions"
    else:
        solution = sp.limit(limit_fn, variable, goes_to, dir=limit_type)
    other_solutions = [i for i in [sp.oo, -sp.oo] if i!=solution]
    return limit, solution, other_solutions


def generate_difficulty_level_3_equations(variable,level_5=False):
    a = random.choice([i for i in range(-20,20) if i != 0])
    b = random.choice([i for i in range(-20,20) if i != 0])
    c = random.choice([1,2,3,4,5])
    if level_5:
        limit_type = "+-"
    else:
        limit_type = random.choice(["+","-"])
    limit_fn = (a*variable+b)/(variable**c)
    goes_to = 0
    limit = sp.Limit(limit_fn, variable, goes_to, dir=limit_type)
    if level_5:
        r_solution = sp.limit(limit_fn, variable, goes_to, dir="+")
        l_solution = sp.limit(limit_fn, variable, goes_to, dir="-")
        if r_solution == l_solution:
            solution = r_solution
        else:
            solution = "no_solutions"
    else:
        solution = sp.limit(limit_fn, variable, goes_to, dir=limit_type)
    other_solutions = [i for i in [sp.oo, -sp.oo] if i!=solution]
    return limit, solution, other_solutions

def generate_difficulty_level_4_equations(variable,level_5=False):
    a = random.choice([i for i in range(-20,20)])
    b = random.choice([i for i in range(-20,20)])
    c = random.choice([1,2,3,4,5])
    p = random.choice([i for i in range(-20,20)])
    q = random.choices( [i for i in range(-20, 0)]+[1]+[j for j in range(2,21)], weights=[1]*20 + [40]+[1]*19, k=1)[0]
    if level_5:
        limit_type = "+-"
    else:
        limit_type = random.choice(["+","-"])
    limit_fn = (a*variable+b)/(q*variable-p)**c
    goes_to = Fraction(p,q)
    limit = sp.Limit(limit_fn, variable, goes_to, dir=limit_type)
    if level_5:
        r_solution = sp.limit(limit_fn, variable, goes_to, dir="+")
        l_solution = sp.limit(limit_fn, variable, goes_to, dir="-")
        if r_solution == l_solution:
            solution = r_solution
        else:
            solution = "no_solutions"
    else:
        solution = sp.limit(limit_fn, variable, goes_to, dir=limit_type)
    other_solutions = [i for i in [sp.oo, -sp.oo] if i!=solution]
    return limit, solution, other_solutions 

def generate_difficulty_level_5_equations(variable):
    level = random.choices([1,2,3,4],weights=[4,3,2,1],k=1)[0]
    if level == 1:
        return generate_difficulty_level_1_equations(variable,level_5=True)
    elif level == 2:
        return generate_difficulty_level_2_equations(variable,level_5=True)
    elif level == 3:
        return generate_difficulty_level_3_equations(variable,level_5=True)
    elif level == 4:
        return generate_difficulty_level_4_equations(variable,level_5=True)
    else:
        return generate_difficulty_level_5_equations(variable,level_5=True)

def generate_problem_22_E_2__4_11_questions(difficulty: int,
                                    questions_count: int):
    equations_and_solutions = []

    for _ in range(questions_count):
        letter = random.choice(["x", "y", "z", "t", "u", "v", "w"])
        variable = sp.Symbol(letter)
        limit, solution,other_solutions = generate_equestion(difficulty,variable)
        selected_answer = 0
        while selected_answer == 0 or selected_answer == solution:
            selected_answer = random.randint(1,10)
        custom_answers = generateCustomeAnswerList(Rule.MULTIPLY.value,selected_answer,3-len(other_solutions))
        print(solution)
        other_solutions = other_solutions + custom_answers
        question = LatexStringModel(
            placeholders=[LatexObject(limit, False, True)],
            string_value="Evaluate the following limit: {}",
        ).convert_to_latex().replace("\left(","",1).rsplit("\\right)",1)[0]+"$$"
        equations_and_solutions.append({
            "question": question,
            "solution": LatexStringModel(
                placeholders=[LatexObject(solution, False, False)],
                string_value="{}"
                ).convert_to_latex() if solution != "no_solutions" else "Do not exist.",
            "other_solutions": [LatexStringModel(
                placeholders=[LatexObject(x, False, False)],
                string_value="{}"
                ).convert_to_latex() for x in other_solutions] + ["Do not exist."]
        })
    return equations_and_solutions

