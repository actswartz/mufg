# Lab 6: Model-Driven Telemetry (The Push Model)

## Lab Overview
In your final lab, you will explore how modern Service Providers monitor their networks. You will move away from **SNMP** (which asks for data) and move to **Telemetry** (where the router pushes data).

By the end of this lab, you will have:
1. Defined a **Sensor Group** (What data to send).
2. Configured a **Destination Group** (Where to send the data).
3. Established a **Subscription** to stream data at a periodic interval.
4. Learned the benefits of **Push vs. Pull** monitoring.

---

## Part 1: Defining the Sensor Group 

### What is happening?
We need to tell the router *which* specific data we want it to stream. We will use a YANG path to specify that we want to monitor interface statistics.

### The Purpose
Streaming only the data you need (using YANG paths) reduces the CPU load on the router and the traffic on your network compared to global SNMP polling.

### ️ Step-by-Step:
Configure the sensor group on **Router 1**:
```ios
conf t
 telemetry model-driven
 sensor-group INTERFACE_STATS
  sensor-path Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-brief
 !
 commit
```

---

## Part 2: Defining the Destination (gRPC) 

### What is happening?
We tell the router where to send the data. We will use **gRPC (Google Remote Procedure Call)**, which is the high-performance transport protocol used by XR.

### ️ Step-by-Step:
Configure a destination group:
```ios
conf t
 telemetry model-driven
 destination-group ANALYTICS_SERVER
  address-family ipv4 172.30.30.1 port 57400
  encoding self-describing-gpb
  protocol grpc no-tls
  !
 commit
```
> **Note:** `172.30.30.1` is your management bridge gateway. In a real environment, this would be a server running an "Inceptor" or "Collector" like Prometheus or Telegraf.

---

## Part 3: The Subscription (Activating the Stream) 

### What is happening?
The Subscription ties the "What" (Sensor) to the "Where" (Destination) and sets the "When" (Interval).

### ️ Step-by-Step:
```ios
conf t
 telemetry model-driven
 subscription DAILY_MONITOR
  sensor-group INTERFACE_STATS sample-interval 10000
  destination-group ANALYTICS_SERVER
 !
 commit
```
> **Note:** `sample-interval 10000` means send data every 10,000 milliseconds (10 seconds).

---

## Part 4: Verification 

#### Command: `show telemetry model-driven subscription DAILY_MONITOR`
Verify that the router is attempting to stream data.

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# show telemetry model-driven subscription DAILY_MONITOR
Subscription: DAILY_MONITOR
 State:    Active
 Sensor groups:
  Id: INTERFACE_STATS
   Sample Interval:   10000 ms
 Destination Groups:
  Id: ANALYTICS_SERVER
   Address:     172.30.30.1
   Port:       57400
   State:      Connecting
```
> **Note:** The state will show `Connecting` because we don't have a collector running on the host, but the router is now actively trying to "Push" its health data out!

---

## Summary Checklist
- [ ] Configured a telemetry `sensor-group` using a YANG path.
- [ ] Configured a `destination-group` using the gRPC protocol.
- [ ] Created a `subscription` to tie them together.
- [ ] Verified the subscription is `Active`.

---

# Course Conclusion
Congratulations! You have completed the **Cisco XRd Specialist Course**. You have progressed from basic CLI commands to complex Segment Routing and modern Model-Driven Telemetry. You now have the skills to operate in a high-scale Service Provider environment!
