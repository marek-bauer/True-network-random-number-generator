import math
import time
import socket
import queue
import random
import threading

TIMER_RESOLUTION_IN_NS = 100  # rozdzielczość czasu#|\label{line:time_res}#|
MOST_SIGNIFICANT_BITS_TO_REJECT = 13  # liczba bitów do odrzucenia #|\label{line:bits_reject}#|


def ping(address):  #|\label{line:ping}#|
    """Procedura nawiązująca i zrywająca połączenie"""
    s = socket.socket()
    s.connect((address, 80))
    s.shutdown(socket.SHUT_RD)


def load_file(file_name):  #|\label{line:loadfile}#|
    """Funkcja wczytująca dane z pliku i zapisująca je do listy"""
    res = []
    f = open(file_name, "r")
    for x in f:
        res.append(x[0:-1])
    f.close()
    return res


def elapsed(fn):  #|\label{line:elapsed}#|
    """Funkcja zwracająca czas potrzebny na wywołanie funkcji fn"""
    start = time.perf_counter_ns()
    fn()
    stop = time.perf_counter_ns()
    return (stop - start) // TIMER_RESOLUTION_IN_NS


class Pinger(threading.Thread):  #|\label{line:pinger}#|
    """Klasa wątku odpytującego kolejne adressy z listy"""

    def __init__(self, output, addresses):
        threading.Thread.__init__(self)
        self._output = output
        self._addresses = addresses
        self._index = random.randint(0, len(addresses))
        self._stop_event = threading.Event()

    def run(self):  #|\label{line:run}#|
        """Procedura generująca bity"""
        while not self._stop_event.is_set():
            try:
                eclipsed = elapsed(lambda: ping(self._addresses[self._index]))
                length = math.ceil(math.log2(eclipsed))
                for _ in range(length - MOST_SIGNIFICANT_BITS_TO_REJECT):
                    self._output.put(eclipsed % 2)
                    eclipsed //= 2
            except:
                print("Connection error with " + self._addresses[self._index])
            finally:
                self._index = (self._index + 1) % len(self._addresses)

    def stop(self):  #|\label{line:pinger_stop}#|
        """Procedura zatrzymująca wątek"""
        self._stop_event.set()


class Generator:  #|\label{line:generator}#|
    """Klasa generatora przyjmująca liczbę wątków"""

    def __init__(self, threads):
        self._queue = queue.Queue()
        addresses = load_file("addresses")
        self._threads = []
        for _ in range(threads):
            thread = Pinger(self._queue, addresses)
            thread.start()
            self._threads.append(thread)

    def get(self):  #|\label{line:get}#|
        """Funkcja zwracająca 64-bitową liczbę losową"""
        result = 0
        for _ in range(64):
            bit = self._queue.get()
            if bit == 0:
                result = result * 2
            else:
                result = result * 2 + 1
        return result

    def stop(self):  #|\label{line:generator_stop}#|
        """Funkcja zatrzymująca generator"""
        for thread in self._threads:
            thread.stop()
