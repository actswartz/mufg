# Lab 7: Intro to Ansible Roles

As your automation library grows, your playbooks can become very large and difficult to manage. **Roles** provide a way to break your automation into small, reusable modules.

## 🧠 Core Concept: Modularization
A **Role** is a standardized directory structure that contains everything needed to perform a specific function (like "Base Config").
- **`tasks/`**: Contains the actual configuration steps.
- **`defaults/`**: Contains default variables.
- **`templates/`**: Contains Jinja2 templates.

## Task 1: Create the `base_config` role 🏗️

1.  Use the `ansible-galaxy` tool to create the directory structure:
    ```bash
    mkdir roles
    ansible-galaxy init roles/base_config
    ```

2.  Update the Role's tasks: `nano roles/base_config/tasks/main.yml`
    ```yaml
    ---
    # These tasks will be performed whenever the role is called
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

## Task 2: Use the Role in a Playbook 🚀

Create `lab07_08_roles.yml`:
```yaml
---
- name: Apply Base Configuration via Role
  hosts: routers
  gather_facts: false
  roles:
    - base_config  # This tells Ansible to look in roles/base_config and run tasks/main.yml
```

### 🔍 Why use Roles?
Imagine you have 1,000 routers. You can write one `base_config` role and use it in every single project you ever build. If you need to change the banner text, you change it in **one** place (the role), and every playbook using that role is automatically updated.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab07_08_roles.yml
```
