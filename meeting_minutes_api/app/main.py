from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from typing import List, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import traceback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print("APIキー：", key)

app = FastAPI(
    title="Meeting Minutes API",
    description="Convert meeting transcripts to structured meeting minutes",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
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
            logger.info("OpenAI APIリクエストを開始します")
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            logger.info("OpenAI APIレスポンスを受信しました")

            ai_content = response.choices[0].message.content
            logger.info(f"AI応答内容の長さ: {len(ai_content) if ai_content else 0}文字")
            
            parsed_data = self._parse_ai_response(ai_content)
            logger.info("AI応答の解析が完了しました")

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
            error_type = type(e).__name__
            error_message = str(e)
            stack_trace = traceback.format_exc()
            
            logger.error(f"トランスクリプト処理エラー - タイプ: {error_type}")
            logger.error(f"エラーメッセージ: {error_message}")
            logger.error(f"スタックトレース:\n{stack_trace}")
            
            detailed_error = {
                "error_type": error_type,
                "error_message": error_message,
                "processing_stage": self._determine_processing_stage(e),
                "stack_trace": stack_trace.split('\n')[-3:-1]  # 最も関連性の高い部分のみ
            }
            
            raise Exception(f"トランスクリプト処理に失敗しました: {json.dumps(detailed_error, ensure_ascii=False, indent=2)}")

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
            logger.info("AI応答の解析を開始します")
            
            if not ai_content:
                raise ValueError("AI応答が空です")
            
            start_idx = ai_content.find('{')
            end_idx = ai_content.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                logger.error(f"AI応答にJSONが見つかりません。応答内容: {ai_content[:200]}...")
                raise ValueError("AI応答にJSON形式のデータが見つかりません")

            json_str = ai_content[start_idx:end_idx]
            logger.info(f"抽出されたJSON文字列の長さ: {len(json_str)}文字")
            
            try:
                parsed_data = json.loads(json_str)
                logger.info("JSON解析が成功しました")
            except json.JSONDecodeError as json_error:
                logger.error(f"JSON解析エラー: {json_error}")
                logger.error(f"解析対象のJSON: {json_str}")
                raise json.JSONDecodeError(f"JSON解析に失敗: {json_error.msg} (位置: {json_error.pos})", json_str, json_error.pos)

            required_keys = ["daily_goals", "progress_and_issues", "problem_solutions"]
            missing_keys = [key for key in required_keys if key not in parsed_data]
            if missing_keys:
                logger.error(f"必須キーが不足: {missing_keys}")
                raise ValueError(f"AI応答に必須キーが不足しています: {missing_keys}")

            try:
                daily_goals = [PersonGoal(**goal) for goal in parsed_data.get("daily_goals", [])]
                logger.info(f"日次目標を{len(daily_goals)}件処理しました")
            except Exception as e:
                logger.error(f"日次目標の処理エラー: {e}")
                raise ValueError(f"日次目標データの処理に失敗: {e}")

            try:
                progress_and_issues = [PersonProgress(**progress) for progress in parsed_data.get("progress_and_issues", [])]
                logger.info(f"進捗・問題点を{len(progress_and_issues)}件処理しました")
            except Exception as e:
                logger.error(f"進捗・問題点の処理エラー: {e}")
                raise ValueError(f"進捗・問題点データの処理に失敗: {e}")

            try:
                problem_solutions = [PersonSolution(**solution) for solution in parsed_data.get("problem_solutions", [])]
                logger.info(f"問題解決策を{len(problem_solutions)}件処理しました")
            except Exception as e:
                logger.error(f"問題解決策の処理エラー: {e}")
                raise ValueError(f"問題解決策データの処理に失敗: {e}")

            return {
                "daily_goals": daily_goals,
                "progress_and_issues": progress_and_issues,
                "problem_solutions": problem_solutions
            }

        except Exception as e:
            error_type = type(e).__name__
            error_context = {
                "error_type": error_type,
                "error_message": str(e),
                "ai_content_length": len(ai_content) if ai_content else 0,
                "ai_content_preview": ai_content[:300] if ai_content else "なし"
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            raise Exception(f"Failed to parse AI response: {str(e)}")

    def _determine_processing_stage(self, error: Exception) -> str:
        """エラーが発生した処理段階を特定する"""
        error_message = str(error).lower()
        
        if "api" in error_message or "openai" in error_message:
            return "OpenAI API呼び出し"
        elif "json" in error_message or "parse" in error_message:
            return "AI応答の解析"
        elif "pydantic" in error_message or "validation" in error_message:
            return "データ検証"
        elif "model" in error_message:
            return "データモデル作成"
        else:
            return "不明な段階"

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

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    認証問題を回避するためOpenAPI仕様を直接埋め込むカスタムSwagger UIエンドポイント
    """
    openapi_schema = app.openapi()
    openapi_json = json.dumps(openapi_schema)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>{app.title} - Swagger UI</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script>
    const spec = {openapi_json};
    const ui = SwaggerUIBundle({{
        spec: spec,
        dom_id: '#swagger-ui',
        layout: 'BaseLayout',
        deepLinking: true,
        showExtensions: true,
        showCommonExtensions: true,
        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
        ]
    }});
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

@app.post("/generate-minutes")
async def generate_minutes(request: TranscriptRequest):
    """
    朝の進捗報告会のトランスクリプトから議事録を生成する単一エンドポイント

    引数:
        request: 会議ヘッダー情報とトランスクリプトを含むリクエスト

    戻り値:
        formatted_minutes: テキスト形式の議事録
    """
    try:
        logger.info("議事録生成リクエストを受信しました")
        logger.info(f"会議タイトル: {request.header.title}")
        logger.info(f"参加者数: {len(request.header.participants)}")
        logger.info(f"トランスクリプト長: {len(request.transcript)}文字")
        
        proc = get_processor()
        logger.info("TranscriptProcessorを取得しました")

        minutes = proc.process_transcript(request)
        logger.info("トランスクリプト処理が完了しました")

        formatted_text = formatter.format_to_text(minutes)
        logger.info(f"議事録フォーマット完了 - 出力長: {len(formatted_text)}文字")

        return {"formatted_minutes": formatted_text}
        
    except HTTPException:
        raise
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        stack_trace = traceback.format_exc()
        
        logger.error(f"議事録生成エラー - タイプ: {error_type}")
        logger.error(f"エラーメッセージ: {error_message}")
        logger.error(f"スタックトレース:\n{stack_trace}")
        
        error_details = {
            "timestamp": "2025-07-10T02:26:42Z",
            "error_type": error_type,
            "error_message": error_message,
            "request_info": {
                "title": request.header.title if hasattr(request, 'header') else "不明",
                "participants_count": len(request.header.participants) if hasattr(request, 'header') and hasattr(request.header, 'participants') else 0,
                "transcript_length": len(request.transcript) if hasattr(request, 'transcript') else 0
            },
            "stack_trace_summary": stack_trace.split('\n')[-3:-1]  # 最も関連性の高い部分
        }
        
        detailed_message = f"議事録生成に失敗しました:\n{json.dumps(error_details, ensure_ascii=False, indent=2)}"
        
        raise HTTPException(
            status_code=500, 
            detail=detailed_message
        )
