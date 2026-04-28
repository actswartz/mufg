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
An **Organization** is the foundational building block of multi-tenancy within AWX. It serves as the highest-level logical container that partitions resources, users, and permissions. Think of it as a completely isolated "business unit" or "department" on the server. Within an Organization, you manage your own Inventories, Projects, and Job Templates, ensuring that your automation environment remains distinct and secure from other teams sharing the same AWX instance. It allows for delegated administration, where an "Organization Admin" can manage their team's assets without requiring global System Administrator privileges.

### 🎯 What is the Purpose?
The purpose is **Isolation**. By creating your own Org, you ensure that your automation doesn't collide with other students. You can use identical names for your templates, and your job history remains private.

### Step-by-Step (As System Admin):
1.  Login to AWX as your assigned student account (e.g., `S1`).
2.  Click **Organizations** in the left menu -> Click **Add**.
3.  **Name:** `Org-SX` (Replace `X` with your student number, e.g., `Org-S1`)
4.  Click **Save**.
5.  Click **Users** in the left menu -> Click **Add**.
6.  **Username:** `SX-user` (e.g., `S1-user`)
7.  **Password:** `800-ePlus`
8.  **Organization:** Select your new `Org-SX`.
9.  Click **Save**.

### Granting "Org Admin" Powers:
1.  Go back to **Organizations** -> Click on your `Org-SX`.
2.  Click the **Access** tab at the top -> Click **Add**.
3.  Select your new user: `SX-user`. Click **Next**.
4.  **Role:** Select `Organization Admin`.
5.  Click **Save**.

**🛑 STOP & SWITCH:** Log out of AWX. Log back in as your new account: **`SX-user`**. You will now complete all future labs using this account.

---

## Part 1: Storing Secrets (Credentials) 🔐

### 📖 What is a Credential?
A **Credential** is a secure, encrypted storage mechanism within AWX designed to handle sensitive authentication data required to interact with managed nodes, version control systems, or external cloud providers. Instead of embedding passwords, SSH keys, or API tokens directly into your playbooks or scripts—which is a significant security risk—you store them in AWX Credentials. AWX then "injects" these secrets into the automation environment only at runtime, ensuring they are never exposed in logs or to unauthorized users. This centralizes secret management and allows for easy rotation of passwords across thousands of devices simultaneously.

### 🎯 What is the Purpose?
It allows AWX to log into your routers automatically while keeping the passwords hidden from human eyes.

### Step-by-Step (As SX-user):
1.  Click **Credentials** -> **Add**.
2.  **Name:** 
    ```text
    Cisco Router Login
    ```
3.  **Organization:** Select your `Org-SX`.
4.  **Credential Type:** `Machine`.
5.  **Username:** 
    ```text
    admin
    ```
6.  **Password:** 
    ```text
    800-ePlus
    ```
7.  **Become Method:** `enable`
8.  **Become Password:** 
    ```text
    800-ePlus
    ```
9.  Click **Save**.

---

## Part 2: Connecting to the Code (Projects) 📦

### 📖 What is a Project?
A **Project** represents a logical link between AWX and a specific Version Control System (VCS) repository, such as GitHub, GitLab, or Bitbucket, where your Ansible playbooks, roles, and files are stored. By defining a Project, you are telling AWX where to find the "source of truth" for your automation code. This integration enables modern DevOps workflows like "Infrastructure as Code" (IaC), allowing you to trigger automation directly from code updates. AWX can automatically synchronize with your repository to ensure that every job execution uses the most recent, peer-reviewed version of your automation logic.

### 🎯 What is the Purpose?
It ensures you are always running the latest version of your playbooks.

### Step-by-Step:
1.  Click **Projects** -> **Add**.
2.  **Name:** 
    ```text
    AAP Workshop Code
    ```
3.  **Organization:** Select your `Org-SX`.
4.  **Source Control Type:** `Git`.
5.  **Source Control URL:** 
    ```text
    https://github.com/actswartz/mufg
    ```
6.  Click **Save**. Wait for the status to turn **Green**.

---

## Part 3: Defining the Target (Inventory) 🗂️

