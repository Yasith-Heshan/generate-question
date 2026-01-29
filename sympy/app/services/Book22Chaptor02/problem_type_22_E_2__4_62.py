import base64
import math
import os
import random
import time

import sympy as sp

from app.models.dataModels import LatexStringModel, LatexObject

from app.services.graphService import FunctionInformation, generate_graph

from pylatex import Document, Section, NoEscape, Figure

from io import BytesIO
from PIL import Image


def save_base64_image1(base64_string, filename):
    """Convert Base64 string to an image file."""
    try:
        if not base64_string or len(base64_string) < 10:
            print(f"Skipping invalid Base64 string for {filename}")
            return None

        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        image.save(filename)
        return filename if os.path.exists(filename) else None
    except Exception as e:
        print(f"Error saving image {filename}: {e}")
        return None


def create_pdf(output, filename="./generated_img/generated_questions.pdf"):
    """Generate a PDF using LaTeX with properly formatted equations and images."""
    doc = Document()
    temp_images = []

    for idx, item in enumerate(output):
        question_latex = item["question"]
        correct_answer = item["solution"]

        other_solutions = item["other_solutions"]
        base64_img = item["graph_img"]

        img_path = os.path.abspath(f"temp_image_{idx}.png")
        time.sleep(1)
        saved_img = save_base64_image1(base64_img, img_path)

        with doc.create(Section(f"Question {idx+1}")):
            doc.append(NoEscape(f"\\textbf{{Question:}} {question_latex}"))
            doc.append(NoEscape("\\\\"))  # Newline in LaTeX
            doc.append(NoEscape(f"\\textbf{{correct answer:}} {correct_answer}"))
            doc.append(NoEscape("\\\\"))
            for b, a in enumerate(other_solutions):
                doc.append(NoEscape(f"\\textbf{b+1} {a}"))
                doc.append(NoEscape("\\\\"))  # Newline in LaTeX

            if saved_img:
                with doc.create(Figure(position="h!")) as fig:
                    fig.add_image(saved_img, width="8cm")
                temp_images.append(saved_img)
            else:
                print(f"missing {img_path}")

            doc.append(NoEscape("\\newpage"))

    doc.generate_pdf(filename.replace(".pdf", ""), clean_tex=True)

    # Cleanup images
    for img_path in temp_images:
        if os.path.exists(img_path):
            os.remove(img_path)

    print(f"PDF saved as {filename}")


def save_base64_image(base64_string, filename, output_folder="generated_img"):
    os.makedirs(output_folder, exist_ok=True)
    image_data = base64.b64decode(base64_string)
    output_path = os.path.join(output_folder, filename)
    with open(output_path, "wb") as image_file:
        image_file.write(image_data)
    return output_path


def refactor_functions2(p, q, a):
    q_list1 = []
    for i in range(a, a + 5):
        q_list1.append(q.eval(x=i))

    p_list1 = []
    for i in range(a - 5, a + 1):
        p_list1.append(p.eval(x=i))
    min_both = min(min(q_list1), min(p_list1))
    max_both = max(max(q_list1), max(p_list1))
    
    # step 2
    con = 10 / (max_both - min_both)
    con_2 = (max_both + min_both) / 2
    p = (p - con_2) * con + con_2
    q = (q - con_2) * con + con_2
 
    p_at_a = p.eval(x=a)
    q_at_a = q.eval(x=a)
    floor_value_in_q = math.floor(q_at_a)
    floor_value_in_p = math.floor(p_at_a)

    q = q + floor_value_in_q - q_at_a
    p = p + floor_value_in_p - p_at_a

    return p, p, a


