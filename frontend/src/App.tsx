import { QuestionGeneratePage } from "./pages/QuestionGeneratePage";
import AppBar from "./Components/AppBar";
import { ToastContainer } from "react-toastify";

function App() {
  return (
    <>
      <AppBar />
      <QuestionGeneratePage />
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

