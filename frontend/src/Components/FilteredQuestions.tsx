import Box from "@mui/material/Box";
import { MathJaxContext, MathJax } from "better-react-mathjax";
import type { QuestionFilterResponseItem } from "../utils/interface";

interface GeneratedQuestionsProps {
  filteredQuestionResponseItems: QuestionFilterResponseItem[]
}

const FilteredQuestions = ({
  filteredQuestionResponseItems,
}: GeneratedQuestionsProps) => {
  if (!filteredQuestionResponseItems || filteredQuestionResponseItems.length === 0) return null;

  const config = {
    loader: { load: ["input/tex", "output/chtml"] },
  };

  return (
    <Box sx={{ marginTop: 4 }}>
      <h2>Filtered Questions</h2>
      {filteredQuestionResponseItems.map((question, index) => (
        <Box
          key={index}
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
                  {`Section: ${filteredQuestionResponseItems[index].section}`}
                </MathJax>
              </h3>
              <h3>
                {" "}
                <MathJax inline>
                  {" "}
                  {`Question Type: ${filteredQuestionResponseItems[index].questionType}`}
                </MathJax>
              </h3>
              <h3>
                {" "}
                <MathJax inline>
                  {" "}
                  {`Question ${index + 1}: ${filteredQuestionResponseItems[index].question}`}
                </MathJax>
              </h3>
              <h4>
                <MathJax inline>{`Correct Answer: ${filteredQuestionResponseItems[index].correctAnswer ?? ""
                  }`}</MathJax>
              </h4>
              {filteredQuestionResponseItems[index].mcqAnswers && filteredQuestionResponseItems[index].mcqAnswers && (
                <h4>
                  <MathJax
                    inline
                  >{`MCQ Answers: ${filteredQuestionResponseItems[index].mcqAnswers}`}</MathJax>
                </h4>
              )}
            </MathJaxContext>
          </Box>
        </Box>
      ))}
    </Box>
  );
};

export default FilteredQuestions;
