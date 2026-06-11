import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Chip from "@mui/material/Chip";
import { MathJaxContext, MathJax } from "better-react-mathjax";
import { useState, useRef, useEffect, useMemo } from "react";
import type { GeneratedQuestionInfo } from "../utils/interface";
import EditQuestionModal from "./EditQuestionModal";

interface GeneratedQuestionsProps {
  questions: string[];
  detailedAnswers?: string[];
  correctAnswers: string[];
  mcqAnswers?: string[];
  graphImages?: string[];
  difficulties?: number[];
  onAddToDB: (generatedQuestionInfo: GeneratedQuestionInfo) => void;
  onEditQuestion: (
    index: number,
    editedData: {
      question: string;
      correctAnswer: string;
      detailedAnswer?: string;
      mcqAnswers: string[];
      difficulty: number;
    }
  ) => void;
  onGenerateBasedOnThis?: (exampleQuestions: string) => void;
}

const GeneratedQuestions = ({
  questions,
  detailedAnswers,
  correctAnswers,
  mcqAnswers,
  graphImages,
  difficulties,
  onAddToDB,
  onEditQuestion,
  onGenerateBasedOnThis,
}: GeneratedQuestionsProps) => {
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editingQuestionIndex, setEditingQuestionIndex] = useState<number | null>(null);
  const [selectedQuestions, setSelectedQuestions] = useState<Set<number>>(new Set());
  const [newQuestionsCount, setNewQuestionsCount] = useState(0);
  const [renderVersion, setRenderVersion] = useState(0);
  const prevCountRef = useRef(0);
  const questionsContainerRef = useRef<HTMLDivElement>(null);

  // Force re-render when any data changes
  useEffect(() => {
    setRenderVersion((prev) => prev + 1);
  }, [questions, correctAnswers, detailedAnswers, mcqAnswers, difficulties]);

  // Track when new questions are generated and show them
  useEffect(() => {
    if (questions.length > prevCountRef.current) {
      // New questions were generated
      const count = questions.length - prevCountRef.current;
      setNewQuestionsCount(count);
      prevCountRef.current = questions.length;
      // Clear selections when new questions arrive to avoid index mismatches
      setSelectedQuestions(new Set());
      if (questionsContainerRef.current) {
        questionsContainerRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  }, [questions.length]);

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
    difficulty: number;
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

  const handleSelectQuestion = (index: number) => {
    setSelectedQuestions((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return new Set(newSet);
    });
  };

  const handleSelectAll = () => {
    if (selectedQuestions.size === questions.length && questions.length > 0) {
      setSelectedQuestions(new Set());
    } else {
      setSelectedQuestions(new Set(questions.map((_, i) => i)));
    }
  };

  const parseMcqAnswers = (answerString: string): string[] => {
    if (answerString.includes("\n")) {
      return answerString.split("\n").map((item) => item.trim()).filter((item) => item !== "");
    }
    return answerString.split(",").map((item) => item.trim()).filter((item) => item !== "");
  };

  return (
    <Box sx={{ marginTop: 4 }} ref={questionsContainerRef}>
      <h2>Generated Questions</h2>
      {onGenerateBasedOnThis && questions.length > 0 && (
        <Box sx={{ mb: 3, p: 2, bgcolor: "#e3f2fd", borderRadius: 1 }}>
          <Box sx={{ mb: 2 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={selectedQuestions.size === questions.length && questions.length > 0}
                  indeterminate={selectedQuestions.size > 0 && selectedQuestions.size < questions.length}
                  onChange={handleSelectAll}
                />
              }
              label={`Select All (${selectedQuestions.size}/${questions.length} selected)`}
            />
          </Box>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            disabled={selectedQuestions.size === 0}
            onClick={() => {
              const selectedIndices = Array.from(selectedQuestions).sort((a, b) => a - b);
              const exampleQuestionsText = selectedIndices
                .map((i) => `Q${i + 1}: ${questions[i]}\nAnswer: ${correctAnswers[i]}${detailedAnswers?.[i] ? `\nDetailed: ${detailedAnswers[i]}` : ""}${mcqAnswers?.[i] ? `\nOptions: ${mcqAnswers[i]}` : ""}\n`)
                .join("\n");
              onGenerateBasedOnThis(exampleQuestionsText);
              setSelectedQuestions(new Set());
            }}
          >
            Generate Based on Selected ({selectedQuestions.size}) Questions
          </Button>
        </Box>
      )}
      {questions.map((_, index) => (
        <Box
          key={`question-${renderVersion}-${index}`}
          sx={{
            bgcolor: "#f5f5f5",
            padding: 2,
            borderRadius: 1,
            boxShadow: 1,
            marginBottom: 2,
            border: index >= (questions.length - newQuestionsCount) ? "2px solid #4caf50" : "none",
            backgroundColor: index >= (questions.length - newQuestionsCount) ? "#f1f8f4" : "#f5f5f5",
          }}
        >
          <Box
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
                {index >= (questions.length - newQuestionsCount) && (
                  <Chip label="NEW" color="success" size="small" sx={{ ml: 2 }} />
                )}
              </h3>
              <Box sx={{ mb: 1 }}>
                <strong>Difficulty: </strong>
                {difficulties && difficulties[index] ? 
                  (difficulties[index] === 1 ? "Easy" : difficulties[index] === 2 ? "Medium" : "Hard") + 
                  ` (${difficulties[index]})` : 
                  "Not specified"}
              </Box>
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
          <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mt: 2 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={selectedQuestions.has(index)}
                  onChange={() => handleSelectQuestion(index)}
                />
              }
              label="Use as example"
            />
            <Box sx={{ display: "flex", gap: 1 }}>
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
                    difficulty: difficulties?.[index] || 1,
                    graphImg: graphImages?.[index] || undefined,
                    index: index,
                  });
                }}
              >
                Add to DB
              </Button>
            </Box>
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
            difficulty: difficulties?.[editingQuestionIndex] || 1,
          }}
        />
      )}
    </Box>
  );
};

export default GeneratedQuestions;
