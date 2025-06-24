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
import { toast } from "react-toastify";
import type { QuestionFilterRequestBody, QuestionFilterResponseItem } from "../utils/interface";
import { filterQuestions } from "../api/openAiService";
import FilteredQuestions from "../Components/FilteredQuestions";

const FilterQuestionsPage = () => {
    const [form, setForm] = useState<QuestionFilterRequestBody>({
        section: "",
        questionType: "",
        difficulty: 1,
    });

    const [filteredQuestions, setFiltedQuestions] = useState<QuestionFilterResponseItem[]>([]);
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
                name === "difficulty" ? Number(value) : value,
        }));
    };

    const clearState = () => {
        setFiltedQuestions([]);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            clearState();
            setIsGenerating(true);
            const response = await filterQuestions(form);
            setFiltedQuestions(response.data);


        } catch (error) {
            console.error("Error generating questions:", error);
            alert("Failed to generate questions. Please try again.");
        } finally {
            setIsGenerating(false);
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
                        />

                        <TextField
                            label="Question Type"
                            name="questionType"
                            type="text"
                            value={form.questionType}
                            onChange={handleChange}
                            fullWidth
                        />

                        <TextField
                            label="Difficulty"
                            name="difficulty"
                            type="number"
                            value={form.difficulty}
                            onChange={handleChange}
                            fullWidth
                        />

                        <Button type="submit" variant="contained">
                            Filter
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
                        <FilteredQuestions
                            filteredQuestionResponseItems={filteredQuestions}
                        />
                    </Box>
                    <Box
                        sx={{
                            display: "flex",
                            justifyContent: "center",
                            marginTop: 2,
                        }}
                    >
                        {/* {!isGenerating && (
                            <Button variant="contained" onClick={() => handleAddAllToDB()}>
                                Add All To DB
                            </Button>
                        )} */}
                    </Box>
                </Box>
            </Grid>
        </Grid>
    )
}

export default FilterQuestionsPage