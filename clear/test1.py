
import time


class A(object):

    def __init__(self):
        self.glo = False

    def aa(self):
        # while True:
        print(self.glo)
            # time.sleep(2)


    def bb(self):
        if self.glo:
            self.glo = False
        else:
            self.glo = True


if __name__ == "__main__":
    a = A()
    while True:

        a.aa()
        a.bb()
        time.sleep(2)