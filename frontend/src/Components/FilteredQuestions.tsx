import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Pagination from "@mui/material/Pagination";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { MathJaxContext, MathJax } from "better-react-mathjax";
import type { QuestionFilterResponseItem } from "../utils/interface";
import { useState } from "react";

interface FilteredQuestionsProps {
  filteredQuestionResponseItems: QuestionFilterResponseItem[];
  onEditQuestion: (question: QuestionFilterResponseItem) => void;
  onDeleteQuestion: (question: QuestionFilterResponseItem) => void;
}

const FilteredQuestions = ({
  filteredQuestionResponseItems,
  onEditQuestion,
  onDeleteQuestion,
}: FilteredQuestionsProps) => {
  const QUESTIONS_PER_PAGE = 5;
  const [currentPage, setCurrentPage] = useState(1);

  if (!filteredQuestionResponseItems || filteredQuestionResponseItems.length === 0) return null;

  const totalPages = Math.ceil(filteredQuestionResponseItems.length / QUESTIONS_PER_PAGE);
  const startIndex = (currentPage - 1) * QUESTIONS_PER_PAGE;
  const endIndex = startIndex + QUESTIONS_PER_PAGE;
  const displayedQuestions = filteredQuestionResponseItems.slice(startIndex, endIndex);

  const config = {
    loader: { load: ["input/tex", "output/chtml"] },
  };

  const handlePageChange = (_event: React.ChangeEvent<unknown>, page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <Box sx={{ marginTop: 4 }}>
      <h2>Filtered Questions</h2>
      <Box sx={{ mb: 2, fontSize: "0.9rem", color: "#666" }}>
        Showing questions {startIndex + 1}-{Math.min(endIndex, filteredQuestionResponseItems.length)} of {filteredQuestionResponseItems.length}
      </Box>
      {displayedQuestions.map((question, relativeIndex) => {
        const absoluteIndex = startIndex + relativeIndex;
        return (
          <Box
            key={absoluteIndex}
            sx={{
              bgcolor: "#f5f5f5",
              padding: 2,
              borderRadius: 1,
              boxShadow: 1,
              marginBottom: 2,
            }}
          >
            <Box
              key={absoluteIndex}
              sx={{
                marginBottom: 2,
              }}
            >
              <MathJaxContext config={config}>
                {question.id && (
                  <h3>
                    <MathJax inline>
                      {`ID: ${question.id}`}
                    </MathJax>
                  </h3>
                )}
                <h3>
                  {" "}
                  <MathJax inline>
                    {" "}
                    {`Section: ${question.section}`}
                  </MathJax>
                </h3>
                <h3>
                  {" "}
                  <MathJax inline>
                    {" "}
                    {`Question Type: ${question.questionType}`}
                  </MathJax>
                </h3>
                <h3>
                  {" "}
                  <MathJax inline>
                    {" "}
                    {`Difficulty: ${question.difficulty}`}
                  </MathJax>
                </h3>
                <h3>
                  {" "}
                  <MathJax inline>
                    {" "}
                    {`Keywords: ${question.keywords?.join(", ") ?? "None"}`}
                  </MathJax>
                </h3>
                <h3>
                  {" "}
                  <MathJax inline>
                    {" "}
                    {`Question ${absoluteIndex + 1}: ${question.question}`}
                  </MathJax>
                </h3>
                {question.graphImg && (
                  <Box sx={{ marginY: 2 }}>
                    <img
                      src={`data:image/png;base64,${question.graphImg}`}
                      alt={`Graph for question ${absoluteIndex + 1}`}
                      style={{
                        maxWidth: "100%",
                        height: "auto",
                        borderRadius: "8px",
                        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
                      }}
                    />
                  </Box>
                )}
                <h4>
                  <MathJax inline>{`Detailed Answer: ${question.detailedAnswer ?? "Not provided"
                    }`}</MathJax>
                </h4>
                <h4>
                  <MathJax inline>{`Correct Answer: ${question.correctAnswer ?? ""
                    }`}</MathJax>
                </h4>
                {question.mcqAnswers && question.mcqAnswers && (
                  <h4>
                    <MathJax
                      inline
                    >{`MCQ Answers: ${question.mcqAnswers}`}</MathJax>
                  </h4>
                )}
              </MathJaxContext>

              {/* Edit Button */}
              <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                <Button
                  variant="outlined"
                  startIcon={<EditIcon />}
                  onClick={() => onEditQuestion(question)}
                  size="small"
                >
                  Edit Question
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<DeleteIcon />}
                  onClick={() => onDeleteQuestion(question)}
                  size="small"
                >
                  Delete Question
                </Button>
              </Box>
            </Box>
          </Box>
        );
      })}
      
      {/* Pagination Controls */}
      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 4, marginBottom: 4 }}>
          <Pagination
            count={totalPages}
            page={currentPage}
            onChange={handlePageChange}
            color="primary"
            size="large"
          />
        </Box>
      )}
    </Box>
  );
};

export default FilteredQuestions;
