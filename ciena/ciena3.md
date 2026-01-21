# **Ciena Automation with Ansible**

A comprehensive guide for automating Ciena optical platforms. This repository covers the **Waveserver** family (utilizing dedicated collections) and the **6500 Reconfigurable Line System (RLS)** (utilizing native NETCONF/YANG).

## **Table of Contents**

* [Prerequisites](https://www.google.com/search?q=%23prerequisites)  
* [Installation](https://www.google.com/search?q=%23installation)  
* [Inventory Setup](https://www.google.com/search?q=%23inventory-setup)  
* [Waveserver 5 Automation](https://www.google.com/search?q=%23waveserver-5-automation)  
* [Waveserver Ai Automation](https://www.google.com/search?q=%23waveserver-ai-automation)  
* [RLS Automation (NETCONF)](https://www.google.com/search?q=%23rls-automation-netconf)  
* [Troubleshooting](https://www.google.com/search?q=%23troubleshooting)

## **Prerequisites**

Before running playbooks, ensure your control node meets the following requirements.

* **Ansible Core**: 2.12 or later.  
* **Python**: 3.8 or later.  
* **Libraries**: ncclient and xmltodict are required for XML payload handling.

pip install ncclient xmltodict

## **Installation**

Install the required Ansible collections from Galaxy.

| Device Family | Collection | Method |  
| RLS / 6500 | ansible.netcommon | Standard NETCONF |  
| Waveserver 5 | ciena.waveserver5 | REST/API Modules |  
| Waveserver Ai | ciena.waveserverai | REST/API Modules |  
\# 1\. Install generic network collection (Required for RLS NETCONF)  
ansible-galaxy collection install ansible.netcommon

\# 2\. Install Ciena Waveserver 5 collection  
ansible-galaxy collection install ciena.waveserver5

\# 3\. Install Ciena Waveserver Ai collection  
ansible-galaxy collection install ciena.waveserverai

\# 4\. (Optional) SAOS 10 support  
ansible-galaxy collection install ciena.saos10

## **Inventory Setup**

Define your hosts.ini with connection variables. Note that Ciena devices typically listen on port **830** for NETCONF.

\[waveserver5\]  
ws5-01 ansible\_host=192.168.10.11

\[waveserver\_ai\]  
wsai-01 ansible\_host=192.168.10.12

\[rls\]  
rls-01 ansible\_host=192.168.10.13

\[all:vars\]  
ansible\_user=admin  
ansible\_password=YourSecurePassword  
ansible\_connection=netconf  
ansible\_port=830  
ansible\_network\_os=auto  
\# Tip: For RLS, if 'auto' fails, use 'default' to force raw NETCONF.

## **Waveserver 5 Automation**

The ciena.waveserver5 collection abstracts the API into Ansible modules.

### **Example: System & Port Configuration**

**File:** waveserver5\_complex.yml

\---  
\- name: Manage Ciena Waveserver 5  
  hosts: waveserver5  
  gather\_facts: no  
  collections:  
    \- ciena.waveserver5

  tasks:  
    \- name: Configure System Location and Contact  
      waveserver5\_system:  
        config:  
          location: "Data Center A \- Row 4"  
          contact: "NetOps Team"  
        state: merged

    \- name: Configure Client Port with TTI  
      waveserver5\_ports:  
        config:  
          \- port\_id: "1-1"  
            admin\_state: enabled  
            description: "100G Uplink to Core"  
            channels:  
              \- channel\_id: 1  
                id:  
                  label: "Service-A"  
                properties:  
                  trace:  
                    tx\_sapi: "WS5-NODE-A"  
                    tx\_dapi: "WS5-NODE-B"  
                    mismatch\_fail\_mode: "alarm-only"  
        state: merged

    \- name: Gather PMs  
      waveserver5\_pm:  
        gather\_subset:  
          \- current  
      register: pm\_data

    \- name: Debug PM Data  
      debug:  
        var: pm\_data

## **Waveserver Ai Automation**

The ciena.waveserverai collection handles specific nuances like Transceivers (XCVRs) and PTPs.

### **Example: Provisioning XCVR & PTP**

**File:** waveserver\_ai\_provisioning.yml

\---  
\- name: Manage Ciena Waveserver Ai  
  hosts: waveserver\_ai  
  gather\_facts: no  
  collections:  
    \- ciena.waveserverai

  tasks:  
    \- name: Configure Transceiver (XCVR) Mode  
      waveserverai\_xcvrs:  
        config:  
          \- xcvr\_id: "1-1"  
            properties:  
              mode: "400GE"  
        state: merged

    \- name: Provision PTP Frequency  
      waveserverai\_ptps:  
        config:  
          \- ptp\_id: "1-1"  
            properties:  
              frequency: 193100.00  \# 193.1 THz  
              tx\_power: \-2.0  
            state:  
              admin\_state: enabled  
        state: merged

    \- name: Verify Configuration  
      waveserverai\_facts:  
        gather\_subset:  
          \- xcvrs  
          \- ptps  
      register: ai\_facts

    \- name: Display Mode  
      debug:  
        msg: "XCVR 1-1 Mode: {{ ai\_facts.ansible\_facts.ansible\_net\_xcvrs\['1-1'\].properties.mode }}"

## **RLS Automation (NETCONF)**

RLS is a **NETCONF-native** platform utilizing OpenConfig and Ciena proprietary YANG models.

**Important:** RLS is strict about XML namespaces (xmlns). Always verify the namespace using show netconf-yang schemas on the device.

### **Example: Advanced Configuration (IP & Shelf)**

**File:** rls\_advanced\_netconf.yml

\---  
\- name: Ciena RLS Advanced Automation  
  hosts: rls  
  connection: netconf  
  gather\_facts: no  
  collections:  
    \- ansible.netcommon

  tasks:  
    \# \--- TASK 1: READ DATA (OpenConfig System) \---  
    \- name: Get System Info via OpenConfig  
      netconf\_get:  
        filter: |  
          \<system xmlns="\[http://openconfig.net/yang/system\](http://openconfig.net/yang/system)"\>  
            \<config\>  
              \<hostname/\>  
              \<domain-name/\>  
            \</config\>  
          \</system\>  
      register: rls\_system

    \- name: Display Hostname  
      debug:  
        msg: "Device Hostname: {{ rls\_system.result\['data'\]\['system'\]\['config'\]\['hostname'\] }}"

    \# \--- TASK 2: CONFIGURATION (IP Interface) \---  
    \- name: Configure IP Interface (OpenConfig Interfaces)  
      netconf\_config:  
        content: |  
          \<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"\>  
            \<interfaces xmlns="\[http://openconfig.net/yang/interfaces\](http://openconfig.net/yang/interfaces)"\>  
              \<interface\>  
                \<name\>ip-1\</name\>  
                \<config\>  
                  \<name\>ip-1\</name\>  
                  \<type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type"\>ianaift:l3ipvlan\</type\>  
                  \<enabled\>true\</enabled\>  
                \</config\>  
                \<subinterfaces\>  
                  \<subinterface\>  
                    \<index\>0\</index\>  
                    \<ipv4 xmlns="\[http://openconfig.net/yang/interfaces/ip\](http://openconfig.net/yang/interfaces/ip)"\>  
                      \<addresses\>  
                        \<address\>  
                          \<ip\>10.0.0.50\</ip\>  
                          \<config\>  
                            \<ip\>10.0.0.50\</ip\>  
                            \<prefix-length\>24\</prefix-length\>  
                          \</config\>  
                        \</address\>  
                      \</addresses\>  
                    \</ipv4\>  
                  \</subinterface\>  
                \</interface\>  
              \</interfaces\>  
            \</config\>  
        commit: yes

    \# \--- TASK 3: SHELF MANAGEMENT (Ciena Proprietary) \---  
    \- name: Enable Shelf Admin State  
      netconf\_config:  
        content: |  
          \<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"\>  
            \<shelves xmlns="urn:ciena:params:xml:ns:yang:ciena-6500r-shelves"\>  
              \<shelf\>  
                \<shelf-name\>1\</shelf-name\>  
                \<admin-state\>enabled\</admin-state\>  
              \</shelf\>  
            \</shelves\>  
          \</config\>  
        commit: yes

    \# \--- TASK 4: OPERATIONAL DATA (Alarms) \---  
    \- name: Retrieve Active Alarms  
      netconf\_rpc:  
        rpc: "get"  
        content: |  
          \<filter type="subtree"\>  
             \<active-alarm xmlns="urn:ciena:params:xml:ns:yang:ciena-pro-alarm"/\>  
          \</filter\>  
      register: alarms

    \- name: Show Alarm Count  
      debug:  
        msg: "Active Alarms: {{ alarms.output\['data'\]\['active-alarm'\] | length }}"  
      when: alarms.output\['data'\]\['active-alarm'\] is defined

## **Troubleshooting**

### **Common Issues**

1. **Access Denied / Authentication Failure**  
   * **Cause:** User lacks NETCONF privileges.  
   * **Fix:** Check show user \<username\> on the device. Ensure the user is in the netconf group.  
2. **Namespace Errors (RLS)**  
   * **Symptom:** rpc-error with bad-element or unknown-namespace.  
   * **Fix:** RLS is strict. Omitting xmlns="http://openconfig.net/..." will cause failure.  
   * **Debug:** Use show netconf-yang schemas on the CLI to confirm the exact URI.  
3. **Collection Not Found**  
   * **Fix:** Run ansible-galaxy collection list to ensure Ciena collections are installed.

**Disclaimer**: This guide is for educational purposes. Always test automation in a lab environment before deploying to production Ciena nodes.
