<img src="images/3 router triangle.jpeg" width="400" alt="Network Topology">

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
    - base_config  # This tells Ansible to look in roles/base_config and run tasks/main.yml
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

## 📂 Deep Dive: The Role Directory Structure
When you run `ansible-galaxy init`, Ansible creates a specific set of folders. Understanding these is key to becoming an Ansible expert.

| Directory | Purpose | Use Case |
| :--- | :--- | :--- |
| **`tasks/`** | **The Engine.** Contains the main list of steps the role will take. | `main.yml` here holds your `ios_config` or `ios_banner` tasks. |
| **`handlers/`** | **The Response.** Contains tasks that only run when "notified" by another task. | Use this to restart a service or clear a counter only *after* a config change. |
| **`defaults/`** | **Safe Variables.** The lowest priority variables for the role. | Set `banner_text: "Welcome"` here. Users can easily override this in their playbook. |
| **`vars/`** | **Locked Variables.** High priority variables that should rarely change. | Technical constants or specific internal settings that shouldn't be touched. |
| **`files/`** | **Static Assets.** Contains files that need to be copied to the target. | A script or a pre-made license file you want to upload to the router. |
| **`templates/`** | **Dynamic Assets.** Contains `.j2` Jinja2 files. | Your `ospf_config.j2` would live here in a production OSPF role. |
| **`meta/`** | **The Blueprint.** Contains data *about* the role itself. | Define dependencies here (e.g., "This role needs the `vlan` role to run first"). |
| **`README.md`** | **The Manual.** Documentation for other humans. | Explains what the role does, what variables it needs, and who wrote it. |

---

## ❓ Knowledge Check
1.  What command creates the boilerplate folder structure for a role?
2.  Which folder inside a role contains the `main.yml` file with your tasks?
3.  Why is it better to use a role instead of a 500-line single playbook?


---

## 📺 Video Tutorial: Watch & Learn
For a visual walkthrough of the concepts in this lab, check out this helpful tutorial:
[https://www.youtube.com/watch?v=K3HOnVfU_P8](https://www.youtube.com/watch?v=K3HOnVfU_P8)
