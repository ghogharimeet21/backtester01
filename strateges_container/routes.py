import logging
from time import time
from flask import Blueprint, request, jsonify

from strateges_container.strategy_exicuter import sample_strategy





logger = logging.getLogger(__name__)
exicuter_endpoint = Blueprint("strategy_exicuter", __name__, url_prefix="/strategy_exicuter")







@exicuter_endpoint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "success", "message": "Engine is running"})


@exicuter_endpoint.route("/sample_strategy", methods=["POST"])
def sample_strategy_f():
    try:
        start_time = time()
        strategy = sample_strategy.Sample_strategy(request.json)
        sample_strategy.start_exicution(strategy)
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Backtest is completed",
                    "data": "report",
                    "time_taken": time() - start_time,
                }
            ),
            200,)
    
    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)}), 500
    


















