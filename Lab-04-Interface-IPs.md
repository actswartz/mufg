<img src="images/3r.jpg" width="400" alt="Network Topology">

---

### 🛠️ How to Connect to a Router
If you need to verify your work or troubleshoot manually, follow these steps:
1.  **Requirement:** You must be logged into the Lab Server.
2.  **Connect via SSH (Replace X with your Pod Number):**
    *   
    *   
    *   
3.  **Password:** 
4.  **Useful Verification Commands:**
    *   
    *   

---


**🚀 Mission Prompt:** Activate the Data Plane. Translate your inventory’s IP schema into a living network, ensuring every interface is alive, configured, and talking.

---

<img src="images/Lab-04-Interface-IPs.jpg" width="600" alt="Lab-04-Interface-IPs">


# Lab 4: Configuring Interface IP Addresses

In this lab, you will tackle one of the most common networking tasks: configuring IP addresses on physical interfaces using **Resource Modules**.

## 📖 What is Data/Logic Separation?
Data/Logic Separation is an architectural pattern where the technical values (Data) are kept in different files than the automation code (Logic). In this lab, your `inventory.yml` acts as the "Database" containing specific IP addresses and interface names, while your playbook acts as the "Engine" that knows how to apply those values. This separation is what allows automation to scale from a single pod to an entire global data center.

## 🎯 What is the Purpose?
The purpose is **abstraction and portability**. By separating data from logic, you can hand your playbook to a colleague, and it will work perfectly in their environment as long as they provide their own inventory data. It also simplifies troubleshooting; if an IP is wrong, you know to check the data file. If the command syntax is wrong, you check the logic file. This modularity is essential for managing complex infrastructure without creating "spaghetti code."

---

## 📖 What are Resource Module States?
Resource Module States (like `merged`, `replaced`, `overridden`, and `deleted`) are the controls that determine how Ansible interacts with a device's current configuration. Unlike a simple CLI command that just "pushes" text, these states allow you to define the *strategy* for configuration management. For example, `merged` safely adds new config, while `overridden` wipes the device clean and forces it to match your YAML exactly.

## 🎯 What is the Purpose?
The purpose is **precision and safety**. Different network tasks require different levels of control. When you are adding a new description, `merged` is perfect because it won't break existing settings. However, when you are performing a security audit or a complete device refresh, `overridden` ensures that no "illegal" or "ghost" configurations are left behind on the router. Understanding these states is the difference between a beginner who just runs commands and an expert who manages network state.

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
