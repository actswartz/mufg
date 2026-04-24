# AWX Lab 2: The Source of Truth (Inventory Sync & Variables)

In Lab 1, you manually typed in your router names and IPs. In a small lab, that's fine. In a large company with 5,000 routers, that's impossible. In this lab, you will learn how to make AWX automatically "read" your `inventory.yml` file from GitHub.

---

## 🧠 Core Concept: Infrastructure as Code (IaC)
When we store our inventory in a file in GitHub instead of typing it into a database, we are practicing **Infrastructure as Code**. 
- **Benefits:** If you change an IP in GitHub, AWX automatically sees the change. You have a history of who changed what, and when.

---

## Part 1: Preparing the Git Source 💾

### 📖 What is an Inventory Source?
An **Inventory Source** is a specific link between an AWX Inventory and an external provider, such as GitHub, Amazon AWS, or Google Cloud.

### 🎯 What is the Purpose?
The purpose of an Inventory Source is to automate the management of your devices. Instead of human error resulting from typing names manually, AWX "fetches" the list of routers directly from your code. This ensures your AWX platform always matches your physical network.

### Step-by-Step:
1.  In the left menu, click **Inventories**.
2.  Click on the inventory you created in Lab 1: **Student Pod Inventory**.
3.  Click the **Sources** tab at the top.
4.  Click **Add**.
5.  **Name:** `Git Inventory Source`
6.  **Source:** Select **Sourced from a Project**.
7.  **Project:** Select **DLR Workshop Code**.
8.  **Inventory file:** Click the magnifying glass or type `inventory.yml`.
    > **💡 Bonus Note:** AWX is looking inside the "DLR Workshop Code" project folder we synced in Lab 1. It sees the `inventory.yml` file you worked on in the CLI labs!
9.  **Update Options:** Check **"Overwrite"** and **"Update on Launch"**.
    > **💡 Bonus Note:** "Update on Launch" means every time you run a job, AWX will first check Git to see if any new routers were added or IPs were changed.
10. Click **Save**.

---

## Part 2: Synchronizing 🔄

### 📖 What is Synchronization?
**Synchronization** (or "Syncing") is the background process where AWX executes a connection to your source (GitHub) and imports the data into its own database.

### 🎯 What is the Purpose?
The purpose of syncing is to refresh AWX's memory. If you added a third router to your lab earlier today, syncing is what makes that new router appear in the AWX dashboard so you can run automation against it.

### Step-by-Step:
1.  On the **Sources** screen, you should see your new source.
2.  Click the **Sync** button (it looks like a circular arrow 🔄).
3.  Wait for the status to turn **Green**.
4.  Now click the **Hosts** tab at the top.
    > **🧠 Pro-Tip:** Look closely! You should see all the routers from your `inventory.yml`.

---

## Part 3: Using Host Variables 📂

### 📖 What are Host Variables?
**Host Variables** are technical details (like IP addresses, interface lists, or OSPF settings) that belong to one specific device.

### 🎯 What is the Purpose?
The purpose of Host Variables is to allow a single "Generic" playbook to perform "Specific" work. By storing the IP `172.20.20.2` as a variable for **S1-R1**, you can write a playbook that simply says `ip address {{ ansible_host }}`. AWX will fill in the correct IP for each router automatically.

### Step-by-Step:
1.  Click on the name of one of your hosts (e.g., **S1-R1**).
2.  Look at the **Variables** box.
3.  You should see the YAML data we defined in previous labs.
4.  This proves that AWX isn't just seeing the "Name" of the router, but also all the technical "Data" needed to configure it.

---

## Part 4: Testing the Sync 🚀

### Step-by-Step:
1.  Click **Templates** in the left menu.
2.  Click **Add** -> **Add Job Template**.
3.  **Name:** `02 - Configure Interface IPs`
4.  **Inventory:** `Student Pod Inventory`.
5.  **Project:** `DLR Workshop Code`.
6.  **Playbook:** `lab04_interfaces.yml`.
7.  **Credentials:** `Cisco Router Login`.
8.  Click **Save**.
9.  Click **Launch**.

---

## ❓ Knowledge Check
1.  What is the main benefit of "Sourcing from a Project" vs. manual entry?
2.  What does the "Update on Launch" checkbox do?
3.  If you add a new router to `inventory.yml` in GitHub, what do you need to do in AWX to see it?

---

## 📂 Deep Dive: The Inventory Plugin
Under the hood, when AWX syncs a project-based inventory, it uses an Ansible feature called an **Inventory Plugin**. It essentially runs `ansible-inventory` against your YAML file and converts the result into the AWX database format. This allows you to use complex logic (like loops and filters) in your YAML files, and AWX will understand them perfectly.
