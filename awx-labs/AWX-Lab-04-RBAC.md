# AWX Lab 4: The Guardrails (RBAC & Organizations)

Automation is a superpower. In a large company, you don't give superpowers to everyone. You use **RBAC** (Role-Based Access Control) to give people exactly the permissions they need—and no more. In this lab, you will learn how to create a "Junior Engineer" user who can run automation but cannot change it.

---

## 🧠 Core Concept: Multi-Tenancy
AWX uses **Organizations** to separate different teams.
- **Organization:** A container for resources (like a company department).
- **Team:** A group of users within an organization.
- **Role:** A specific permission (Admin, Auditor, Execute).

---

## Part 1: Organizations & Teams 👥

### 📖 What is an Organization?
An **Organization** is the highest level of grouping in AWX. It is like a "folder" that holds its own Inventories, Projects, and Users.

### 🎯 What is the Purpose?
The purpose is isolation. A large company like Google or Nike might have thousands of engineers. Organizations ensure the "Security Team" can't accidentally delete the "Router Team's" playbooks.

### Step-by-Step:
1.  In the left menu, click **Organizations**.
2.  Click **Add**.
3.  **Name:** `Engineering Dept`
4.  Click **Save**.
5.  Now click **Teams** in the left menu.
6.  Click **Add**.
7.  **Name:** `Junior Network Admins`
8.  **Organization:** `Engineering Dept`
9.  Click **Save**.

---

## Part 2: Users 👤

### 📖 What is a User?
A **User** is an individual account that can log into the AWX web interface.

### 🎯 What is the Purpose?
The purpose is accountability and security. By giving every student their own user account, you can see an "Audit Trail" of exactly who ran which playbook and at what time. It also allows you to revoke access for one person without affecting the rest of the team.

### Step-by-Step:
1.  Click **Users** in the left menu.
2.  Click **Add**.
3.  **Username:** `junior_user`
4.  **Organization:** `Engineering Dept`
5.  **Password:** `Ansible123!`
6.  **Confirm Password:** `Ansible123!`
7.  **User Type:** Normal User.
    > **💡 Bonus Note:** Never make a standard user a "System Administrator" unless they need to delete the entire AWX server!
8.  Click **Save**.

---

## Part 3: Role-Based Access (RBAC) 🔑

### 📖 What is RBAC?
**Role-Based Access Control** is a security model where permissions are attached to "Roles" (like *Execute* or *Admin*) rather than individuals.

### 🎯 What is the Purpose?
The purpose is "Safe Delegation." You want to give a junior engineer the power to fix a router (Execute), but you don't want them to be able to change the underlying code or see the admin passwords (Admin). RBAC provides these "Guardrails."

### Step-by-Step:
1.  Click **Templates** in the left menu.
2.  Click on the template you made in Lab 3: `03 - Self-Service Banner Change`.
3.  Click the **User Access** (or **Access**) tab at the top.
4.  Click **Add**.
5.  Select your user: `junior_user`.
6.  Click **Next**.
7.  **Role:** Select **Execute**.
    > **🔍 Understanding Roles:**
    > - **Admin:** Can change the code, credentials, and delete the template.
    > - **Execute:** Can only click the "Launch" button and fill out the survey.
8.  Click **Save**.

---

## Part 4: The Proof 🧪

Log out of AWX and log back in as the `junior_user` / `Ansible123!` to see the restricted view.

---

## ❓ Knowledge Check
1.  What does RBAC stand for?
2.  What is the difference between the **Admin** role and the **Execute** role?
3.  Why is it safe to give a user "Execute" permission even if they don't know the router password?

---

## 📂 Deep Dive: Permission Inheritance
Permissions in AWX flow "downwards." If you give a Team "Admin" permission on an **Organization**, they automatically become admins of every Inventory, Project, and Template *inside* that organization. To be safe, always try to give permissions at the lowest level possible (the specific Template) rather than the highest level. This is known as the **Principle of Least Privilege**.
