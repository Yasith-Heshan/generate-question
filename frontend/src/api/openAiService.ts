import { openAiAxiosInstance as axios } from "../utils/axiosInstance";
import type {
  QuestionFilterRequestBody,
  QuestionGenerationRequestBody,
  QuestionSaveRequestBody,
} from "../utils/interface";

export const generateQuestion = async (
  questionGenerationRequestBody: QuestionGenerationRequestBody
) => {
  return await axios.post("/api/v1/questions", questionGenerationRequestBody);
};

export const saveQuestion = async (
  questionSaveRequestBody: QuestionSaveRequestBody
) => {
  return await axios.post("/api/v1/add_question", questionSaveRequestBody);
};

export const saveAllQuestions = async (
  questions: QuestionSaveRequestBody[]
) => {
  return await axios.post("/api/v1/add_all_questions", questions);
};

export const filterQuestions = async (
  questionFilterRequestBody: QuestionFilterRequestBody
) => {
  return await axios.post("/api/v1/filter_questions", questionFilterRequestBody);
}

export const getAllSections = async () => {
  return await axios.get("/api/v1/sections");
}

export const getAllQuestionTypes = async () => {
  return await axios.get("/api/v1/question_types");
}

export const getAllKeywords = async () => {
  return await axios.get("/api/v1/keywords");
}

export const getKeywordsByFilter = async (section?: string, questionType?: string, difficulty?: number) => {
  const params = new URLSearchParams();
  if (section) params.append("section", section);
  if (questionType) params.append("questionType", questionType);
  if (difficulty !== undefined) params.append("difficulty", difficulty.toString());

  const queryString = params.toString();
  return await axios.get(`/api/v1/keywords/filter${queryString ? `?${queryString}` : ""}`);
}

export const getQuestionTypesBySection = async (section?: string) => {
  const params = new URLSearchParams();
  if (section) params.append("section", section);

  const queryString = params.toString();
  return await axios.get(`/api/v1/question_types/filter${queryString ? `?${queryString}` : ""}`);
}
