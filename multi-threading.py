# ****************************************************
# Python threading tutorial
# ****************************************************
# thread =  a flow of execution. Like a separate order of instructions.
#                  However, each thread takes a turn running to achieve concurrency
#                  GIL = (global interpreter lock),
#                  allows only one thread to hold the control of the Python interpreter at any one time

# cpu bound = program/task spends most of it's time waiting for internal events (CPU intensive)
#             use multiprocessing

# io bound = program/task spends most of it's time waiting for external events (user input, web scraping)
#            use multithreading

import threading
import time


def eat_breakfast(name):
    time.sleep(3)
    print(f"{name} eat breakfast")


def drink_coffee(name):
    time.sleep(4)
    print(f"{name} drank coffee")


def study(name):
    time.sleep(5)
    print(f"{name} finish studying")

name = "John"

# Create 3 thread for each task
x = threading.Thread(target=eat_breakfast, args=(name,))
x.start()

y = threading.Thread(target=drink_coffee, args=(name,))
y.start()

z = threading.Thread(target=study, args=(name,))
z.start()

# Comment these out to show 4 threads below, the main thread will print the active_count and enumerate before the threads are completed
# join is a blocking call (thread synchronization)
x.join()
y.join()
z.join()

print(threading.active_count())  # Shows how man thread is running
print(threading.enumerate())  # Shows the list of all the thread
print(time.perf_counter())  # How long does it take for the main thread to finish the set of instructions

# ****************************************************
