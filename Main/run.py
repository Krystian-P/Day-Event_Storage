from app import app
import os


# Run Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=os.getenv("PORT") or 5000)
