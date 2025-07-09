from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from openai import OpenAI
import json

app = FastAPI(title="Meeting Minutes API", description="Convert meeting transcripts to structured meeting minutes")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class MeetingHeader(BaseModel):
    title: str
    date: str
    location: str
    participants: List[str]
    absent_members: List[str] = []
    facilitator: str

class PersonProgress(BaseModel):
    name: str
    previous_achievement_rate: int
    progress_status: str
    issues: str

class PersonGoal(BaseModel):
    name: str
    goal_content: str

class PersonSolution(BaseModel):
    name: str
    solution_content: str

class MeetingMinutes(BaseModel):
    title: str
    date: str
    location: str
    participants: List[str]
    absent_members: List[str]
    facilitator: str
    daily_goals: List[PersonGoal]
    progress_and_issues: List[PersonProgress]
    problem_solutions: List[PersonSolution]
    next_meeting_content: List[str] = [
        "①先日業務目標について",
        "②進捗、課題報告", 
        "③課題に対する解決策"
    ]

class TranscriptRequest(BaseModel):
    header: MeetingHeader
    transcript: str

class TranscriptProcessor:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)
    
    def process_transcript(self, request: TranscriptRequest) -> MeetingMinutes:
        prompt = self._create_processing_prompt(request.transcript)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            ai_content = response.choices[0].message.content
            parsed_data = self._parse_ai_response(ai_content)
            
            meeting_minutes = MeetingMinutes(
                title=request.header.title,
                date=request.header.date,
                location=request.header.location,
                participants=request.header.participants,
                absent_members=request.header.absent_members,
                facilitator=request.header.facilitator,
                daily_goals=parsed_data["daily_goals"],
                progress_and_issues=parsed_data["progress_and_issues"],
                problem_solutions=parsed_data["problem_solutions"]
            )
            
            return meeting_minutes
            
        except Exception as e:
            raise Exception(f"Failed to process transcript: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        return """
あなたは朝の進捗報告会の議事録作成アシスタントです。
会議のトランスクリプトを分析して、以下の形式で構造化された情報を抽出してください：

1. 本日の業務目標（各参加者の目標）
2. 現在の進捗と問題点（各参加者の前日達成度、進捗状況、問題点）
3. 問題解決方法（各参加者の解決策）

回答は必ずJSON形式で返してください。参加者の名前は正確に抽出し、内容は簡潔にまとめてください。
"""
    
    def _create_processing_prompt(self, transcript: str) -> str:
        return f"""
以下の朝の進捗報告会のトランスクリプトを分析して、構造化された情報を抽出してください：

トランスクリプト:
{transcript}

以下のJSON形式で回答してください：
{{
    "daily_goals": [
        {{"name": "参加者名", "goal_content": "目標内容"}}
    ],
    "progress_and_issues": [
        {{"name": "参加者名", "previous_achievement_rate": 80, "progress_status": "進捗状況", "issues": "問題点"}}
    ],
    "problem_solutions": [
        {{"name": "参加者名", "solution_content": "解決策内容"}}
    ]
}}
"""
    
    def _parse_ai_response(self, ai_content: str) -> dict:
        try:
            start_idx = ai_content.find('{')
            end_idx = ai_content.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in AI response")
            
            json_str = ai_content[start_idx:end_idx]
            parsed_data = json.loads(json_str)
            
            daily_goals = [PersonGoal(**goal) for goal in parsed_data.get("daily_goals", [])]
            progress_and_issues = [PersonProgress(**progress) for progress in parsed_data.get("progress_and_issues", [])]
            problem_solutions = [PersonSolution(**solution) for solution in parsed_data.get("problem_solutions", [])]
            
            return {
                "daily_goals": daily_goals,
                "progress_and_issues": progress_and_issues,
                "problem_solutions": problem_solutions
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            raise Exception(f"Failed to parse AI response: {str(e)}")

class MeetingMinutesFormatter:
    def format_to_text(self, minutes: MeetingMinutes) -> str:
        output = []
        
        output.append(f"タイトル：{minutes.title}")
        output.append(f"日時：{minutes.date}")
        output.append(f"場所：{minutes.location}")
        output.append(f"参加者：{', '.join(minutes.participants)}")
        output.append(f"欠席者：{', '.join(minutes.absent_members) if minutes.absent_members else 'なし'}")
        output.append(f"ファシリティ：{minutes.facilitator}")
        output.append("")
        
        output.append("アジェンダ")
        output.append("本日の業務目標")
        output.append("現在の進捗と問題点")
        output.append("問題解決方法")
        output.append("次回進捗報告内容")
        output.append("")
        
        output.append("・本日の業務目標")
        for goal in minutes.daily_goals:
            output.append(f"　{goal.name}")
            output.append(f"　{goal.goal_content}")
        output.append("")
        
        output.append("・現在の進捗と問題点")
        for progress in minutes.progress_and_issues:
            output.append(f"　・{progress.name}")
            output.append(f"　　　前日の達成度：{progress.previous_achievement_rate}%")
            output.append(f"　　　進捗状況：{progress.progress_status}")
            output.append(f"　　　問題点：{progress.issues}")
        output.append("")
        
        output.append("・問題解決方法")
        for solution in minutes.problem_solutions:
            output.append(f"　・{solution.name}")
            output.append(f"　　{solution.solution_content}")
        output.append("")
        
        output.append("次回進捗報告内容")
        for item in minutes.next_meeting_content:
            output.append(f"　{item}")
        
        return "\n".join(output)

processor = None
formatter = MeetingMinutesFormatter()

def get_processor():
    global processor
    if processor is None:
        try:
            processor = TranscriptProcessor()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return processor

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/process-transcript", response_model=MeetingMinutes)
async def process_transcript(request: TranscriptRequest):
    try:
        proc = get_processor()
        return proc.process_transcript(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/format-minutes")
async def format_minutes(minutes: MeetingMinutes):
    try:
        formatted_text = formatter.format_to_text(minutes)
        return {"formatted_minutes": formatted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-minutes")
async def generate_minutes(request: TranscriptRequest):
    try:
        proc = get_processor()
        minutes = proc.process_transcript(request)
        formatted_text = formatter.format_to_text(minutes)
        return {"formatted_minutes": formatted_text, "structured_data": minutes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