### 📖 What is an Inventory?
An **Inventory** is a structured collection of **Hosts** (the servers, routers, or switches you want to automate) and the specific metadata or variables associated with them. In AWX, inventories go beyond just a list of IP addresses; they allow you to group devices by function, location, or environment (e.g., "production" vs "staging"). You can define variables at the group level (shared by many hosts) or the individual host level. This allows Ansible to make intelligent decisions, such as applying a specific configuration only to Arista switches in the Dallas data center while ignoring Cisco routers in New York.

**Example of what the Groups should look like:**
```yaml
---
all:
  children:
    routers:
      hosts:
        R1:
        R2:
        R3:
```

**Example of what the individual Host Variables should look like:**
When you click on a specific host (like R1), you define its unique IP address in the Variables box:
```yaml
ansible_host: 172.20.20.44
```

### Step-by-Step:
1.  Click **Inventories** -> **Add** -> **Add Inventory**.
2.  **Name:** 
    ```text
    Student Pod Inventory
    ```
3.  **Organization:** `Org-SX`.
4.  Click **Save**.
5.  Click the **Groups** tab -> **Add**.
6.  **Name:** 
    ```text
    routers
    ```
7.  Click **Save**.
8.  Click the **Hosts** tab -> **Add** -> **Add New Host**.
9.  **Name:** 
    ```text
    R1
    ```
10. **Variables:** In the YAML box, paste your IP (Replace `X` with your specific R1 IP):
    ```yaml
    ansible_host: 172.20.20.X
    ```
11. *Repeat for R2 and R3.* (e.g., R2: `172.20.20.45`, R3: `172.20.20.46`)

---

## Part 4: The Start Button (Job Template) 🚀

### 📖 What is a Job Template?
A **Job Template** is the "blueprints" or "execution definition" that orchestrates all the individual components of your automation into a repeatable task. It acts as the glue that ties together a specific **Playbook** (from a Project), a target set of devices (from an **Inventory**), and the necessary authentication (from a **Credential**). Beyond just launching a playbook, a Job Template allows you to define the runtime environment (Execution Environment), verbosity levels, and "Surveys" that prompt users for input before a job starts. Once a template is defined, any authorized user can run complex automation with a single click, ensuring consistent results every time.

### Step-by-Step:
1.  Click **Templates** -> **Add** -> **Add Job Template**.
2.  **Name:** 
    ```text
    01 - Gather Cisco Facts
    ```
3.  **Inventory:** `Student Pod Inventory`.
4.  **Project:** `AAP Workshop Code`.
5.  **Playbook:** 
    ```text
    lab01_facts.yml
    ```
6.  **Credentials:** `Cisco Router Login`.
7.  Click **Save -> Launch**.

---

## 📂 Deep Dive: The Anatomy of a Job Launch
When you click that blue **Launch** button, a complex chain of events happens behind the scenes in the AWX "Control Plane." First, AWX creates a temporary environment called an **Execution Environment (EE)**. This is a lightweight Linux container that contains only the specific Python libraries and Ansible collections needed to talk to your Cisco hardware. This isolation is crucial because it prevents one job from "infecting" another with conflicting library versions.

Once the EE is running, AWX performs a **Handshake** with your secrets. It securely pulls your router password from the encrypted database and "injects" it into the environment as an environment variable or a temporary file. This is why you never see the password in the job logs—AWX is shielding that sensitive data from being recorded in the standard output.

Next, AWX performs a **Project Update** (if you enabled it). It reaches out to GitHub to see if your `lab01_facts.yml` file has changed. If it has, it performs a `git pull` to ensure your automation is up-to-date. Finally, it starts the `ansible-playbook` command, targeting only the routers in your specific inventory. All of this orchestration happens in less than a second before the first task even begins.

Finally, consider the **Audit Trail**. Because you are now logged in as `SX-user`, every single character of output from this job is recorded and tied to your name. In a professional SOC (Security Operations Center), this is how engineers prove that a configuration change was authorized. You aren't just running a script; you are creating a permanent record of network maintenance that can be reviewed months or years later.
