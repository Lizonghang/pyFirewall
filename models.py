class LogItem:

    def __init__(self, datetime, timestamp, prefix, IN, OUT, MAC, SRC, DST, PROTO, SPT, DPT):
        self.datetime = datetime
        self.timestamp = timestamp
        self.prefix = prefix
        self.IN = IN
        self.OUT = OUT
        self.MAC = MAC
        self.SRC = SRC
        self.DST = DST
        self.PROTO = PROTO
        self.SPT = SPT
        self.DPT = DPT
