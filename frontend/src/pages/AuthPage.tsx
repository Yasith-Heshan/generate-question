import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, TextField, Typography, ToggleButton, ToggleButtonGroup } from "@mui/material";
import { signup, login } from "../api/authService";
import { toast } from "react-toastify";
import type { UserCreateRequest, UserLoginRequest } from "../utils/interface";

const AuthPage = () => {
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem("access_token")) {
      navigate("/");
    }
  }, [navigate]);

  const handleModeChange = (_event: React.MouseEvent<HTMLElement>, nextMode: "login" | "signup" | null) => {
    if (nextMode !== null) {
      setMode(nextMode);
      setUsername("");
      setEmail("");
      setPassword("");
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      if (mode === "signup") {
        if (password !== confirmPassword) {
          toast.error("Passwords do not match");
          return;
        }

        if (password.length < 6) {
          toast.error("Password must be at least 6 characters");
          return;
        }

        const payload: UserCreateRequest = { username, email, password };
        await signup(payload);
        toast.success("Signup successful—please login");
        setMode("login");
        setPassword("");
        setConfirmPassword("");
        return;
      }

      const payload: UserLoginRequest = { email, password };
      const res = await login(payload);
      if (res && res.data) {
        const token = res.data.access_token;
        localStorage.setItem("access_token", token);
        toast.success("Login successful");
        navigate("/");
      }
    } catch (error: any) {
      const message = error.response?.data?.detail || "Authentication failed";
      toast.error(message);
    }
  };

  return (
    <Box sx={{ maxWidth: 420, mx: "auto", mt: 6, p: 3, bgcolor: "#fafafa", borderRadius: 2, boxShadow: 2 }}>
      <Typography variant="h5" align="center" mb={2}>
        {mode === "login" ? "Login" : "Sign Up"}
      </Typography>
      <ToggleButtonGroup value={mode} exclusive onChange={handleModeChange} fullWidth sx={{ mb: 2 }}>
        <ToggleButton value="login">Login</ToggleButton>
        <ToggleButton value="signup">Sign Up</ToggleButton>
      </ToggleButtonGroup>

      <Box component="form" onSubmit={handleSubmit} display="grid" gap={2}>
        {mode === "signup" && (
          <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        )}
        <TextField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {mode === "signup" && (
          <TextField
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        )}

        <Button type="submit" variant="contained" color="primary">
          {mode === "login" ? "Login" : "Sign Up"}
        </Button>
      </Box>
    </Box>
  );
};

export default AuthPage;
