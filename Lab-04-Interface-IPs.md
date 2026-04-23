# Lab 4: Configuring Interface IP Addresses

In this lab, you will tackle one of the most common networking tasks: configuring IP addresses on physical interfaces using **Resource Modules**.

## 🧠 Core Concept: Data vs Logic
As your automation grows, you want to keep your **Technical Data** (like IP addresses) separate from your **Automation Logic** (the playbook).
- **Data:** Stored in your `inventory.yml`. This changes per student and per router.
- **Logic:** Stored in your `lab04_interfaces.yml`. This remains the same for everyone.

## Part 1: Update Your Inventory with Interface Data 🗂️

Open your `inventory.yml` and update your hosts to include the `l3_interfaces` list. 

### 🔍 Deep Dive: The Data Structure
The `l3_interfaces` variable is a **List of Dictionaries**.
- The `[]` brackets represent a **List** (like a shopping list).
- The `{}` curly braces represent a **Dictionary** (a key and its value).
- `ipv4` is nested inside the dictionary because an interface can have multiple settings (IP, description, speed).

```yaml
        S1-R1:
          ansible_host: 172.20.20.2
          l3_interfaces:
            - { name: Ethernet0/0, ipv4: [{ address: 172.20.20.2/24 }] }
            - { name: Ethernet0/1, ipv4: [{ address: 12.12.12.1/24 }] }
            - { name: Ethernet0/3, ipv4: [{ address: 13.13.13.1/24 }] }
```

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

### 🔍 Technical Breakdown:
1.  **`cisco.ios.ios_l3_interfaces`**: This is a **Resource Module**. It is designed to manage the "Layer 3" (IP) state of an interface. 
    - **`config: "{{ l3_interfaces }}"`**: This tells Ansible to look at the list we made in the inventory.
2.  **`cisco.ios.ios_interfaces`**: This manages the "Layer 2" or physical state.
    - **`enabled: true`**: In Cisco terms, this sends the `no shutdown` command. 
    - **Crucial Note:** In many virtual environments (like IOL), interfaces are "Admin Down" by default. Without this task, your IPs would be configured, but the interface would stay "red" or "down".

## Part 3: Running and Verifying 🛠️

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab04_interfaces.yml
```

### 🔍 Verification (The "Human" way):
After the playbook finishes, log into **S1-R1** and run:
```bash
show ip interface brief
```
You should see `up` and `up` for the Status and Protocol columns of the interfaces you configured. If they say `administratively down`, the second task in your playbook failed or was skipped.
