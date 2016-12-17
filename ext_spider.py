import requests
import time


class SimpleScrawl:

    def __init__(self, url):
        self.target_url = url
        self.crawl_interval = 0.5

    def crawl(self):
        try:
            while True:
                print requests.get(self.target_url, timeout=3)
                time.sleep(self.crawl_interval)
        except requests.exceptions.ConnectionError:
            print '[WARNING] ConnectError, the spider maybe has been banned! '
        except requests.exceptions.Timeout:
            print '[WARNING] Timeout, the spider has been banned! '


class PortScanner:

    def __init__(self, ip, fport, eport):
        self.ip = ip
        self.fport = fport
        self.eport = eport
        self.uri_template = 'http://%s:%s/'
        self.scan_interval = 0.5

    def scan(self):
        ip = self.ip
        port = self.fport
        while port <= self.eport:
            try:
                requests.get(self.uri_template % (ip, port), timeout=3)
                print 'ip %s : port %s is reachable' % (ip, port)
            except requests.exceptions.Timeout:
                print '[WARNING] Timeout, ip %s : port %s is unreachable!' % (ip, port)
            except requests.exceptions.ConnectionError:
                print 'ip %s : port %s is reachable' % (ip, port)
            time.sleep(self.scan_interval)
            port += 1


if __name__ == '__main__':
    scrawl = SimpleScrawl('http://100.64.132.73:8000/iwantrent/getAllProduct/')
    scrawl.crawl()
    #port_scanner = PortScanner('100.64.132.73', 7990, 8010)
    #port_scanner.scan()
