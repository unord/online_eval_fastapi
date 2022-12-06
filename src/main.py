from fastapi import FastAPI
from pydantic import BaseModel
from . import tools
app = FastAPI()


class CloseEvalAndSendCsv(BaseModel):
    username: str
    password: str
    refrence: str
    teacher_initials: str


@app.get("/close_eval_and_send_csv/{username, password, refrence, teacher_initials}")
def close_eval_and_send_csv(username: str, password: str, refrence: str, teacher_initials: str) -> dict:
    tools.close_eval_and_send_csv(username, password, refrence, teacher_initials)
    return {'msg': 'success', 'success': True}

@app.post("/close_eval_and_send_csv/{username, password, refrence, teacher_initials}")
def close_eval_and_send_csv(username: str, password: str, refrence: str, teacher_initials: str) -> dict:
    tools.close_eval_and_send_csv(username, password, refrence, teacher_initials)
    return {'msg': 'success', 'success': True}
def main():
    pass


if __name__ == "__main__":
    main()
