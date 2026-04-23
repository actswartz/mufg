<img src="images/3 router triangle.jpeg" width="400" alt="Network Topology">

# Lab 5: Dynamic Routing with OSPF

Now that your interfaces have IPs, it's time to enable routing so the devices can talk to each other across the network.

## 🧠 Core Concept: Jinja2 Templating
Sometimes, a standard Ansible module doesn't cover every specific command you need, or you want to generate a very long configuration file quickly. In these cases, we use **Jinja2 Templates**. 

A template is a blueprints file (`.j2`). It contains standard Cisco commands with "placeholders" (`{{ ... }}`) that Ansible fills in dynamically.

---

## Task 1: Create the Jinja2 Template 📄

Create a folder named `templates`: `mkdir templates`
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

### 🔍 Deep Dive: Jinja2 Logic
*   **Loops (`{% for ... %}`)**: Allows you to repeat a command for every item in a list (like OSPF networks).
*   **Conditionals (`{% if ... %}`)**: Allows you to skip certain items. Here, we skip `Ethernet0/0` because we don't want to run OSPF on our management network.

---

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

### 🔍 Why use `src`?
When you use `src:`, Ansible performs the "Rendering" on your Ubuntu machine, and then pushes the resulting text to the router. This is much faster than running 20 individual commands one-by-one.

### 💡 Industry Pro-Tip: Dynamic Routing vs Static
In a large network, we never use static routes if we can avoid it. Dynamic protocols like OSPF allow the network to "self-heal." If a link breaks, OSPF automatically finds a new path. By automating OSPF, you ensure your network is resilient from day one.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab05_ospf.yml
```

---

## 📂 Deep Dive: Whitespace Control
Jinja2 can sometimes leave accidental blank lines in your configuration, which can cause errors on a Cisco router.

Professional developers use the **hyphen (`-`)** inside tags to control this:
- **`{%-`**: Removes whitespace *before* the block.
- **`-%}`**: Removes whitespace *after* the block.

**Example:**
`{%- for net in networks -%}` will generate a clean list without any extra carriage returns.

---

## ❓ Knowledge Check
1.  What is the file extension for a Jinja2 template?
2.  Why did we exclude `Ethernet0/0` from the OSPF configuration?
3.  What is the difference between a variable (`{{ }}`) and a loop (`{% %}`) in Jinja2?


---

## 📺 Video Tutorial: Watch & Learn
For a visual walkthrough of the concepts in this lab, check out this helpful tutorial:
[https://www.youtube.com/watch?v=j9tVfEIsYms](https://www.youtube.com/watch?v=j9tVfEIsYms)
