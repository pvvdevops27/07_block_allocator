from flask import Flask
from functions import *
import os


app = Flask(__name__)


@app.route("/")
def main():

    block_allocator()

    return "Block allocator is ready for requests..."


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
