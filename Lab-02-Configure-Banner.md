# Lab 2: Configuring Device Banners

In this lab, you will learn how to use Ansible to manage device configurations using the `ios_banner` module.

## Task: Create the `lab02_banner.yml` Playbook

```yaml
---
- name: Configure MOTD Banner
  hosts: routers
  gather_facts: false
  tasks:
    - name: Set Message of the Day
      cisco.ios.ios_banner:
        banner: motd
        text: "Welcome to Student Pod Router - Authorized Access Only!"
        state: present
```

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab02_banner.yml
```
