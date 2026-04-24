# AWX Lab 1: The Enterprise Foundation (Credentials & Projects)

Welcome to your first AWX lab! 🏢 Up until now, you've been running Ansible from a "CLI" (Command Line Interface). While powerful, CLI automation is hard to share with a team. **AWX** provides a central platform where automation can be scheduled, secured, and audited.

---

## 🧠 Core Concept: The AWX "Legos"
To run a job in AWX, you need four pieces to click together:
1.  **Inventory:** Which routers am I talking to?
2.  **Credential:** What is the username and password?
3.  **Project:** Where is my Ansible code (GitHub)?
4.  **Job Template:** The "Start Button" that ties the other three together.

---

## Part 1: Storing Secrets (Credentials) 🔐

### 📖 What is a Credential?
A **Credential** is a secure, encrypted container within AWX that stores authentication data, such as passwords, SSH private keys, or API tokens.

### 🎯 What is the Purpose?
The purpose of a Credential is to allow AWX to log into your routers automatically while keeping the passwords hidden from human eyes. Instead of typing a password into a text file, you "attach" the credential to a job, and AWX handles the handshake securely.

### Step-by-Step:
1.  In the AWX left-hand menu, click **Credentials**.
2.  Click the **Add** button.
3.  **Name:** `Cisco Router Login`
4.  **Credential Type:** Click the magnifying glass and select **Machine**.
    > **💡 Bonus Note:** "Machine" is the most common type. It tells AWX: "Use these details to SSH into a computer or router."
5.  **Username:** `admin`
6.  **Password:** `800-ePlus`
7.  **Become Method:** `enable` (standard for Cisco).
8.  **Become Password:** `800-ePlus`
9.  Click **Save**.

---

## Part 2: Connecting to the Code (Projects) 📦

### 📖 What is a Project?
A **Project** is a logical link between AWX and a Source Control Management (SCM) system, most commonly a **GitHub** repository.

### 🎯 What is the Purpose?
The purpose of a Project is to act as your "Source of Truth." Rather than manually uploading scripts, AWX "syncs" with GitHub to pull the latest versions of your playbooks. This ensures that every team member is always running the most up-to-date code.

### Step-by-Step:
1.  Click **Projects** in the left menu.
2.  Click **Add**.
3.  **Name:** `DLR Workshop Code`
4.  **Source Control Type:** Select **Git**.
5.  **Source Control URL:** `https://github.com/actswartz/dlr`
6.  **Source Control Update Options:** Check the box **"Clean"** and **"Delete on Update"**.
    > **💡 Bonus Note:** These options ensure that if you delete a file in GitHub, it also gets deleted in AWX. It keeps your code perfectly synced.
7.  Click **Save**.
8.  Wait for the status circle to turn **Green** (Successful).

---

## Part 3: Defining the Target (Inventory) 🗂️

### 📖 What is an Inventory?
An **Inventory** in AWX is a database collection of **Hosts** (your routers) and **Groups** (how you organize them).

### 🎯 What is the Purpose?
The purpose of an Inventory is to tell AWX exactly which devices should be targeted by your automation. It also allows you to store specific "Variables" for each device (like their unique IP addresses) so that one playbook can behave differently on each host.

### Step-by-Step:
1.  Click **Inventories** in the left menu.
2.  Click **Add** -> **Add Inventory**.
3.  **Name:** `Student Pod Inventory`
4.  Click **Save**.
5.  Now click the **Hosts** tab at the top of the screen.
6.  Click **Add** -> **Add New Host**.
7.  **Name:** `S1-R1` (Replace with your router name).
8.  **Variables:** In the YAML box, paste:
    ```yaml
    ansible_host: 172.20.20.2
    ```
    *(Repeat this for R2 and R3 with their respective IPs).*

---

## Part 4: The Start Button (Job Template) 🚀

### 📖 What is a Job Template?
A **Job Template** is a definition that combines a **Project** (the code), an **Inventory** (the target), and a **Credential** (the login) into a single executable unit.

### 🎯 What is the Purpose?
The purpose of a Job Template is to create a "Push-Button" experience. Instead of remembering complex CLI commands, a user can simply click the "Launch" button on a template. It standardizes how automation is run, ensuring that everyone uses the same settings every time.

### Step-by-Step:
1.  Click **Templates** in the left menu.
2.  Click **Add** -> **Add Job Template**.
3.  **Name:** `01 - Gather Cisco Facts`
4.  **Inventory:** Select `Student Pod Inventory`.
5.  **Project:** Select `DLR Workshop Code`.
6.  **Execution Environment:** Select the default (usually `AWX EE`).
    > **💡 Bonus Note:** An "Execution Environment" is a mini-container that has all the Cisco modules pre-installed so you don't have to worry about Python libraries.
7.  **Playbook:** Click the dropdown and select `lab01_facts.yml`.
8.  **Credentials:** Click the magnifying glass and select your `Cisco Router Login`.
9.  Click **Save**.

---

## Part 5: Launch! 🎆

1.  Click the blue **Launch** button.
2.  AWX will open a "Job Result" screen. You can watch the Ansible output in real-time as if you were in the terminal.
3.  Verify that the output shows the hostname and version of your routers.

---

## ❓ Knowledge Check
1.  Why is it better to store passwords in AWX than in an `inventory.yml` file?
2.  What does a **Project** in AWX represent?
3.  Which "Lego" piece acts as the "Start Button" for automation?

---

## 📂 Deep Dive: The SCM Sync
SCM stands for **Source Control Management**. When you clicked "Save" on your Project, AWX ran a background job called a **Project Sync**. It performed a `git pull` into a special hidden folder on the server. Every time you run a job, AWX can be configured to "Update Revision on Launch," ensuring you are always running the absolute latest version of your code.
