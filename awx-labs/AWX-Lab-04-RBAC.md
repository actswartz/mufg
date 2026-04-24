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
The purpose is group management. Instead of giving permissions to 50 individual people one-by-one, you give the permission to the **Team**. When a new person joins the company, you just add them to the Team, and they instantly get all the access they need.

### Step-by-Step:
1.  Click **Teams** in the left menu -> Click **Add**.
2.  **Name:** 
3.  **Organization:** Select your .
4.  Click **Save**.

---

## Part 2: Users 👤

### 📖 What is a User?
A **User** is an individual account that can log into the AWX web interface.

### 🎯 What is the Purpose?
The purpose is accountability and security. By giving every person their own account, AWX creates an "Audit Trail." You can see exactly who ran which playbook and at what time.

### Step-by-Step:
1.  Click **Users** in the left menu -> Click **Add**.
2.  **Username:**  (e.g., ).
3.  **Organization:** Select your .
4.  **Password:** 
5.  Click **Save**.
6.  Go to **Teams** -> **Junior Network Admins** -> **Users** tab.
7.  Click **Add** and select your new .

---

## Part 3: Role-Based Access Control (RBAC) 🔑

### 📖 What is RBAC?
**RBAC** is a security model where permissions are attached to "Roles" (like *Execute* or *Admin*) rather than individuals.

### 🎯 What is the Purpose?
The purpose is "Safe Delegation." You want to give a junior engineer the power to fix a router (Execute), but you don't want them to be able to change the underlying code or see the admin passwords (Admin). RBAC provides these "Guardrails."

### Step-by-Step:
1.  Click **Templates** -> .
2.  Click the **User Access** (or **Access**) tab -> Click **Add**.
3.  Select your **Team**: . Click **Next**.
4.  **Role:** Select **Execute**.
5.  Click **Save**.

---

## Part 4: The Proof 🧪

Log out and log back in as the . Notice how your menu is restricted and you cannot edit the template—you can only launch it!

---

## 📂 Deep Dive: The RBAC Inheritance Model
AWX uses a **Hierarchical Permission Model**, which is designed to minimize the amount of work an admin has to do. Permissions flow from the top down. If you give a user 'Admin' rights at the **Organization** level, they automatically inherit Admin rights to every Inventory, Project, and Template inside that Org. This is convenient, but it can be dangerous. This is why we practice the **Principle of Least Privilege**.

In this lab, you gave the  the **'Execute'** role on a specific template. Notice that they did *not* get the ability to see the Credentials. This is a brilliant piece of security engineering: AWX allows a user to *use* a password without ever *knowing* the password. The  can log into a router using the  account, but they can't see the  password in the UI, and they can't even see the stars () because they don't have access to the Credential object itself.

Teams add another layer of efficiency. In a real company, you don't manage 500 individual users. You manage 5 **Teams** (e.g., 'Level-1-NOC', 'Architecture', 'Security-Auditors'). You assign the permissions to the Team, and then you simply drop users into the Team. If an employee changes jobs or leaves the company, you just remove them from the Team, and their access across the entire AWX infrastructure is instantly revoked.

Lastly, consider the **'Auditor'** role. This is a special role that allows a user to see everything—all configurations, all job results, all inventories—but they cannot change or run anything. This is perfect for compliance officers who need to verify that the network is being managed correctly without being able to accidentally (or intentionally) disrupt operations.
