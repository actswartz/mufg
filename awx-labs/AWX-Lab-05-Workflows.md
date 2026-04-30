# AWX Lab 5: Visual Orchestration (Workflows)

Real-world automation rarely involves just one playbook. You might need to configure hostnames, then IPs, then OSPF—but only if the previous step was successful. In this lab, you as **SX-user** will build a **Workflow** to tie your entire pod build together into a single, logical process.

---

## 🧠 Core Concept: Orchestration
Orchestration is the coordination of multiple automated tasks into a single, logical process. It’s the difference between a single musician (a playbook) and an entire symphony (a workflow). It allows you to build complex "Decision Trees" for your infrastructure.

---

## Part 1: Creating the Workflow Master 🗺️

### 📖 What is a Workflow Template?
A **Workflow Job Template** is a master template that organizes and triggers other Job Templates in a specific order. It doesn't run a playbook itself; instead, it manages the execution of other templates.

### Step-by-Step:
1.  In the left menu, click **Templates**.
2.  Click **Add** -> **Add Workflow Job Template**.
3.  Fill in the following details:
    *   **Name:** 
        ```text
        05 - Complete Pod Build
        ```
    *   **Organization:** 
        ```text
        Org-SX
        ```
    *   **Inventory:** 
        ```text
        Student Pod Inventory
        ```
4.  Click **Save**.

---

## Part 2: The Visualizer (Building the Logic) 🧩

### 📖 What is the Visualizer?
The **Visualizer** is a drag-and-drop canvas within AWX that allows you to "draw" the flowchart of your automation. Each "Node" in the chart is one of your existing Job Templates.

### Step-by-Step:
1.  Click the **Visualizer** tab at the top of your new workflow.
2.  Click **Start**.
3.  **Node 1 (The Foundation):**
    *   Select `03 - Configure Hostnames`.
    *   Click **Save**.
4.  **Node 2 (The Banner):**
    *   Hover over the "Hostnames" node and click the **Plus (+)** icon.
    *   **Run Type:** Select **On Success**.
    *   Select `02 - Configure Banner`.
    *   Click **Save**.
5.  **Node 3 (The Interfaces):**
    *   Hover over the "Banner" node and click **Plus (+)**.
    *   **Run Type:** Select **On Success**.
    *   Select `04 - Configure Interfaces`.
    *   Click **Save**.
6.  **Node 4 (The Audit):**
    *   Hover over the "Interfaces" node and click **Plus (+)**.
    *   **Run Type:** Select **Always**.
    *   Select `06 - Validation & Compliance`.
    *   Click **Save**.
7.  Click **Save** in the top right of the Visualizer, then click **Launch 🚀**.

---

## Part 3: Monitoring the Symphony 📺

### 🎯 What is the Purpose?
Watching a workflow run provides immediate visual feedback. You can see exactly where a process is currently executing and, more importantly, exactly where it fails.

### Tasks:
1.  Watch the Workflow Job screen. Nodes will turn **Blue** (Running), then **Green** (Success) or **Red** (Failure).
2.  Click on any node while it is running to see the live console output for that specific playbook.
3.  **The "Always" Path:** Notice that even if a previous step had a minor issue, the `Validation` node still runs because we chose the **Always** link.

---

## 📂 Deep Dive: Orchestration Logic and Convergence
A Workflow is more than just a sequence of playbooks; it is a **Decision Engine**. Each link between nodes represents a logic gate. 

**1. Convergence (The "Wait for All" logic):**
In advanced workflows, you can have multiple parallel paths (e.g., configuring 5 different sites at once) that all "Converge" on a single final node (e.g., "Send Report"). AWX can be configured to wait until *all* parallel paths are finished before moving to the final step.

**2. Self-Healing Paths (The "On Failure" logic):**
While you used 'On Success' links, you can also use **'On Failure'** links. For example, if a deployment fails, the 'On Failure' link could trigger a 'Rollback' playbook that restores the previous day's configuration. This ensures that your automation never leaves the network in a 'half-broken' state.

**3. Human-in-the-Loop (Approval Nodes):**
You can insert an **Approval Node** into a workflow. This causes the automation to **Pause** and wait for a human to click an 'Approve' button. This is perfect for high-risk changes. The automation does all the hard work of preparing the change, then a senior engineer reviews the plan and hits the final button to authorize the execution.

---

## ❓ Knowledge Check
1.  What is the difference between a "Job Template" and a "Workflow Job Template"?
2.  Why would you use an "Always" link instead of an "On Success" link?
3.  If a node in a workflow fails and has no "On Failure" path, what happens to the rest of the workflow?
