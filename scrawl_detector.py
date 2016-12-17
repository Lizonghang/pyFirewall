from message_handler import MessageHandler


class ScrawlDetector:

    def __init__(self):
        self.message_handler = MessageHandler('/var/log/messages')
        self.log_dict = self.message_handler.get_external_log_dict()

    def parse_log_dict(self):
        for ip in self.log_dict:
            print 'ip %s log info as following: ' % ip
            print 'timestamp\t\toperation\t\tsrc\t\t\tdst'
            for log in self.log_dict[ip]['logs']:
                print '[%s]\t[%s]\t[%s]\t[%s]' % (log.timestamp, log.prefix, log.SRC, log.DST)
            print

    def detect_scrawl(self):
        scrawler_ip_list = []
        despire_sample_interval = 15
        despire_time_interval = 15
        for target_ip in self.log_dict:
            num = self.log_dict[target_ip]['num']
            target_ip_log_list = self.log_dict[target_ip]['logs']
            # print 'processing ip %s ...' % target_ip
            # print 'ip %s has %s log info' % (target_ip, num)
            for i in range(num-despire_sample_interval):
                time_interval = target_ip_log_list[i+despire_sample_interval].timestamp - target_ip_log_list[i].timestamp
                if time_interval < despire_time_interval:
                    # print '[WARNING] ip %s requests %s times in %s seconds!' % (target_ip, despire_sample_interval, time_interval)
                    # print '[WARNING] ip %s is crawler!' % target_ip
                    scrawler_ip_list.append(target_ip)
                    break
            # print
        return scrawler_ip_list


if __name__ == '__main__':
    scrawl_detector = ScrawlDetector()
    # scrawl_detector.parse_log_dict()
    print scrawl_detector.detect_scrawl()
