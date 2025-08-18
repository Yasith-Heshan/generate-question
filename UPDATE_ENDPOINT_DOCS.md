# Update Question Endpoint Documentation

## Overview
A new endpoint has been added to update existing questions in the database.

## Endpoint Details

**Method:** `PUT`  
**URL:** `/questions/{question_id}`  
**Description:** Updates an existing question by its ID

## Parameters

### Path Parameters
- `question_id` (string, required): The unique identifier of the question to update

### Request Body
The request body should contain a JSON object with the fields you want to update. All fields are optional:

```json
{
  "section": "string (optional)",
  "questionType": "string (optional)", 
  "difficulty": "integer (optional)",
  "question": "string (optional)",
  "correctAnswer": "string (optional)",
  "detailedAnswer": "string (optional)",
  "mcqAnswers": ["string array (optional)"],
  "keywords": ["string array (optional)"]
}
```

## Response

### Success Response (200)
```json
{
  "message": "Question updated successfully",
  "question": {
    "id": "question_id",
    "section": "updated_section",
    "questionType": "updated_type",
    "difficulty": 1,
    "question": "updated_question",
    "correctAnswer": "updated_answer",
    "detailedAnswer": "updated_detailed_answer",
    "mcqAnswers": ["option1", "option2", "option3", "option4"],
    "keywords": ["keyword1", "keyword2"]
  }
}
```

### Error Responses

#### Question Not Found (404)
```json
{
  "detail": "Question not found"
}
```

#### Bad Request (400)
```json
{
  "detail": "Error message describing the issue"
}
```

## Usage Examples

### Example 1: Update question text and difficulty
```bash
curl -X PUT "http://localhost:8000/questions/64f8d2e5a1b2c3d4e5f6789a" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the derivative of x^2?",
    "difficulty": 2
  }'
```

### Example 2: Update multiple choice answers
```bash
curl -X PUT "http://localhost:8000/questions/64f8d2e5a1b2c3d4e5f6789a" \
  -H "Content-Type: application/json" \
  -d '{
    "mcqAnswers": ["2x", "x", "x^2", "2"],
    "correctAnswer": "2x"
  }'
```

### Example 3: Update keywords and section
```bash
curl -X PUT "http://localhost:8000/questions/64f8d2e5a1b2c3d4e5f6789a" \
  -H "Content-Type: application/json" \
  -d '{
    "section": "Calculus",
    "keywords": ["derivatives", "power rule", "differentiation"]
  }'
```

## Implementation Details

- The endpoint uses the `QuestionUpdateRequestBody` schema which allows partial updates
- Only provided fields will be updated; omitted fields remain unchanged
- If keywords are updated, they are also synchronized with the keywords collection
- The function validates that the question ID exists before attempting updates
- All database operations are wrapped in error handling for robust error reporting

## Related Endpoints

- `GET /questions/{question_id}` - Get a specific question (if implemented)
- `POST /questions` - Create a new question
- `POST /filter_questions` - Filter questions based on criteria
- `DELETE /questions/{question_id}` - Delete a question (if implemented)
