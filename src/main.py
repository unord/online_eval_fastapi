from fastapi import FastAPI
from pydantic import BaseModel
from . import tools, unord_mail
app = FastAPI()


class CloseEvalAndSendCsv(BaseModel):
    username: str
    password: str
    refrence: str
    teacher_initials: str

class TestPayload(BaseModel):
    test_data: str

@app.get("/close_eval_and_send_mail/{username, password, refrence, teacher_initials}")
def close_eval_and_send_mail(username: str, password: str, refrence: str, teacher_initials: str) -> dict:
    tools.close_eval_and_send_mail(username, password, refrence, teacher_initials)
    return {'msg': 'success', 'success': True}

@app.post("/close_eval_and_send_mail/")
def close_eval_and_send_mail(close_eval_and_send_csv: CloseEvalAndSendCsv) -> dict:
    msg = tools.close_eval_and_send_mail(close_eval_and_send_csv.username,close_eval_and_send_csv.password, close_eval_and_send_csv.refrence, close_eval_and_send_csv.teacher_initials)
    print(f"msg: {msg}")
    if msg['success']:
        return {'msg': 'success', 'success': True, 'public_link': msg['public_link'], 'responses': msg['responses']}
    else:
        unord_mail.send_email_with_attachments('ubot@unord.dk', ['gore@unord.dk'], 'Online-Eval-FastApi Error', str(msg), [], [], [])
        return {'msg': 'failed', 'success': False}


@app.post("/test_endpoint/")
def test_endpoint(payload: TestPayload) -> dict:
    """Echoes back the received payload."""
    return {"received_data": payload.test_data}


def main():
    pass


if __name__ == "__main__":
    main()
