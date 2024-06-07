import os
from polygon.app import app


def main():
    # if production mode is on
    if os.getenv("FLASK_ENV") == "production":
        # run the app gunicorn
        app.run(host="0.0.0.0", port=5001, debug=False)
    else:
        # run the app flask
        app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
