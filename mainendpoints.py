# fastapi-service/main.py
# Step-by-Step Guide: Creating FastAPI Endpoints

from fastapi import FastAPI, HTTPException, Body, Query, Path
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any, Optional
import logging

# Initialize FastAPI app
app = FastAPI(
    title="AutoAdvisor API",
    description="Academic advising system with transcript analysis",
    version="1.0.0"
)

logger = logging.getLogger(__name__)


# ============================================================
# STEP 1: Define Data Models (Pydantic)
# These define what JSON structure you expect
# ============================================================

class Course(BaseModel):
    """Model for a single course"""
    name: str
    grade: str
    credits: float
    semester: str
    notes: Optional[str] = None


class Transcript(BaseModel):
    """Model for complete transcript"""
    freshman_1: List[Course] = []
    freshman_2: List[Course] = []
    sophomore_1: List[Course] = []
    sophomore_2: List[Course] = []
    junior_1: List[Course] = []
    junior_2: List[Course] = []
    senior_1: List[Course] = []
    senior_2: List[Course] = []


class StudentData(BaseModel):
    """Model for student information"""
    name: str
    student_id: str
    advisor: str
    transcript: Transcript


# ============================================================
# STEP 2: Create Simple GET Endpoint (No JSON needed)
# ============================================================

