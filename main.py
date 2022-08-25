from sqlalchemy.exc import PendingRollbackError

from config import create_app
from db import db

app = create_app()


@app.after_request
def return_resp(resp):
    try:
        db.session.commit()
    except PendingRollbackError:
        db.session.rollback()
    return resp


if __name__ == "__main__":
    app.run()
