import psutil
import libvirt
import sys


# cpu信息
def get_cpu_info():
    cpu_percent = 10
    while cpu_percent < 20:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_info = "CPU使用率：%i%%" % cpu_percent
        print(cpu_info)
    return cpu_percent


domName = 'labV1'
conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

dest_conn = libvirt.open('qemu+ssh://192.168.1.2/system')
if conn == None:
    print('Failed to open connection to qemu+ssh://192.168.1.2/system', file=sys.stderr)
    exit(1)


vm_domain=conn.lookupByName('domName')
if dom == None:
    print('Failed to find the domain '+domName, file=sys.stderr)
    exit(1)
cpu_per = get_cpu_info()
print(vm_domain.migrate(dest_conn,1,'labV2','ssh://192.168.1.1',0))