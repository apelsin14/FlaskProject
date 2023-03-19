
from typing import Optional
import uptime
from flask import Flask, request

app = Flask(__name__)


@app.route(
    "/uptiime/", methods=["GET"]
)
def search():
    time = str(uptime.uptime())

    UPTIME: Optional[float] = request.args.get(time, type=float, default=None)


    return (
        f"Current uptime is {UPTIME}"
    )


if __name__ == "__main__":
    app.run(debug=True)
