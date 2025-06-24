import AppBar from "./Components/AppBar";
import { ToastContainer } from "react-toastify";
import FilterQuestionsPage from "./pages/FilterQuestionsPage";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QuestionGeneratePage } from "./pages/QuestionGeneratePage";

function App() {
  return (
    <>
      <AppBar />
      <Routes>
        <Route path="/" element={<QuestionGeneratePage />} />
        <Route path="/view" element={<FilterQuestionsPage />} />
      </Routes>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </>
  );
}

export default App;

