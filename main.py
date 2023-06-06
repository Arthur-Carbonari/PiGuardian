import threading

from flask_server.flask_server import FlaskServer
from pi_guardian.pi_guardian import PiGuardian

pi_guardian = PiGuardian()
flask_server = FlaskServer(pi_guardian)


def main():
    flask_thread = threading.Thread(target=flask_server.start)
    flask_thread.start()


if __name__ == "__main__":
    main()
