import React from "react";
import Box from "@mui/material/Box";
import {
  TextField,
  Button,
  Stack,
  TextareaAutosize,
  CircularProgress,
  Switch,
  Autocomplete
} from "@mui/material";
import Grid from "@mui/material/Grid";
import { useState, useEffect } from "react";
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
  getAllSections,
  getQuestionTypesBySection,
  getKeywordsByFilter
} from "../api/openAiService";
import { toast } from "react-toastify";
import { FileUploader } from "react-drag-drop-files";

export const QuestionGeneratePage = () => {
  const [form, setForm] = useState<QuestionGenerationRequestBody>({
    section: "",
    description: "",
    count: 1,
    questionType: "",
    difficulty: 1,
    detailedAnswer: false,
    keywords: [],
  });

  const [questions, setQuestions] = useState<string[]>([]);
  const [correctAnswers, setCorrectAnswers] = useState<string[]>([]);
  const [detailedAnswers, setDetailedAnswers] = useState<string[]>([]);
  const [mcqAnswers, setMcqAnswers] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [file, setFile] = useState<File | null>(null)
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null)
  const [prevResponseId, setPrevResponseId] = useState<string>("");

  // State for autocomplete options
  const [sections, setSections] = useState<string[]>([]);
  const [questionTypes, setQuestionTypes] = useState<string[]>([]);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [isLoadingOptions, setIsLoadingOptions] = useState(false);

  const fileTypes = ["JPG", "JPEG", "PNG", "GIF", "WEBP"];

  // Fetch sections and question types on component mount
  useEffect(() => {
    const fetchOptions = async () => {
      setIsLoadingOptions(true);
      try {
        const [sectionsResponse, questionTypesResponse, keywordsResponse] = await Promise.all([
          getAllSections(),
          getQuestionTypesBySection(),
          getKeywordsByFilter(),
        ]);
        setSections(sectionsResponse.data);
        setQuestionTypes(questionTypesResponse.data);
        setKeywords(keywordsResponse.data);



      } catch (error) {
        console.error("Error fetching options:", error);
        toast.error("Failed to load options. Please refresh the page.");
      } finally {
        setIsLoadingOptions(false);
      }
    };

    fetchOptions();
  }, []);

  // Fetch keywords and question types based on form changes
  useEffect(() => {
    const fetchKeywordsAndQuestionTypes = async () => {
      setIsGenerating(true);
      try {
        const [keywordsResponse, questionTypesResponse] = await Promise.all([
          getKeywordsByFilter(form.section, form.questionType, form.difficulty),
          getQuestionTypesBySection(form.section),
        ]);
        setKeywords(keywordsResponse.data);
        setQuestionTypes(questionTypesResponse.data);
      } catch (error) {
        console.error("Error fetching keywords or question types:", error);
        toast.error("Failed to load keywords or question types. Please refresh the page.");
      } finally {
        setIsGenerating(false);
      }
    };

    if (form.section || form.questionType || form.difficulty) {
      fetchKeywordsAndQuestionTypes();
    }
  }, [form.section, form.questionType, form.difficulty]);

  // Cleanup image preview URL to prevent memory leaks
  useEffect(() => {
    return () => {
      if (imagePreviewUrl) {
        URL.revokeObjectURL(imagePreviewUrl);
      }
    };
  }, [imagePreviewUrl]);



  // convert file into base64 string
  const convertFileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = (error) => reject(error);
    });
  };

  const handleFileChange = async (input: File | File[]) => {
    let file: File;
    if (Array.isArray(input)) {
      if (input.length === 0) return;
      file = input[0];
    } else {
      file = input;
    }

    // Clean up previous preview URL if it exists
    if (imagePreviewUrl) {
      URL.revokeObjectURL(imagePreviewUrl);
    }

    setFile(file);

    // Create preview URL for the image
    const previewUrl = URL.createObjectURL(file);
    setImagePreviewUrl(previewUrl);

    const base64String = await convertFileToBase64(file);
    let desc = form.description;
    if (desc === "") {
      desc = "Image content:";
    }
    setForm({
      ...form, image: base64String, description: desc
    });
  }  

  const handleRemoveFile = () => {
    // Clean up preview URL
    if (imagePreviewUrl) {
      URL.revokeObjectURL(imagePreviewUrl);
    }

    setFile(null);
    setImagePreviewUrl(null);
    setForm((prev) => ({
      ...prev,
      image: undefined,
    }));
  }


  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name as string]:
        name === "count" || name === "difficulty"
          ? Number(value)
          : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      clearState();
      setIsGenerating(true);
      const response = await generateQuestion(form);
      let tempMcqAnswers: string[] = [];
      if (response.data.mcqAnswers) {
        tempMcqAnswers = (response.data.mcqAnswers as string[]).map(
          (mcqAnswer) => mcqAnswer.replace(/^\[|\]|\]\n\n|\]|---$/g, '')
        )
      }

      setQuestions(response.data.questions);
      setCorrectAnswers(response.data.correctAnswers);
      setDetailedAnswers(response.data.detailedAnswers || []);
      setMcqAnswers(tempMcqAnswers);
      setPrevResponseId(response.data.responseId || "");

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
    setDetailedAnswers((prev) =>
      prev.map((d, i) => i === index ? (editedData.detailedAnswer || "") : d)
    );
    setMcqAnswers((prev) =>
      prev.map((m, i) => i === index ? editedData.mcqAnswers.join(",") : m)
    );
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
      if (form.keywords?.length == 0) {
        toast.error("Please select at least one keyword before adding to the database.");
        setForm((prev) => ({
          ...prev,
          keywords: [],
        }));
        return;
      }

      await saveQuestion({
        ...generatedQuestionInfo,
        section: form.section,
        questionType: form.questionType,
        difficulty: form.difficulty,
        keywords: form.keywords,
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
        detailedAnswer: detailedAnswers
          ? detailedAnswers[index]
          : undefined,
        correctAnswer: correctAnswers[index],
        mcqAnswers: mcqAnswers[index].split(",") || [],
        keywords: form.keywords,
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
                setForm((prev) => ({
                  ...prev,
                  section: newValue || "",
                }));
              }}
              onInputChange={(_event, newInputValue) => {
                setForm((prev) => ({
                  ...prev,
                  section: newInputValue,
                }));
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
              value={form.questionType}
              onChange={(_event, newValue) => {
                setForm((prev) => ({
                  ...prev,
                  questionType: newValue || "",
                }));
              }}
              onInputChange={(_event, newInputValue) => {
                setForm((prev) => ({
                  ...prev,
                  questionType: newInputValue,
                }));
              }}
              freeSolo
              loading={isLoadingOptions}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Question Type"
                  name="questionType"
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
              maxRows={5}
              placeholder="Description"
              required
            />

            <Autocomplete
              multiple
              freeSolo
              options={keywords}
              value={form.keywords}
              loading={isLoadingOptions}
              onChange={(_event, newValue) => {
                const keywords = Array.isArray(newValue) ? newValue : [];
                setForm((prev) => ({
                  ...prev,
                  keywords: keywords,
                }));
              }}

              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Keywords"
                  name="keywords"
                  fullWidth
                  placeholder="e.g. algebra, equations, quadratic"
                  helperText="Type keywords and press Enter to add them, or select from existing options"
                />
              )}
            />

            <FileUploader
              handleChange={handleFileChange}
              name="image"
              types={fileTypes}
              multiple={false}
              children={
                <Box
                  sx={{
                    border: "1px dashed #ccc",
                    padding: 2,
                    textAlign: "center",
                    cursor: "pointer",
                  }}
                >
                  {file ? (<p>{file.name}</p>) : (
                    <p>Drag and drop an image file here, or click to select</p>
                  )}
                </Box>
              }
            />
            {file && (
              <Box>
                <Stack direction="column" justifyContent="center" alignItems="center" sx={{ mb: 1 }}>
                  {imagePreviewUrl && (
                    <Box sx={{ mt: 2 }}>
                      <img
                        src={imagePreviewUrl}
                        alt="Preview"
                        style={{
                          maxWidth: "100%",
                          maxHeight: "200px",
                          objectFit: "contain",
                          border: "1px solid #ddd",
                          borderRadius: "4px",
                        }}
                      />
                    </Box>
                  )}
                  <Button
                    size="small"
                    color="error"
                    variant="outlined"
                    onClick={(e) => {
                      e.stopPropagation(); // Prevent triggering file upload
                      handleRemoveFile();
                    }}
                  >
                    Remove
                  </Button>
                </Stack>

              </Box>
            )}

            <Stack direction="row" alignItems="center">
              <Switch
                name="detailedAnswer"
                checked={form.detailedAnswer || false}
                onChange={(e) =>
                  setForm((prev) => ({
                    ...prev,
                    detailedAnswer: e.target.checked,
                  }))
                }
                color="primary"
              />
              <label htmlFor="detailedAnswer">Detailed Answer</label>
            </Stack>

            <TextareaAutosize
              name="exampleQuestion"
              value={form.exampleQuestion}
              onChange={handleChange}
              style={{ width: "100%" }}
              minRows={3}
              placeholder="Example Question (optional)"
            />
            <Stack direction="row" justifyContent="center" gap={1}>
              <Button type="submit" variant="contained">
                Generate
              </Button>
              <Button
                variant="contained"
                onClick={() => {
                  setForm(
                    {
                      ...form,
                      prevResponseId: prevResponseId,
                    }
                  )
                  handleSubmit({ preventDefault: () => { } } as React.FormEvent);
                }}
              >Generate As Previous</Button>
            </Stack>
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
              detailedAnswers={detailedAnswers}
              correctAnswers={correctAnswers}
              mcqAnswers={mcqAnswers}
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
