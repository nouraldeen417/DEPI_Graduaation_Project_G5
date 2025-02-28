import ansible_runner
#ping all hosts in tobology
def Ping():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/ping.yaml",
    inventory="hosts",    # Path to external inventory file
    rotate_artifacts=10
    )
    #host=[]
    #task=[]
    #status=[]
    devices = []

    for event in r.events: 
        event_data = event.get('event_data', {})
        cur_stat= event.get('event')
        #Check for task completion statuses
        if cur_stat in ('runner_on_ok', 'runner_on_skipped', 'runner_on_failed', 'runner_on_unreachable'):
            hst=event_data.get('host', event_data.get('remote_addr'))  
            tsk=event_data.get('task', event_data.get('name', event_data.get('play')))
            stat=event.get('event')
            if (stat == 'runner_on_ok'):
                stat = "Device is connected successfully"
            else:
                stat = "Device is OFF"
  
            devices.append(Device(host=hst, task=tsk, status=stat))
            
    # print(host + status + task)
    #return  host,status,task 
    return devices
class Device:
    def __init__(self, host, task, status):
        self.host = host
        self.task = task
        self.status = status