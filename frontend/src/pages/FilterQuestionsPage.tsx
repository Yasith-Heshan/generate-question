import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import {
    TextField,
    Button,
    Stack,
    CircularProgress,
    MenuItem,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import { useState } from "react";
import type { QuestionFilterRequestBody, QuestionFilterResponseItem } from "../utils/interface";
import { filterQuestions, getAllQuestionTypes, getAllSections } from "../api/openAiService";
import FilteredQuestions from "../Components/FilteredQuestions";
import { toast } from "react-toastify";

const FilterQuestionsPage = () => {
    const [form, setForm] = useState<QuestionFilterRequestBody>({
        section: "",
        questionType: "",
        difficulty: 1,
    });

    const [filteredQuestions, setFiltedQuestions] = useState<QuestionFilterResponseItem[]>([]);
    const [isGenerating, setIsGenerating] = useState(false);
    const [sections, setSections] = useState<string[]>([]);
    const [questionTypes, setQuestionTypes] = useState<string[]>([]);

    useEffect(() => {
        const fetchSectionsAndTypes = async () => {
            try {
                const sectionsResponse = await getAllSections();
                setSections(sectionsResponse.data);

                const typesResponse = await getAllQuestionTypes();
                setQuestionTypes(typesResponse.data);
            } catch (error) {
                toast.error("Failed to fetch sections or question types. Please try again.");
            }
        };

        fetchSectionsAndTypes();
    }, []);





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
                            select
                            label="Section"
                            name="section"
                            value={form.section}
                            onChange={handleChange}
                            fullWidth
                        >
                            {sections.map((section) => (
                                <MenuItem key={section} value={section}>
                                    {section}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            label="Question Type"
                            name="questionType"
                            type="text"
                            value={form.questionType}
                            onChange={handleChange}
                            fullWidth
                            select
                        >
                            {questionTypes.map((type) => (
                                <MenuItem key={type} value={type}>
                                    {type}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            label="Difficulty"
                            name="difficulty"
                            value={form.difficulty}
                            onChange={handleChange}
                            fullWidth
                            select
                        >
                            {[1, 2, 3, 4, 5].map((difficulty) => (
                                <MenuItem key={difficulty} value={difficulty}>
                                    {difficulty}
                                </MenuItem>
                            ))}
                        </TextField>

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