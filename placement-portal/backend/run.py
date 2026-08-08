
from flask import send_from_directory
import os

from app import create_app

app = create_app()


# =========================================================
# SERVE UPLOADED FILES
# =========================================================

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )

