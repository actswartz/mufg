# AWX Lab 3: The Self-Service Portal (Surveys & User Input)

In your CLI labs, if you wanted to change the router banner, you had to edit a YAML file and run a command. In an enterprise, you might want a Helpdesk worker to be able to change a banner without knowing anything about YAML or Git. In this lab, you acting as **SX-user** will build a **Survey** to make that possible.

---

## 🧠 Core Concept: Abstraction
A **Survey** is a web form that asks the user questions. AWX takes the answers and turns them into **Extra Variables**. This "abstracts" the complexity away from the user—they see a simple form, while you handle the code.

---

## Part 1: The Job Template 🛠️

### 📖 What is a Job Template?
A **Job Template** is the blueprint for an automated task. It is the "Start Button" that combines your code, your targets, and your login credentials into one repeatable unit.

### 🎯 What is the Purpose?
The purpose is standardization. It ensures that every time a task is run, it uses the exact same version of the code and the same security settings. In this lab, the template acts as the engine that will power our self-service web form.

### Step-by-Step:
1.  In the left menu, click **Templates**.
2.  Click **Add** -> **Add Job Template**.
3.  **Name:** 
4.  **Inventory:** .
5.  **Project:** .
6.  **Playbook:** .
7.  **Credentials:** .
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
3.  **Question:** 
4.  **Answer Variable Name:** my_variable
    > **💡 Bonus Note:** This is the most important field! This name must match the variable name inside your Ansible playbook (). 
5.  **Answer Type:** Select **Textarea** (this allows for multiple lines).
6.  **Required:** Check the box.
7.  Click **Save**.
8.  **Toggle the Switch:** On the Survey screen, click the toggle to **Enabled**.

---

## Part 3: Variable Injection 🔗

### 📖 What is Variable Injection?
**Variable Injection** is the process where AWX takes the text typed into a Survey box and "injects" it into the Ansible playbook as a variable at runtime.

### 🎯 What is the Purpose?
The purpose is to make your automation dynamic. Instead of having a playbook that *always* sets the banner to "Hello, world!", you have a playbook that sets the banner to *whatever the user currently needs*.

### Task: Verify your code in GitHub
Ensure your  is updated to use the variable:


---

## Part 4: The Launch Experience 🚀

### Step-by-Step:
1.  Go back to **Templates** in AWX.
2.  Click the Rocket ship 🚀 icon next to your template.
3.  **The Form Appears!** Enter a message and click **Launch**.

---

## 📂 Deep Dive: Variable Precedence and Injection
When a user fills out a Survey, they are creating what Ansible calls **'Extra Vars'** (Extra Variables). In the hierarchy of Ansible, Extra Vars are the most powerful variables in existence. They sit at the very top of the **Precedence Pyramid**. This means that even if you have a variable defined in your inventory, your playbook, or your role, the value from the Survey will always "win" and overwrite them.

This power comes with a responsibility: **Validation**. In a production environment, you don't just want a blank text box. AWX Surveys allow you to use **Regular Expressions (Regex)** to enforce rules. For example, if you were asking for a VLAN ID, you could use a regex to ensure the user only types numbers between 1 and 4094. This turns your survey into a safety barrier, preventing human typos from ever reaching your production routers.

Another advanced technique is the use of **'Multiple Choice'** survey questions. Instead of letting a user type the name of a site, you can give them a dropdown menu populated by another inventory. This ensures that the user can only choose valid targets that actually exist in your network. This is known as **'Service Cataloging,'** and it is how large IT departments provide self-service tools to thousands of employees.

Finally, notice that the Survey answers are recorded in the **Job Environment** data. If a change causes a network outage, an auditor can look back at the job and see exactly what the user typed into the box. This provides a clear link between a human decision and an automated action, which is vital for troubleshooting and accountability.
