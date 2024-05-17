# *********************************
# Python multiprocessing
# *********************************
# multiprocessing = running tasks in parallel on different cpu cores, bypasses GIL used for threading
#                   multiprocessing = better for cpu bound tasks (heavy cpu usage)
#                   multithreading = better for io bound tasks (waiting around)

from multiprocessing import Process, cpu_count
import time


def counter(num):
    count = 0
    while count < num:
        count += 1


def main():
    # Get the number of additional processes that you can run
    # If you run more processes allowed than cpu_count, the program will be slower instead due to the additional overhead needed create and destroy the process
    print("cpu count:", cpu_count())

    # 1 Process count to 1 Billion, will take a long time to finish, program will take long time to complete
    # a = Process(target=counter, args=(1_000_000_000,))

    # Divided the task to 2 different processes, each count 500 Million, program will take shorter to complete
    a = Process(target=counter, args=(500_000_000,))
    b = Process(target=counter, args=(500_000_000,))

    a.start()
    b.start()

    print("processing...")

    # Process synchronization
    a.join()
    b.join()

    print("Done!")
    print("finished in:", time.perf_counter(), "seconds")


main()

# *********************************
