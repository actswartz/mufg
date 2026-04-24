# AWX Lab 2: The Source of Truth (Inventory Sync & Variables)

In Lab 1, you acting as `SX-user` manually typed in your router names and IPs. In this lab, you will learn how to make AWX automatically "read" your `inventory.yml` file from GitHub. This is the foundation of modern **Infrastructure as Code (IaC)**.

---

## 🧠 Core Concept: Infrastructure as Code (IaC)
IaC means managing your network hardware using the same tools and processes as software developers. Instead of "pointing and clicking" in a UI, you define your network in a text file. AWX then syncs that file to ensure the platform always knows about every device.

---

## Part 1: Preparing the Git Source 💾

### 📖 What is an Inventory Source?
An **Inventory Source** is a specific link between an AWX Inventory and an external data provider (like GitHub).

### 🎯 What is the Purpose?
The purpose is to automate the discovery of your routers. If you add a new router to your GitHub file, AWX will automatically "discover" it without you having to type anything into the UI.

### Step-by-Step (As SX-user):
1.  In the left menu, click **Inventories**.
2.  Click on your **Student Pod Inventory**.
3.  Click the **Sources** tab at the top -> Click **Add**.
4.  **Name:** `Git Inventory Source`
5.  **Source:** Select **Sourced from a Project**.
6.  **Project:** Select **AAP Workshop Code**.
    > **💡 Bonus Note:** Notice we are selecting the project you created in Lab 1. AWX is now looking *inside* that project folder for your inventory data.
7.  **Inventory file:** Click the magnifying glass and select `inventory.yml`.
8.  **Update Options:** Check **"Overwrite"** and **"Update on Launch"**.
    > **💡 Bonus Note:** "Overwrite" ensures that if you delete a router in GitHub, it also gets deleted in AWX. This keeps the two systems perfectly in sync.
9.  Click **Save**.

---

## Part 2: Synchronizing 🔄

### 📖 What is Synchronization?
**Synchronization** is the process where AWX executes a connection to GitHub, reads your YAML file, and imports the data into its database.

### 🎯 What is the Purpose?
The purpose is to refresh the platform's knowledge. Syncing is what turns a text file in GitHub into functional "Host Objects" inside the AWX dashboard.

### Step-by-Step:
1.  On the **Sources** screen, click the **Sync All** (or circular arrow 🔄) button.
2.  Wait for the status circle to turn **Green** (Successful).
3.  Now click the **Hosts** tab at the top of the Inventory screen.
    > **🧠 Pro-Tip:** You should now see your routers (e.g., S1-R1, S1-R2, S1-R3) appear automatically!

---

## Part 3: Using Host Variables 📂

### 📖 What are Host Variables?
**Host Variables** are the technical specificities (IPs, VLANs, neighbor IDs) that belong to a single device.

### 🎯 What is the Purpose?
They allow you to use one "Generic" playbook for your entire company. The playbook says "configure an IP," and the Host Variables provide the *specific* IP for the router currently being configured.

### Step-by-Step:
1.  Click on the name of one of your newly synced hosts (e.g., **SX-R1**).
2.  Look at the **Variables** box.
3.  You should see the YAML data from your CLI labs. AWX has successfully "ingested" your technical data!

---

## Part 4: Testing the Sync 🚀

### Step-by-Step:
1.  Click **Templates** -> **Add** -> **Add Job Template**.
2.  **Name:** `02 - Configure Interface IPs`
3.  **Inventory:** `Student Pod Inventory`.
4.  **Project:** `AAP Workshop Code`.
5.  **Playbook:** `lab04_interfaces.yml`.
6.  **Credentials:** `Cisco Router Login`.
7.  Click **Save** -> **Launch**.

---

## ❓ Knowledge Check
1.  What is the main benefit of "Sourcing from a Project" vs. manual entry?
2.  What does the "Update on Launch" checkbox do?
3.  If you add a new router to `inventory.yml` in GitHub, what do you need to do in AWX to see it?
