<img src="images/3 router triangle.jpeg" width="400" alt="Network Topology">

# Lab 3: Using Variables for Hostnames

This lab introduces **Dynamic Automation**. Instead of hard-coding names into a playbook, we use variables so the same playbook works for every device in your network.

## 🧠 Core Concept: The DRY Principle
In software engineering and automation, we follow the **DRY (Don't Repeat Yourself)** principle. 
If you have 3 routers, you *could* write 3 separate tasks. But if you have 3,000 routers, that is impossible. Variables allow you to write **one** task that works for **all** routers.

---

## 🧠 Core Concept: Magic Variables
Ansible has built-in variables called "Magic Variables" that it creates automatically.
*   **`inventory_hostname`**: This contains the name of the current device as defined in your `inventory.yml` (e.g., `S1-R1`).

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

### 🔍 Deep Dive: The Curly Braces `{{ ... }}`
In Ansible, whenever you see double curly braces, it means **"Variable substitution happens here."**
Ansible looks up the value of `inventory_hostname` and replaces the braces with the actual name (like `S1-R1`) before sending the command to the router.

### 💡 Industry Pro-Tip: Naming Conventions
Standardizing hostnames is the first step in network management. A good hostname often includes the site code, device type, and rack number (e.g., `NY-CORE-SW01`). Automation ensures these names are applied perfectly every time.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab03_hostnames.yml
```

---

## 📂 Deep Dive: Variable Filters
You can transform variables on the fly using **Filters** (pipes).

| Filter | Usage | Result Example |
| :--- | :--- | :--- |
| **`upper`** | `{{ inventory_hostname | upper }}` | `s1-r1` becomes `S1-R1` |
| **`lower`** | `{{ inventory_hostname | lower }}` | `S1-R1` becomes `s1-r1` |
| **`default`** | `{{ my_var | default('Router') }}` | Uses 'Router' if the variable is missing. |

Filters allow you to enforce naming standards (like "all hostnames must be lowercase") even if the inventory has typos.

---

## ❓ Knowledge Check
1.  What does the "DRY" principle stand for?
2.  What would happen if you forgot the `{{ }}` around a variable name in a playbook?
3.  Where does the value for `inventory_hostname` come from?


---

## 📺 Video Tutorial: Watch & Learn
For a visual walkthrough of the concepts in this lab, check out this helpful tutorial:
[https://www.youtube.com/watch?v=RIsV6oD-Iio](https://www.youtube.com/watch?v=RIsV6oD-Iio)
