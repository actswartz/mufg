# Lab 7: Intro to Ansible Roles

Roles allow you to bundle variables, tasks, and templates into a reusable structure.

## Task: Create the `base_config` role
1. `ansible-galaxy init roles/base_config`
2. Update `roles/base_config/tasks/main.yml`:
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
    text: "Configured via Role"
    state: present
```

3. Create `lab07_08_roles.yml`:
```yaml
---
- name: Apply Base Role
  hosts: routers
  roles:
    - base_config
```
