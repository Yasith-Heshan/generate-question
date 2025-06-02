import Box from "@mui/material/Box";
import { TextField, Button, Stack, TextareaAutosize } from "@mui/material";
import { useState } from "react";
import axios from "axios";
import GeneratedQuestions from "./Components/GeneratedQeustions";

function App() {
  const [form, setForm] = useState({
    section: "",
    description: "",
    count: 1,
    questionType: "",
    difficulty: 1,
  });

  const [questions, setQuestions] = useState([]);
  const [correctAnswers, setCorrectAnswers] = useState([]);
  // const [mcqAnswers, setMcqAnswers] = useState([]);
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
    console.log(form);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // handle form submission
    try {
      setIsGenerating(true);
      setQuestions([]);
      setCorrectAnswers([]);
      // setMcqAnswers([]);
      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/questions",
        form
      );
      console.log("Response from server:", response.data);
      setQuestions(response.data.questions);
      setCorrectAnswers(response.data.correctAnswers);
      // setMcqAnswers(response.data.mcqAnswers);
    } catch (error) {
      console.error("Error generating questions:", error);
      alert("Failed to generate questions. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  async function handleAddToDB(): Promise<void> {
    try {
      // await axios.post("http://127.0.0.1:8000/api/v1/questions/save", {
      //   questions,
      //   correctAnswers,
      //   mcqAnswers,
      // });
      alert("Questions added to database successfully!");
    } catch (error) {
      console.error("Error adding questions to DB:", error);
      alert("Failed to add questions to the database.");
    }
  }
  return (
    <Box
      sx={{
        borderRadius: 1,
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
          label="Count"
          name="count"
          type="number"
          value={form.count}
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

      {isGenerating && (
        <Box sx={{ marginTop: 2 }}>
          <p>Generating questions, please wait...</p>
        </Box>
      )}

      <GeneratedQuestions
        questions={questions}
        correctAnswers={correctAnswers}
        onAddToDB={handleAddToDB}
      />
    </Box>
  );
}

export default App;