def refactor_functions(p, q, a):
    q_list1 = []
    for i in range(a, a + 5):
        q_list1.append(q.eval(x=i))

    p_list1 = []
    for i in range(a - 5, a + 1):
        p_list1.append(p.eval(x=i))
  
    min_both = min(min(q_list1), min(p_list1))
    max_both = max(max(q_list1), max(p_list1))
  
    # step 2
    con = 10 / (max_both - min_both)
    con_2 = (max_both + min_both) / 2
    p = (p - con_2) * con + con_2
    q = (q - con_2) * con + con_2
 
    p_at_a = p.eval(x=a)
    q_at_a = q.eval(x=a)

    if q_at_a < p_at_a:
        floor_value_in_q = math.floor(q_at_a)
        ceil_in_p = math.ceil(p_at_a)
        q = q + floor_value_in_q - q_at_a
        p = p + ceil_in_p - p_at_a
        new_p_at_a = p.eval(x=a)
        new_q_at_a = q.eval(x=a)
        if new_p_at_a - new_q_at_a < 3:
            q = q - 1
            p = p + 1

    else:
        floor_value_in_p = math.floor(p_at_a)
        ceil_in_q = math.ceil(q_at_a)
        p = p + floor_value_in_p - p_at_a
        q = q + ceil_in_q - q_at_a
        new_p_at_a = p.eval(x=a)
        new_q_at_a = q.eval(x=a)
        if new_q_at_a - new_p_at_a < 3:
            q = q + 1
            p = p - 1

    return p, q, a


