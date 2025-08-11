import React, { useState, useEffect } from "react";
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    Box,
    Chip,
    IconButton,
} from "@mui/material";
import { Add as AddIcon, Close as CloseIcon, Edit as EditIcon, Check as CheckIcon, ContentCopy as CopyIcon } from "@mui/icons-material";
import { MathJaxContext, MathJax } from "better-react-mathjax";

interface EditQuestionModalProps {
    open: boolean;
    onClose: () => void;
    onSave: (editedData: {
        question: string;
        correctAnswer: string;
        detailedAnswer?: string;
        mcqAnswers: string[];
    }) => void;
    initialData: {
        question: string;
        correctAnswer: string;
        detailedAnswer?: string;
        mcqAnswers: string[];
    };
}

const EditQuestionModal: React.FC<EditQuestionModalProps> = ({
    open,
    onClose,
    onSave,
    initialData,
}) => {
    const [question, setQuestion] = useState("");
    const [correctAnswer, setCorrectAnswer] = useState("");
    const [detailedAnswer, setDetailedAnswer] = useState("");
    const [mcqAnswers, setMcqAnswers] = useState<string[]>([]);
    const [newMcqAnswer, setNewMcqAnswer] = useState("");
    const [editingMcqIndex, setEditingMcqIndex] = useState<number | null>(null);
    const [editingMcqValue, setEditingMcqValue] = useState("");

    const config = {
        loader: { load: ["input/tex", "output/chtml"] },
    };

    useEffect(() => {
        if (open) {
            setQuestion(initialData.question);
            setCorrectAnswer(initialData.correctAnswer);
            setDetailedAnswer(initialData.detailedAnswer || "");
            setMcqAnswers(initialData.mcqAnswers || []);
            setNewMcqAnswer("");
            setEditingMcqIndex(null);
            setEditingMcqValue("");
        }
    }, [open, initialData]);

    const handleAddMcqAnswer = () => {
        if (newMcqAnswer.trim() && !mcqAnswers.includes(newMcqAnswer.trim())) {
            setMcqAnswers([...mcqAnswers, newMcqAnswer.trim()]);
            setNewMcqAnswer("");
        }
    };

    const handleRemoveMcqAnswer = (indexToRemove: number) => {
        setMcqAnswers(mcqAnswers.filter((_, index) => index !== indexToRemove));
    };

    const handleEditMcqAnswer = (index: number) => {
        setEditingMcqIndex(index);
        setEditingMcqValue(mcqAnswers[index]);
    };

    const handleSaveMcqEdit = () => {
        if (editingMcqIndex !== null && editingMcqValue.trim()) {
            const updatedAnswers = [...mcqAnswers];
            updatedAnswers[editingMcqIndex] = editingMcqValue.trim();
            setMcqAnswers(updatedAnswers);
            setEditingMcqIndex(null);
            setEditingMcqValue("");
        }
    };

    const handleCancelMcqEdit = () => {
        setEditingMcqIndex(null);
        setEditingMcqValue("");
    };

    const handleCopyMcqAnswer = async (answer: string) => {
        try {
            await navigator.clipboard.writeText(answer);
            // You could add a toast notification here if you have one available
            console.log('MCQ answer copied to clipboard:', answer);
        } catch (err) {
            console.error('Failed to copy to clipboard:', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = answer;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
    };

    const handleSave = () => {
        onSave({
            question,
            correctAnswer,
            detailedAnswer: detailedAnswer || undefined,
            mcqAnswers,
        });
        onClose();
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && e.currentTarget === e.target) {
            handleAddMcqAnswer();
        }
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>Edit Question</DialogTitle>
            <DialogContent>
                <Box sx={{ display: "flex", flexDirection: "column", gap: 3, mt: 1 }}>
                    {/* Question Field */}
                    <Box>
                        <TextField
                            label="Question"
                            multiline
                            rows={4}
                            fullWidth
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            variant="outlined"
                        />
                        {question && (
                            <Box sx={{ mt: 2, p: 2, bgcolor: "#f5f5f5", borderRadius: 1 }}>
                                <strong>Preview:</strong>
                                <MathJaxContext config={config}>
                                    <MathJax>{question}</MathJax>
                                </MathJaxContext>
                            </Box>
                        )}
                    </Box>

                    {/* Correct Answer Field */}
                    <Box>
                        <TextField
                            label="Correct Answer"
                            multiline
                            rows={2}
                            fullWidth
                            value={correctAnswer}
                            onChange={(e) => setCorrectAnswer(e.target.value)}
                            variant="outlined"
                        />
                        {correctAnswer && (
                            <Box sx={{ mt: 2, p: 2, bgcolor: "#f5f5f5", borderRadius: 1 }}>
                                <strong>Preview:</strong>
                                <MathJaxContext config={config}>
                                    <MathJax>{correctAnswer}</MathJax>
                                </MathJaxContext>
                            </Box>
                        )}
                    </Box>

                    {/* Detailed Answer Field */}
                    <Box>
                        <TextField
                            label="Detailed Answer (Optional)"
                            multiline
                            rows={4}
                            fullWidth
                            value={detailedAnswer}
                            onChange={(e) => setDetailedAnswer(e.target.value)}
                            variant="outlined"
                            placeholder="Enter a detailed explanation of the solution..."
                        />
                        {detailedAnswer && (
                            <Box sx={{ mt: 2, p: 2, bgcolor: "#f5f5f5", borderRadius: 1 }}>
                                <strong>Preview:</strong>
                                <MathJaxContext config={config}>
                                    <MathJax>{detailedAnswer}</MathJax>
                                </MathJaxContext>
                            </Box>
                        )}
                    </Box>

                    {/* MCQ Answers Field */}
                    <Box>
                        <Box sx={{ display: "flex", gap: 1, mb: 2 }}>
                            <TextField
                                label="Add MCQ Answer"
                                fullWidth
                                value={newMcqAnswer}
                                onChange={(e) => setNewMcqAnswer(e.target.value)}
                                onKeyPress={handleKeyPress}
                                variant="outlined"
                                placeholder="Enter an MCQ answer option"
                            />
                            <Button
                                variant="contained"
                                onClick={handleAddMcqAnswer}
                                startIcon={<AddIcon />}
                                sx={{ minWidth: "auto", px: 2 }}
                            >
                                Add
                            </Button>
                        </Box>

                        {mcqAnswers.length > 0 && (
                            <Box>
                                <strong>MCQ Answer Options:</strong>
                                <Box sx={{ display: "flex", flexDirection: "column", gap: 1, mt: 1 }}>
                                    {mcqAnswers.map((answer, index) => (
                                        <Box key={index} sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                                            {editingMcqIndex === index ? (
                                                // Edit mode
                                                <>
                                                    <TextField
                                                        value={editingMcqValue}
                                                        onChange={(e) => setEditingMcqValue(e.target.value)}
                                                        size="small"
                                                        fullWidth
                                                        onKeyPress={(e) => {
                                                            if (e.key === "Enter") {
                                                                handleSaveMcqEdit();
                                                            } else if (e.key === "Escape") {
                                                                handleCancelMcqEdit();
                                                            }
                                                        }}
                                                        autoFocus
                                                    />
                                                    <IconButton
                                                        size="small"
                                                        onClick={handleSaveMcqEdit}
                                                        color="primary"
                                                    >
                                                        <CheckIcon />
                                                    </IconButton>
                                                    <IconButton
                                                        size="small"
                                                        onClick={handleCancelMcqEdit}
                                                        color="secondary"
                                                    >
                                                        <CloseIcon />
                                                    </IconButton>
                                                </>
                                            ) : (
                                                // Display mode
                                                <>
                                                    <Chip
                                                        label={
                                                            <MathJaxContext config={config}>
                                                                <MathJax inline>{answer}</MathJax>
                                                            </MathJaxContext>
                                                        }
                                                        variant="outlined"
                                                        sx={{ maxWidth: "300px", flexGrow: 1 }}
                                                    />
                                                    <IconButton
                                                        size="small"
                                                        onClick={() => handleCopyMcqAnswer(answer)}
                                                        color="info"
                                                        title="Copy to clipboard"
                                                    >
                                                        <CopyIcon />
                                                    </IconButton>
                                                    <IconButton
                                                        size="small"
                                                        onClick={() => handleEditMcqAnswer(index)}
                                                        color="primary"
                                                        title="Edit this answer"
                                                    >
                                                        <EditIcon />
                                                    </IconButton>
                                                    <IconButton
                                                        size="small"
                                                        onClick={() => handleRemoveMcqAnswer(index)}
                                                        color="error"
                                                        title="Delete this answer"
                                                    >
                                                        <CloseIcon />
                                                    </IconButton>
                                                </>
                                            )}
                                        </Box>
                                    ))}
                                </Box>
                            </Box>
                        )}
                    </Box>
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} variant="outlined">
                    Cancel
                </Button>
                <Button onClick={handleSave} variant="contained">
                    Save Changes
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default EditQuestionModal;
