from datetime import datetime

from flask import Blueprint, jsonify

from .models import BarrierModel
from .serializers import BarrierSerializer
from .db import db

gateman_blueprint = Blueprint("gateman_blueprint", __name__)


@gateman_blueprint.route("/gateman/barrier", methods=["GET"])
def get_barrier_status():
    barrier_obj: BarrierModel = BarrierModel.query.get(1)
    barrier_obj_dict = BarrierSerializer.to_dict(barrier_obj)
    return jsonify(barrier_obj_dict), 200


@gateman_blueprint.route("/gateman/barrier/open", methods=["PUT"])
def open_barrier():
    barrier_obj: BarrierModel = BarrierModel.query.get(1)

    barrier_obj.state = 1
    barrier_obj.last_modify = datetime.now()

    db.session.commit()

    barrier_obj_dict = BarrierSerializer.to_dict(barrier_obj)
    return jsonify(barrier_obj_dict), 200


@gateman_blueprint.route("/gateman/barrier/close", methods=["PUT"])
def close_barrier():
    barrier_obj: BarrierModel = BarrierModel.query.get(1)

    barrier_obj.state = 0
    barrier_obj.last_modify = datetime.now()

    db.session.commit()

    barrier_obj_dict = BarrierSerializer.to_dict(barrier_obj)
    return jsonify(barrier_obj_dict), 200
