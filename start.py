from flask import Flask
from flask_cors import CORS

from data_storage import load_data_from_dataset

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] [%(threadName)s] : %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

load_data_from_dataset()

from strateges_container.routes import exicuter_endpoint
app.register_blueprint(exicuter_endpoint)



app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)