import threading
from Camera import Camera
from FlaskServer import FlaskServer

camera = Camera()
flaskServer = FlaskServer(camera)


def greet_user():
    print("Hello! Welcome to the program.")


def display_menu():
    print("Please choose one of the following options:")
    print("1. Take a photo")
    print("2. Start Server")
    print("3. Option 3")
    print("4. Option 4")
    print("5. Option 5")


def handle_option(option):
    if option == 1:
        camera.take_photo()
    elif option == 2:
        flask_thread = threading.Thread(target=flaskServer.start)
        flask_thread.start()
        print("Flask server started on a separate thread.")
    elif option == 3:
        print("You selected Option 3.")
    elif option == 4:
        print("You selected Option 4.")
    elif option == 5:
        print("You selected Option 5.")
    else:
        print("Invalid option. Please choose a valid option.")


def main():
    greet_user()
    display_menu()

    while True:
        try:
            option = int(input("Enter your choice (1-5): "))
            handle_option(option)
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
