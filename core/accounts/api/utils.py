import threading

class EmailThread(threading.Thread):
    def __init__(self, emial_obj):
        threading.Thread.__init__(self)
        self.email_obj = emial_obj

    def run(self):
        self.email_obj.send()