import json
from typing import Dict

from .models import BarrierModel


class BarrierSerializer:
    @classmethod
    def to_dict(cls, barrier_obj: BarrierModel) -> Dict:
        dict_: Dict = {
            "state": barrier_obj.state,
            "last_modify": barrier_obj.last_modify,
        }
        return dict_

    @classmethod
    def to_json(cls, barrier_obj: BarrierModel) -> str:
        dict_ = cls.to_dict(barrier_obj)
        return json.dumps(dict_)
