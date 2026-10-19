import time

def task(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} completed")


task("A")
task("B")