# AWX Lab 4: The Guardrails (RBAC & Organizations)

Automation is a superpower. In a large company, you don't give superpowers to everyone. You acting as **SX-user** (an Org Admin) will learn how to create a "Junior Engineer" user who can run automation but cannot change it.

---

## 🧠 Core Concept: Multi-Tenancy
AWX uses **Organizations** to separate different teams. This ensures that the Security team can't accidentally delete the Network team's configurations.

---

## Part 1: Teams 👥

### 📖 What is a Team?
A **Team** is a subdivision within an Organization. It is a group of users who typically share the same job function (e.g., "Helpdesk" or "Network-Ops").

### 🎯 What is the Purpose?
The purpose is group management. Instead of giving permissions to 50 individual people one-by-one, you give the permission to the **Team**.

### Step-by-Step:
1.  Click **Teams** in the left menu -> Click **Add**.
2.  **Name:** 
    ```text
    Junior Network Admins
    ```
3.  **Organization:** Select your `Org-SX`.
4.  Click **Save**.

---

## Part 2: Users 👤

### 📖 What is a User?
A **User** is an individual account that can log into the AWX web interface.

### 🎯 What is the Purpose?
The purpose is accountability and security. By giving every person their own account, AWX creates an "Audit Trail." 

### Step-by-Step:
1.  Click **Users** in the left menu -> Click **Add**.
2.  **Username:** 
    ```text
    SX-junior
    ```
3.  **Organization:** Select your `Org-SX`.
4.  **Password:** 
    ```text
    800-ePlus
    ```
5.  Click **Save**.
6.  Go to **Teams** -> **Junior Network Admins** -> **Users** tab.
7.  Click **Add** and select your new **SX-junior** user.

---

## Part 3: Role-Based Access Control (RBAC) 🔑

### 📖 What is RBAC?
**RBAC** is a security model where permissions are attached to "Roles" (like *Execute* or *Admin*) rather than individuals.

### 🎯 What is the Purpose?
The purpose is "Safe Delegation." You want to give a junior engineer the power to fix a router (Execute), but you don't want them to be able to change the underlying code.

### Step-by-Step:
1.  Click **Templates** -> Click on `01 - Gather Cisco Facts`.
2.  Click the **Access** tab at the top -> Click **Add**.
3.  Select your **Team**: `Junior Network Admins`. Click **Next**.
4.  **Role:** Select **Execute**.
5.  Click **Save**.

---

## Part 4: The Proof 🧪

### Step-by-Step:
1.  Log out of AWX.
2.  Log back in as the junior user: **`SX-junior`**.
3.  Notice how your menu is restricted.
4.  Try to edit a template. You should find that you cannot change any settings—you can only click the **Rocket Ship 🚀** to launch it!

---

## 📂 Deep Dive: The RBAC Inheritance Model
AWX uses a **Hierarchical Permission Model**. Permissions flow from the top down. If you give a user 'Admin' rights at the **Organization** level, they automatically inherit Admin rights to every Inventory, Project, and Template inside that Org. This is why we practice the **Principle of Least Privilege**.

In this lab, you gave the `SX-junior` user the **'Execute'** role. Notice that they did *not* get the ability to see the Credentials. This is a brilliant piece of security engineering: AWX allows a user to *use* a password without ever *knowing* the password. The junior user can log into a router, but they can't see the `800-ePlus` password in the UI.

Lastly, consider the **'Auditor'** role. This is a special role that allows a user to see everything—all configurations, all job results—but they cannot change or run anything. This is perfect for compliance officers who need to verify that the network is being managed correctly without being able to disrupt operations.

---

## ❓ Knowledge Check
1.  Why is it better to assign permissions to a **Team** rather than a **User**?
2.  What is the difference between the **Admin** role and the **Execute** role?
3.  Can a user with the **Execute** role see the passwords stored in a Credential?
