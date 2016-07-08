from bt_text import app
import os

PORT = int(os.environ.get('FLASK_PORT', 80))


if __name__ == '__main__':
    app.debug = True
    print("Listening on port {}".format(PORT))
    app.run(host='0.0.0.0', port=PORT)
