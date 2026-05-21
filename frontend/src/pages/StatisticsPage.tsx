import { useState, useEffect } from "react";
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  MenuItem,
} from "@mui/material";

import { getQuestionStatistics, getUserList } from "../api/statisticsService";
import type { QuestionStatisticsResponse, UserItem } from "../api/statisticsService";
import { toast } from "react-toastify";

const getDefaultDates = () => {
  const today = new Date();

  const endDateObj = new Date(today);
  endDateObj.setDate(endDateObj.getDate() + 1);

  const end = endDateObj.toISOString().slice(0, 10);

  const startDateObj = new Date(today);
  startDateObj.setFullYear(startDateObj.getFullYear() - 1);

  const start = startDateObj.toISOString().slice(0, 10);

  return { start, end };
};

export default function StatisticsPage() {
  const defaultDates = getDefaultDates();
  const [statistics, setStatistics] = useState<QuestionStatisticsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState<string>("");
  const [startDate, setStartDate] = useState<string>(defaultDates.start);
  const [endDate, setEndDate] = useState<string>(defaultDates.end);
  const [users, setUsers] = useState<UserItem[]>([]);
  useEffect(() => {
    fetchStatistics(undefined, defaultDates.start, defaultDates.end);
  }, []);

  useEffect(() => {
  fetchStatistics(undefined, defaultDates.start, defaultDates.end);
  fetchUsers();
}, []);

const fetchUsers = async () => {
  try {
    const data = await getUserList();
    setUsers(data);
  } catch (error) {
    console.error("Error fetching users:", error);
    toast.error("Failed to fetch users");
  }
};

  const fetchStatistics = async (userId?: string, start?: string, end?: string) => {
    try {
      setLoading(true);
      const response = await getQuestionStatistics(userId || undefined, start || undefined, end || undefined);
      setStatistics(response);
    } catch (error) {
      console.error("Error fetching statistics:", error);
      toast.error("Failed to fetch statistics");
    } finally {
      setLoading(false);
    }
  };

  const handleApplyFilters = () => {
    fetchStatistics(selectedUserId, startDate, endDate);
  };

  const handleClearFilters = () => {
    setSelectedUserId("");
    setStartDate(defaultDates.start);
    setEndDate(defaultDates.end);
    fetchStatistics(undefined, defaultDates.start, defaultDates.end);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3 }}>
        Question Generation Statistics
      </Typography>

      {/* Filter Section */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Filters
        </Typography>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <TextField
              fullWidth
              select
              label="User ID"
              value={selectedUserId}
              onChange={(e) => setSelectedUserId(e.target.value)}
              variant="outlined"
              helperText="Select a user or leave empty for all"
            >
              <MenuItem value="">All Users</MenuItem>
              {users.length > 0
                ? users.map((u) => (
                    <MenuItem key={u.userId} value={u.username}>
                      {u.username}
                    </MenuItem>
                  ))
                : statistics?.userStats?.map((stat) => (
                    <MenuItem key={stat.userId ?? stat.username} value={stat.userId ?? stat.username}>
                      {stat.userId || stat.username}
                    </MenuItem>
                  ))}
            </TextField>
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <TextField
              fullWidth
              label="Start Date"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              slotProps={{ inputLabel: { shrink: true } }}
              variant="outlined"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <TextField
              fullWidth
              label="End Date"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              slotProps={{ inputLabel: { shrink: true } }}
              variant="outlined"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 3 }} sx={{ display: "flex", gap: 1 }}>
            <Button
              fullWidth
              variant="contained"
              color="primary"
              onClick={handleApplyFilters}
              disabled={loading}
            >
              Apply Filters
            </Button>
            <Button
              fullWidth
              variant="outlined"
              onClick={handleClearFilters}
              disabled={loading}
            >
              Clear
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Summary Cards */}
      {statistics && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Total Questions
                </Typography>
                <Typography variant="h5">
                  {statistics.totalQuestions}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Unique Users
                </Typography>
                <Typography variant="h5">
                  {statistics.userStats?.length ?? 0}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Average per User
                </Typography>
                <Typography variant="h5">
                  {(statistics.userStats?.length ?? 0) > 0
                    ? (statistics.totalQuestions / statistics.userStats.length).toFixed(2)
                    : 0}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Statistics Table */}
      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", p: 3 }}>
          <CircularProgress />
        </Box>
      ) : statistics && (statistics.userStats?.length ?? 0) > 0 ? (
        <TableContainer component={Paper}>
          <Table>
            <TableHead sx={{ backgroundColor: "#f5f5f5" }}>
              <TableRow>
                <TableCell sx={{ fontWeight: "bold" }}>User ID / Name</TableCell>
                <TableCell align="right" sx={{ fontWeight: "bold" }}>
                  Question Count
                </TableCell>
                <TableCell align="right" sx={{ fontWeight: "bold" }}>
                  Percentage
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {statistics.userStats.map((stat) => (
                  <TableRow key={stat.userId || stat.username}>
                  <TableCell>{stat.userId || stat.username}</TableCell>
                  <TableCell align="right">{stat.count}</TableCell>
                  <TableCell align="right">
                    {(
                      (stat.count / statistics.totalQuestions) *
                      100
                    ).toFixed(2)}
                    %
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <Alert severity="info">
          {loading ? "Loading..." : "No data available for the selected filters."}
        </Alert>
      )}
    </Box>
  );
}
