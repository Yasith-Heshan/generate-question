import { openAiAxiosInstance as axios } from "../utils/axiosInstance";

export interface UserQuestionStat {
  userId?: string;
  username: string;
  count: number;
}

export interface QuestionStatisticsResponse {
  userStats: UserQuestionStat[];
  totalQuestions: number;
}

// export const getQuestionStatistics = async (
//   userId?: string,
//   startDate?: string,
//   endDate?: string
// ): Promise<QuestionStatisticsResponse> => {
//   const params = new URLSearchParams();
//   if (userId) params.append("user_id", userId);
//   if (startDate) params.append("start_date", startDate);
//   if (endDate) params.append("end_date", endDate);

//   const queryString = params.toString();
//   const url = `/api/v1/statistics${queryString ? "?" + queryString : ""}`;
  
//   return await axios.get(url);
// };


export const getQuestionStatistics = async (
  userId?: string,
  startDate?: string,
  endDate?: string
): Promise<QuestionStatisticsResponse> => {
  const params = new URLSearchParams();

  if (userId) params.append("user_id", userId);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  const queryString = params.toString();

  const url = `/api/v1/statistics${queryString ? "?" + queryString : ""}`;

  const response = await axios.get<QuestionStatisticsResponse>(url);

  console.log("API DATA:", response.data);

  return response.data;
};

export interface UserItem {
  userId: string;
  username?: string;
}

export const getUserList = async (): Promise<UserItem[]> => {
  const response = await axios.get<UserItem[]>("/api/v1/users");
  return response.data;
};