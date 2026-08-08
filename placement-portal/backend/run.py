
import os

from flask import send_from_directory

from app import create_app


app = create_app()


# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = app.config.get("UPLOAD_FOLDER")

print("UPLOAD FOLDER:", UPLOAD_FOLDER)


# =========================================================
# SERVE UPLOADED FILES
# =========================================================

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
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