def generate_problem_22_E_2__4_62_questions(difficulty: int, questions_count: int):
    def random_polynomial(degree):
        x = sp.symbols("x")

        return sp.Poly(
            [random.randint(-5, 5) if degree < 2 else 1 for _ in range(degree + 1)], x
        )

    def generate_question_and_answers(difficulty):
        x = sp.symbols("x")
        expression = sp.Function("f")(sp.symbols("x"))

        if difficulty == 1:
            x = sp.symbols("x")

            a = random.randint(1, 3)
            p_degree = random.randint(0, 3)
            q_degree = random.randint(0, 2)

            p = random_polynomial(p_degree)
            q = p + random.randint(1, 5)
            q_type = random.choice([True, False])
            if q_type:
                p, q, a = refactor_functions(p, q, a)
            else:
                q = p
                p, q, a = refactor_functions2(p, q, a)

            f = sp.Piecewise((p.as_expr(), x < a), (q.as_expr(), x >= a))
            a1, b1, c1, d1 = (
                p.eval(x=a)-4,
                p.eval(x=a) - 1,
                p.eval(x=a) + 4,
                p.eval(x=a) + 2,
            )
            if p.eval(x=a) == q.eval(x=a):
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
                        x_range=(a, a + 5),
                    ),
                ]

                one_side = LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), q.eval(x=a)),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex()
                other_solutions = [
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), a),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), a1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                # sp.Eq(sp.Limit(p.as_expr(), x, a, dir="-"), p.eval(x=b1)),
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), a1),
                                False,
                                False,
                            ),
                            LatexObject(
                                # sp.Eq(sp.Limit(q.as_expr(), x, a, dir="+"), p.eval(x=a)),
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), a),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), b1),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), c1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                ]

            else:
                piecewise_function_details = [
                    FunctionInformation(
                        sympy_function=p.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        inEqual_points=[(a, p.eval(x=a))],
                        x_range=(-5 + a, a),
                    ),
                    FunctionInformation(
                        sympy_function=q.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        equal_points=[(a, q.eval(x=a))],
                        x_range=(a, a + 5),
                    ),
                ]
                one_side = LatexStringModel(
                    string_value="Does not exist.",
                    placeholders=[],
                ).convert_to_latex()
                other_solutions = [
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), a),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), a1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                # sp.Eq(sp.Limit(p.as_expr(), x, a, dir="-"), p.eval(x=b1)),
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), a1),
                                False,
                                False,
                            ),
                            LatexObject(
                                # sp.Eq(sp.Limit(q.as_expr(), x, a, dir="+"), p.eval(x=a)),
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), a),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), q.eval(x=a)),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), p.eval(x=a)),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                ]


            # Generate graph for the piecewise function
            generated_img = generate_graph(piecewise_function_details)

            graph = f

            
            correct_answer = LatexStringModel(
                string_value="  {}, {}. ",
                placeholders=[
                    LatexObject(
                        sp.Eq(sp.Limit(expression, x, a, dir="-"), p.eval(x=a)),
                        False,
                        False,
                    ),
                    LatexObject(
                        sp.Eq(sp.Limit(expression, x, a, dir="+"), q.eval(x=a)),
                        False,
                        False,
                    ),
                ],
            ).convert_to_latex()
            
            one_side_other_solutions = [
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), a1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), b1),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), -a1),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), q.eval(x=a)),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Does not exist.",
                    placeholders=[],
                ).convert_to_latex()
            ]
            one_side_other_solutions.remove(one_side)
        
            return (
                graph,
                other_solutions,
                correct_answer,
                one_side,
                one_side_other_solutions,
                generated_img,
                a,
            )
        

        elif difficulty == 2:

            a = random.randint(1, 5)
            p_degree = random.randint(0, 2)
            q_degree = random.randint(0, 2)
            q_type = random.choice([True, False,False])
            p = random_polynomial(p_degree)
            if q_type:
            
                q = p + random.randint(1, 5)
           
                p, q, a = refactor_functions(p, q, a)
          
                constant_value = random.choice(
                    [
                        min(p.eval(x=a), q.eval(x=a)) - 1,
                        max(p.eval(x=a), q.eval(x=a)) + 1,
                        random.randint(
                            min(p.eval(x=a), q.eval(x=a)) + 1,
                            max(p.eval(x=a), q.eval(x=a)) - 1,
                        ),
                    ]
                )

            else:

                q = p
                p, q, a = refactor_functions2(p, q, a)
                constant_value = p.eval(x=a) + random.choice(
                    [random.randint(-2, -1), random.randint(1, 2)]
                )

            f = sp.Piecewise((p.as_expr(), x < a), (q.as_expr(), x >= a))

            if p.eval(x=a) == q.eval(x=a):
                
                piecewise_function_details = [
                    FunctionInformation(
                        sympy_function=p.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        x_range=(-5 + a, a),
                        inEqual_points=[(a, p.eval(x=a))],
                    ),
                    FunctionInformation(
                        sympy_function=q.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        equal_points=[(a, constant_value)],
                        x_range=(a, a + 5),
                    ),
                ]

                one_side = LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), p.eval(x=a))
                        )
                    ],
                ).convert_to_latex()
            else:
                piecewise_function_details = [
                    FunctionInformation(
                        sympy_function=p.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        inEqual_points=[(a, p.eval(x=a))],
                        x_range=(-5 + a, a),
                    ),
                    FunctionInformation(
                        sympy_function=q.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        inEqual_points=[(a, q.eval(x=a))],
                        equal_points=[(a, constant_value)],
                        x_range=(a, a + 5),
                    ),
                ]
                one_side = LatexStringModel(
                    string_value="Does not exist. ",
                    placeholders=[],
                ).convert_to_latex()

            # Generate graph for the piecewise function
            generated_img = generate_graph(piecewise_function_details)

         

            f = sp.Piecewise(
                (p.as_expr(), x < a), (q.as_expr(), x > a), (constant_value, x == a)
            )
            graph = f

            a1, b1 = p.eval(x=a), q.eval(x=a)
       
            correct_answer = LatexStringModel(
                string_value="  {}, {}. ",
                placeholders=[
                    LatexObject(
                        sp.Eq(sp.Limit(expression, x, a, dir="-"), p.eval(x=a)),
                        False,
                        False,
                    ),
                    LatexObject(
                        sp.Eq(sp.Limit(expression, x, a, dir="+"), q.eval(x=a)),
                        False,
                        False,
                    ),
                ],
            ).convert_to_latex()
            if a1 ==b1:
                other_solutions = [
                    
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), a1+7),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), b1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), constant_value),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), b1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), a1),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), constant_value),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                ]
            else:
                other_solutions = [
                    
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), a1+1),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), b1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), constant_value),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), b1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="  {}, {}. ",
                        placeholders=[
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="-"), b1),
                                False,
                                False,
                            ),
                            LatexObject(
                                sp.Eq(sp.Limit(expression, x, a, dir="+"), a1),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                ]
           

            one_side_other_solutions = [
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), p.eval(x=a))
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), a1 - 4),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), constant_value),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), b1 + 3),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Does not exist. ",
                    placeholders=[],
                ).convert_to_latex()
            ]
            one_side_other_solutions.remove(one_side)
            return (
                graph,
                other_solutions,
                correct_answer,
                one_side,
                one_side_other_solutions,
                generated_img,
                a,
            )

        elif difficulty == 3:
            a = random.randint(1, 5)

            # Random degree for polynomial p(x) (0, 1, or 2)
            p_degree = random.randint(0, 2)

            # Generate polynomial p(x)
            p = random_polynomial(p_degree)

            # Randomly choose d to be 1 or 2 for the rational function (1 / (x - a)^d)
            d = 2

            # Define the rational function 1 / (x - a)^d
            q = 1 / (sp.symbols("x") - a) ** d
            f = sp.Piecewise((p.as_expr(), x < a), (q.as_expr(), x >= a))

            piecewise_function_details = [
                FunctionInformation(
                    sympy_function=p.as_expr(),
                    line_color="blue",
                    point_color="blue",
                    edge_color="blue",
                    inEqual_points=[(a, p.eval(x=a))],
                    x_range=(-5 + a, a),
                ),
                FunctionInformation(
                    sympy_function=q.as_expr(),
                    line_color="blue",
                    point_color="blue",
                    edge_color="blue",
                    x_range=(a, a + 5),
                    is_infinity=True,
                    y_limit=max(20, p.eval(x=a) + 5),
                ),
            ]

            # Generate graph for the piecewise function
            generated_img = generate_graph(
                piecewise_function_details,
                is_infinity=True,
                y_limit=max(20, p.eval(x=a) + 5),
            )

            # Create the piecewise function
            f = sp.Piecewise(
                (p.as_expr(), sp.symbols("x") <= a), (q, sp.symbols("x") > a)
            )

            graph = f

            one_side = LatexStringModel(
                string_value="Does not exist.",
                placeholders=[],
            ).convert_to_latex()
            # a1, b1 = a + 1, a - 3
            a1, b1 = p.eval(x=a), sp.limit(q, x, a, dir="+")
            correct_answer = LatexStringModel(
                string_value="  {}, {}. ",
                placeholders=[
                    LatexObject(
                        # sp.Eq(sp.Limit(p.as_expr(), x, a, dir="-"), p.eval(x=a)),
                        sp.Eq(sp.Limit(expression, x, a, dir="-"), p.eval(x=a)),
                        False,
                        False,
                    ),
                    LatexObject(
                        sp.Eq(
                            sp.Limit(expression, x, a, dir="+"),
                            sp.limit(q, x, a, dir="+"),
                        ),
                        # sp.Eq(sp.Limit(q.as_expr(), x, a, dir="+"), p.eval(x=a)),
                        False,
                        False,
                    ),
                ],
            ).convert_to_latex()
            one_side_other_solutions = [
                LatexStringModel(
                    string_value="  {}.",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, "+-"), a1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}.",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, "+-"), -a1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}.",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, "+-"), b1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}.",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, "+-"), -b1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Does not exist.",
                    placeholders=[],
                ).convert_to_latex()
            ]

            other_solutions = [
                LatexStringModel(
                    string_value="  {}, {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="-"), b1),
                            False,
                            False,
                        ),
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+"), a1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}, {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="-"), a1),
                            False,
                            False,
                        ),
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+"), -b1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}, {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="-"), -b1),
                            False,
                            False,
                        ),
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+"), a1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
            ]
            one_side_other_solutions.remove(one_side)
            return (
                graph,
                other_solutions,
                correct_answer,
                one_side,
                one_side_other_solutions,
                generated_img,
                a,
            )
        elif difficulty == 4:

            a = random.randint(1, 10)
            d = random.choice([1, 2])

            q = 1 / (sp.symbols("x") - a) ** d

            f = random.choice([-1, +1]) * q
            q = f

            piecewise_function_details = [
                FunctionInformation(
                    sympy_function=f.as_expr(),
                    line_color="blue",
                    point_color="blue",
                    edge_color="blue",
                    x_range=(-5 + a, a + 5),
                )
            ]

            # Generate graph for the piecewise function
            generated_img = generate_graph(
                [
                    FunctionInformation(
                        sympy_function=f.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        x_range=(-5 + a, a),
                        is_infinity=True,
                    ),
                    FunctionInformation(
                        sympy_function=f.as_expr(),
                        line_color="blue",
                        point_color="blue",
                        edge_color="blue",
                        x_range=(a, a + 5),
                        is_infinity=True,
                    ),
                ]
            )

            graph = f
            if sp.Limit(q, x, a, dir="-").doit() == sp.Limit(q, x, a, dir="+").doit():

                one_side = LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="+-"),
                                sp.Limit(q, x, a).doit(),
                            ),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex()
            else:
                one_side = LatexStringModel(
                    string_value="Does not exist.",
                    placeholders=[],
                ).convert_to_latex()
            a1, b1 = (
                sp.Limit(q, x, a, dir="-").doit(),
                sp.Limit(q, x, a, dir="+").doit(),
            )
            one_side_other_solutions = [
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="+-"), a1),
                            False,
                            False,
                        )
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="+-"),
                                -a1,
                            ),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="+-"),
                                a,
                                # sp.Limit(q.as_expr(), x, a, dir="+-"),c1
                            ),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="+-"),
                                a + random.randint(1, 4),
                                # sp.Limit(q.as_expr(), x, a, dir="+-"), d1
                            ),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Does not exist.",
                    placeholders=[],
                ).convert_to_latex()
            ]
            
            correct_answer = LatexStringModel(
                string_value="  {}, {}. ",
                placeholders=[
                    LatexObject(
                        sp.Eq(
                            sp.Limit(expression, x, a, dir="-"),
                            sp.Limit(q, x, a, dir="-").doit(),
                        ),
                        False,
                        False,
                    ),
                    LatexObject(
                        sp.Eq(
                            sp.Limit(expression, x, a, dir="+"),
                            sp.Limit(q, x, a, dir="+").doit(),
                        ),
                        False,
                        False,
                    ),
                ],
            ).convert_to_latex()
            other_solutions = [
                LatexStringModel(
                    string_value="  {}, {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="-"), a1),
                            False,
                            False,
                        ),
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="+"),
                                -a1,
                            ),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}, {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="-"), a1),
                            False,
                            False,
                        ),
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="+"),
                                a1,
                            ),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}, {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="-"),
                                -a1,
                            ),
                            False,
                            False,
                        ),
                        LatexObject(
                            sp.Eq(
                                sp.Limit(expression, x, a, dir="+"),
                                a1,
                            ),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="  {}, {}. ",
                    placeholders=[
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="-"), -a1),
                            False,
                            False,
                        ),
                        LatexObject(
                            sp.Eq(sp.Limit(expression, x, a, dir="-"), -a1),
                            False,
                            False,
                        ),
                    ],
                ).convert_to_latex(),
            ]
            one_side_other_solutions.remove(one_side)
            other_solutions.remove(correct_answer)
            return (
                graph,
                other_solutions,
                correct_answer,
                one_side,
                one_side_other_solutions,
                generated_img,
                a,
            )

    output = []
    for _ in range(questions_count):
        os.path.exists(
            "generated_img",
        )
        if difficulty != 5:
      
            (
                function,
                other_solution,
                correct_answer,
                one_side,
                one_side_other_solutions,
                generate_img,
                a,
            ) = generate_question_and_answers(difficulty)
            output.append(
                {
                    "question": LatexStringModel(
                        string_value="Find the one-sided limits at {} of the function {} shown in the graph. ",
                        placeholders=[
                            LatexObject(sp.Eq(sp.symbols("x"), a), False, False),
                            LatexObject(
                                sp.Eq(
                                    sp.symbols("y"), sp.Function("f")(sp.symbols("x"))
                                ),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    "solution": correct_answer,
                    "other_solutions": other_solution + ["Does not exist."],
                    "graph_img": generate_img,
                }
            )
            save_base64_image(generate_img, f"{difficulty}_{_}.png")
        else:

            difficulty1 = random.choice([1, 2, 3, 4])
            (
                function,
                other_solution,
                correct_answer,
                one_side,
                one_side_other_solutions,
                generate_img,
                a,
            ) = generate_question_and_answers(difficulty1)
           
            output.append(
                {
                    "question": LatexStringModel(
                        string_value="Find the (two sided) limit at {} of the function {} shown in the graph. ",
                        placeholders=[
                            LatexObject(sp.Eq(sp.symbols("x"), a), False, False),
                            LatexObject(
                                sp.Eq(
                                    sp.symbols("y"), sp.Function("f")(sp.symbols("x"))
                                ),
                                False,
                                False,
                            ),
                        ],
                    ).convert_to_latex(),
                    "solution": one_side,
                    "other_solutions": one_side_other_solutions,
                    "graph_img": generate_img,
                }
            )
            save_base64_image(generate_img, f"5_{_}.png")

    # create_pdf(output, f"./generated_img/generated_questions_difficulty_{difficulty}")

    return output
