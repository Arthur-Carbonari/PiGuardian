import threading

from flask_server.flask_server import FlaskServer
from pi_guardian.pi_guardian import PiGuardian

piGuardian = PiGuardian()
flaskServer = FlaskServer(piGuardian)


def main():
    flask_thread = threading.Thread(target=flaskServer.start)
    flask_thread.start()


if __name__ == "__main__":
    main()
