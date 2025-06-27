from fastapi import APIRouter, Depends, HTTPException, Request, Header
import httpx 
from app import models
from app.dependencies import get_current_user

router = APIRouter(prefix="/canvas", tags=["canvas"])

CANVAS_API_BASE = "http://172.23.148.229/api/v1"

def translate(value: str, category: str) -> str:
    translations = {
        "enrollment_state": {
            "active": "Активный",
            "invited": "Ожидает подтверждения",
            "creation_pending": "Ожидает создания",
            "completed": "Завершён",
            "concluded": "Завершён",
        },
        "type": {
            "StudentEnrollment": "Студент",
            "TeacherEnrollment": "Преподаватель",
        },
        "role": {
            "StudentEnrollment": "Студент",
            "TeacherEnrollment": "Преподаватель",
        }
    }
    return translations.get(category, {}).get(value, value)

@router.get("/enrollments")
async def get_user_enrollments(
    canvas_token: str = Header(default=None, alias="X-Canvas-Token"),
):
    if not canvas_token:
        raise HTTPException(status_code=401, detail="Canvas token not provided")

    try:
        async with httpx.AsyncClient() as client:
            # Проверка: админ или нет
            is_admin = False
            admin_resp = await client.get(
                f"{CANVAS_API_BASE}/accounts/self/admins/self",
                headers={"Authorization": canvas_token}
            )
            if admin_resp.status_code == 200:
                admin_data = admin_resp.json()
                is_admin = any(admin.get("role") == "AccountAdmin" for admin in admin_data)

            result = []

            if is_admin:
                # 🧑‍🏫 Получаем ВСЕ курсы, в которых пользователь преподаватель
                courses_resp = await client.get(
                    f"{CANVAS_API_BASE}/courses",
                    headers={"Authorization": canvas_token},
                    params={
                        "enrollment_type": "teacher",
                        "include[]": "total_students"
                    }
                )
                courses_resp.raise_for_status()
                courses = courses_resp.json()

                for course in courses:
                    result.append({
                        "course_id": course.get("id"),
                        "course_name": course.get("name"),
                        "course_code": course.get("course_code"),
                        "enrollment_state": "Активный" if course.get("workflow_state") == "available" else "Ожидает публикации",
                        "enrollment_type": "Преподаватель",
                        "workflow_state": course.get("workflow_state"),
                        "role": "Преподаватель",
                    })
            
            else:
                # 👤 Обычный пользователь — получаем только его enrollment-ы
                enrollments_resp = await client.get(
                    f"{CANVAS_API_BASE}/users/self/enrollments",
                    headers={"Authorization": canvas_token},
                    params={"enrollment_state[]": ["current_and_invited"]}
                )
                enrollments_resp.raise_for_status()
                enrollments = enrollments_resp.json()

                for enr in enrollments:
                    course_id = enr.get("course_id")

                    # Получаем инфу о курсе
                    course_resp = await client.get(
                        f"{CANVAS_API_BASE}/courses/{course_id}",
                        headers={"Authorization": canvas_token}
                    )
                    if course_resp.status_code != 200:
                        continue
                    course = course_resp.json()

                    progress_percent = None
                    try:
                        progress_resp = await client.get(
                            f"{CANVAS_API_BASE}/courses/{course_id}/users/self/progress",
                            headers={"Authorization": canvas_token}
                        )
                        if progress_resp.status_code == 200:
                            progress = progress_resp.json()
                            total = progress.get("requirement_count", 0)
                            completed = progress.get("requirement_completed_count", 0)
                            if total > 0:
                                progress_percent = round(completed / total * 100)
                    except httpx.HTTPStatusError:
                        pass  # silently ignore if no progress

                    result.append({
                    "course_id": course_id,
                    "enrollment_id": enr.get("id"),  # 👈 обязательно
                    "course_name": course.get("name"),
                    "course_code": course.get("course_code"),
                    "enrollment_state": translate(enr.get("enrollment_state"), "enrollment_state"),
                    "enrollment_type": translate(enr.get("type"), "type"),
                    "workflow_state": course.get("workflow_state"),
                    "role": translate(enr.get("role"), "role"),
                    "progress_percent": progress_percent,
                })


            return {
                "courses": result,
                "is_admin": is_admin
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    


@router.post("/courses/{course_id}/enrollments/{enrollment_id}/accept")
async def accept_invitation(
    course_id: int,
    enrollment_id: int,
    canvas_token: str = Header(default=None, alias="X-Canvas-Token"),
):
    
    if not canvas_token:
        raise HTTPException(status_code=401, detail="Canvas token not provided")
    
    if not canvas_token.startswith("Bearer "):
        canvas_token = f"Bearer {canvas_token}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{CANVAS_API_BASE}/courses/{course_id}/enrollments/{enrollment_id}/accept",
            headers={"Authorization": canvas_token}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()


@router.post("/courses/{course_id}/enrollments/{enrollment_id}/reject")
async def reject_invitation(
    course_id: int,
    enrollment_id: int,
    canvas_token: str = Header(default=None, alias="X-Canvas-Token"),
):
    if not canvas_token:
        raise HTTPException(status_code=401, detail="Canvas token not provided")
    
    if not canvas_token.startswith("Bearer "):
        canvas_token = f"Bearer {canvas_token}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{CANVAS_API_BASE}/courses/{course_id}/enrollments/{enrollment_id}/reject",
            headers={"Authorization": canvas_token}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

@router.get("/courses/{course_id}/students")
async def get_students_with_activity(
    course_id: int,
    canvas_token: str = Header(alias="X-Canvas-Token", default=None),
):
    if not canvas_token.startswith("Bearer "):
        canvas_token = f"Bearer {canvas_token}"

    async with httpx.AsyncClient() as client:
        enrollments_resp = await client.get(
            f"{CANVAS_API_BASE}/courses/{course_id}/enrollments",
            headers={"Authorization": canvas_token},
            params={"type[]": "StudentEnrollment"}
        )
        enrollments_resp.raise_for_status()
        enrollments = enrollments_resp.json()

        students = []
        for enr in enrollments:
            user_id = enr["user_id"]
            user_resp = await client.get(
                f"{CANVAS_API_BASE}/users/{user_id}",
                headers={"Authorization": canvas_token}
            )
            user_data = user_resp.json()

            students.append({
                "id": user_data["id"],
                "name": user_data["name"],
                "email": user_data["email"],
                "enrollment_state": enr.get("enrollment_state"),
                "registered_at": enr.get("created_at"),
                "last_login": user_data.get("last_login"),
            })

        return {"students": students}
