export interface QuestionGenerationRequestBody {
  section: string;
  questionType: string;
  difficulty: number;
  count: number;
  description: string;
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
