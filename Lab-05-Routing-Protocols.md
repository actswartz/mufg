# Lab 5: Dynamic Routing with OSPF

Now that your interfaces have IPs, it's time to enable routing so the devices can talk to each other across the network.

## 🧠 Core Concept: Jinja2 Templating
While standard Ansible modules like `ios_l3_interfaces` are great, they don't cover every legacy or specialized command. In these cases, we use **Jinja2 Templates**. 

A template is a blueprints file. It looks like a standard Cisco configuration but uses "placeholders" (`{{ ... }}`) that Ansible fills in for each device. This allows one single file to generate unique configurations for dozens of routers.

## Task 1: Create the Jinja2 Template 📄

Create a folder named `templates` (this is the standard name Ansible looks for): `mkdir templates`
Create `templates/ospf_config.j2`:
```text
router ospf 1
 router-id {{ ospf.router_id }}
 log-adjacency-changes
{% for net in ospf.networks %}
 network {{ net.network }} {{ net.wildcard }} area {{ net.area }}
{% endfor %}
{% for intf in l3_interfaces %}
 {% if intf.name != 'Ethernet0/0' %}
 interface {{ intf.name }}
  ip ospf 1 area 0
 {% endif %}
{% endfor %}
```

### 🔍 Deep Dive: Jinja2 Syntax
*   **`{{ ospf.router_id }}`**: This is a **Variable Expression**. Ansible looks into your `inventory.yml`, finds the `ospf` dictionary for the current router, and grabs the `router_id`.
*   **`{% for net in ospf.networks %}`**: This is a **Control Structure**. It iterates through the list of networks you defined. For every network in that list, it generates one `network x.x.x.x y.y.y.y area 0` line.
*   **`{% if intf.name != 'Ethernet0/0' %}`**: This is a **Conditional**. We use this to prevent OSPF from being enabled on our management interface, which would be a security risk in a real network.

## Task 2: Create the `lab05_ospf.yml` Playbook

```yaml
---
- name: Lab 5 - OSPF Configuration
  hosts: routers
  gather_facts: false
  tasks:
    - name: Generate and Apply OSPF Config
      cisco.ios.ios_config:
        src: templates/ospf_config.j2
```

### 🔍 Why use `src` instead of `lines`?
Normally, the `ios_config` module uses the `lines:` parameter for simple commands. By using **`src:`**, you are telling Ansible to:
1.  Read the template file.
2.  Render it (fill in the variables).
3.  Compare the result to the router's current "running-config".
4.  Only send the commands that are missing (**Idempotency!**).

## Part 3: Running and Verifying 🛠️

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab05_ospf.yml
```

### 🔍 Verification:
Log into **S1-R1** and check the running configuration for OSPF:
```bash
show run | section router ospf
```
You should see that the Router ID matches what you put in your inventory for that specific device!
