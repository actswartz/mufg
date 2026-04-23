# Lab 7: Intro to Ansible Roles

As your automation library grows, your playbooks can become very large and difficult to manage. **Roles** provide a way to break your automation into small, reusable modules.

## 🧠 Core Concept: Modularization
Think of a **Role** as a "plugin" for your automation. If you write a great role for "Cisco Hardening," you can simply drop that folder into any new project and it "just works." This follows the principle of **Modular Design**.

---

## Task 1: Create the `base_config` role 🏗️

1.  Create a directory for your roles:
    ```bash
    mkdir roles
    ```

2.  Use the `ansible-galaxy` tool to create the directory structure:
    ```bash
    ansible-galaxy init roles/base_config
    ```

### 🔍 Breakdown of the Role Folders:
When you run the command above, Ansible creates several folders. 
- **`tasks/`**: This is where your playbook logic lives (`main.yml`).
- **`defaults/`**: This is where you store default variables that the role needs.
- **`templates/`**: This is where you put your `.j2` files.
- **`vars/`**: Higher priority variables (harder to override than defaults).

---

## Task 2: Build the `base_config` Role 🛠️

Update the Role's tasks: `nano roles/base_config/tasks/main.yml`
```yaml
---
- name: Configure Hostname
  cisco.ios.ios_hostname:
    config:
      hostname: "{{ inventory_hostname }}"
    state: merged

- name: Configure Banner
  cisco.ios.ios_banner:
    banner: motd
    text: "Authorized Access Only - Managed by Ansible Role"
    state: present
```

---

## Task 3: Use the Role in a Playbook 🚀

Create `lab07_08_roles.yml`:
```yaml
---
- name: Apply Base Configuration via Role
  hosts: routers
  gather_facts: false
  roles:
    - base_config  # This tells Ansible to look in roles/base_config/tasks/main.yml
```

### 🔍 The Power of Abstraction
Notice how simple your playbook is now. You aren't saying "Run these 5 Cisco commands." You are saying "Make these routers have a **Base Config**." 

This is the goal of high-level automation: **Abstraction**. You describe *what* the device should be, and the role handles the *how*.

### 💡 Industry Pro-Tip: Role Sharing
Roles are the standard way teams share automation. You can even download community-made roles from the **Ansible Galaxy** website for things like firewall rules, BGP setup, or SNMP monitoring.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab07_08_roles.yml
```

---

## ❓ Knowledge Check
1.  What command creates the boilerplate folder structure for a role?
2.  Which folder inside a role contains the `main.yml` file with your tasks?
3.  Why is it better to use a role instead of a 500-line single playbook?
