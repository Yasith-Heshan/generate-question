import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import {
    TextField,
    Button,
    Stack,
    CircularProgress,
    MenuItem,
    Autocomplete,
    Chip,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import { useState } from "react";
import type { QuestionFilterRequestBody, QuestionFilterResponseItem } from "../utils/interface";
import { filterQuestions, getAllSections, getKeywordsByFilter, getQuestionTypesBySection } from "../api/openAiService";
import FilteredQuestions from "../Components/FilteredQuestions";
import { toast } from "react-toastify";

const FilterQuestionsPage = () => {
    const [form, setForm] = useState<QuestionFilterRequestBody>({
        section: "",
        questionType: "",
        difficulty: 1,
        keywords: [],
    });

    const [filteredQuestions, setFiltedQuestions] = useState<QuestionFilterResponseItem[]>([]);
    const [isGenerating, setIsGenerating] = useState(false);
    const [sections, setSections] = useState<string[]>([]);
    const [questionTypes, setQuestionTypes] = useState<string[]>([]);
    const [availableKeywords, setAvailableKeywords] = useState<string[]>([]);
    const [isLoadingOptions, setIsLoadingOptions] = useState(false);

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
                setAvailableKeywords(keywordsResponse.data);
            } catch (error) {
                console.error("Error fetching options:", error);
                toast.error("Failed to load options. Please refresh the page.");
            } finally {
                setIsLoadingOptions(false);
            }
        };

        fetchOptions();
    }, []);

    useEffect(() => {
        const fetchKeywordsAndQuestionTypes = async () => {
            setIsGenerating(true);
            try {
                const [keywordsResponse, questionTypesResponse] = await Promise.all([
                    getKeywordsByFilter(form.section, form.questionType, form.difficulty),
                    getQuestionTypesBySection(form.section),
                ]);
                setAvailableKeywords(keywordsResponse.data);
                setQuestionTypes(questionTypesResponse.data);
            } catch (error) {
                console.error("Error fetching keywords or question types:", error);
                toast.error("Failed to load keywords or question types. Please refresh the page.");
            } finally {
                setIsGenerating(false);
            }
        };

        fetchKeywordsAndQuestionTypes();

        if (form.section || form.questionType || form.difficulty) {
            fetchKeywordsAndQuestionTypes();
        }
    }, [form.section, form.questionType, form.difficulty]);





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

    const resetForm = () => {
        setForm({
            section: "",
            questionType: "",
            difficulty: 1,
            keywords: [],
        });
        clearState();
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

                        <Autocomplete
                            multiple
                            options={availableKeywords}
                            value={form.keywords || []}
                            loading={isLoadingOptions}
                            onChange={(_, newValue) => {
                                setForm((prev) => ({
                                    ...prev,
                                    keywords: newValue,
                                }));
                            }}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => (
                                    <Chip variant="outlined" label={option} {...getTagProps({ index })} />
                                ))
                            }
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="Keywords"
                                    placeholder="Select or type keywords"
                                    helperText="Choose keywords to filter questions"
                                />
                            )}
                            freeSolo
                        />



                        <Button type="submit" variant="contained">
                            Filter
                        </Button>

                        <Button type="button" variant="outlined" onClick={resetForm}>
                            Clear
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