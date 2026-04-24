# AWX Lab 6: Autonomous Ops (Schedules & Notifications)

Automation is truly powerful when you no longer have to trigger it yourself. In this lab, you as **SX-user** will learn how to make your network self-healing and proactive.

---

## Part 1: Schedules ⏰

### 📖 What is a Schedule?
A **Schedule** is a time-based trigger that tells AWX to run a specific task at a future time or on a repeating interval (like every day at midnight).

### 🎯 What is the Purpose?
The purpose is **"Hands-Free" Operations**. You shouldn't have to manually check if your routers are healthy every morning. By scheduling a validation check, you ensure the network is being audited even while you sleep.

### Step-by-Step:
1.  Click **Templates** -> Your **Validation** template.
2.  Click the **Schedules** tab -> Click **Add**.
3.  **Name:** .
4.  **Repeat Frequency:** Select **Daily**.
5.  Click **Save**.

---

## Part 2: Notifications 📢

### 📖 What is a Notification?
A **Notification** is an external alert sent by AWX to a communication tool like Slack, Email, or PagerDuty.

### 🎯 What is the Purpose?
The purpose is **Real-Time Awareness**. If an automated health check fails at 3:00 AM, you want an immediate alert on your phone so you can respond before users even notice the problem.

### Step-by-Step:
1.  Click **Notifications** in the left menu -> Click **Add**.
2.  **Name:** . **Type:**  (or Email).
3.  Click **Save**.
4.  Go to your **Validation Template** -> **Notifications** tab.
5.  **Toggle the "Failure" switch to ON.**
    > **💡 Bonus Note:** We only enable "Failure" to avoid "Notification Spam." We only want to be interrupted if there is an actual problem.

---

## Part 3: Remediation (Drift Correction) 🌪️

### 📖 What is Remediation?
**Remediation** is the process where automation automatically "fixes" a problem it has detected.

### 🎯 What is the Purpose?
The purpose is **Self-Healing Infrastructure**. If a human makes a manual mistake on a router (Configuration Drift), the automation detects it and automatically overwrites the mistake with the correct settings.

### Task: Test the Self-Healing Network
1.  SSH into your router and manually change the banner to something wrong.
2.  In AWX, launch your **Complete Pod Build** workflow.
3.  Watch as AWX detects the difference and automatically restores the correct configuration!

---

## 📂 Deep Dive: From Automation to Autonomy
The shift from manual 'Launch' buttons to **Schedules and Notifications** represents the move from 'Standard Automation' to **'Autonomous Operations.'** In this model, the human engineer is no longer the trigger; instead, the engineer becomes the **Architect** of a system that manages itself. The automation runs on a heartbeat, constantly checking the network's health and reporting back only when something is wrong.

This leads to the concept of **'Configuration Drift.'** In any network, humans will eventually make manual changes (the 'Oops' factor). Over time, these changes make the network unpredictable and hard to troubleshoot. By scheduling your 'Pod Build' or 'Validation' labs to run every hour, you are creating a **Self-Correcting Network**. The automation becomes an immune system that 'heals' the configuration back to the GitHub standard every time it drifts.

Notifications are the **Feedback Loop** of this system. A well-designed notification strategy uses 'Negative Filtering.' You only want to be notified of failures. If a system tells you 'Everything is fine' 1,000 times a day, you will eventually start ignoring it (this is called **'Alert Fatigue'**). By only triggering on failure, you ensure that every alert you receive is meaningful and requires immediate action.

Finally, notice the **Activity Stream**. This is the 'Black Box' flight recorder of your network. In the event of a security breach or a major outage, the Activity Stream allows you to reconstruct the exact state of the automation platform at any microsecond. It records who logged in, what variables they changed, and which schedule triggered a job. In the modern enterprise, this level of **Accountability** is not optional—it is a requirement for doing business.
