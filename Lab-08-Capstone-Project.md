# Lab 8: Capstone Project 🎓

This is your final challenge! The goal is to build a "Master Playbook" that can configure a brand new pod from scratch.

## 🧠 The Objective
Create a single execution path that performs all the following steps in order.

## Requirements:
1.  **Preparation:** Ensure your `inventory.yml` is accurate and complete with all IP and OSPF data.
2.  **Base Config:** Use the `base_config` role from Lab 7 to set hostnames and banners.
3.  **Connectivity:** Include the tasks from Lab 4 to configure all interface IPs and bring them up.
4.  **Routing:** Include the OSPF configuration logic from Lab 5.
5.  **Validation:** Perform a final check to ensure OSPF is working.

## Task: Create the `site.yml` Master Playbook
```yaml
---
- name: Master Deployment Playbook
  hosts: routers
  gather_facts: false
  
  roles:
    - base_config

  tasks:
    - name: Section 1 - Interfaces
      import_tasks: lab04_interfaces.yml  # You can reuse existing playbook files!

    - name: Section 2 - OSPF
      import_tasks: lab05_ospf.yml

    - name: Section 3 - Validation
      import_tasks: lab06_validation.yml
```

### 🔍 Tips for Success:
*   **Run it in parts:** Use the `--start-at-task` flag if you want to skip parts you've already tested.
*   **Check the console:** Watch the "PLAY RECAP" at the end. You want to see "failed=0".

Run your masterpiece:
```bash
ansible-playbook -i inventory.yml site.yml
```
