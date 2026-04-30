# AWX Lab 5: Visual Orchestration (Workflows)

Real-world automation rarely involves just one playbook. You might need to configure hostnames, then IPs, then OSPF—but only if the previous step was successful. In this lab, you as **S<student_id>-user** will build a **Workflow** to tie your entire pod build together.

---

## 🧠 Core Concept: Orchestration
Orchestration is the coordination of multiple automated tasks into a single, logical process. It’s the difference between a single musician (a playbook) and an entire symphony (a workflow).

---

## Part 1: Workflow Job Templates 🗺️

### 📖 What is a Workflow Template?
A **Workflow Job Template** is a master template that organizes and triggers other Job Templates in a specific order.

### 🎯 What is the Purpose?
The purpose is to handle complex logic. If building a site takes 10 playbooks, you don't want to click "Launch" 10 times. A workflow runs them all automatically, and it can even choose a different path if one of them fails (e.g., "If IP setup fails, run the Rollback playbook").

### Step-by-Step:
1.  Click **Templates** -> **Add** -> **Add Workflow Job Template**.
2.  **Name:** `Complete Pod Build`
3.  **Organization:** `Org-S<student_id>`.
4.  **Inventory:** `Student Pod Inventory`.
5.  Click **Save**.

**✅ Success Criteria:** You have created a master container for your automated workflow.

---

## Part 2: The Visualizer 🧩

### 📖 What is the Visualizer?
The **Visualizer** is a drag-and-drop canvas within AWX that allows you to "draw" the flowchart of your automation.

### 🎯 What is the Purpose?
The purpose is visibility. Looking at a flowchart is much easier for a human to understand than reading hundreds of lines of code. It allows you to visually see exactly how your network deployment flows from start to finish.

### Step-by-Step:
1.  Click the **Visualizer** tab at the top. Click **Start**.
2.  Select **01 - Gather Cisco Facts**. Click **Save**.
3.  Hover over that node, click the **Plus (+)** icon.
4.  **Run Type:** Select **On Success**.
    > **💡 Bonus Note:** This prevents a "Broken Config" from spreading. If the first task fails, the workflow stops.
5.  Select **02 - Configure Interface IPs**. Click **Save**.
6.  Hover over the "Interfaces" node, click the **Plus (+)** icon.
7.  **Run Type:** Select **Always**.
8.  Select **03 - Self-Service Banner Change**. Click **Save**.
9.  Click **Save** in the top right of the Visualizer.
10. Click **Launch 🚀**.

**✅ Success Criteria:** The workflow launches and executes all three templates in the sequence you defined.

---

## ❓ Knowledge Check
1.  What is the difference between a **Job Template** and a **Workflow Job Template**?
2.  What does an **On Success** link do in a workflow?
3.  Why would you use an **Always** link instead of **On Success**?

---

## 📂 Deep Dive: Orchestration Logic and Convergence
A Workflow is more than just a sequence of playbooks; it is a **Decision Engine**. Each link between nodes represents a logic gate. While you used 'On Success,' you can also use **'On Failure'** links to create a 'Self-Healing' path. For example, if a deployment fails, the 'On Failure' link could trigger a 'Rollback' playbook that restores the previous day's configuration. This ensures that your automation never leaves the network in a 'half-broken' state.

Workflows also support **Parallelism**. You can have five different nodes all branching off the 'Start' node. AWX will launch all five jobs simultaneously, as long as you have enough capacity in your cluster. This is how engineers update 50 different remote branch offices at the exact same time. The speed of the network update is no longer limited by how fast a human can type, but by the bandwidth of the AWX server.

Another advanced concept is **'Always'** links. These are essential for **Cleanup and Notification**. Even if a configuration task fails, you might still want to run a task that deletes temporary files or sends a final status report. By using 'Always,' you guarantee that your 'Housekeeping' tasks are performed regardless of the success or failure of the main mission.

Finally, consider **'Approval Nodes.'** You can insert a node into a workflow that causes the automation to **Pause** and wait for a human to click an 'Approve' button. This is perfect for high-risk changes. The automation does all the hard work of preparing the change, then a senior engineer reviews the plan and hits the final button to authorize the execution. This 'Human-in-the-Loop' strategy is the best way to transition from manual to fully automated operations.
