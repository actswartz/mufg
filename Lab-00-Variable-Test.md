<img src="images/3r.jpg" width="400" alt="Network Topology">

---

### 🛠️ How to Connect to a Router
If you need to verify your work or troubleshoot manually, follow these steps:
1.  **Requirement:** You must be logged into the Lab Server.
2.  **Connect via SSH (Replace X with your Pod Number):**
    *   **R1:** `ssh admin@172.20.20.2`
    *   **R2:** `ssh admin@172.20.20.3`
    *   **R3:** `ssh admin@172.20.20.4`
3.  **Password:** `800-ePlus`

---

**🚀 Mission Prompt:** The Variable Foundation. Before we touch the network, we must ensure we can pass data through the Ansible engine.

---

# Lab 0: Testing Variables

Welcome to the foundation of automation! In this "Zero-Day" lab, you will learn how to define a variable in your inventory and retrieve it using a playbook. This ensures your Ansible environment is correctly processing data.

## 📖 What is a Variable?
A variable is a reserved memory location to store values. In Ansible, variables are used to manage differences between different hosts or environments. Instead of hard-coding values, variables allow you to write flexible, reusable playbooks.

---

## Part 1: Adding a Variable to your Inventory 🗂️

Open your `inventory.yml` file and add `my_variable` to the `vars` section.

```yaml
all:
  vars:
    ansible_user: admin
    ansible_password: 800-ePlus
    ...
    my_variable: "Student-Pod-X"  # Replace X with your Pod Number (e.g., Student-Pod-1)
```

---

## Part 2: Create the `lab00_var_test.yml` Playbook 📜

Create a new file called `lab00_var_test.yml`:

```yaml
---
- name: Lab 0 - Variable Test
  hosts: routers
  gather_facts: false
  tasks:
    - name: variable test
      debug:
        msg: "variable value is -- {{ my_variable }}"
```

### 🔍 Breakdown:
*   **`debug`**: This module prints statements during execution.
*   **`{{ my_variable }}`**: This tells Ansible to look up the value of `my_variable` and insert it here.

**Run the playbook:**
```bash
ansible-playbook -i inventory.yml lab00_var_test.yml
```

**✅ Success Criteria:** You see the output: `"msg": "variable value is -- Student-Pod-X"` in your terminal.

---

## ❓ Knowledge Check
1.  What is the purpose of the `debug` module?
2.  Where in the inventory did we define the variable?
3.  What symbols are used to tell Ansible to perform variable substitution?
