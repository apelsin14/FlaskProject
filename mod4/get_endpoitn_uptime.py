
from typing import Optional
from flask import request
import uptime
from flask import Flask

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
