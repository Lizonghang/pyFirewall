import os
import time
from datetime import datetime
from scrawl_detector import ScrawlDetector
from port_scan_detector import PortScanDetector
from setting_handler import SettingHandler


class DynamicFirewall:

    def __init__(self):
        self.white_list = ['100.64.132.72']
        os.system('echo "" > /var/log/messages')

    def scrawl_scanner(self):
        while True:
            self.spider_scanner_handler()
            self.port_scanner_handler()
            os.system('echo "" > /var/log/messages')
            time.sleep(20)

    def spider_scanner_handler(self):
        scrawl_detector = ScrawlDetector()
        scrawl_list = scrawl_detector.detect_scrawl()
        if scrawl_list:
            print 'Detect at %s, scrawl list: %s' % (datetime.now(), scrawl_list)
            ban_list = self.white_filter(scrawl_list)
            print 'ip %s has been banned' % self.scrawl_banner(ban_list)
        else:
            print 'No scrawl detected.'
        del scrawl_detector

    def port_scanner_handler(self):
        port_scan_detector = PortScanDetector()
        ip_scanner = port_scan_detector.detect_scanner()
        if ip_scanner:
            print 'Detect at %s, scanner list: %s' % (datetime.now(), ip_scanner)
            print 'ip %s has been banned' % self.scrawl_banner(ip_scanner)
        else:
            print 'No scanner detected.'
        del port_scan_detector

    def white_filter(self, scrawl_list):
        for ip in self.white_list:
            try:
                scrawl_list.remove(ip)
                print 'Detect scrawl from white list %s, pass' % ip
            except ValueError:
                pass
        return scrawl_list

    def scrawl_banner(self, ban_list):
        setting_handler = SettingHandler('/home/parallels/Desktop/mSetting.sh')
        setting_handler.insert_ip_banner(ban_list)
        return ban_list


if __name__ == '__main__':
    dynamic_firewall = DynamicFirewall()
    dynamic_firewall.scrawl_scanner()
