# Lab 8: Capstone Project 🎓

Congratulations! You have reached the final challenge. The goal of the Capstone Project is to combine everything you've learned into a single, unified "Master Playbook."

## 🧠 Core Concept: Orchestration
Up until now, you've run separate playbooks for hostnames, IPs, and routing. In the real world, we use **Orchestration** to tie these pieces together into a single "Push-Button" deployment.

---

## The Objective
Create a single execution path that performs all deployment steps in the correct order.

## Requirements:
1.  **Preparation:** Ensure your `inventory.yml` is accurate.
2.  **Base Config:** Use your `base_config` role to set standards.
3.  **Connectivity:** Apply the interface IPs and ensure they are `up`.
4.  **Routing:** Deploy OSPF using your Jinja2 template.
5.  **Validation:** Automatically verify that the network is healthy.

---

## Task: Create the `site.yml` Master Playbook

```yaml
---
- name: Master Deployment Playbook (Pod Build)
  hosts: routers
  gather_facts: false
  
  roles:
    - base_config

  tasks:
    - name: Section 1 - Interfaces
      import_tasks: lab04_interfaces.yml

    - name: Section 2 - OSPF
      import_tasks: lab05_ospf.yml

    - name: Section 3 - Validation
      import_tasks: lab06_validation.yml
```

### 🔍 Deep Dive: `import_tasks`
The `import_tasks` keyword allows you to include other files as if they were part of the current playbook. This lets you build complex systems out of simple, tested building blocks.

### 💡 Industry Pro-Tip: CI/CD
This `site.yml` file is the type of file that would be triggered automatically in a **CI/CD Pipeline** (Continuous Integration / Continuous Deployment). Whenever a network engineer changes a variable in the inventory, a system like GitLab or Jenkins runs this file to update the network instantly.

---

## Part 2: Final Run 🚀

Run your masterpiece:
```bash
ansible-playbook -i inventory.yml site.yml
```

### 🔍 Verification:
If the "Validation" section at the end passes with **GREEN** messages, you have successfully automated an entire network pod!

---

## ❓ Knowledge Check
1.  What is the benefit of using `import_tasks` instead of copying and pasting code?
2.  In what order does Ansible execute roles and tasks in a playbook?
3.  How does a Master Playbook relate to a "Push-Button" deployment strategy?
