import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, TextField, Typography } from "@mui/material";
import { login, resetPassword, getProfile } from "../api/authService";
import { toast } from "react-toastify";
import type { UserLoginRequest } from "../utils/interface";

const AuthPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [resetRequired, setResetRequired] = useState(false);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem("access_token")) {
      navigate("/");
    }
  }, [navigate]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const payload: UserLoginRequest = { email, password };
      const res = await login(payload);
      if (res && res.data) {
        const token = res.data.access_token;
        localStorage.setItem("access_token", token);
        try {
          const profile = await getProfile();
          localStorage.setItem("is_admin", profile.data.is_admin ? "true" : "false");
        } catch {
          localStorage.setItem("is_admin", "false");
        }
        toast.success("Login successful");
        navigate("/");
      }
    } catch (error: any) {
      const message = error.response?.data?.detail || "Authentication failed";
      if (message === "Password reset required") {
        setResetRequired(true);
        toast.info("Your account requires a password reset. Please choose a new password.");
        return;
      }
      toast.error(message);
    }
  };

  const handleResetPassword = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (newPassword !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    if (newPassword.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }

    try {
      await resetPassword(email, password, newPassword);
      toast.success("Password reset successful. Please log in with your new password.");
      setResetRequired(false);
      setPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (error: any) {
      const message = error.response?.data?.detail || "Password reset failed";
      toast.error(message);
    }
  };

  return (
    <Box sx={{ maxWidth: 420, mx: "auto", mt: 6, p: 3, bgcolor: "#fafafa", borderRadius: 2, boxShadow: 2 }}>
      <Typography variant="h5" align="center" mb={2}>
        {resetRequired ? "Reset Password" : "Login"}
      </Typography>

      {!resetRequired ? (
        <Box component="form" onSubmit={handleSubmit} display="grid" gap={2}>
          <TextField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Button type="submit" variant="contained" color="primary">
            Login
          </Button>
        </Box>
      ) : (
        <Box component="form" onSubmit={handleResetPassword} display="grid" gap={2}>
          <TextField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required disabled />
          <TextField label="New Password" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
          <TextField
            label="Confirm New Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <Button type="submit" variant="contained" color="primary">
            Reset Password
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default AuthPage;
