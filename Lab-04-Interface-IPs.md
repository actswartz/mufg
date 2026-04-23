# Lab 4: Configuring Interface IP Addresses

In this lab, you will tackle one of the most common networking tasks: configuring IP addresses on physical interfaces using **Resource Modules**.

## 🧠 Core Concept: Data vs Logic
As your automation grows, you want to keep your **Technical Data** (like IP addresses) separate from your **Automation Logic** (the playbook).
- **Data:** Stored in your `inventory.yml`. This changes per student and per router.
- **Logic:** Stored in your `lab04_interfaces.yml`. This remains the same for everyone.

This separation allows you to scale. If you add a new router, you only update the data file, not the code.

---

## Part 1: Update Your Inventory with Interface Data 🗂️

Open your `inventory.yml` and update your hosts to include the `l3_interfaces` list. 

### 🔍 Deep Dive: The Data Structure
The `l3_interfaces` variable is a **List of Dictionaries**.
- The `[]` brackets represent a **List** (an ordered sequence of items).
- The `{}` curly braces represent a **Dictionary** (a collection of labels and values).
- `ipv4` is nested inside because an interface can have multiple addresses.

```yaml
        S1-R1:
          ansible_host: 172.20.20.2
          l3_interfaces:
            - { name: Ethernet0/0, ipv4: [{ address: 172.20.20.2/24 }] }
            - { name: Ethernet0/1, ipv4: [{ address: 12.12.12.1/24 }] }
            - { name: Ethernet0/3, ipv4: [{ address: 13.13.13.1/24 }] }
```

---

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
1.  **`cisco.ios.ios_l3_interfaces`**: This is a **Resource Module**. It only cares about Layer 3 (IP) settings.
2.  **`cisco.ios.ios_interfaces`**: This manages Layer 2/Physical settings.
    - **`enabled: true`**: This is the Ansible way of saying `no shutdown`. 

### 💡 Industry Pro-Tip: Admin Down
In virtual labs like IOL, interfaces are **shutdown** by default. Even if you configure an IP address, the interface will stay "red" (down) until you explicitly enable it. Always include an "Enable Interfaces" task in your base deployment.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab04_interfaces.yml
```

---

## 📂 Deep Dive: Resource Module States
Resource modules are powerful because they have multiple "States" that determine how they behave.

| State | Action |
| :--- | :--- |
| **`merged`** | **(Add Only)** Adds your configuration to the router without touching anything else. (The safest option). |
| **`replaced`** | **(Update)** If an interface exists but has a different IP, it replaces it. It doesn't touch other interfaces. |
| **`overridden`** | **(Clean Slate)** Makes the router look *exactly* like your YAML. Any interface not in your YAML will be wiped clean. |
| **`deleted`** | **(Remove)** Removes the IP configuration from the interfaces listed in your YAML. |

---

## ❓ Knowledge Check
1.  What is the purpose of the `l3_interfaces` variable?
2.  Why do we need a separate task for `enabled: true`?
3.  What command would you run on the Cisco CLI to verify the IPs were applied?


---

## 📺 Video Tutorial: Watch & Learn
For a visual walkthrough of the concepts in this lab, check out this helpful tutorial:
[https://www.youtube.com/watch?v=GAnO0V6j5Cg](https://www.youtube.com/watch?v=GAnO0V6j5Cg)
