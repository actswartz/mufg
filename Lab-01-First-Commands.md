# Lab 1: Setting Up Your Environment & First Commands

Welcome to your first lab! The goal of this exercise is to introduce you to the fundamental concepts of Ansible, establish a connection to your network devices, and run your first commands.

## Objectives 🎯

*   Understand and create an Ansible inventory.yml file.
*   Learn what an Ansible ad-hoc command is and how to use one.
*   Verify connectivity to your three Cisco IOL devices.
*   Gather information ("facts") from your devices using Ansible.
*   Write and run your very first Ansible Playbook to display specific facts.

## Introduction to Ansible

Ansible is a powerful automation tool that allows you to manage and configure computers and network devices automatically. One of its biggest advantages is that it is **agentless**. This means you don't need to install any special software on the devices you want to manage. It communicates using standard protocols like SSH.

You will work from a central machine called the **control node** (your lab environment), which runs Ansible. The devices you manage are called **managed nodes** (your pod's routers).

For this lab, your three devices have already been pre-configured with:
*   A unique management IP address.
*   SSH access enabled.
*   Authentication required with the username **`admin`** and password **`800-ePlus`** for all routers.

![Lab Topology](images/topo.jpg)

---
Management IP Address
|       | Router 1    | Router 2    | Router 3    |
|-------|-------------|-------------|-------------|
| Pod1  | 172.20.20.2 | 172.20.20.3 | 172.20.20.4 |
| Pod2  | 172.20.20.5 | 172.20.20.6 | 172.20.20.7 |
| Pod3  | 172.20.20.8 | 172.20.20.9 | 172.20.20.10 |
| Pod4  | 172.20.20.11| 172.20.20.12| 172.20.20.13 |
| Pod5  | 172.20.20.14| 172.20.20.15| 172.20.20.16 |
| Pod6  | 172.20.20.17| 172.20.20.18| 172.20.20.19 |
| Pod7  | 172.20.20.20| 172.20.20.21| 172.20.20.22 |
| Pod8  | 172.20.20.23| 172.20.20.24| 172.20.20.25 |
| Pod9  | 172.20.20.26| 172.20.20.27| 172.20.20.28 |
| Pod10 | 172.20.20.29| 172.20.20.30| 172.20.20.31 |
| Pod11 | 172.20.20.32| 172.20.20.33| 172.20.20.34 |
| Pod12 | 172.20.20.35| 172.20.20.36| 172.20.20.37 |
| Pod13 | 172.20.20.38| 172.20.20.39| 172.20.20.40 |
| Pod14 | 172.20.20.41| 172.20.20.42| 172.20.20.43 |
| Pod15 | 172.20.20.44| 172.20.20.45| 172.20.20.46 |


---

## Part 1: Create Your Ansible Inventory 🗂️

The first step in any Ansible project is to tell Ansible what devices it should manage. You do this with an **inventory.yml file**. This file is a simple text document that lists the IP addresses or hostnames of your managed nodes.

### Task: Create the `inventory` file

1.  create a directory called 'gem'.  use "mkdir gem" and then change into that directory
2.  In your gem directory, create a new file named `inventory`.
3.  Use nano to create or re-edit the file at any time:

```bash
nano inventory.yml
```yaml
all:
  vars:
    ansible_user: admin
    ansible_ssh_pass: 800-ePlus
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: cisco.ios.ios
    ansible_become: yes
    ansible_become_method: enable
    ansible_become_pass: 800-ePlus
    ansible_ssh_extra_args: '-o StrictHostKeyChecking=no'
    ansible_network_cli_ssh_type: libssh

  children:
    routers:
      hosts:
        S1-R1:
          ansible_host: 172.20.20.2
          l3_interfaces:
            - { name: Ethernet0/0, ipv4: [{ address: 172.20.20.2/24 }] }
            - { name: Ethernet0/1, ipv4: [{ address: 12.12.12.1/24 }] }
            - { name: Ethernet0/3, ipv4: [{ address: 13.13.13.1/24 }] }
        S1-R2:
          ansible_host: 172.20.20.3
          l3_interfaces:
            - { name: Ethernet0/0, ipv4: [{ address: 172.20.20.3/24 }] }
            - { name: Ethernet0/1, ipv4: [{ address: 12.12.12.2/24 }] }
            - { name: Ethernet0/2, ipv4: [{ address: 23.23.23.2/24 }] }
        S1-R3:
          ansible_host: 172.20.20.4
          l3_interfaces:
            - { name: Ethernet0/0, ipv4: [{ address: 172.20.20.4/24 }] }
            - { name: Ethernet0/2, ipv4: [{ address: 23.23.23.3/24 }] }
            - { name: Ethernet0/3, ipv4: [{ address: 13.13.13.3/24 }] }
```ini
[all:vars]
ansible_user=admin
ansible_password=800-ePlus
ansible_connection=network_cli

[routers]
cisco
arista
juniper

[cisco:vars]
ansible_network_os=cisco.ios.ios
ansible_connection=ansible.netcommon.network_cli
ansible_network_cli_ssh_type=paramiko
ansible_command_timeout=120

[arista:vars]
ansible_network_os=cisco.ios.ios
ansible_connection=ansible.netcommon.network_cli
ansible_become=true
ansible_become_method=enable
ansible_become_password=800-ePlus

[juniper:vars]
ansible_network_os=cisco.ios.ios
ansible_connection=ansible.netcommon.netconf

```

### Explanation of the Inventory File

*   **`[routers]`**: This creates a new group called `routers` that contains other groups. It's a convenient way to target all of your network devices at once.



## Part 2: First Contact with Ad-Hoc Commands 🛰️

An **ad-hoc command** is a quick, one-line command that you can run to perform a single task. They are great for quick checks and simple actions but are not meant for complex, repeatable workflows.

### Task: Verify Connectivity with the `ping` Module

Let's send our first command. We will use the `ping` module, which is a simple test to see if Ansible can successfully connect and authenticate to the devices.

1.  From your terminal, run the following command.

```bash
ansible routers -i inventory.yml -m ping
```

2.  You should see a **GREEN** success message for each of your three devices.
 ignore the warning messages that may appear in purple 

```
r1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
r2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
r3 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

### Explanation of the Command

*   `ansible`: The command-line tool for running ad-hoc commands.
*   `routers`: The group of hosts from our inventory we want to target.
*   `-i inventory.yml`: Specifies the path to our inventory.yml file.
*   `-m ping`: Specifies the module to run. The `ping` module returns a `pong` on success.

**If you see a RED error message**, double-check the IP addresses, username, and password in your `inventory` file.

---

## Part 3: Your First Playbook for Gathering Facts 📋

While ad-hoc commands are useful, most automation is done with **Playbooks**. A playbook is a file written in YAML that describes a set of tasks to be executed on your managed nodes.

Our goal is to gather information (facts) from our devices and display the OS version for each one.

### Task: Create and Run the `gather_facts.yml` Playbook

1.  In your `gem` directory, create a new file named `gather_facts.yml`.
2.  Launch or reopen the file with nano:

```bash
nano gather_facts.yml
```

3.  Copy and paste the following YAML text into this new file.

```yaml
---
- name: Gather and Display Device Facts
  hosts: routers
  gather_facts: false

  tasks:
    - name: Gather device facts
      ansible.builtin.gather_facts:

    - name: Display OS Version for each device
      ansible.builtin.debug:
        msg: "The OS version of {{ inventory_hostname }} is {{ ansible_facts.net_version }}"

```

### Explanation of the Playbook

*   `---`: A YAML file optionally starts with `---`.
*   `- name: ...`: This is the name of our **play**. A playbook can have multiple plays.
*   `hosts: routers`: This specifies that this play should run against the `routers` group from our inventory.
*   `gather_facts: false`: By default, Ansible gathers facts at the start of every play. We turn this off here because we want to manually control when it happens in our tasks.
*   `tasks:`: This is the list of actions the playbook will perform.
*   `- name: Gather device facts`: The name of our first task. Good naming is important for readability.
*   `ansible.builtin.gather_facts:`: This is the task itself. It calls the module that collects all the information about the devices.
*   `- name: Display OS Version...`: The name of our second task.
*   `ansible.builtin.debug:`: This module is used to print messages to the console. It's very useful for debugging.
*   `msg: "..."`: The message to be printed.
*   `{{ inventory_hostname }}` and `{{ ansible_facts.net_version }}`: These are **variables**. The double curly braces `{{ }}` tell Ansible to replace the placeholder with the value of the variable.
    *   `inventory_hostname` is the name of the device the task is currently running on (e.g., `r1`).
    *   `ansible_facts.net_version` is one of the many facts that was collected by the `gather_facts` module.
    *   **Cisco prerequisite:** the `cisco.ios.ios_facts` module requires the `xmltodict` Python library on your control node. If you see errors about `xmltodict` missing, install it in your Ansible virtual environment with `pip install xmltodict` and rerun the playbook.

### Run the Playbook

1.  From your terminal, execute the playbook with the `ansible-playbook` command.

```bash
ansible-playbook -i inventory.yml gather_facts.yml
```

2.  You should see output for each task. The final task will give you a clean, readable message for each device.

```
...
TASK [Display OS Version for each device] **************************************
ok: [r1] => {
    "msg": "The OS version of r1 is 16.09.03"
}
ok: [r2] => {
    "msg": "The OS version of r2 is 4.21.8M"
}
ok: [r3] => {
    "msg": "The OS version of r3 is 19.4R1.10"
}
...
```
*(Note: Your OS versions may vary)*

---

## Conclusion

Congratulations! You have successfully:
*   Built a working Ansible inventory.
*   Verified full connectivity to your lab devices.
*   Run both an ad-hoc command and your first playbook.
*   Learned how to gather and display specific information from your network devices.

In the next lab, you will expand on these skills to start making configuration changes to your devices.
