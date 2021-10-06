from .models import BarrierModel


def populate_barrier(db) -> None:
    if not BarrierModel.query.get(1):
        barrier_obj = BarrierModel()
        db.session.add(barrier_obj)
        db.session.commit()
