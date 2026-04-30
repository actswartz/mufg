# AWX Lab 3: The Self-Service Portal (Surveys & User Input)

In your CLI labs, if you wanted to change the router banner, you had to edit a YAML file and run a command. In an enterprise, you might want a Helpdesk worker to be able to change a banner without knowing anything about YAML or Git. In this lab, you acting as **SX-user** will build a **Survey** to make that possible.

---

## 🧠 Core Concept: Abstraction
A **Survey** is a web form that asks the user questions. AWX takes the answers and turns them into **Extra Variables**. This "abstracts" the complexity away from the user—they see a simple form, while you handle the code.

---

## Part 1: The Job Template 🛠️

### 📖 What is a Job Template?
A **Job Template** is the blueprint for an automated task. It is the "Start Button" that combines your code, your targets, and your login credentials into one repeatable unit.

### Step-by-Step:
1.  In the left menu, click **Templates**.
2.  Click **Add** -> **Add Job Template**.
3.  Fill in the following details:
    *   **Name:** 
        ```text
        03 - Self-Service Banner Change
        ```
    *   **Inventory:** 
        ```text
        Student Pod Inventory
        ```
    *   **Project:** 
        ```text
        AAP Workshop Code
        ```
    *   **Playbook:** 
        ```text
        lab02_banner.yml
        ```
    *   **Credentials:** 
        ```text
        Cisco Router Login
        ```
4.  Click **Save**.

---

## Part 2: Building the Survey 📝

### 📖 What is a Survey?
A **Survey** is a user-friendly interface layer added on top of a Job Template. It consists of questions (text boxes, dropdowns, etc.) that the user must answer before the job starts.

### Step-by-Step:
1.  On the Template details screen, click the **Survey** tab at the top.
2.  Click the **Add** button.
3.  **Question:** 
    ```text
    What would you like the new login banner to say?
    ```
4.  **Answer Variable Name:** 
    ```text
    banner_text
    ```
    > **💡 Bonus Note:** This is the most important field! This name must match the variable name inside your Ansible playbook (`{{ banner_text }}`). 
5.  **Answer Type:** Select **Textarea**.
6.  **Required:** Check the box.
7.  Click **Save**.
8.  **Toggle the Switch:** On the Survey screen, click the toggle to **Enabled**.

---

## Part 3: Variable Injection & Validation 🔗

### 📖 What is Variable Injection?
**Variable Injection** is the process where AWX takes the text typed into a Survey box and "injects" it into the Ansible playbook as a variable at runtime.

### 🎯 What is the Purpose?
The purpose is to make your automation dynamic. Instead of having a playbook that *always* sets the banner to "Hello, world!", you have a playbook that sets the banner to *whatever the user currently needs*.

### 🛡️ Guardrails: Adding Regex Validation
In a professional environment, you don't want a user to accidentally put "garbage" data into your router.
1.  Click the **Edit** icon next to your survey question.
2.  In the **Regular Expression** box, paste:
    ```text
    ^[\w\s\.!\?-]+$
    ```
    > **🧠 Pro-Tip:** This regex ensures the user only types letters, numbers, and basic punctuation. It prevents them from using special characters that might break the Cisco CLI.

---

## Part 4: The Launch Experience 🚀

### Step-by-Step:
1.  Go back to **Templates** in AWX.
2.  Click the Rocket ship 🚀 icon next to your template.
3.  **The Form Appears!** Enter a professional message (e.g., `Authorized Access Only. All activities are monitored.`) and click **Launch**.
4.  **Verify:** Once the job finishes, log into your router and run:
    ```bash
    show run | include banner
    ```

---

## 📂 Deep Dive: Variable Precedence and the "Pyramid of Power"
When a user fills out a Survey, they are creating what Ansible calls **'Extra Vars'** (Extra Variables). In the hierarchy of Ansible, Extra Vars are the most powerful variables in existence. They sit at the very top of the **Precedence Pyramid**.

**Why is this important?** 
Imagine you have a default banner defined in your `group_vars/all.yml` file. If you run the playbook normally, that default banner wins. However, when you launch via a Survey, the Survey value **overwrites** the default value for that specific job execution. This allows you to have "Safe Defaults" for 99% of the time, while still allowing "One-Off Exceptions" via the UI.

Furthermore, notice that the Survey answers are recorded in the **Job Environment** data. If a change causes a network outage, an auditor can look back at the job and see exactly what the user typed into the box. This provides a clear link between a human decision and an automated action, which is vital for troubleshooting and accountability. In a modern SOC (Security Operations Center), this transparency is the difference between a "mystery outage" and a "documented event."

---

## ❓ Knowledge Check
1.  What is the benefit of a "Survey" compared to editing a YAML file in Git?
2.  Where does a Survey Variable sit in the Ansible Precedence hierarchy?
3.  Why is Regex validation important when asking for user input?
