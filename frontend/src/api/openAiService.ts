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
