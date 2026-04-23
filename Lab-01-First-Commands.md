# Lab 1: Setting Up Your Environment & First Commands

Welcome to your first lab! The goal of this exercise is to introduce you to the fundamental concepts of Ansible, establish a connection to your network devices, and run your first commands.

## Objectives 🎯
* Understand and create an Ansible YAML inventory file.
* Verify connectivity to your three Cisco IOL devices.
* Gather information ("facts") from your devices using Ansible.

## Part 1: Create Your Ansible Inventory 🗂️

1. Create a directory called 'gem': `mkdir gem && cd gem`
2. Create your inventory file: `nano inventory.yml`
3. Paste the following (replace X with your Pod number):

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
    ansible_ssh_extra_args: '-o StrictHostKeyChecking=no -o PreferredAuthentications=password -o PubkeyAuthentication=no'
    ansible_network_cli_ssh_type: libssh

  children:
    routers:
      hosts:
        S1-R1: { ansible_host: 172.20.20.2 }
        S1-R2: { ansible_host: 172.20.20.3 }
        S1-R3: { ansible_host: 172.20.20.4 }
```

## Part 2: Ad-Hoc Commands 🛰️

Test connectivity:
```bash
ansible routers -i inventory.yml -m ping
```

Gather facts:
```bash
ansible routers -i inventory.yml -m cisco.ios.ios_facts
```
## Part 3: Your First Playbook

Create `lab01_facts.yml`:

```yaml
---
- name: Lab 1 - Display Specific Facts
  hosts: routers
  gather_facts: true
  tasks:
    - name: Display Hostname and Version
      debug:
        msg: "The hostname is {{ ansible_net_hostname }} and the version is {{ ansible_net_version }}"
```

Run it:
```bash
ansible-playbook -i inventory.yml lab01_facts.yml
```