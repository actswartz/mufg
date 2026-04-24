# AWX Lab 5: Visual Orchestration (Workflows)

Real-world automation rarely involves just one playbook. You might need to configure hostnames, then IPs, then OSPF—but only if the previous step was successful. In this lab, you will build a **Workflow Job Template** to tie your entire pod build together.

---

## 🧠 Core Concept: Chaining
A **Workflow** is a flowchart for your automation.
- **Nodes:** The individual templates you've already created.
- **Links:** The "lines" connecting them.
- **Logic:** You can decide to run the next step only **On Success**, only **On Failure**, or **Always**.

---

## Part 1: Workflow Job Templates 🗺️

### 📖 What is a Workflow Template?
A **Workflow Job Template** is a "Master Template" that doesn't contain a playbook itself. Instead, it acts as a conductor that organizes and triggers other Job Templates in a specific order.

### 🎯 What is the Purpose?
The purpose is **Orchestration**. If building a data center takes 50 different playbooks, you don't want an engineer clicking "Launch" 50 times. You want one button that runs the entire sequence automatically, handling errors and dependencies along the way.

### Step-by-Step:
1.  In the left menu, click **Templates**.
2.  Click **Add** -> **Add Workflow Job Template**.
3.  **Name:** `WORKFLOW - Complete Pod Build`
4.  **Inventory:** `Student Pod Inventory`.
5.  Click **Save**.

---

## Part 2: The Visualizer (Mapping) 🧩

### 📖 What is the Visualizer?
The **Visualizer** is a drag-and-drop canvas within AWX that allows you to draw the logic of your automation.

### 🎯 What is the Purpose?
The purpose is to make complex logic easy to see. Looking at a flowchart is much easier for a human to understand than reading 1,000 lines of code. It allows you to visually see "If Task A fails, then run Task B (the fix)."

### Step-by-Step Mapping:
1.  Click the **Visualizer** tab at the top.
2.  Click **Start**.
3.  Select `01 - Gather Cisco Facts`. Click **Save**.
4.  Hover over that node, click the **Plus (+)** icon.
5.  **Run Type:** Select **On Success**.
    > **💡 Bonus Note:** This prevents "Broken Config" from spreading if the first step fails.
6.  Select `02 - Configure Interface IPs`. Click **Save**.
7.  Hover over the "Interfaces" node and click **Plus (+)**.
8.  **Run Type:** Select **Always**.
9.  Select your **Validation** template. Click **Save**.

---

## Part 3: The Launch 🎆

### Step-by-Step:
1.  Click **Save** (or **Done**) in the Visualizer.
2.  Click **Launch** 🚀.
3.  **Watch the Flow:** You will see a real-time graph. Nodes will turn **Blue** (Running), then **Green** (Success).

---

## ❓ Knowledge Check
1.  What is the benefit of a Workflow vs. one giant playbook with 50 tasks?
2.  What does the **"On Success"** link type prevent?
3.  In the visualizer, what does a **Green** node represent?

---

## 📂 Deep Dive: Converging Workflows
In complex environments, you can have multiple branches running at the same time (Parallelism). For example, you could update 10 different sites simultaneously. You can also use "Convergence" nodes, which wait for *all* previous branches to finish before starting the final step (like a final "Network Health Check").
