from todolist.scripts.menu import menu

def runapp():
    running = True
    while running:
        running = menu()

if __name__ == "__main__":
    runapp()
