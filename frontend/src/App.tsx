import AppBar from "./Components/AppBar";
import { ToastContainer } from "react-toastify";
import FilterQuestionsPage from "./pages/FilterQuestionsPage";
import { Routes, Route } from 'react-router-dom';
import { QuestionGeneratePage } from "./pages/QuestionGeneratePage";
import { SympyGeneratePage } from "./pages/SympyGenPage";
import { QuestionProvider } from "./context/QuestionContext";
import { FilterProvider } from "./context/FilterContext";
import { SympyProvider } from "./context/SympyContext";

function App() {
  return (
    <QuestionProvider>
    <FilterProvider>
    <SympyProvider>
      <AppBar />
      <Routes>
        <Route path="/" element={<QuestionGeneratePage />} />
        <Route path="/sympy" element={<SympyGeneratePage />} />
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
    </SympyProvider>
    </FilterProvider>
    </QuestionProvider>
  );
}

export default App;

