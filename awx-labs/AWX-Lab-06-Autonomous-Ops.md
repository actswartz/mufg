# AWX Lab 6: Autonomous Ops (Schedules & Notifications)

Automation is truly powerful when you no longer have to trigger it yourself. In this lab, you as **SX-user** will learn how to make your network self-healing and proactive.

---

## 🧠 Core Concept: Autonomy
Autonomous operations move beyond manual triggers. By combining schedules and notifications, you create a system that audits itself and alerts you only when human intervention is required.

---

## Part 1: Schedules ⏰

### 📖 What is a Schedule?
A **Schedule** is a time-based trigger that tells AWX to run a specific task at a future time or on a repeating interval (like every day at midnight).

### 🎯 What is the Purpose?
The purpose is **"Hands-Free" Operations**. You shouldn't have to manually check if your routers are healthy every morning. By scheduling a validation check, you ensure the network is being audited even while you sleep.

### Step-by-Step:
1.  Click **Templates** -> Your **01 - Gather Cisco Facts** template.
2.  Click the **Schedules** tab -> Click **Add**.
3.  **Name:** 
    ```text
    Daily Health Audit
    ```
4.  **Repeat Frequency:** Select **Daily**.
5.  **Start Time:** Set it for 1 hour from now.
6.  Click **Save**.

---

## Part 2: Notifications 📢

### 📖 What is a Notification?
A **Notification** is an external alert sent by AWX to a communication tool like Slack, Email, or PagerDuty.

### 🎯 What is the Purpose?
The purpose is **Real-Time Awareness**. If an automated health check fails at 3:00 AM, you want an immediate alert so you can respond before users notice the problem.

### Step-by-Step:
1.  Click **Notifications** in the left menu -> Click **Add**.
2.  **Name:** 
    ```text
    Operations Slack Alert
    ```
3.  **Type:** Select **Slack**.
4.  **Target URL:** Enter a dummy URL (e.g., `https://hooks.slack.com/services/T0000/B0000/XXXX`).
5.  Click **Save**.
6.  Go back to **Templates** -> **01 - Gather Cisco Facts** -> **Notifications** tab.
7.  **Toggle the "Failure" switch to ON.**
    > **💡 Bonus Note:** We only enable "Failure" to avoid "Notification Spam." We only want to be interrupted if there is an actual problem.

---

## Part 3: Remediation (Drift Correction) 🌪️

### 📖 What is Remediation?
**Remediation** is the process where automation automatically "fixes" a problem it has detected.

### 🎯 What is the Purpose?
The purpose is **Self-Healing Infrastructure**. If a human makes a manual mistake on a router (Configuration Drift), the automation detects it and automatically overwrites the mistake with the correct settings.

### Task: Test the Self-Healing Network
1.  **Manual Change:** SSH into your router and manually change the banner to something "wrong" or "unauthorized."
2.  **Manual Trigger:** In AWX, launch your **05 - Complete Pod Build** workflow.
3.  **Watch the magic:** Watch as AWX detects the difference and automatically restores the correct configuration from your GitHub "Source of Truth"!

---

## 📂 Deep Dive: From Automation to Autonomy
The shift from manual 'Launch' buttons to **Schedules and Notifications** represents the move from 'Standard Automation' to **'Autonomous Operations.'** In this model, the engineer becomes the **Architect** of a system that manages itself.

This leads to the concept of **'Configuration Drift.'** In any network, humans will eventually make manual changes (the 'Oops' factor). Over time, these changes make the network unpredictable. By scheduling your 'Pod Build' to run every hour, you are creating a **Self-Correcting Network**. The automation becomes an immune system that 'heals' the configuration back to the GitHub standard.

Notifications are the **Feedback Loop** of this system. A well-designed notification strategy uses 'Negative Filtering.' You only want to be notified of failures. If a system tells you 'Everything is fine' 1,000 times a day, you will eventually start ignoring it (this is called **'Alert Fatigue'**).

---

## ❓ Knowledge Check
1.  What is "Configuration Drift"?
2.  Why do we usually only enable notifications for **Failure**?
3.  What is the difference between Automation and Autonomy?
