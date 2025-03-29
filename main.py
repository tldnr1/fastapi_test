from fastapi import FastAPI, BackgroundTasks
import asyncio
import uuid

app = FastAPI()

# 메모리 상태 저장소 (실제 서비스는 Redis 추천)
TASKS = {}

# 모의 응답 생성기
async def generate_response(task_id: str, user_input: str):
    await asyncio.sleep(10)  # 긴 처리 시간 시뮬레이션
    TASKS[task_id]["status"] = "done"
    TASKS[task_id]["result"] = f"{user_input}에 대한 날씨는 맑음입니다. 특별한 이슈는 없습니다."

@app.post("/ask")
async def ask_question(user_input: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    print(f"New task_id: {task_id}")
    TASKS[task_id] = {"status": "processing", "result": None}
    background_tasks.add_task(generate_response, task_id, user_input)
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "응답을 생성 중입니다. 결과는 /check/{task_id} 에서 확인하세요."
    }

@app.get("/check/{task_id}")
async def check_status(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        return {"error": "Invalid task ID"}
    return task
