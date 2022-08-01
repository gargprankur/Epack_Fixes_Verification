import paramiko
from UcodeFixes import UcodeFixes

user_name = "root"
password = "dangerous"
host_ip = "10.60.153.151"

class HostConnectivity:
    def __init__(self, host_ip, username, password, sid):
        self._host_ip = host_ip
        self._username = username
        self._password = password
        self._sid = sid

    def host_connect(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(hostname = self._host_ip, username = self._username, password = self._password)
        print('/usr/symcli/bin/symcfg list -upatches -sid {self._sid} -output xml')
        stdin, stdout, stderr = ssh_client.exec_command(f'/usr/symcli/bin/symcfg list -upatches -sid {self._sid} -output xml')
        with open('ucode_fixes', 'w') as f1:
            for line in stdout.readlines():
                f1.write(line)


    def get_symm_fixes(self):
        self.host_connect()
        ucode_fixes = UcodeFixes('ucode_fixes')
        fix_set = ucode_fixes.fixes
        return fix_set





