import React from "react";
import Box from "@mui/material/Box";
import {
  TextField,
  Button,
  Stack,
  CircularProgress,
  Checkbox,
  Autocomplete
} from "@mui/material";
import Grid from "@mui/material/Grid";
import { useState, useEffect } from "react";
import GeneratedQuestions from "../Components/GeneratedQeustions";
import type {
  GeneratedQuestionInfo,
  QuestionSaveRequestBody,
  SympyGeneratorResponseItem,
} from "../utils/interface";
import {
  generateQuestion,
} from "../api/sympyService";
import { toast } from "react-toastify";
import { saveQuestion, saveAllQuestions, getAllSections, getQuestionTypesBySection } from "../api/openAiService";
import { useSympyQuestions } from "../context/SympyContext";

export const SympyGeneratePage = () => {
  const { questions, setQuestions, correctAnswers, setCorrectAnswers, mcqAnswers, setMcqAnswers, graphImages, setGraphImages, form, setForm, clearQuestions } = useSympyQuestions();
  const [isGenerating, setIsGenerating] = useState(false);
  // keep track of AI response id similar to the regular generation page (unused for sympy currently)
  const [prevResponseId, setPrevResponseId] = useState<string>("");

  // State for autocomplete options
  const [sections, setSections] = useState<string[]>([]);
  const [questionTypes, setQuestionTypes] = useState<string[]>([]);
  const [isLoadingOptions, setIsLoadingOptions] = useState(false);

  // Fetch sections and question types on mount
  useEffect(() => {
    const fetchOptions = async () => {
      setIsLoadingOptions(true);
      try {
        const [sectionsResponse, questionTypesResponse] = await Promise.all([
          getAllSections(),
          getQuestionTypesBySection(),
        ]);
        setSections(sectionsResponse.data);
        setQuestionTypes(questionTypesResponse.data);
      } catch (error) {
        console.error("Error fetching options:", error);
        toast.error("Failed to load options. Please refresh the page.");
      } finally {
        setIsLoadingOptions(false);
      }
    };
    fetchOptions();
  }, []);

  // Refresh question types when section changes
  useEffect(() => {
    const fetchQuestionTypes = async () => {
      try {
        const response = await getQuestionTypesBySection(form.section);
        setQuestionTypes(response.data);
      } catch (error) {
        console.error("Error fetching question types:", error);
      }
    };
    if (form.section) {
      fetchQuestionTypes();
    }
  }, [form.section]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name as string]:
        name === "questions_count" || name === "difficulty" ? Number(value) : value,
    }));
  };

  const formatAnswer = (answer: string): string => {
    return answer.replace(/\$([^$]+)\$/g, (_, expr) => `$$${expr}$$`)
  }

  const formatMcqAnswers = (answers: string[]): string[] => {
    return answers.map((answer) =>
      formatAnswer(answer)
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      clearState();
      setIsGenerating(true);
      const requestBody = { ...form, prevResponseId };
      const response = await generateQuestion(requestBody);
      let questions: string[] = [];
      let correctAnswers: string[] = [];
      let mcqAnswers: string[] = [];
      let graphImages: string[] = [];
      response.data.forEach((item: SympyGeneratorResponseItem) => {
        questions.push(item.question);
        correctAnswers.push(formatAnswer(item.correct_solution));
        if (form.mcq && item.other_solutions) {
          mcqAnswers.push(formatMcqAnswers(item.other_solutions).join(","));
        }
        graphImages.push(item.graph_img ?? "");
      });
      setQuestions(questions);
      setCorrectAnswers(correctAnswers);
      setMcqAnswers(mcqAnswers);
      setGraphImages(graphImages);
      const newResp = response.data.responseId || "";
      setPrevResponseId(newResp);
      setForm((prev) => ({ ...prev, prevResponseId: newResp }));
    } catch (error) {
      console.error("Error generating questions:", error);
      toast.error("Failed to generate questions. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  const removeAddedQuestion = (index: number) => {
    setQuestions((prev) => prev.filter((_, i) => i !== index));
    setCorrectAnswers((prev) => prev.filter((_, i) => i !== index));
    setMcqAnswers((prev) => prev.filter((_, i) => i !== index));
    setGraphImages((prev) => prev.filter((_, i) => i !== index));
  };

  const handleEditQuestion = (
    index: number,
    editedData: {
      question: string;
      correctAnswer: string;
      detailedAnswer?: string;
      mcqAnswers: string[];
    }
  ) => {
    setQuestions((prev) =>
      prev.map((q, i) => i === index ? editedData.question : q)
    );
    setCorrectAnswers((prev) =>
      prev.map((a, i) => i === index ? editedData.correctAnswer : a)
    );
    setMcqAnswers((prev) =>
      prev.map((m, i) => i === index ? editedData.mcqAnswers.join(",") : m)
    );
  };


  const clearState = () => {
    clearQuestions();
  };

  async function handleAddToDB(
    generatedQuestionInfo: GeneratedQuestionInfo
  ): Promise<void> {
    if (!form.section || !form.question_type || !form.difficulty) {
      toast.error("Please fill in Section, Question Type, and Difficulty before saving.");
      return;
    }
    try {
      await saveQuestion({
        ...generatedQuestionInfo,
        section: form.section,
        questionType: form.question_type,
        difficulty: form.difficulty,
        responseId: prevResponseId,
        graphImg: generatedQuestionInfo.graphImg,
      } as QuestionSaveRequestBody);
      removeAddedQuestion(generatedQuestionInfo.index);
      toast.success("Question added to the database successfully!");
    } catch (error) {
      console.error("Error adding questions to DB:", error);
      toast.error("Failed to add question to the database. Please try again.");
    }
  }

  const handleAddAllToDB = async () => {
    if (!form.section || !form.question_type || !form.difficulty) {
      toast.error("Please fill in Section, Question Type, and Difficulty before saving.");
      return;
    }
    const questionSaveRequestBody: QuestionSaveRequestBody[] = questions.map(
      (question, index) =>
      ({
        section: form.section,
        questionType: form.question_type,
        difficulty: form.difficulty,
        question: question,
        correctAnswer: correctAnswers[index],
        mcqAnswers: mcqAnswers[index].split(",") || [],
        responseId: prevResponseId,
        graphImg: graphImages[index] || undefined,
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
            <Autocomplete
              options={sections}
              value={form.section}
              onChange={(_event, newValue) => {
                setForm((prev) => ({ ...prev, section: newValue || "" }));
              }}
              onInputChange={(_event, newInputValue) => {
                setForm((prev) => ({ ...prev, section: newInputValue }));
              }}
              freeSolo
              loading={isLoadingOptions}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Section"
                  name="section"
                  fullWidth
                  required
                />
              )}
            />

            <Autocomplete
              options={questionTypes}
              value={form.question_type}
              onChange={(_event, newValue) => {
                setForm((prev) => ({ ...prev, question_type: newValue || "" }));
              }}
              onInputChange={(_event, newInputValue) => {
                setForm((prev) => ({ ...prev, question_type: newInputValue }));
              }}
              freeSolo
              loading={isLoadingOptions}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Question Type"
                  name="question_type"
                  fullWidth
                  required
                />
              )}
            />

            <TextField
              label="Difficulty"
              name="difficulty"
              type="number"
              value={form.difficulty}
              onChange={handleChange}
              fullWidth
              inputProps={{ min: 1, max: 5 }}
              required
            />
            <TextField
              label="Count"
              name="questions_count"
              type="number"
              value={form.questions_count}
              onChange={handleChange}
              fullWidth
              required
            />

            <Box display="flex" alignItems="center">
              <Checkbox
                name="mcq"
                checked={form.mcq}
                onChange={(e) =>
                  setForm((prev) => ({
                    ...prev,
                    mcq: e.target.checked,
                  }))
                }
              />
              <label>Generate MCQ</label>
            </Box>


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
              height: "70vh",
              overflowY: "auto",
            }}
          >
            <GeneratedQuestions
              questions={questions}
              correctAnswers={correctAnswers}
              mcqAnswers={mcqAnswers}
              graphImages={graphImages}
              onAddToDB={handleAddToDB}
              onEditQuestion={handleEditQuestion}
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
