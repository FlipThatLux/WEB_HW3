from threading import Thread
import logging



class MyThread(Thread):
    # def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
    #     super().__init__(group=group, target=target, name=name, daemon=daemon)
    #     self.args = args
    #     self.kwargs = kwargs

    def run(self, function, path, reference_path) -> None:
        function(path, reference_path)
        logging.warning('This thread is doing something')