@app.get("/")
def root():
    """
    Simplest endpoint - just returns JSON
    
    Access: http://localhost:8001/
    """
    return {
        "message": "Welcome to AutoAdvisor API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    
    Access: http://localhost:8001/health
    """
    return {
        "status": "healthy",
        "service": "AutoAdvisor"
    }


# ============================================================
# STEP 3: GET Endpoint with Path Parameters
# ============================================================

@app.get("/students/{student_id}")
def get_student(student_id: str):
    """
    Get student by ID from URL path
    
    Access: http://localhost:8001/students/V123456789
    
    The {student_id} in the URL becomes a function parameter
    """
    return {
        "student_id": student_id,
        "message": f"Fetching data for student {student_id}"
    }


@app.get("/students/{student_id}/gpa")
def get_student_gpa(student_id: str):
    """
    Get specific student's GPA
    
    Access: http://localhost:8001/students/V123456789/gpa
    """
    # In real app, you'd fetch from database
    fake_gpa = 3.75
    
    return {
        "student_id": student_id,
        "gpa": fake_gpa
    }


# ============================================================
# STEP 4: GET Endpoint with Query Parameters
# ============================================================

@app.get("/search")
def search_students(
    name: Optional[str] = Query(None, description="Student name"),
    major: Optional[str] = Query(None, description="Major"),
    min_gpa: Optional[float] = Query(None, description="Minimum GPA")
):
    """
    Search students with query parameters
    
    Access examples:
    - http://localhost:8001/search?name=John
    - http://localhost:8001/search?major=CS&min_gpa=3.0
    - http://localhost:8001/search?name=John&major=CS
    """
    return {
        "search_params": {
            "name": name,
            "major": major,
            "min_gpa": min_gpa
        },
        "results": "Would return matching students here"
    }


# ============================================================
# STEP 5: POST Endpoint - Receive Simple JSON
# ============================================================

@app.post("/students/create")
def create_student(
    name: str = Body(...),
    student_id: str = Body(...),
    email: str = Body(...)
):
    """
    Create a student - receives simple JSON fields
    
    Send this JSON:
    {
        "name": "John Doe",
        "student_id": "V123456789",
        "email": "john@vsu.edu"
    }
    """
    return {
        "message": "Student created",
        "student": {
            "name": name,
            "student_id": student_id,
            "email": email
        }
    }


# ============================================================
# STEP 6: POST Endpoint - Receive Pydantic Model
# ============================================================

@app.post("/courses/add")
def add_course(course: Course):
    """
    Add a course - receives Course model
    
    Send this JSON:
    {
        "name": "Data Structures",
        "grade": "A",
        "credits": 3.0,
        "semester": "FA23",
        "notes": "Excellent course"
    }
    """
    return {
        "message": "Course added successfully",
        "course": course.dict()
    }


# ============================================================
# STEP 7: POST Endpoint - Receive Complex Nested JSON
# ============================================================

@app.post("/transcript/analyze")
def analyze_transcript(student: StudentData):
    """
    Analyze complete transcript - receives StudentData model
    
    Send this JSON:
    {
        "name": "John Doe",
        "student_id": "V123456789",
        "advisor": "Dr. Smith",
        "transcript": {
            "freshman_1": [
                {
                    "name": "Intro to CS",
                    "grade": "A",
                    "credits": 3.0,
                    "semester": "FA22",
                    "notes": null
                }
            ],
            "freshman_2": [],
            "sophomore_1": [],
            "sophomore_2": [],
            "junior_1": [],
            "junior_2": [],
            "senior_1": [],
            "senior_2": []
        }
    }
    """
    # Calculate total credits
    total_credits = 0
    all_courses = []
    
    # Loop through all semesters
    for semester in ['freshman_1', 'freshman_2', 'sophomore_1', 'sophomore_2',
                     'junior_1', 'junior_2', 'senior_1', 'senior_2']:
        courses = getattr(student.transcript, semester)
        for course in courses:
            total_credits += course.credits
            all_courses.append(course.name)
    
    return {
        "student_name": student.name,
        "student_id": student.student_id,
        "advisor": student.advisor,
        "total_credits": total_credits,
        "total_courses": len(all_courses),
        "courses": all_courses
    }


# ============================================================
# STEP 8: PUT Endpoint - Update Data
# ============================================================

@app.put("/students/{student_id}/advisor")
def update_advisor(
    student_id: str = Path(..., description="Student ID"),
    advisor_name: str = Body(..., description="New advisor name")
):
    """
    Update student's advisor
    
    URL: http://localhost:8001/students/V123456789/advisor
    
    Send JSON:
    {
        "advisor_name": "Dr. Johnson"
    }
    """
    return {
        "message": "Advisor updated",
        "student_id": student_id,
        "new_advisor": advisor_name
    }


# ============================================================
# STEP 9: DELETE Endpoint
# ============================================================

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    """
    Delete a course
    
    Access: http://localhost:8001/courses/123
    Method: DELETE
    """
    return {
        "message": f"Course {course_id} deleted successfully"
    }


# ============================================================
# STEP 10: Complete Example - Full CRUD Operations
# ============================================================

# Request/Response Models
class AnalyzeRequest(BaseModel):
    email: EmailStr
    password: str
    student_data: StudentData
    prompt: Optional[str] = None


class AnalyzeResponse(BaseModel):
    success: bool
    gpa: float
    total_credits: float
    recommendations: List[str]


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_student(request: AnalyzeRequest):
    """
    Complete analysis endpoint with validation
    
    Send this JSON:
    {
        "email": "john@vsu.edu",
        "password": "SecurePass123!",
        "student_data": {
            "name": "John Doe",
            "student_id": "V123456789",
            "advisor": "Dr. Smith",
            "transcript": {
                "freshman_1": [
                    {"name": "CS 101", "grade": "A", "credits": 3.0, "semester": "FA22"}
                ],
                "freshman_2": [],
                "sophomore_1": [],
                "sophomore_2": [],
                "junior_1": [],
                "junior_2": [],
                "senior_1": [],
                "senior_2": []
            }
        },
        "prompt": "What courses should I take?"
    }
    """
    # Validate credentials (simplified)
    if len(request.password) < 8:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Calculate GPA
    grade_values = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    total_credits = 0
    grade_points = 0
    
    # Process all semesters
    transcript = request.student_data.transcript
    for semester_name in transcript.dict():
        courses = getattr(transcript, semester_name)
        for course in courses:
            total_credits += course.credits
            grade_points += grade_values.get(course.grade, 0) * course.credits
    
    gpa = grade_points / total_credits if total_credits > 0 else 0.0
    
    # Generate recommendations
    recommendations = []
    if gpa >= 3.5:
        recommendations.append("Excellent work! Consider honors courses")
    elif gpa >= 3.0:
        recommendations.append("Good progress! Stay on track")
    else:
        recommendations.append("Consider tutoring services")
    
    if total_credits < 30:
        recommendations.append("Take 15-18 credits per semester")
    
    return AnalyzeResponse(
        success=True,
        gpa=round(gpa, 2),
        total_credits=total_credits,
        recommendations=recommendations
    )


# ============================================================
# STEP 11: Error Handling
# ============================================================

@app.post("/validate")
def validate_data(student_id: str = Body(...)):
    """
    Example of raising HTTP exceptions
    """
    if not student_id.startswith("V"):
        raise HTTPException(
            status_code=400,
            detail="Student ID must start with 'V'"
        )
    
    if len(student_id) != 10:
        raise HTTPException(
            status_code=400,
            detail="Student ID must be 10 characters"
        )
    
    return {"message": "Valid student ID", "student_id": student_id}


# ============================================================
# STEP 12: Optional/Default Parameters
# ============================================================

@app.get("/courses")
def list_courses(
    semester: str = Query("FA23", description="Semester code"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Skip first N results")
):
    """
    List courses with pagination
    
    Examples:
    - /courses (uses defaults)
    - /courses?semester=SP24
    - /courses?limit=20&offset=10
    """
    return {
        "semester": semester,
        "limit": limit,
        "offset": offset,
        "courses": ["Course 1", "Course 2", "Course 3"]  # Would be real data
    }


# ============================================================
# HOW TO TEST YOUR ENDPOINTS
# ============================================================

"""
TESTING METHODS:

1. FastAPI Interactive Docs (Recommended for beginners):
   - Start server: uvicorn main:app --reload --port 8001
   - Visit: http://localhost:8001/docs
   - Click any endpoint → "Try it out" → Fill in JSON → "Execute"

2. Using curl:
   
   # GET request
   curl http://localhost:8001/health
   
   # POST request with JSON
   curl -X POST http://localhost:8001/students/create \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "student_id": "V123", "email": "john@vsu.edu"}'
   
   # POST with JSON file
   curl -X POST http://localhost:8001/api/analyze \
     -H "Content-Type: application/json" \
     -d @sample_transcript.json

3. Using Python requests:
   
   import requests
   
   # GET
   response = requests.get("http://localhost:8001/health")
   print(response.json())
   
   # POST
   data = {"name": "John", "student_id": "V123", "email": "john@vsu.edu"}
   response = requests.post("http://localhost:8001/students/create", json=data)
   print(response.json())

4. REST Client Extension (.http file):
   
   ### Create Student
   POST http://localhost:8001/students/create
   Content-Type: application/json
   
   {
       "name": "John Doe",
       "student_id": "V123456789",
       "email": "john@vsu.edu"
   }
"""


# ============================================================
# ENDPOINT PATTERNS SUMMARY
# ============================================================

"""
PATTERN 1 - Simple GET (no parameters):
@app.get("/endpoint")
def function_name():
    return {"data": "value"}

PATTERN 2 - GET with path parameter:
@app.get("/endpoint/{param}")
def function_name(param: str):
    return {"param": param}

PATTERN 3 - GET with query parameters:
@app.get("/endpoint")
def function_name(param: str = Query(...)):
    return {"param": param}

PATTERN 4 - POST with simple body:
@app.post("/endpoint")
def function_name(field: str = Body(...)):
    return {"field": field}

PATTERN 5 - POST with Pydantic model:
@app.post("/endpoint")
def function_name(model: MyModel):
    return model.dict()

PATTERN 6 - POST with response model:
@app.post("/endpoint", response_model=ResponseModel)
def function_name(request: RequestModel):
    return ResponseModel(...)

Common HTTP methods:
- GET: Retrieve data
- POST: Create new data
- PUT: Update existing data
- DELETE: Remove data
- PATCH: Partial update
"""