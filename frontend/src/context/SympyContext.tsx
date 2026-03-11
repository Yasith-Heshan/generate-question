import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode, Dispatch, SetStateAction } from "react";

interface SympyContextType {
  questions: string[];
  correctAnswers: string[];
  mcqAnswers: string[];
  graphImages: string[];
  setQuestions: Dispatch<SetStateAction<string[]>>;
  setCorrectAnswers: Dispatch<SetStateAction<string[]>>;
  setMcqAnswers: Dispatch<SetStateAction<string[]>>;
  setGraphImages: Dispatch<SetStateAction<string[]>>;
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

const SympyContext = createContext<SympyContextType | undefined>(undefined);

export function SympyProvider({ children }: { children: ReactNode }) {
  const [questions, setQuestions] = usePersistedState<string[]>("sq_questions", []);
  const [correctAnswers, setCorrectAnswers] = usePersistedState<string[]>("sq_correctAnswers", []);
  const [mcqAnswers, setMcqAnswers] = usePersistedState<string[]>("sq_mcqAnswers", []);
  const [graphImages, setGraphImages] = usePersistedState<string[]>("sq_graphImages", []);

  const clearQuestions = () => {
    setQuestions([]);
    setCorrectAnswers([]);
    setMcqAnswers([]);
    setGraphImages([]);
  };

  return (
    <SympyContext.Provider
      value={{ questions, correctAnswers, mcqAnswers, graphImages, setQuestions, setCorrectAnswers, setMcqAnswers, setGraphImages, clearQuestions }}
    >
      {children}
    </SympyContext.Provider>
  );
}

export function useSympyQuestions() {
  const ctx = useContext(SympyContext);
  if (!ctx) throw new Error("useSympyQuestions must be used within a SympyProvider");
  return ctx;
}
