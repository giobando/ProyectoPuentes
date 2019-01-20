# -*- coding: utf-8 -*-

#!/usr/bin/python
# take from: https://magmax.org/blog/patterns-observer/

from threading import Thread
import time

class Observable(object):
    def __init__(self):
        self._observers = set()

    def add_observer(self, observer):
        self._observers.add(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(self, event)


class Observer(object):
    def update(self, observable, event):
        raise NotImplemented('This method is Abstract!')


class MyObservable(Thread, Observable):
    def __init__(self, *args, **kargs):
        Thread.__init__(self, *args, **kargs)
        Observable.__init__(self, *args, **kargs)
        self._finish = False

    def run(self):
        while not self._finish:
            self.fire_event()
            time.sleep(0.5)

    def fire_event(self):
        self.notify_observers("Ey! What's up?")

    def stop(self):
        self._finish = True


class MyObserver(Observer):
    def update(self, observable, event):
        print "Something happened!"


def main():
    myobservable = MyObservable()
    myobserver = MyObserver()

    myobservable.add_observer(myobserver)

    myobservable.start()

    time.sleep(2)
    myobservable.stop()

    print("Finishing!")

if __name__ == '__main__':
    main()