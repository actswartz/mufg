# Lab 2: Configuring Device Banners

In this lab, you will learn how to use specialized **Network Resource Modules** to change the configuration of your routers.

## 🧠 Core Concept: Idempotency
One of Ansible's most important features is **Idempotency**. 
- If you run a playbook and the change is needed, Ansible makes the change (`changed=1`).
- If you run it again and the configuration is already correct, Ansible does nothing (`ok=1`).
This ensures your automation is safe to run multiple times.

## Task: Create the `lab02_banner.yml` Playbook

```yaml
---
- name: Configure MOTD Banner
  hosts: routers
  gather_facts: false
  tasks:
    - name: Set Message of the Day
      cisco.ios.ios_banner:
        banner: motd
        text: "Welcome to Student Pod Router - Authorized Access Only!"
        state: present
```

### 🔍 Breakdown of the Module:
*   **`cisco.ios.ios_banner`**: A specific module for managing Cisco banners.
*   **`banner: motd`**: Specifies we are changing the "Message of the Day".
*   **`state: present`**: This is **Declarative**. We are telling Ansible "I want this banner to exist," not "Run the command to add a banner." If it's already there, Ansible won't touch it.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab02_banner.yml
```

**Challenge:** Change the text and run it again. Notice the output says "changed". Run it a third time without changing the text and notice it says "ok".
