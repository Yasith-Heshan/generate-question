import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { MathJaxContext, MathJax } from "better-react-mathjax";
import type { GeneratedQuestionInfo } from "../utils/interface";

interface GeneratedQuestionsProps {
  questions: string[];
  detailedAnswers?: string[];
  correctAnswers: string[];
  mcqAnswers?: string[];
  onAddToDB: (generatedQuestionInfo: GeneratedQuestionInfo) => void;
}

const GeneratedQuestions = ({
  questions,
  detailedAnswers,
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
        <Box
          sx={{
            bgcolor: "#f5f5f5",
            padding: 2,
            borderRadius: 1,
            boxShadow: 1,
            marginBottom: 2,
          }}
        >
          <Box
            key={index}
            sx={{
              marginBottom: 2,
            }}
          >
            <MathJaxContext config={config}>
              <h3>
                {" "}
                <MathJax inline>
                  {" "}
                  {`Question ${index + 1}: ${questions[index]}`}
                </MathJax>
              </h3>
              <h5>
                {"Detailed Answer: \n"}
                {detailedAnswers && detailedAnswers[index]
                  ? <MathJax inline>{detailedAnswers[index]}</MathJax>
                  : "Not provided"}
              </h5>
              <h4>
                <MathJax inline>{`Correct Answer: ${correctAnswers[index] ?? ""
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
            <Button
              variant="outlined"
              onClick={() => {
                onAddToDB({
                  question: questions[index],
                  correctAnswer: correctAnswers[index],
                  mcqAnswers: mcqAnswers
                    ? mcqAnswers[index].split(",")
                    : undefined,
                  index: index,
                });
              }}
            >
              Add to DB
            </Button>
          </Box>
        </Box>
      ))}
    </Box>
  );
};

export default GeneratedQuestions;
