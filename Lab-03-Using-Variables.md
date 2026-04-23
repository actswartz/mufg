# Lab 3: Using Variables for Hostnames

This lab demonstrates how to use the `inventory_hostname` variable to dynamically configure your devices.

## Task: Create the `lab03_hostnames.yml` Playbook

```yaml
---
- name: Configure Device Hostnames
  hosts: routers
  gather_facts: false
  tasks:
    - name: Configure Hostname
      cisco.ios.ios_hostname:
        config:
          hostname: "{{ inventory_hostname }}"
        state: merged
```

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab03_hostnames.yml
```
