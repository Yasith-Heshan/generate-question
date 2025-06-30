import { sympyAxiosInstance as axios } from "../utils/axiosInstance";
import type {
  SympyGeneratorRequestBody,
} from "../utils/interface";

export const generateQuestion = async (
  questionGenerationRequestBody: SympyGeneratorRequestBody
) => {
  return await axios.post("/api/math_question", questionGenerationRequestBody);
};
