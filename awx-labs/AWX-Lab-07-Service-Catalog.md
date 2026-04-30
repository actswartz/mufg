# AWX Lab 7: The Professional Portal (Service Cataloging)

In Lab 3, you built a survey where a user could type in anything. In a professional environment, "typing anything" is dangerous. **Service Cataloging** is the practice of providing pre-approved, valid choices to users. In this lab, you acting as **SX-user** will build a "Safe Dropdown" tool to manage interface descriptions.

---

## 🧠 Core Concept: The "Safe" UI
A professional service catalog doesn't ask "What is the interface name?" It provides a list of valid interfaces. This eliminates typos, prevents users from trying to configure non-existent hardware, and ensures 100% compliance with company standards.

---

## Part 1: Preparing the "Menu" 📋

### 📖 What is a Survey Dropdown?
A **Dropdown** (or "Multiple Choice") question in a survey restricts the user to a specific list of answers that you, the architect, have defined.

### 🎯 What is the Purpose?
The purpose is **Error Prevention**. If a user tries to configure "Eth 0/1" but your router calls it "Ethernet0/1," the automation will fail. By using a dropdown, you ensure the user picks the *exact* string the router expects.

### Step-by-Step (As SX-user):
1.  In the left menu, click **Templates**.
2.  Find your `03 - Self-Service Banner Change` template and click on its name.
3.  Click the **Survey** tab.
4.  Click **Add** to create a new question.
5.  **Question:** 
    ```text
    Which interface do you want to update?
    ```
6.  **Answer Variable Name:** 
    ```text
    target_interface
    ```
7.  **Answer Type:** Select **Multiple Choice (Single Select)**.
8.  **Choices:** Enter the following (one per line):
    ```text
    Ethernet0/1
    Ethernet0/2
    Ethernet0/3
    ```
9.  **Required:** Check the box.
10. Click **Save**.

---

## Part 2: Building the Dynamic Logic 🔗

### 📖 What is Dynamic Target Logic?
This is when your playbook uses a variable from a survey (the dropdown choice) to decide *which* specific piece of hardware to touch.

### 🎯 What is the Purpose?
It allows your playbook to be a "Multi-Tool." Instead of 3 playbooks (one for each interface), you have 1 playbook that can adapt to whichever interface the user picks from the menu.

### Task: Understand the Playbook logic
The `lab07_description.yml` file in your GitHub project is designed to use the variable from your survey:

```yaml
---
- name: Lab 7 - Service Catalog Interface Update
  hosts: routers
  gather_facts: false
  tasks:
    - name: Apply standard description
      cisco.ios.ios_interfaces:
        config:
          - name: "{{ target_interface }}"
            description: "Updated via Service Portal by SX-user"
            enabled: true
        state: merged
```

---

## Part 3: The User Experience (UX) 🚀

### Step-by-Step:
1.  In AWX, update your Job Template to use the `lab07_description.yml` playbook.
2.  Click **Save**.
3.  Click the **Rocket Ship 🚀** icon.
4.  Notice how the user can no longer type the interface name. They *must* pick from your predefined menu.
5.  Select `Ethernet0/1` and click **Next** then **Launch**.
6.  **Verify:** Log into your router and run:
    ```bash
    show run interface Ethernet0/1
    ```

---

## 📂 Deep Dive: The Service Catalog Ecosystem
In a true enterprise, AWX is often "hidden" behind a tool like **ServiceNow** or **Jira.** These tools act as the "Storefront" where a user clicks a button to request a service. When they hit 'Submit,' ServiceNow sends an API call to AWX, which runs the playbook. This is known as **Northbound Integration**.

The power of the dropdowns you built in this lab is that they map perfectly to these external portals. By creating strict "Multiple Choice" questions, you are creating a "Contract" between the user and the automation. There is no room for interpretation or human error.

Furthermore, consider **Dynamic Dropdowns**. While we typed our choices manually in this lab, advanced AWX users use the **AWX API** to populate those choices. For example, the dropdown could automatically query a database to show only the interfaces that are currently "down." This is known as **Intelligent Self-Service**.

---

## ❓ Knowledge Check
1.  What is the primary benefit of a **Multiple Choice** question over a **Textarea**?
2.  In Part 2, what variable did we use to tell the playbook which interface to touch?
3.  What is "Northbound Integration" in the context of a Service Catalog?
