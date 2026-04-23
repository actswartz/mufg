# Lab 4: Configuring Interface IP Addresses

In this lab, we use the `l3_interfaces` data from your inventory to configure all interfaces and ensure they are active.

## Task: Create the `lab04_interfaces.yml` Playbook

```yaml
---
- name: Lab 4 - Interface IPs
  hosts: routers
  gather_facts: false
  tasks:
    - name: Configure IP Addresses
      cisco.ios.ios_l3_interfaces:
        config: "{{ l3_interfaces }}"
        state: merged

    - name: Ensure Interfaces are Up
      cisco.ios.ios_interfaces:
        config:
          - { name: Ethernet0/0, enabled: true }
          - { name: Ethernet0/1, enabled: true }
          - { name: Ethernet0/2, enabled: true }
          - { name: Ethernet0/3, enabled: true }
        state: merged
```

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab04_interfaces.yml
```
