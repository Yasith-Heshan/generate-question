import random
import sympy as sp
import random
from fractions import Fraction
from typing import Any, Dict, List

import sympy as sp
from fractions import Fraction
from app.models.dataModels import LatexStringModel, LatexObject, ServiceResponce
from app.utils.helpers import  generate_general_constant_number, random_non_zero_real
from app.services.mcqRuleService import generateCustomeAnswerList, Rule


def generate_22_E_2__3_21_questions(difficulty: int, questions_count: int):

        def generate_limit_question(difficulty: int) -> Dict[str, Any]:
            other_solutions = None
            a = random_non_zero_real([4, 1, 1, 0])
            b = random_non_zero_real([4, 1, 1, 0])

            symbol = random.choice(['x', 'y', 't', 'u', 'v', 'z', 'r', 's'])
            x = sp.symbols(symbol)
            question_expr = None

            if difficulty == 1:
                # Randomly select the form of the limit question
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin(ax) / (bx))

                    expr = sp.sin(a * x) / (b * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:
                    # Form: lim x -> 0 (bx / sin(ax))
                    expr = (b * x) / sp.sin(a * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 2:
                # Randomly select the form of the limit question
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                c = random.randint(1, 4)
                if c ==4:
                    c = 3
                    d = 4
                else:
                    d = random.choice([c, c, random.randint(c,4), random.randint(c,4), random.randint(c,4)])
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin^2(ax) / (bx^2))
                    expr = (sp.sin(a * x) ** d) / (b * x ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:
                    # Form: lim x -> 0 (bx^2 / sin^2(ax))
                    expr = (b * x ** d) / (sp.sin(a * x) ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 3:
                a = random.randint(1, 10)
                b = random.randint(11, 20)
                # Randomly select the form of the limit question
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin(ax) / sin(bx))
                    expr = sp.sin(a * x) / sp.sin(b * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:

                    expr = sp.sin(b * x) / sp.sin(a * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 4:

                choice = random.choice([1, 2,3,4])
                if choice == 1:
                    # Form: lim x -> 0 (1 - cos(ax) / bx^2)
                    c = random.choice([1,2,2,2,2])
                    expr = (1 - sp.cos(a * x)) / (b * x ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                elif choice==2:

                    c = random.choice([3,4,2,2,2,2])
                    expr = (b * x ** c)/ (1 - sp.cos(a * x))
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                elif choice ==3:
                    c = random.choice([1,2,2,2,2])
                    expr = (1 - sp.cos(a * x)) / (sp.sin(b * x) ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:
                    c = random.choice([3,4,2,2,2,2])
                    if b**c>=200:
                        c = 2
                        b= random.choice([3,4,5,6,7,8])
                    expr = sp.sin(b * x) ** c/ (1 - sp.cos(a * x))
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 5:
                p = random.randint(1, 9)
                q = random.choice([i for i in range(-9, 10) if i != 0])
                a = b = 1
                transformed_x = p * x + q
                limit_value = sp.Rational(-q, p)
                sub_difficulty = random.choice([1, 2, 4])
                if sub_difficulty == 1:
                    if random.choice([True, False]):
                        expr = sp.sin(a * transformed_x) / (b * transformed_x)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    else:
                        expr = (b * transformed_x) / sp.sin(a * transformed_x)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                elif sub_difficulty == 2:
                    c = random.randint(1, 4)
                    if c == 4:
                        c = 3
                        d = 4
                    else:
                        d = random.choice([c, c, random.randint(c, 4), random.randint(c, 4), random.randint(c, 4)])
                    if random.choice([True, False]):
                        expr = (sp.sin(a * transformed_x) ** d) / (b * transformed_x ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    else:
                        expr = (b * transformed_x ** d) / (sp.sin(a * transformed_x) ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                elif sub_difficulty == 4:
                    choice = random.choice([1, 2, 3, 4])
                    if choice == 1:
                        c = random.choice([1, 2, 2, 2, 2])
                        expr = (1 - sp.cos(a * transformed_x)) / (b * transformed_x ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    elif choice == 2:
                        c = random.choice([3, 4, 2, 2, 2, 2])
                        expr = (b * transformed_x ** c) / (1 - sp.cos(a * transformed_x))
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    elif choice == 3:
                        c = random.choice([1, 2, 2, 2, 2])
                        expr = (1 - sp.cos(a * transformed_x)) / (sp.sin(b * transformed_x) ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    else:
                        c = random.choice([3, 4, 2, 2, 2, 2])
                        if b ** c >= 200:
                            c = 2
                            b = random.choice([3, 4, 5, 6, 7, 8])
                        expr = sp.sin(b * transformed_x) ** c / (1 - sp.cos(a * transformed_x))
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                other_solutions = [0, 1, 2, sp.Rational(1, 2), random.randint(3, 9)]
                other_solutions.remove(limit)
            elif difficulty == 6:
                c = random.randint(-20, 20)
                if random.choice([True, False]):
                    d = random.randint(-20, 20)
                    # Form: lim x -> -d/c (sin(ax + b) / (cx + d))
                    expr = sp.sin(a * x + b) / (c * x + d)
                    limit = sp.limit(expr, x, -d / c, dir="+-")
                    question_expr = sp.Limit(expr, x, -d / c, dir="+-")
                else:
                    d = random.randint(-20, 20)
                    # Form: lim x -> d/c (sin^2(ax - b) / (1 - cos(cx - d)))
                    expr = sp.sin(a * x - b) ** 2 / (1 - sp.cos(c * x - d))
                    limit = sp.limit(expr, x, d / c, dir="+-")
                    question_expr = sp.Limit(expr, x, d / c, dir="+-")

            return expr, limit, question_expr, sp.latex(limit), other_solutions

        output = []
        for _ in range(questions_count):
            if difficulty != 5:
                q, a, question_exp, b, other_Solution = generate_limit_question(difficulty)

                output.append({

                    'question': LatexStringModel(
                        string_value="Evaluate the following limit (without using any derivatives). {} ",
                        placeholders=[LatexObject(question_exp, False, True)]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(a)]
                    ).convert_to_latex()
                }
                )

                questions_and_answers = list(
                    map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']), output))
            else:
                q, a, question_exp, b, other_Solution = generate_limit_question(difficulty)

                output.append({

                    'question': LatexStringModel(
                        string_value="Evaluate the following limit (without using any derivatives). {} ",
                        placeholders=[LatexObject(question_exp, False, True)]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(a)]
                    ).convert_to_latex(),
                    'other_solutions': [LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(a)]
                    ).convert_to_latex() for a in other_Solution]
                }
                )
                
                questions_and_answers = list(
                    map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'],
                                                  other_solutions=x['other_solutions']), output))

        return questions_and_answers
