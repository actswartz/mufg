# Lab 1: Setting Up Your Environment & First Commands

Welcome to your first lab! The goal of this exercise is to introduce you to the fundamental concepts of Ansible, establish a connection to your network devices, and run your first commands.

## 🧠 Core Concept: How Ansible Works
Ansible is an **agentless** automation tool. 
- **Control Node:** The Ubuntu machine you are logged into. It has Ansible installed.
- **Managed Nodes:** Your pod's three Cisco IOL routers. 
Ansible connects to these routers over **SSH**, executes a task, and then disconnects. It doesn't require any software to be installed on the routers themselves.

## Part 1: Create Your Ansible Inventory 🗂️

The **Inventory** is a file that tells Ansible *who* to talk to and *how* to authenticate. We use **YAML** format because it is human-readable and structured.

1. Create a directory called 'gem': `mkdir gem && cd gem`
2. Create your inventory file: `nano inventory.yml`
3. Paste the following (replace IPs with your specific pod IPs):

```yaml
all:
  vars:
    # Connection settings for all devices
    ansible_user: admin
    ansible_ssh_pass: 800-ePlus
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: cisco.ios.ios
    ansible_become: yes
    ansible_become_method: enable
    ansible_become_pass: 800-ePlus
    # Security flags to ensure smooth lab connectivity
    ansible_ssh_extra_args: '-o StrictHostKeyChecking=no -o PreferredAuthentications=password -o PubkeyAuthentication=no'
    ansible_network_cli_ssh_type: libssh

  children:
    routers:
      hosts:
        S1-R1: { ansible_host: 172.20.20.2 }
        S1-R2: { ansible_host: 172.20.20.3 }
        S1-R3: { ansible_host: 172.20.20.4 }
```

### 🔍 Breakdown of Inventory Variables:
*   **`ansible_network_os`**: Tells Ansible to use Cisco IOS logic.
*   **`network_cli`**: A specialized connection type for network devices that don't run Linux.
*   **`libssh`**: The high-performance SSH library we use to talk to IOL.

## Part 2: Ad-Hoc Commands 🛰️

An **Ad-Hoc command** is a one-liner used for quick tasks.

### 1. The Ping Test
This isn't a "network ping" (ICMP). It's an **Ansible Ping**, which verifies that Ansible can log into the device and execute Python code (or scripts).
```bash
ansible routers -i inventory.yml -m ping
```

### 2. Gathering Facts
Managed nodes have a lot of data (model, version, serial number). The `ios_facts` module collects this automatically.
```bash
ansible routers -i inventory.yml -m cisco.ios.ios_facts
```

## Part 3: Your First Playbook 📜

A **Playbook** is a file where you record your automation steps so you can run them repeatedly.

Create `lab01_facts.yml`:
```yaml
---
- name: Lab 1 - Display Specific Facts
  hosts: routers
  gather_facts: true  # This triggers the automatic collection of device data
  tasks:
    - name: Display Hostname and Version
      debug:
        msg: "The hostname is {{ ansible_net_hostname }} and the version is {{ ansible_net_version }}"
```

### 🔍 Why use `debug`?
The `debug` module is like a `print()` statement in programming. It is used to show information on your screen during the playbook run. Here, we are printing **Variables** (`{{ ... }}`) that Ansible gathered for us.

Run it:
```bash
ansible-playbook -i inventory.yml lab01_facts.yml
```
