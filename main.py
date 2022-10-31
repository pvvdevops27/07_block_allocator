from flask import Flask
from functions import *
import datetime
import os


app = Flask(__name__)


@app.route("/block_allocator")
def main():

    now = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")

    block_allocator()

    return f"Block allocator succesfully executed on {now}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
