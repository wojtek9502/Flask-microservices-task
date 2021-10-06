from .db import db
from datetime import datetime


class BarrierModel(db.Model):
    __tablename__ = "Barrier"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer, default=0, nullable=False)  # 0 - closed, 1 - open
    last_modify = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(),
    )

    def __str__(self):
        state = "OPEN" if self.state else "CLOSED"
        return f"Barrier{self.id}, state: {state}, last modify: {self.last_modify}"
