import React from "react";
import Box from "@mui/material/Box";
import {
  TextField,
  Button,
  Stack,
  TextareaAutosize,
  CircularProgress,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import { useState } from "react";
import GeneratedQuestions from "../Components/GeneratedQeustions";
import type {
  GeneratedQuestionInfo,
  QuestionGenerationRequestBody,
  QuestionSaveRequestBody,
} from "../utils/interface";
import {
  generateQuestion,
  saveAllQuestions,
  saveQuestion,
} from "../api/openAiService";
import { toast } from "react-toastify";

export const QuestionGeneratePage = () => {
  const [form, setForm] = useState<QuestionGenerationRequestBody>({
    section: "",
    description: "",
    count: 1,
    questionType: "",
    difficulty: 1,
  });

  const [questions, setQuestions] = useState<string[]>([]);
  const [correctAnswers, setCorrectAnswers] = useState<string[]>([]);
  const [mcqAnswers, setMcqAnswers] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name as string]:
        name === "count" || name === "difficulty" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      clearState();
      setIsGenerating(true);
      const response = await generateQuestion(form);
      setQuestions(response.data.questions);
      setCorrectAnswers(response.data.correctAnswers);
      setMcqAnswers(response.data.mcqAnswers);
    } catch (error) {
      console.error("Error generating questions:", error);
      alert("Failed to generate questions. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  const removeAddedQuestion = (index: number) => {
    setQuestions((prev) => prev.filter((_, i) => i !== index));
    setCorrectAnswers((prev) => prev.filter((_, i) => i !== index));
    setMcqAnswers((prev) => prev.filter((_, i) => i !== index));
  };

  const clearState = () => {
    setQuestions([]);
    setCorrectAnswers([]);
    setMcqAnswers([]);
  };

  async function handleAddToDB(
    generatedQuestionInfo: GeneratedQuestionInfo
  ): Promise<void> {
    try {
      await saveQuestion({
        ...generatedQuestionInfo,
        section: form.section,
        questionType: form.questionType,
        difficulty: form.difficulty,
      } as QuestionSaveRequestBody);
      removeAddedQuestion(generatedQuestionInfo.index);
      toast.success("Question added to the database successfully!");
    } catch (error) {
      console.error("Error adding questions to DB:", error);
      toast.error("Failed to add question to the database. Please try again.");
    }
  }

  const handleAddAllToDB = async () => {
    const questionSaveRequestBody: QuestionSaveRequestBody[] = questions.map(
      (question, index) =>
        ({
          section: form.section,
          questionType: form.questionType,
          difficulty: form.difficulty,
          question: question,
          correctAnswer: correctAnswers[index],
          mcqAnswers: mcqAnswers[index].split(",") || [],
        } as QuestionSaveRequestBody)
    );
    try {
      await saveAllQuestions(questionSaveRequestBody);
      toast.success("All questions added to the database successfully!");
      clearState();
    } catch (error) {
      console.error("Error adding all questions to DB:", error);
      toast.error(
        "Failed to add all questions to the database. Please try again."
      );
    }
  };

  return (
    <Grid container spacing={2} justifyContent="center">
      <Grid size={4}>
        <Box
          sx={{
            borderRadius: 1,
            padding: 2,
          }}
        >
          <Stack component="form" spacing={2} onSubmit={handleSubmit}>
            <TextField
              label="Section"
              name="section"
              value={form.section}
              onChange={handleChange}
              fullWidth
              required
            />

            <TextField
              label="Question Type"
              name="questionType"
              type="text"
              value={form.questionType}
              onChange={handleChange}
              fullWidth
              required
            />

            <TextField
              label="Difficulty"
              name="difficulty"
              type="number"
              value={form.difficulty}
              onChange={handleChange}
              fullWidth
              required
            />
            <TextField
              label="Count"
              name="count"
              type="number"
              value={form.count}
              onChange={handleChange}
              fullWidth
              required
            />
            <TextareaAutosize
              name="description"
              value={form.description}
              onChange={handleChange}
              style={{ width: "100%" }}
              minRows={3}
              placeholder="Description"
              required
            />
            <Button type="submit" variant="contained">
              Generate
            </Button>
          </Stack>
        </Box>
      </Grid>
      <Grid size={8}>
        <Box>
          {isGenerating && (
            <Box display="flex" justifyContent="center" alignItems="center">
              <CircularProgress />
            </Box>
          )}
          <Box
            sx={{
              height: "80vh",
              overflowY: "auto",
            }}
          >
            <GeneratedQuestions
              questions={questions}
              correctAnswers={correctAnswers}
              mcqAnswers={mcqAnswers}
              onAddToDB={handleAddToDB}
            />
          </Box>
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              marginTop: 2,
            }}
          >
            {!isGenerating && (
              <Button variant="contained" onClick={() => handleAddAllToDB()}>
                Add All To DB
              </Button>
            )}
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
};
