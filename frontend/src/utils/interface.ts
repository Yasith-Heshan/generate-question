export interface QuestionGenerationRequestBody {
  section: string;
  questionType: string;
  difficulty: number;
  count: number;
  description: string;
  detailedAnswer: boolean;
  exampleQuestion?: string;
}

export interface QuestionSaveRequestBody {
  section: string;
  questionType: string;
  difficulty: number;
  question: string;
  correctAnswer: string;
  mcqAnswers?: string[];
}

export interface GeneratedQuestionInfo {
  question: string;
  correctAnswer: string;
  mcqAnswers?: string[];
  index: number;
}

export interface QuestionFilterRequestBody {
  section: string;
  questionType: string;
  difficulty: number;
}

export interface QuestionFilterResponseItem {
  section: string;
  questionType: string;
  difficulty: number;
  question: string;
  correctAnswer: string;
  mcqAnswers?: string[];
}

export interface QuestionFilterResponse {
  questions: QuestionFilterResponseItem[];
}

export interface SympyGeneratorRequestBody {
  section: string;
  question_type: string;
  difficulty: number;
  questions_count: number;
  mcq: boolean;
}

export interface SympyGeneratorResponseItem {
  question: string;
  correct_solution: string;
  other_solutions: string[];
}
