import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { MathJaxContext, MathJax } from "better-react-mathjax";
import { useState } from "react";
import type { GeneratedQuestionInfo } from "../utils/interface";
import EditQuestionModal from "./EditQuestionModal";

interface GeneratedQuestionsProps {
  questions: string[];
  detailedAnswers?: string[];
  correctAnswers: string[];
  mcqAnswers?: string[];
  graphImages?: string[];
  onAddToDB: (generatedQuestionInfo: GeneratedQuestionInfo) => void;
  onEditQuestion: (
    index: number,
    editedData: {
      question: string;
      correctAnswer: string;
      detailedAnswer?: string;
      mcqAnswers: string[];
    }
  ) => void;
}

const GeneratedQuestions = ({
  questions,
  detailedAnswers,
  correctAnswers,
  mcqAnswers,
  graphImages,
  onAddToDB,
  onEditQuestion,
}: GeneratedQuestionsProps) => {
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editingQuestionIndex, setEditingQuestionIndex] = useState<number | null>(null);

  if (!questions || questions.length === 0) return null;

  const config = {
    loader: { load: ["input/tex", "output/chtml"] },
  };

  const handleEditClick = (index: number) => {
    setEditingQuestionIndex(index);
    setEditModalOpen(true);
  };

  const handleEditSave = (editedData: {
    question: string;
    correctAnswer: string;
    mcqAnswers: string[];
  }) => {
    if (editingQuestionIndex !== null) {
      onEditQuestion(editingQuestionIndex, editedData);
    }
    setEditModalOpen(false);
    setEditingQuestionIndex(null);
  };

  const handleEditClose = () => {
    setEditModalOpen(false);
    setEditingQuestionIndex(null);
  };

  const parseMcqAnswers = (answerString: string): string[] => {
    if (answerString.includes("\n")) {
      return answerString.split("\n").map((item) => item.trim()).filter((item) => item !== "");
    }
    return answerString.split(",").map((item) => item.trim()).filter((item) => item !== "");
  };

  return (
    <Box sx={{ marginTop: 4 }}>
      <h2>Generated Questions</h2>
      {questions.map((_, index) => (
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
                <Box sx={{ mt: 1 }}>
                  <strong>MCQ Answers:</strong>
                  <Box sx={{ mt: 1 }}>
                    {parseMcqAnswers(mcqAnswers[index]).map((answer, answerIndex) => (
                      <Box key={answerIndex} sx={{ mb: 0.5 }}>
                        <MathJax inline>{answer}</MathJax>
                      </Box>
                    ))}
                  </Box>
                </Box>
              )}
            </MathJaxContext>
            {graphImages && graphImages[index] && (
              <Box sx={{ mt: 2 }}>
                <img
                  src={`data:image/png;base64,${graphImages[index]}`}
                  alt={`Graph for question ${index + 1}`}
                  style={{ maxWidth: "100%" }}
                />
              </Box>
            )}
          </Box>
          <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1, mt: 2 }}>
            <Button
              variant="outlined"
              onClick={() => handleEditClick(index)}
            >
              Edit
            </Button>
            <Button
              variant="outlined"
              onClick={() => {
                onAddToDB({
                  question: questions[index],
                  correctAnswer: correctAnswers[index],
                  detailedAnswer: detailedAnswers
                    ? detailedAnswers[index]
                    : undefined,
                  mcqAnswers: mcqAnswers?.[index]
                    ? parseMcqAnswers(mcqAnswers[index])
                    : undefined,
                  graphImg: graphImages?.[index] || undefined,
                  index: index,
                });
              }}
            >
              Add to DB
            </Button>
          </Box>
        </Box>
      ))}
      {editingQuestionIndex !== null && (
        <EditQuestionModal
          open={editModalOpen}
          onClose={handleEditClose}
          onSave={handleEditSave}
          initialData={{
            question: questions[editingQuestionIndex],
            correctAnswer: correctAnswers[editingQuestionIndex],
            detailedAnswer: detailedAnswers?.[editingQuestionIndex] || "",
            mcqAnswers: mcqAnswers?.[editingQuestionIndex]
              ? parseMcqAnswers(mcqAnswers[editingQuestionIndex])
              : [],
          }}
        />
      )}
    </Box>
  );
};

export default GeneratedQuestions;
