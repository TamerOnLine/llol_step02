# main/run.py

from main import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # Use "127.0.0.1" to run locally only
        port=40514,       # Change this port if needed
        debug=True        # Set to False in production
    )
