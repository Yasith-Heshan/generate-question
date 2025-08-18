import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import { MathJaxContext, MathJax } from "better-react-mathjax";
import type { QuestionFilterResponseItem } from "../utils/interface";

interface FilteredQuestionsProps {
  filteredQuestionResponseItems: QuestionFilterResponseItem[];
  onEditQuestion: (question: QuestionFilterResponseItem) => void;
}

const FilteredQuestions = ({
  filteredQuestionResponseItems,
  onEditQuestion,
}: FilteredQuestionsProps) => {
  if (!filteredQuestionResponseItems || filteredQuestionResponseItems.length === 0) return null;

  const config = {
    loader: { load: ["input/tex", "output/chtml"] },
  };

  return (
    <Box sx={{ marginTop: 4 }}>
      <h2>Filtered Questions</h2>
      {filteredQuestionResponseItems.map((_, index) => (
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
              {filteredQuestionResponseItems[index].id && (
                <h3>
                  <MathJax inline>
                    {`ID: ${filteredQuestionResponseItems[index].id}`}
                  </MathJax>
                </h3>
              )}
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
                  {`Keywords: ${filteredQuestionResponseItems[index].keywords?.join(", ") ?? "None"}`}
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
                <MathJax inline>{`Detailed Answer: ${filteredQuestionResponseItems[index].detailedAnswer ?? "Not provided"
                  }`}</MathJax>
              </h4>
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

            {/* Edit Button */}
            <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="outlined"
                startIcon={<EditIcon />}
                onClick={() => onEditQuestion(filteredQuestionResponseItems[index])}
                size="small"
              >
                Edit Question
              </Button>
            </Box>
          </Box>
        </Box>
      ))}
    </Box>
  );
};

export default FilteredQuestions;
