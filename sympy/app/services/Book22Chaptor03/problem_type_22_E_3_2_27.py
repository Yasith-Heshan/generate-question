import math
import random
from fractions import Fraction
from typing import Any, Dict, List

import numpy as np
import copy
import sympy as sp
from app.models.dataModels import (LatexObject, LatexStringModel,
                                   ServiceResponce)


from app.services.graphService import FunctionInformation, generate_graph

def different_int(exclude, low=-10, high=10):
    """Get a random integer different from 'exclude'."""
    while True:
        val = random.randint(low, high)
        if val != exclude:
            return val

def generate_random_case_polynomials_5(x):
    a = random.randint(-2, 2)
    case = random.choice(["case1", "case2", "case3"])
    
    if case == "case1":
        # Case 1: e ≠ b
        b = random.randint(-1, 1)
        e = different_int(b,-2,2)
        c = random.randint(1, 2)
        d = random.randint(-5, 5)
        p = sp.expand(b * (x - a)**2 + c * (x - a) + d)
        q = sp.expand(e * (x - a)**2 + c * (x - a) + d)
    
    elif case == "case2":
        # Case 2: e ≠ b, c ≠ f
        b = random.randint(-1, 1)
        
        c = random.randint(-1, 1)
        
        if c== 0 and b ==0:
            b=3
        e = different_int(b,-2,2)
        f = different_int(c,1,2)
        d = random.randint(-3, 5)
        p = sp.expand(b * (x - a)**2 + c * (x - a) + d)
        q =sp.expand(e * (x - a)**2 + f * (x - a) + d)

    else:
        # Case 3: g ≠ d
        b = random.randint(-1, 1)
        e = random.randint(-1, 1)
        c = random.randint(1, 2)
        f = random.randint(1, 2)
        d = random.randint(-3, 5)
        g = different_int(d,-3,3)
        p = sp.expand(b * (x - a)**2 + c * (x - a) + d)
        q = sp.expand(e * (x - a)**2 + f * (x - a) + g)
  
    return p, q, a

def random_coefficient1():
    """Generate a random coefficient: integer (higher probability), fraction, or square root."""
    choice = random.choices(["int", "frac", "sqrt"], weights=[5, 2, 2])[0]
    if choice == "int":
        return sp.Integer(random.randint(-10, 10))
    elif choice == "frac":
        return sp.Rational(random.randint(-10, 10), random.randint(1, 5))
    elif choice == "sqrt":
        return sp.sqrt(random.randint(1, 10)) * random.choice([-1, 1])


def generate_polynomial(x, degree =5):
    """Generate a polynomial function with a random degree between 0 and 5."""
  
    degree = random.randint(2, degree)
    polynomial = sum(random_coefficient_3() * x**i for i in range(degree + 1))
    return polynomial


def random_coefficient_3(nonzero=False, min_val=-15, max_val=15):
    """Generate a random integer coefficient within the given range."""
    val = random.randint(min_val, max_val)
    return val if not nonzero or val != 0 else random_coefficient_3(nonzero, min_val, max_val)


def generate_type1(x):
    """Generate a rational function of type (ax^3 + bx^2 + c) / (dx + e)."""
    x = sp.Symbol('x')
    a, b, c = random_coefficient_3(), random_coefficient_3(), random_coefficient_3(nonzero=True)
    d, e = random_coefficient_3(nonzero=True), random_coefficient_3()
    
    f_x = (a * x**3 + b * x**2 + c) / (d * x + e)
    correct_answer = LatexStringModel(
                    string_value="Is neither continuous nor differentiable at {}.",
                    placeholders=[ LatexObject(sp.Eq(x, Fraction(-e, d)), False, False)]
               
                ).convert_to_latex()
    other_solutions = [
        "Is both continuous and differentiable on the entire real numbers.",
        LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at {}.",
                    placeholders=[LatexObject(sp.Eq(x, Fraction(-e, d)), False, False)]
               
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is differentiable on the entire real numbers but not continuous at {}. ",
                    placeholders=[LatexObject(sp.Eq(x, Fraction(-e, d)), False, False)]
                ).convert_to_latex(),
                                    "None of the above."]
    return f_x, correct_answer, other_solutions


