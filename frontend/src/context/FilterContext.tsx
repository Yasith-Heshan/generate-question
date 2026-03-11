import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode, Dispatch, SetStateAction } from "react";
import type { QuestionFilterRequestBody, QuestionFilterResponseItem } from "../utils/interface";

interface FilterContextType {
  form: QuestionFilterRequestBody;
  setForm: Dispatch<SetStateAction<QuestionFilterRequestBody>>;
  filteredQuestions: QuestionFilterResponseItem[];
  setFilteredQuestions: Dispatch<SetStateAction<QuestionFilterResponseItem[]>>;
  clearFilteredQuestions: () => void;
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
    } catch {
      // ignore storage errors
    }
  }, [key, state]);

  return [state, setState] as const;
}

const defaultForm: QuestionFilterRequestBody = {
  section: "",
  questionType: "",
  difficulty: 1,
  keywords: [],
  id: "",
};

const FilterContext = createContext<FilterContextType | undefined>(undefined);

export function FilterProvider({ children }: { children: ReactNode }) {
  const [form, setForm] = usePersistedState<QuestionFilterRequestBody>("fq_form", defaultForm);
  const [filteredQuestions, setFilteredQuestions] = usePersistedState<QuestionFilterResponseItem[]>(
    "fq_filteredQuestions",
    []
  );

  const clearFilteredQuestions = () => {
    setFilteredQuestions([]);
  };

  return (
    <FilterContext.Provider
      value={{ form, setForm, filteredQuestions, setFilteredQuestions, clearFilteredQuestions }}
    >
      {children}
    </FilterContext.Provider>
  );
}

export function useFilter() {
  const ctx = useContext(FilterContext);
  if (!ctx) throw new Error("useFilter must be used within a FilterProvider");
  return ctx;
}
