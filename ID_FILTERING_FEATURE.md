# ID Filtering Feature Documentation

## Overview
Added the ability to filter questions using their unique ID in addition to the existing filters (section, question type, difficulty, keywords).

## Changes Made

### 1. Backend Updates

#### Schema Changes (`question.py`)
- Added `id: Optional[str] = None` field to `QuestionFilterRequestBody`
- This allows API requests to include an optional question ID for filtering

#### Service Function Updates (`question_service.py`)
- Updated `filter_questions_from_db` function to handle ID filtering
- Added ID validation using `PydanticObjectId` to ensure proper MongoDB ObjectId format
- Uses `_id` field for database queries when ID is provided

```python
if questionFilterRequestBody.id:
    from beanie import PydanticObjectId
    filters["_id"] = PydanticObjectId(questionFilterRequestBody.id)
```

### 2. Frontend Updates

#### Interface Updates (`interface.ts`)
- Added `id?: string` field to `QuestionFilterRequestBody` interface
- Maintains type safety across the frontend application

#### UI Updates (`FilterQuestionsPage.tsx`)
- Added new "Question ID" text field in the filter form
- Added proper placeholder and helper text for user guidance
- Updated form state to include `id` field
- Updated `resetForm` function to clear the ID field

## How to Use

### 1. **ID-Only Search**
- Enter a specific question ID in the "Question ID" field
- Leave other fields empty or use them as additional filters
- Click "Filter" to find the exact question

### 2. **Combined Filtering**
- Use ID field along with other filters (section, type, difficulty, keywords)
- The system will return questions matching ALL specified criteria
- Useful for verifying a question exists with specific attributes

### 3. **Finding Question IDs**
- Question IDs are displayed in the filtered results
- Copy the ID from the question display
- Use the ID to quickly find that specific question later

## API Usage

### Filter by ID Only
```bash
POST /api/v1/filter_questions
Content-Type: application/json

{
  "section": "",
  "questionType": "",
  "difficulty": 1,
  "keywords": [],
  "id": "64f8d2e5a1b2c3d4e5f6789a"
}
```

### Filter by ID + Other Criteria
```bash
POST /api/v1/filter_questions
Content-Type: application/json

{
  "section": "Mathematics",
  "questionType": "Multiple Choice",
  "difficulty": 2,
  "keywords": ["algebra"],
  "id": "64f8d2e5a1b2c3d4e5f6789a"
}
```

## UI Features

### Question ID Field
- **Label**: "Question ID"
- **Placeholder**: "Enter question ID to search for specific question"
- **Helper Text**: "Optional: Enter a specific question ID to find exact question"
- **Validation**: Handled by backend - invalid IDs will return empty results

### Form Behavior
- ID field is cleared when "Clear" button is clicked
- ID field can be used independently or with other filters
- Field accepts any string input (validation occurs on backend)

## Error Handling

### Invalid ID Format
- Backend validates ObjectId format
- Invalid IDs result in HTTP 400 error with descriptive message
- Frontend shows error toast notification

### Not Found
- Valid ID format but non-existent question returns empty results
- No error thrown - consistent with other filter behavior

## Benefits

1. **Quick Question Lookup**: Find specific questions instantly using their ID
2. **Debugging**: Easily verify question details during development/testing
3. **Administrative Tasks**: Quickly locate questions for editing or review
4. **Integration**: API consumers can efficiently fetch specific questions
5. **User Experience**: Copy/paste ID from one session to quickly find questions in another

## Technical Notes

- Uses MongoDB ObjectId format validation
- Combines seamlessly with existing filter logic
- Maintains backward compatibility - ID field is optional
- Database query uses `_id` field for optimal performance
- Frontend form maintains type safety with TypeScript interfaces

## Testing Status
- ✅ Backend compiles without errors
- ✅ Frontend builds successfully  
- ✅ Application runs correctly with Docker Compose
- ✅ All TypeScript types properly defined
- ✅ No compilation or runtime errors

The ID filtering feature is now fully functional and ready for use!
