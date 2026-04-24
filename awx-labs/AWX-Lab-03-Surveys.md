# AWX Lab 3: The Self-Service Portal (Surveys & User Input)

In your CLI labs, if you wanted to change the router banner, you had to edit a YAML file and run a command. In an enterprise, you might want a Helpdesk worker to be able to change a banner *without* knowing anything about YAML or Git. In this lab, you will build a **Survey** to make that possible.

---

## 🧠 Core Concept: Abstraction
A **Survey** is a web form that asks the user questions. AWX takes the answers and turns them into **Extra Variables** (`-e` flag in CLI). This "abstracts" the complexity away from the user—they see a form, you handle the code.

---

## Part 1: The Job Template 🛠️

### 📖 What is a Job Template? (Review)
A **Job Template** is the blueprint for a task. It combines your code, your targets, and your credentials.

### 🎯 What is the Purpose?
The purpose is to create a repeatable, standard way to run a playbook. In this lab, the template acts as the "Engine" that will power our self-service web form.

### Step-by-Step:
1.  In the left menu, click **Templates**.
2.  Click **Add** -> **Add Job Template**.
3.  **Name:** `03 - Self-Service Banner Change`
4.  **Inventory:** `Student Pod Inventory`.
5.  **Project:** `DLR Workshop Code`.
6.  **Playbook:** `lab02_banner.yml`.
7.  **Credentials:** `Cisco Router Login`.
8.  Click **Save**.

---

## Part 2: Building the Survey 📝

### 📖 What is a Survey?
A **Survey** is a user-friendly interface layer added on top of a Job Template. It consists of questions (text boxes, dropdowns, etc.) that the user must answer before the job starts.

### 🎯 What is the Purpose?
The purpose of a Survey is to allow non-technical people to interact with Ansible safely. Instead of letting a user edit your code (where they might make a typo), you give them a simple box to type in. This makes automation accessible to the entire company.

### Step-by-Step:
1.  On the Template details screen, click the **Survey** tab at the top.
2.  Click the **Add** button.
3.  **Question:** `What text should we put in the MOTD banner?`
4.  **Answer Variable Name:** `banner_text`
    > **💡 Bonus Note:** This is the most important field! This name must match the variable name inside your Ansible playbook. 
5.  **Answer Type:** Select **Textarea** (this allows for multiple lines).
6.  **Required:** Check the box.
7.  Click **Save**.
8.  **Toggle the Switch:** On the Survey screen, click the toggle to **Enabled**.

---

## Part 3: Variable Injection 🔗

### 📖 What is Variable Injection?
**Variable Injection** is the process where AWX takes the text typed into a Survey box and "injects" it into the Ansible playbook as a variable at runtime.

### 🎯 What is the Purpose?
The purpose is to make your automation dynamic. Instead of having a playbook that *always* sets the banner to "Hello," you have a playbook that sets the banner to *whatever the user typed in*.

### Task: Edit your code in GitHub (or on the Lab Server)
Change your `lab02_banner.yml` to look like this:

```yaml
---
- name: Configure MOTD Banner
  hosts: routers
  gather_facts: false
  tasks:
    - name: Set Message of the Day
      cisco.ios.ios_banner:
        banner: motd
        # We replace the hard-coded text with our variable from the survey!
        text: "{{ banner_text | default('Welcome to the Network') }}"
        state: present
```

---

## Part 4: The Launch Experience 🚀

### Step-by-Step:
1.  Go back to **Templates** in AWX.
2.  Click the Rocket ship 🚀 icon next to `03 - Self-Service Banner Change`.
3.  **The Form Appears!** You are now prompted to enter the banner text.
4.  Type a creative message: `Warning: This Pod is under the control of Student X!`
5.  Click **Next** -> **Launch**.
6.  Watch the Job output. Look for the "Variables" section to see `banner_text` being passed in.

---

## ❓ Knowledge Check
1.  What does a Survey turn user input into?
2.  What happens if the "Answer Variable Name" in the survey doesn't match the variable in your playbook?
3.  Why is "Textarea" better than "Text" for a router banner?

---

## 📂 Deep Dive: Survey Validation
In a real environment, you don't want users typing *anything* they want. You can use **Regular Expressions (Regex)** in a survey to validate the input. For example, if you were asking for a VLAN number, you could set the "Answer Type" to **Integer** and set a range of `1 to 4094`. This prevents users from breaking the network with invalid data.
