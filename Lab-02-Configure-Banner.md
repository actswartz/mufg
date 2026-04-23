# Lab 2: Configuring Device Banners

In this lab, you will learn how to use specialized **Network Resource Modules** to change the configuration of your routers.

## 🧠 Core Concept: Idempotency
One of Ansible's most important features is **Idempotency**. 
- If you run a playbook and the change is needed, Ansible makes the change (`changed=1`).
- If you run it again and the configuration is already correct, Ansible does nothing (`ok=1`).
This ensures your automation is safe to run multiple times without causing accidental restarts or duplicates.

---

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
*   **`state: present`**: This is **Declarative Programming**. 
    - **Imperative:** "Run the command `banner motd ...`"
    - **Declarative:** "I want the banner to be present."
    Ansible figures out the commands needed to make your wish a reality.

### 💡 Industry Pro-Tip: The Login Banner
In the real world, banners aren't just for welcome messages. They are legal requirements. Many organizations use them to warn unauthorized users that their activity is being monitored, which is often required to prosecute hackers.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab02_banner.yml
```

---

## 📂 Deep Dive: Check Mode & Diff Mode
Professional engineers often "dry-run" their changes before applying them to a live network.

| Feature | Flag | Purpose |
| :--- | :--- | :--- |
| **Check Mode** | `--check` | Tells Ansible to "pretend" to run the tasks. It shows what *would* change without actually touching the router. |
| **Diff Mode** | `--diff` | Shows you the "Before and After" text. You will see exactly what lines of config are being added or removed. |

**Try it!** Run `ansible-playbook -i inventory.yml lab02_banner.yml --check --diff` and see the detailed report.

---

## ❓ Knowledge Check
1.  If a playbook says `changed=0`, did it fail? (Yes/No)
2.  What is the difference between an "Imperative" command and a "Declarative" task?
3.  Why is "Idempotency" useful when updating 500 routers at once?


---

## 📺 Video Tutorial: Watch & Learn
For a visual walkthrough of the concepts in this lab, check out this helpful tutorial:
[https://www.youtube.com/watch?v=j9_t_p1p8-k](https://www.youtube.com/watch?v=j9_t_p1p8-k)
