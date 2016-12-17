# coding=utf-8
import re
from models import LogItem


class MessageHandler:

    def __init__(self, logfile):
        self.states = (
            'DROP STATE INVALID',
            'ACCEPT Internal 8000',
            'ACCEPT External 8000',
            'ACCEPT White Loopback',
            'ACCEPT White Host',
            'DROP External Request',
            'DROP Black Host')
        self.log_items = []
        with open(logfile, 'r') as fp:
            raw_data = fp.readlines()
        for item in raw_data:
            item = item.strip()
            try:
                if re.findall('\[.*?\]', item)[1]:
                    datetime = ' '.join(item.split()[:3])
                    timestamp = float(re.findall('\[.*?\]', item)[0][3:-1])
                    prefix = re.findall('\[.*?\]', item)[1][1:-1]
                    IN = re.findall('IN=.*? ', item)[0].strip()
                    OUT = re.findall('OUT=.*?', item)[0].strip()
                    MAC = re.findall('MAC=.*? ', item)[0].strip().split('=')[1]
                    SRC = re.findall('SRC=.*? ', item)[0].strip().split('=')[1]
                    DST = re.findall('DST=.*? ', item)[0].strip().split('=')[1]
                    PROTO = re.findall('PROTO=.*? ', item)[0].strip().split('=')[1]
                    SPT = re.findall('SPT=.*? ', item)[0].strip().split('=')[1]
                    DPT = re.findall('DPT=.*? ', item)[0].strip().split('=')[1]
                    log = LogItem(datetime, timestamp, prefix, IN, OUT, MAC, SRC, DST, PROTO, SPT, DPT)
                    self.log_items.append(log)
            except IndexError:
                pass

    def get_external_request_ip(self):
        external_ip_list = []
        for log in self.log_items:
            if log.prefix == self.states[2]:
                external_ip_list.append(log.SRC)
        return list(set(external_ip_list))

    def ip_filter(self, ip):
        ip_request_list = []
        for log in self.log_items:
            if log.prefix == self.states[2] and log.SRC == ip:
                ip_request_list.append(log)
        return ip_request_list

    def get_external_log_dict(self):
        external_ip_list = self.get_external_request_ip()
        log_dict = {}
        for external_ip in external_ip_list:
            log_dict[external_ip] = {}
            ip_log_list = self.ip_filter(external_ip)
            log_dict[external_ip]['logs'] = ip_log_list
            log_dict[external_ip]['num'] = len(ip_log_list)
        return log_dict

    def get_dropped_log_dict(self):
        dropped_log_dict = {}
        for log in self.log_items:
            if log.prefix == self.states[5]:
                dropped_log_dict[log.SRC] = dropped_log_dict.get(log.SRC, [])
                dropped_log_dict[log.SRC].append(log.DPT)
        for ip in dropped_log_dict:
            dropped_log_dict[ip] = set(dropped_log_dict[ip])
        return dropped_log_dict


if __name__ == '__main__':
    message_handler = MessageHandler('/var/log/messages')
    logs = message_handler.log_items
    print 'timestamp\t\toperation\t\tsrc\t\t\tdst'
    for log in logs:
        print '[%s]\t[%s]\t[%s]\t[%s]' % (log.timestamp, log.prefix, log.SRC, log.DST)
    print
    print 'request ip set from external: '
    external_request_ip = message_handler.get_external_request_ip()
    print external_request_ip
    print
    target_ip = external_request_ip[0]
    print 'ip %s request log as following: ' % target_ip
    print 'timestamp\t\toperation\t\tsrc\t\t\tdst'
    for log in message_handler.ip_filter(target_ip):
        print '[%s]\t[%s]\t[%s]\t[%s]' % (log.timestamp, log.prefix, log.SRC, log.DST)
    print
    print 'external log dict as following: '
    print message_handler.get_external_log_dict()
    print
    print 'drop packets: '
    print message_handler.get_dropped_log_dict()
    print
