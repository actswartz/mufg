# AWX Lab 6: Autonomous Ops (Schedules & Notifications)

Congratulations! You've reached the final lab. Automation is truly powerful when you no longer have to trigger it yourself. In this lab, you will learn how to schedule a "Compliance Check" and set up notifications so that the network tells *you* when it has a problem.

---

## 🧠 Core Concept: Continuous Compliance
In a professional network, we don't just fix things when they break. We run "Compliance Audits" every hour to ensure that no one has made an unauthorized manual change. 

---

## Part 1: Schedules ⏰

### 📖 What is a Schedule?
A **Schedule** is a time-based trigger that tells AWX to run a specific template at a future time or on a repeating interval (like every Monday at 8:00 AM).

### 🎯 What is the Purpose?
The purpose is to achieve **"Hands-Free" Operations**. Network engineers shouldn't have to manually check if OSPF is working every morning. By scheduling Lab 6 to run daily, you ensure the network is being audited even while you sleep.

### Step-by-Step:
1.  In the left menu, click **Templates**.
2.  Click on your **Validation** template (Lab 6).
3.  Click the **Schedules** tab at the top.
4.  Click **Add**.
5.  **Name:** `Nightly Health Audit`
6.  **Repeat Frequency:** Select **Daily**.
7.  Click **Save**.

---

## Part 2: Notifications 📢

### 📖 What is a Notification?
A **Notification** is an external alert sent by AWX to a communication tool like Slack, Microsoft Teams, Email, or PagerDuty.

### 🎯 What is the Purpose?
The purpose is **Real-Time Awareness**. If an automated health check fails at 2:00 AM, you don't want to find out when you log in at 9:00 AM. You want an immediate alert on your phone so you can respond to the outage instantly.

### Step-by-Step:
1.  Click **Notifications** in the left menu.
2.  Click **Add**.
3.  **Name:** `Engineering Slack Alert`. **Type:** `Slack`.
4.  Click **Save**.
5.  Now go back to your **Validation Template** -> **Notifications** tab.
6.  **Toggle the "Failure" switch to ON.**
    > **💡 Bonus Note:** We only enable "Failure" to avoid "Notification Spam." We only want to be interrupted if there is a problem.

---

## Part 3: Remediation (Drift Correction) 🌪️

### 📖 What is Remediation?
**Remediation** is the process where automation automatically "fixes" a problem it has detected.

### 🎯 What is the Purpose?
The purpose is **Self-Healing Infrastructure**. If a human makes a manual mistake on a router, the automation detects the "Drift" from the standard and automatically reapplies the correct configuration.

### Task: Test the Self-Healing Network
1.  SSH into your router and manually change the MOTD banner to something wrong.
2.  In AWX, launch your **Complete Pod Build** workflow.
3.  Watch as AWX detects the difference and "Overwrites" your mistake.

---

## ❓ Knowledge Check
1.  What is "Configuration Drift"?
2.  Why do we usually only enable notifications for **Failure**?
3.  What is the benefit of a "Schedule" for a network engineer?

---

## 📂 Deep Dive: The AWX Activity Stream
Every single thing that happens in AWX is recorded in the **Activity Stream**. In a production environment, this is your **Audit Log**. It provides 100% accountability, showing exactly which template (or person) changed a router and when.
