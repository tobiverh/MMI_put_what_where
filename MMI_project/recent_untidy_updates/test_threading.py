from threading import Thread

def infinity_loop() -> None:
    while True:
        continue

def print_stuff() -> None:
    print("stuff")
    
infinity_thread = Thread(target=infinity_loop)
infinity_thread.daemon = True
print_thread = Thread(target=print_stuff)

infinity_thread.start()
print_thread.start()