def generate_type2(x):
    """Generate a rational function of type (ax^4 + bx + c) / (x^2 + dx + e), where the denominator is not factored."""

    a, b, c = random_coefficient_3(), random_coefficient_3(), random_coefficient_3(nonzero=True)
    d, e = random_coefficient_3(), random_coefficient_3()
    
    denominator = x**2 + d * x + e
    while sp.discriminant(denominator, x) == 0:
        d, e = random_coefficient_3(), random_coefficient_3()
    
    f_x = (a * x**4 + b * x + c) / sp.expand((x-d)*(x-e))
    correct_answer = LatexStringModel(
                    string_value="Is neither continuous nor differentiable at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(x, d), False, False), LatexObject(sp.Eq(x, e), False, False)]
               
                ).convert_to_latex()
    other_solutions = [
        "Is both continuous and differentiable on the entire real numbers.",
        LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(x, d), False, False), LatexObject(sp.Eq(x, e), False, False)]
               
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is differentiable on the entire real numbers but not continuous at {} and {}. ",
                    placeholders=[LatexObject(sp.Eq(x, d), False, False), LatexObject(sp.Eq(x,e), False, False)]
                ).convert_to_latex(),
                                    "None of the above."]
    
    return f_x, correct_answer, other_solutions


def generate_type3(x):
    """Generate a rational function of type (x^2 + bx + c) / (2x^2 + 5x + 9) where b^2 - 4ac < 0."""
   
    while True:
        a, b, c = random_coefficient_3(), random_coefficient_3(), random_coefficient_3()
        if (b**2 - 4*a*c) < 0:
            break
    
    f_x = sp.expand((x-a)*(x-b)+random.randint(1,10)) / (a*x**2 + b*x + c)
    correct_answer = "Is both continuous and differentiable on the entire real numbers."
    other_solutions = [
        LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(x, a), False, False), LatexObject(sp.Eq(x, b), False, False)]
               
                ).convert_to_latex(),
        LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(x, a), False, False), LatexObject(sp.Eq(x, b), False, False)]
               
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is differentiable on the entire real numbers but not continuous at {} and {}. ",
                    placeholders=[LatexObject(sp.Eq(x, a), False, False), LatexObject(sp.Eq(x,b), False, False)]
                ).convert_to_latex(),
                                    "None of the above."]
    
    return f_x, correct_answer, other_solutions

def refactor_functions2(p, q, a):
    q_list1 = []
    for i in range(a, a + 5):
        q_list1.append(q.eval(x=i))
    # print(min(q_list1),max(q_list1))

    p_list1 = []
    for i in range(a - 5, a + 1):
        p_list1.append(p.eval(x=i))
    # print(min(p_list1),max(p_list1))
    min_both = min(min(q_list1), min(p_list1))
    max_both = max(max(q_list1), max(p_list1))
    # print(f"min {min(min(q_list1),min(p_list1))},max {max(max(q_list1),max(p_list1))}")

    # step 2
    con = 10 / (max_both - min_both)
    con_2 = (max_both + min_both) / 2
    p = (p - con_2) * con + con_2
    q = (q - con_2) * con + con_2
    # print(p.eval(x=a),q.eval(x=a))
    p_at_a = p.eval(x=a)
    q_at_a = q.eval(x=a)
    floor_value_in_q = math.floor(q_at_a)
    floor_value_in_p = math.floor(p_at_a)

    q = q + floor_value_in_q - q_at_a
    p = p + floor_value_in_p - p_at_a

    return p, p, a
