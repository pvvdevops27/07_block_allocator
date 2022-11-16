from flask import Flask
from functions import *
import datetime
import os


app = Flask(__name__)


@app.route("/")
def main():
    try:
        now = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")

        massive_email_sender("1Jmm-7jZuABj__t0uRv98esMwXks7XPpJu30q47qMul8", "Input")

        return f"Block allocator succesfully executed on {now}"

    except:
        return "No valid request found"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8087)))
