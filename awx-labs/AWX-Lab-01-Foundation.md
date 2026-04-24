# AWX Lab 1: The Enterprise Foundation (Tenant Setup & First Job)

Welcome to AWX! 🏢 In this first lab, you will act as a **System Administrator** to build your own private "Sandbox" (Organization). Then, you will switch to a daily user account to run your first automated job.

---

## 🧠 Core Concept: The Isolated Tenant
AWX is a **multi-tenant** platform. This means many different teams can use the same server without seeing each other's work. 
- **Organization:** Your private "folder" on the server.
- **Organization Admin:** A user who has full control over an Organization but cannot touch global server settings.

---

## Part 0: Creating Your Command Center (Tenant Setup) 🏗️

### 📖 What is an Organization?
An **Organization** is the highest level of grouping in AWX. It is a secure container that holds its own Inventories, Projects, and Users.

### 🎯 What is the Purpose?
The purpose is **Isolation**. By creating your own Org, you ensure that your automation doesn't collide with other students. You can use identical names for your templates, and your job history remains private.

### Step-by-Step (As System Admin):
1.  Login to AWX as your assigned student account (e.g., `S1`).
2.  Click **Organizations** in the left menu -> Click **Add**.
3.  **Name:** `Org-SX` (Replace `X` with your student number, e.g., `Org-S5`).
4.  Click **Save**.
5.  Click **Users** in the left menu -> Click **Add**.
6.  **Username:** `SX-user` (e.g., `S5-user`).
7.  **Password:** `800-ePlus`
8.  **Organization:** Select your new `Org-SX`.
9.  Click **Save**.

### Granting "Org Admin" Powers:
1.  Go back to **Organizations** -> Click on your `Org-SX`.
2.  Click the **Access** tab at the top -> Click **Add**.
3.  Select your new user: `SX-user`. Click **Next**.
4.  **Role:** Select **Organization Admin**.
5.  Click **Save**.

**🛑 STOP & SWITCH:** Log out of AWX. Log back in as your new account: **`SX-user`**. You will now complete all future labs using this account.

---

## Part 1: Storing Secrets (Credentials) 🔐

### 📖 What is a Credential?
A **Credential** is a secure, encrypted container within AWX that stores sensitive authentication data.

### 🎯 What is the Purpose?
It allows AWX to log into your routers automatically while keeping the passwords hidden from human eyes.

### Step-by-Step (As SX-user):
1.  Click **Credentials** -> **Add**.
2.  **Name:** `Cisco Router Login`
3.  **Organization:** Select your `Org-SX`.
4.  **Credential Type:** **Machine**.
5.  **Username:** `admin` | **Password:** `800-ePlus`
6.  **Become Method:** `enable` | **Become Password:** `800-ePlus`
7.  Click **Save**.

---

## Part 2: Connecting to the Code (Projects) 📦

### 📖 What is a Project?
A **Project** is a logical link between AWX and your **GitHub** repository.

### 🎯 What is the Purpose?
It ensures you are always running the latest version of your playbooks.

### Step-by-Step:
1.  Click **Projects** -> **Add**.
2.  **Name:** `DLR Workshop Code`
3.  **Organization:** Select your `Org-SX`.
4.  **Source Control Type:** **Git**.
5.  **Source Control URL:** `https://github.com/actswartz/dlr`
6.  Click **Save**. Wait for the status to turn **Green**.

---

## Part 3: Defining the Target (Inventory) 🗂️

### 📖 What is an Inventory?
A collection of **Hosts** (your routers) and their specific data.

### Step-by-Step:
1.  Click **Inventories** -> **Add** -> **Add Inventory**.
2.  **Name:** `Student Pod Inventory` | **Organization:** `Org-SX`.
3.  Click **Save**.
4.  Click the **Hosts** tab -> **Add** -> **Add New Host**.
5.  **Name:** `SX-R1` (e.g., `S5-R1`).
6.  **Variables:** In the YAML box, paste: `ansible_host: 172.20.20.X` (Use your router IP).
7.  *Repeat for R2 and R3.*

---

## Part 4: The Start Button (Job Template) 🚀

### 📖 What is a Job Template?
A definition that ties your code, targets, and login together into a single executable unit.

### Step-by-Step:
1.  Click **Templates** -> **Add** -> **Add Job Template**.
2.  **Name:** `01 - Gather Cisco Facts`
3.  **Inventory:** `Student Pod Inventory`.
4.  **Project:** `DLR Workshop Code`.
5.  **Playbook:** `lab01_facts.yml`.
6.  **Credentials:** `Cisco Router Login`.
7.  Click **Save** -> **Launch**.

---

## 📂 Deep Dive: The Principle of Least Privilege
By switching from `S1` (System Admin) to `S1-user` (Org Admin), you are practicing a core security standard. If you make a mistake now, you can only break things inside your own organization. You cannot accidentally delete another student's routers or crash the entire server. This is how professional automation environments are managed.
