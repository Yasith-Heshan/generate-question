import { openAiAxiosInstance as axios } from "../utils/axiosInstance";
import type { UserCreateRequest, UserLoginRequest, UserProfile, UserListItem } from "../utils/interface";

export const signup = async (user: UserCreateRequest) => {
  return await axios.post("/api/v1/auth/signup", user);
};

export const login = async (user: UserLoginRequest) => {
  return await axios.post("/api/v1/auth/login", user);
};

export const resetPassword = async (email: string, oldPassword: string, newPassword: string) => {
  return await axios.post("/api/v1/auth/reset-password", {
    email,
    old_password: oldPassword,
    new_password: newPassword,
  });
};

export const getProfile = async () => {
  return await axios.get<UserProfile>("/api/v1/auth/me");
};

export const getUsers = async () => {
  return await axios.get<UserListItem[]>("/api/v1/auth/users");
};

