export interface QuestionGenerationRequestBody {
  section: string;
  questionType: string;
  difficulty: number;
  count: number;
  description: string;
  detailedAnswer: boolean;
  exampleQuestion?: string;
  image?: string; // Optional field for image content
  prevResponseId?: string; // Optional field for response ID
  keywords?: string[]; // Optional field for keywords
}

export interface QuestionSaveRequestBody {
  section: string;
  questionType: string;
  difficulty: number;
  question: string;
  correctAnswer: string;
  mcqAnswers?: string[];
  keywords?: string[];
  responseId?:string;
}

export interface GeneratedQuestionInfo {
  question: string;
  correctAnswer: string;
  detailedAnswer?: string;
  mcqAnswers?: string[];
  index: number;
  // optional id returned from generation API so that saved questions can
  // be associated with a particular response batch
  responseId?: string;
}

export interface QuestionFilterRequestBody {
  section: string;
  questionType: string;
  difficulty: number;
  keywords?: string[];
  id?: string;  // Optional field for filtering by question ID
}

export interface QuestionFilterResponseItem {
  id?: string;  // MongoDB ObjectId as string
  section: string;
  questionType: string;
  difficulty: number;
  question: string;
  detailedAnswer?: string;
  correctAnswer: string;
  keywords?: string[];
  mcqAnswers?: string[];
}

export interface QuestionUpdateRequestBody {
  section?: string;
  questionType?: string;
  difficulty?: number;
  question?: string;
  correctAnswer?: string;
  detailedAnswer?: string;
  mcqAnswers?: string[];
  keywords?: string[];
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
