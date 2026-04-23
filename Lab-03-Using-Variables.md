# Lab 3: Using Variables for Hostnames

This lab introduces **Dynamic Automation**. Instead of hard-coding names into a playbook, we use variables so the same playbook works for every device.

## 🧠 Core Concept: Magic Variables
Ansible has "Magic Variables" that are always available.
*   **`inventory_hostname`**: The name of the current device as defined in your `inventory.yml` (e.g., `S1-R1`).

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

### 🔍 Why use `config:` and `state: merged`?
This is the **Resource Module** standard.
- **`config:`**: A dictionary containing the actual settings (the hostname).
- **`state: merged`**: This tells Ansible to "merge" this setting with the existing configuration. It is the safest way to apply changes without overwriting other unrelated settings.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab03_hostnames.yml
```

**Verification:** Log into your router via SSH. You should see the prompt has changed from `Router>` or `r1>` to `S1-R1#`.
