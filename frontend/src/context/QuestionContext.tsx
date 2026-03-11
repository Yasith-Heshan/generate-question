import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode, Dispatch, SetStateAction } from "react";

interface QuestionState {
  questions: string[];
  correctAnswers: string[];
  detailedAnswers: string[];
  mcqAnswers: string[];
  prevResponseId: string;
}

interface QuestionContextType extends QuestionState {
  setQuestions: Dispatch<SetStateAction<string[]>>;
  setCorrectAnswers: Dispatch<SetStateAction<string[]>>;
  setDetailedAnswers: Dispatch<SetStateAction<string[]>>;
  setMcqAnswers: Dispatch<SetStateAction<string[]>>;
  setPrevResponseId: Dispatch<SetStateAction<string>>;
  clearQuestions: () => void;
}

function usePersistedState<T>(key: string, defaultValue: T) {
  const [state, setState] = useState<T>(() => {
    try {
      const stored = localStorage.getItem(key);
      return stored !== null ? (JSON.parse(stored) as T) : defaultValue;
    } catch {
      return defaultValue;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(state));
    } catch(err) {
      console.error("Failed to persist state to localStorage:", err);
    }
  }, [key, state]);

  return [state, setState] as const;
}

const QuestionContext = createContext<QuestionContextType | undefined>(undefined);

export function QuestionProvider({ children }: { children: ReactNode }) {
  const [questions, setQuestions] = usePersistedState<string[]>("gq_questions", []);
  const [correctAnswers, setCorrectAnswers] = usePersistedState<string[]>("gq_correctAnswers", []);
  const [detailedAnswers, setDetailedAnswers] = usePersistedState<string[]>("gq_detailedAnswers", []);
  const [mcqAnswers, setMcqAnswers] = usePersistedState<string[]>("gq_mcqAnswers", []);
  const [prevResponseId, setPrevResponseId] = usePersistedState<string>("gq_prevResponseId", "");

  const clearQuestions = () => {
    setQuestions([]);
    setCorrectAnswers([]);
    setMcqAnswers([]);
  };

  return (
    <QuestionContext.Provider
      value={{
        questions,
        correctAnswers,
        detailedAnswers,
        mcqAnswers,
        prevResponseId,
        setQuestions,
        setCorrectAnswers,
        setDetailedAnswers,
        setMcqAnswers,
        setPrevResponseId,
        clearQuestions,
      }}
    >
      {children}
    </QuestionContext.Provider>
  );
}

export function useQuestions() {
  const ctx = useContext(QuestionContext);
  if (!ctx) throw new Error("useQuestions must be used within a QuestionProvider");
  return ctx;
}