def  generate_problem_22_E_3__2_27_questions(difficulty: int, questions_count: int):
    def generate_question_and_answers(difficulty):
        variable_names = ['x', 'y', 't', 'u', 'v', 'z', ]
        function_names = ['f', 'g', 'h']
        
        var = sp.Symbol(random.choice(variable_names))
        func_name = random.choice(function_names)
        if difficulty == 1:
            function = sp.Eq(sp.Function(func_name)(var), generate_polynomial(var))
            a = random.randint(0, 10)
            other_solutions = [
                LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at  {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is differentiable on the entire real numbers but not continuous at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is neither continuous nor differentiable at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="None of the above. ",
                    placeholders=[]
                ).convert_to_latex()
            ]
            correct_answer = LatexStringModel(
                    string_value="Is both continuous and differentiable on the entire real numbers. ",
                    placeholders=[]
                ).convert_to_latex()
            return function, other_solutions, correct_answer
        
        elif difficulty == 2:
            x = var
            p = random.randint(-3, 3) or 1
            q = random.randint(-10, 10)
            r = random.randint(-3, 3) or 1
            s = random.randint(-10, 10)
            type = random.choice([1,0, 2])
            if type==1:
                r = random.randint(1, 3) or 1
                while q / p == s / r:
                    q = random.randint(-10, 10)
                    s = random.randint(-10, 10)
                
                function = sp.Eq(sp.Function(func_name)(var),sp.Abs((p * x + q) * (r * x + s)).expand())
                correct_answer = LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -q,p)), False, False), LatexObject(sp.Eq(var,Fraction( -s,r)), False, False)]
                ).convert_to_latex()

                other_solutions = [
                     LatexStringModel(
                    string_value="Is both continuous and differentiable on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is differentiable on the entire real numbers but not continuous at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(var,Fraction( -q,p)), False, False), LatexObject(sp.Eq(var, Fraction( -s,r)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is neither continuous nor differentiable at {} and {}. ",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -q,p)), False, False), LatexObject(sp.Eq(var, Fraction( -s,r)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="None of the above.",
                    placeholders=[]
                ).convert_to_latex()
                    
            ]
            elif type == 0:
                a = random.randint(-8, 8) or 1
                b = random.randint(-8, 8) or 1
                function = sp.Eq(sp.Function(func_name)(var),sp.Abs((a * x + b) ).expand())
                correct_answer =  LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at {} .",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -b,a)), False, False)]
                ).convert_to_latex()
                other_solutions = [LatexStringModel(
                    string_value="Is both continuous and differentiable on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is differentiable on the entire real numbers but not continuous at {} .",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -b,a)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is neither continuous nor differentiable at {} .",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -b,a)), False, False)]
                ).convert_to_latex(),
                
                                    "None of the above."]
            else:
                r = random.randint(1, 3) or 1
                function = sp.Eq(sp.Function(func_name)(var),sp.Abs((p * x + q) ** 2 + r).expand())
                correct_answer = "Is both continuous and differentiable on the entire real numbers."
                other_solutions = [LatexStringModel(
                    string_value="Is continuous on the entire real numbers but not differentiable at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -q,p)), False, False), LatexObject(sp.Eq(var, Fraction( -r,p)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is differentiable on the entire real numbers but not continuous at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -q,p)), False, False), LatexObject(sp.Eq(var, Fraction( -r,p)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Is neither continuous nor differentiable at {} and {}.",
                    placeholders=[LatexObject(sp.Eq(var, Fraction( -q,p)), False, False), LatexObject(sp.Eq(var, Fraction( -r,p)), False, False)]
                ).convert_to_latex(),
                
                                    "None of the above."]

            return function, other_solutions, correct_answer
        
        elif difficulty == 3:
            type = random.choice([1, 2, 3])
            print(type)
            if type == 1:
                function, correct_answer, other_solutions = generate_type1(var)
                
            if type == 2:
                function, correct_answer, other_solutions = generate_type2(var)
                
            if type == 3:
                function, correct_answer, other_solutions = generate_type3(var)
            function = sp.Eq(sp.Function(func_name)(var),function)
            return function, other_solutions, correct_answer
        elif difficulty == 4:
            choice = random.randint(0,1)
            if choice:
                var = sp.Symbol('x')
                function = generate_polynomial(var, degree = random.randint(2,5))
                correct_answer = LatexStringModel(
                            string_value= "Is both continuous and differentiable on {}.",
                            placeholders=[LatexObject(sp.Interval(-8, 8), False, False)]
                            ).convert_to_latex()
        
                img = generate_graph(
                    [
                        FunctionInformation(
                            sympy_function=copy.deepcopy(function.as_expr()),
                            line_color="blue",
                            point_color="blue",
                            edge_color="blue",
                            x_range=(-8, 8),
                        )],
                    )
                
                function = sp.Eq(sp.Function(func_name)(var), function)
                a = random.randint(-8,8)
                
                other_solutions =  [ 
                        LatexStringModel(
                            string_value=" Is continuous on {} but not differentiable at {}. ",
                            placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                            ).convert_to_latex(),
                        LatexStringModel(
                                string_value="Is differentiable on {} but not continuous at {}. ",
                                placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                            ).convert_to_latex(),
                        LatexStringModel(
                            string_value="Is neither continuous nor differentiable at {}. ",
                            placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                        ).convert_to_latex(),
                        "None of the above."]
            else:
                
                var = sp.Symbol('x')
                v1 = random.randint(-2,2)
                v2 = random.choice([-1,1,-2,2])
                con = random.randint(-10,10)
                number = random.randint(-7, 7)
                number2 = random.randint(8, 10)
                v3 =sp.tan(random.randint(110,130)/180*math.pi)

                # 150 120 tan
                v4 = sp.tan(random.randint(60, 80)/180*math.pi)
                # 30 60 tan
                # print(v1,v2,v3,v4)
                p = con + v1*(var- number)**2+ v3*(var- number)
        
                q = con + v2*(var- number)**2+ v4*(var- number)
                a = number
                function = p
              
                piecewise_function_details = [
                    FunctionInformation(
                        sympy_function=p.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                       
                        x_range=(-5 + a, a),
                    ),
                    FunctionInformation(
                        sympy_function=q.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        equal_points=[(a, p.subs(var, a))],
                        x_range=(a, a + 5),
                    ),
                ]
                correct_answer = LatexStringModel(
                            string_value=" Is continuous on {} but not differentiable at {}. ",
                            placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                            ).convert_to_latex()
        
                img = generate_graph(
                    piecewise_function_details
                    )
                
                function = sp.Eq(sp.Function(func_name)(var), function)
            
                
                other_solutions =  [ 
                        LatexStringModel(
                            string_value= "Is both continuous but not differentiable at {}.",
                            placeholders=[LatexObject(a, False, False)]
                            ).convert_to_latex(),
                        LatexStringModel(
                                string_value="Is differentiable on {} but not continuous at {}. ",
                                placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                            ).convert_to_latex(),
                        LatexStringModel(
                            string_value="Is neither continuous nor differentiable at {}. ",
                            placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                        ).convert_to_latex(),
                        "None of the above."]
            
            return function, other_solutions, correct_answer, img
        elif difficulty == 5:
            x = var
            p_expr, q_expr , a_val = generate_random_case_polynomials_5(x)      
            dp_expr = sp.diff(p_expr, x)
            dq_expr = sp.diff(q_expr, x)
            p_at_a = p_expr.subs(x, a_val)
            q_at_a = q_expr.subs(x, a_val)
            dp_at_a = dp_expr.subs(x, a_val)
            dq_at_a = dq_expr.subs(x, a_val)
            a= a_val
            function = sp.Piecewise(
                    (p_expr, x <= a_val),
                    (q_expr, x > a_val), Evaluate=False
                )
            if  p_at_a == q_at_a and dp_at_a == dq_at_a:
                correct_answer =LatexStringModel(
                        string_value= "Is both continuous and differentiable on {}.",
                        placeholders=[LatexObject(sp.Interval(-8, 8), False, False)]
                        ).convert_to_latex()
                other_solutions =[ 
                    LatexStringModel(
                        string_value=" Is continuous on {} but not differentiable at {}. ",
                        placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                        ).convert_to_latex(),
                    LatexStringModel(
                            string_value="Is differentiable on {} but not continuous at {}. ",
                            placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                        ).convert_to_latex(),
                    LatexStringModel(
                        string_value="Is neither continuous nor differentiable at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                    ).convert_to_latex(),
                    "None of the above."]
            elif p_at_a == q_at_a and dp_at_a != dq_at_a:
                correct_answer = LatexStringModel(
                                    string_value=" Is continuous on {} but not differentiable at {}. ",
                                    placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                                ).convert_to_latex()
                other_solutions =[
                    LatexStringModel(
                        string_value= "Is both continuous and differentiable on {}.",
                        placeholders=[LatexObject(sp.Interval(-8, 8), False, False)]
                        ).convert_to_latex(),
                                    
                    LatexStringModel(
                        string_value="Is differentiable on {} but not continuous at {}. ",
                        placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="Is neither continuous nor differentiable at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                    ).convert_to_latex(),
                     "None of the above."]   

            elif  p_at_a != q_at_a:
                correct_answer = LatexStringModel(
                                    string_value="Is neither continuous nor differentiable at {}. ",
                                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                                ).convert_to_latex()
                other_solutions =[
                    LatexStringModel(
                        string_value= "Is both continuous and differentiable on {}.",
                        placeholders=[LatexObject(sp.Interval(-8, 8), False, False)]
                        ).convert_to_latex(),
                    LatexStringModel(
                        string_value=" Is continuous on {} but not differentiable at {}. ",
                        placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="Is differentiable on {} but not continuous at {}. ",
                        placeholders=[LatexObject(sp.Interval(-8, 8), False, False),LatexObject(sp.Eq(var, a), False, False)]
                    ).convert_to_latex(),
                    "None of the above."]
            print()
            return sp.Eq(sp.Function(func_name)(var),function), other_solutions, correct_answer
    output = []
    for _ in range(questions_count):
        if difficulty !=4:
            function, other_solution, correct_answer = generate_question_and_answers(difficulty)
            output.append({
                    'question': LatexStringModel(
                        string_value="What is true about the following function? {} ",
                        placeholders=[LatexObject(function, False, True)]
                    ).convert_to_latex(),
                    'solution': correct_answer,
                    'other_solutions': other_solution
                }
                )
            questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'],other_solutions=x['other_solutions']), output))
        else:
            function, other_solution, correct_answer,img = generate_question_and_answers(difficulty)
            output.append({
                    'question': LatexStringModel(
                        string_value="What is true about the following function? ",
                        placeholders=[]
                    ).convert_to_latex(),
                    'solution': correct_answer,
                    'other_solutions': other_solution,
                    "graph_img":img
                }
                )
            questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'],other_solutions=x['other_solutions'], graph_img=x['graph_img']), output))

        

    return questions_and_answers

