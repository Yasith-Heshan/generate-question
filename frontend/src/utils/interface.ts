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
}
