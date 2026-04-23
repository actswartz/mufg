# Lab 4: Configuring Interface IP Addresses

In this lab, you will tackle one of the most common networking tasks: configuring IP addresses on physical interfaces.

## 🧠 Core Concept: Data vs Logic
As your automation grows, you want to keep your **Technical Data** (like IP addresses) separate from your **Automation Logic** (the playbook).
- **Data:** Stored in your `inventory.yml`.
- **Logic:** Stored in your `lab04_interfaces.yml`.

## Part 1: Update Your Inventory with Interface Data 🗂️

Open your `inventory.yml` and update your hosts to include the `l3_interfaces` list. This list defines exactly what each router should look like.

```yaml
        S1-R1:
          ansible_host: 172.20.20.2
          l3_interfaces:
            - { name: Ethernet0/0, ipv4: [{ address: 172.20.20.2/24 }] }
            - { name: Ethernet0/1, ipv4: [{ address: 12.12.12.1/24 }] }
            - { name: Ethernet0/3, ipv4: [{ address: 13.13.13.1/24 }] }
```

### 🔍 Breakdown of the List:
The `l3_interfaces` variable is a **List of Dictionaries**.
- The `[]` brackets represent a list.
- The `{}` curly braces represent a dictionary (key-value pairs).
Ansible will loop through this list and apply the settings to each named interface.

## Part 2: Create the `lab04_interfaces.yml` Playbook

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

### 🔍 Why two tasks?
1.  **`ios_l3_interfaces`**: Handles Layer 3 settings (IP addresses).
2.  **`ios_interfaces`**: Handles Layer 2/Physical settings. Here, we use `enabled: true` which is the Ansible equivalent of the Cisco command `no shutdown`.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab04_interfaces.yml
```
