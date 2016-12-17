import os


class SettingHandler:

    def __init__(self, setting_file):
        self.setting_file = setting_file
        f = open(self.setting_file, 'r')
        self.settings = f.readlines()
        f.close()
        self.blocks = self.get_blocks()

    def get_blocks(self):
        block = {}
        for i in range(len(self.settings)):
            if self.settings[i][:3] == '###':
                block_name = self.settings[i].replace('### ', '').strip()
                block[block_name] = i + 1
        return block

    def insert_ip_banner(self, ip_list):
        insert_index = self.blocks['DROP External Host in Black List']
        rule_template1 = 'iptables -A INPUT -i eth1 -s %s -j LOG --log-prefix "[DROP Black Host]"\n'
        rule_template2 = 'iptables -A INPUT -i eth1 -s %s -j DROP\n'
        for ip in ip_list:
            if rule_template2 % ip not in self.settings:
                self.settings.insert(insert_index, rule_template2 % ip)
                self.settings.insert(insert_index, rule_template1 % ip)
        self.blocks = self.get_blocks()
        f = open(self.setting_file, 'w')
        f.writelines(self.settings)
        f.close()
        os.system('/home/parallels/Desktop/mSetting.sh')

    def remove_ip_banner(self, ip_list):
        rule_template1 = 'iptables -A INPUT -i eth1 -s %s -j LOG --log-prefix "[DROP Black Host]"\n'
        rule_template2 = 'iptables -A INPUT -i eth1 -s %s -j DROP\n'
        for ip in ip_list:
            try:
                self.settings.remove(rule_template1 % ip)
                self.settings.remove(rule_template2 % ip)
            except ValueError:
                pass
        self.blocks = self.get_blocks()
        f = open(self.setting_file, 'w')
        f.writelines(self.settings)
        f.close()
        os.system('/home/parallels/Desktop/mSetting.sh')


if __name__ == '__main__':
    setting_handler = SettingHandler('/home/parallels/Desktop/mSetting.sh')
    setting_handler.insert_ip_banner(['100.64.132.198', '100.64.132.199', '100.64.132.200'])
    setting_handler.remove_ip_banner(['100.64.132.198', '100.64.132.199'])
