import { QuestionGeneratePage } from "./pages/QuestionGeneratePage";
import AppBar from "./Components/AppBar";
import { ToastContainer } from "react-toastify";
import FilterQuestionsPage from "./pages/FilterQuestionsPage";

function App() {
  return (
    <>
      <AppBar />
      {/* <QuestionGeneratePage /> */}
      <FilterQuestionsPage />
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

