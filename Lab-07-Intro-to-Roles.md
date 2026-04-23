# Lab 7: Intro to Ansible Roles

As you build more automation, your playbooks will become hundreds of lines long. **Roles** allow you to break this "monolithic" code into small, manageable, and reusable pieces.

## 🧠 Core Concept: Modularization (The Role)
Think of a **Role** as a "plugin" for your automation. If you write a great role for "Cisco Hardening," you can simply drop that folder into any new project and it "just works."

## Task 1: Initialize the Role Structure 🏗️

1.  Create a directory for your roles:
    ```bash
    mkdir roles
    ```

2.  Use the `ansible-galaxy` tool to create the boilerplate structure:
    ```bash
    ansible-galaxy init roles/base_config
    ```

### 🔍 Breakdown of the Role Folders:
When you run the command above, Ansible creates several folders. Here are the most important ones:
- **`tasks/`**: This is where your playbook logic lives (`main.yml`).
- **`defaults/`**: This is where you store default variables that the role needs.
- **`templates/`**: This is where you put your `.j2` files.
- **`handlers/`**: Tasks that only run when "notified" (like restarting a service after a config change).

## Task 2: Build the `base_config` Role 🛠️

Update the Role's tasks: `nano roles/base_config/tasks/main.yml`
```yaml
---
# These tasks are now separate from any specific playbook
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

## Task 3: Use the Role in a Playbook 🚀

Create `lab07_08_roles.yml`:
```yaml
---
- name: Apply Base Configuration via Role
  hosts: routers
  gather_facts: false
  roles:
    - base_config  # Ansible automatically looks in roles/base_config/tasks/main.yml
```

### 🔍 The Power of Abstraction
Notice how simple your playbook is now. You aren't saying "Run these 5 Cisco commands." You are saying "Make these routers have a **Base Config**." 

This is the goal of high-level automation: **Abstraction**. You describe *what* the device should be (a device with a base config), and the role handles the *how*.

## Part 4: Running the Role 🛠️

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab07_08_roles.yml
```
