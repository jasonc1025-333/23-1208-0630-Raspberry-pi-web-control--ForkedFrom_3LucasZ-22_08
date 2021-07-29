import time
import threading

def printSquares():
    for i in range(10):
        print(i * i)
        time.sleep(0.5)

def printCubes():
    for i in range(10):
        print(i * i * i)
        time.sleep(0.8)

def intermediary():
    for i in range(10):

t1 = threading.Thread(target=printSquares)
t2 = threading.Thread(target=printCubes)

if __name__ == '__main__':
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("DONE!")