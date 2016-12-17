from message_handler import MessageHandler


class PortScanDetector:
    def __init__(self):
        self.message_handler = MessageHandler('/var/log/messages')
        self.dropped_dict = self.message_handler.get_dropped_log_dict()

    def detect_scanner(self):
        ip_scanner = []
        for dropped_ip in self.dropped_dict:
            request_ports = [int(port) for port in self.dropped_dict[dropped_ip]]
            for i in range(len(request_ports)):
                if (request_ports[i] + 1 in request_ports and request_ports[i] + 2 in request_ports) or \
                        (request_ports[i] - 1 in request_ports and request_ports[i] - 2 in request_ports):
                    ip_scanner.append(dropped_ip)
                    break
        return ip_scanner


if __name__ == '__main__':
    port_scanner = PortScanDetector()
    port_scanner.detect_scanner()
