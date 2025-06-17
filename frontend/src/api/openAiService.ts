import { openAiAxiosInstance as axios } from "../utils/axiosInstance";
import type {
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
