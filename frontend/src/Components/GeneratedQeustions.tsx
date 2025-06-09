import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { MathJaxContext, MathJax } from "better-react-mathjax";

interface GeneratedQuestionsProps {
  questions: string[];
  correctAnswers: string[];
  mcqAnswers?: string[];
  onAddToDB?: () => void;
}

const GeneratedQuestions = ({
  questions,
  correctAnswers,
  mcqAnswers,
  onAddToDB,
}: GeneratedQuestionsProps) => {
  if (!questions || questions.length === 0) return null;

  const config = {
    loader: { load: ["input/tex", "output/chtml"] },
  };

  return (
    <Box sx={{ marginTop: 4 }}>
      <h2>Generated Questions</h2>
      {questions.map((question, index) => (
        <>
          <Box key={index} sx={{ marginBottom: 2 }}>
            <MathJaxContext config={config}>
              <h3>
                {" "}
                <MathJax inline>
                  {" "}
                  {`Question ${index + 1}: ${questions[index]}`}
                </MathJax>
              </h3>
              <h4>
                <MathJax inline>{`Correct Answer: ${
                  correctAnswers[index] ?? ""
                }`}</MathJax>
              </h4>
              {mcqAnswers && mcqAnswers[index] && (
                <h4>
                  <MathJax
                    inline
                  >{`MCQ Answers: ${mcqAnswers[index]}`}</MathJax>
                </h4>
              )}
            </MathJaxContext>
          </Box>
          <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
            <Button variant="outlined" onClick={onAddToDB}>
              Add to DB
            </Button>
          </Box>
        </>
      ))}
    </Box>
  );
};

export default GeneratedQuestions;
