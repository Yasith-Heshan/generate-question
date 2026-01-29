import base64
import math
import os
from pylatex import Document, Section, NoEscape, Figure

from io import BytesIO
from PIL import Image
import time

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
    doc.packages.append(NoEscape(r'\usepackage{amsmath}'))
    temp_images = []

    for idx, item in enumerate(output):
        question_latex = item.question
        correct_answer = item.correct_solution

        other_solutions = item.other_solutions
        base64_img = item.graph_img
        saved_img = None
        if base64_img:
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
           

            doc.append(NoEscape("\\newpage"))

    doc.generate_pdf(filename.replace(".pdf", ""), clean_tex=True)

    # Cleanup images
    for img_path in temp_images:
        if os.path.exists(img_path):
            os.remove(img_path)

    print(f"PDF saved as {filename}")
