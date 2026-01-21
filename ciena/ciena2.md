**Ansible Automation Guide for Ciena RLS, Waveserver 5, and Waveserver Ai**

**Overview and Setup**

**Introduction to Ansible:** Ansible is an open-source IT automation platform used for configuration management, application deployment, and orchestration of complex tasks. It works by pushing small programs (modules) from a central **control node** to managed devices over standard protocols (usually SSH), executing tasks without needing an agent on the remote device. This makes Ansible ideal for network automation, as it can consistently apply configurations and gather information across many devices.

**Ansible Control Node Installation:** To get started, set up a Linux control node (e.g. a server or VM running Red Hat, Ubuntu, etc.) and install Ansible (version 2.12+ recommended, since Ciena modules are tested on 2.12+ and 2.15+). You can install Ansible via package manager or pip. For example, on Ubuntu/Debian:

sudo apt update && sudo apt install -y ansible

On RHEL/CentOS, enable the EPEL repository and install Ansible, or use pip install ansible. Ensure that Python and ncclient are installed on the control node as well (the Ciena modules use NETCONF, which typically requires the Python ncclient library).

**Inventory File Setup for Ciena Devices:** Ansible uses an **inventory** file to define the devices it will manage. You can organize Ciena RLS, Waveserver 5, and Waveserver Ai devices into groups (such as **lab** vs **production** or by device type). Each host entry should include connection details and variables specific to network devices. Below is an example inventory snippet (in INI style) with group variables for different Ciena device types:

| **Hostname**  | **Device Type** | **ansible_host** | **ansible_connection**    | **ansible_network_os**          | **ansible_user** | **ansible_password** |
|---------------|-----------------|------------------|---------------------------|---------------------------------|------------------|----------------------|
| rls-node1     | 6500 RLS        | 10.0.0.10        | ansible.netcommon.netconf | auto (NETCONF auto-detect)      | admin            | \`!vault             |
| ws5-device1   | Waveserver 5    | 10.0.0.20        | ansible.netcommon.netconf | ciena.waveserver5.waveserver5   | admin            | \`!vault             |
| ws-ai-device1 | Waveserver Ai   | 10.0.0.30        | ansible.netcommon.netconf | ciena.waveserverai.waveserverai | admin            | \`!vault             |

In this example, ansible_host is the management IP or DNS name. We set ansible_connection=ansible.netcommon.netconf for NETCONF access. For Waveserver 5 and Ai, we specify the fully qualified ansible_network_os that corresponds to Ciena’s provided plugins (e.g. ciena.waveserver5.waveserver5 for Waveserver 5, and ciena.waveserverai.waveserverai for Waveserver Ai). The RLS currently has no dedicated Ansible collection, so we use ansible_network_os=auto to let Ansible attempt auto-detection or use a generic NETCONF plugin for the RLS. We also define ansible_user and ansible_password (here shown as encrypted via **Ansible Vault**). The use of Vault ensures sensitive credentials are not stored in plain text.

**Required Collections or Modules:** Ciena provides official Ansible **collections** on Ansible Galaxy for Waveserver 5 and Waveserver Ai devices. These collections include modules and plugins tailored to those platforms. Make sure to install the collections on your control node before running playbooks. For example:

-   **Ciena Waveserver 5 Collection:** Install with ansible-galaxy collection install ciena.waveserver5. This provides modules such as waveserver5_facts, waveserver5_ports, waveserver5_system, etc., and a NETCONF plugin for the Waveserver 5. (Waveserver 5 runs Ciena’s SAOS-based network OS and supports management via NETCONF/YANG.)

-   **Ciena Waveserver Ai Collection:** Install with ansible-galaxy collection install ciena.waveserverai. This provides similar modules (e.g. waveserverai_facts, waveserverai_ports, waveserverai_system, plus a waveserverai_command module for CLI commands) and supports both NETCONF and CLI connectivity.

There is currently **no official Ansible collection for the 6500 RLS**, but the RLS is designed as an open line system with support for standard NETCONF/YANG interfaces. For RLS, you may leverage generic modules (like ansible.netcommon.netconf_get/netconf_rpc) with the device’s YANG models, or use CLI-based automation if necessary. (Ciena’s 6500 RLS supports open “northbound” APIs via NETCONF/YANG, so it’s ideal to use those instead of legacy methods.)

**Authentication and Connectivity**

**SSH and API Access:** All three device types support secure remote management interfaces:

-   *Waveserver 5 and Waveserver Ai:* These platforms offer a **NETCONF** management interface (over SSH, usually on port 830) and also have a CLI (accessible via SSH on port 22). Waveserver 5 is typically managed via NETCONF/YANG (it also has a CLI, but the Ansible collection for WS5 is built for NETCONF). Waveserver Ai can be managed via NETCONF **or** via its CLI – the Ansible collection provides plugins for both methods.

-   *6500 RLS:* The RLS (Reconfigurable Line System) is managed through a NETCONF/YANG API as part of Ciena’s 6500 family. It may also have a CLI (potentially a TL1 or CLI interface on a specific port), but for automation the NETCONF interface is preferred. **Before using Ansible with RLS, ensure that NETCONF is enabled on the device.** (On some Ciena devices, you may need to log in via SSH and issue a command to enable the NETCONF server or configure an access list for it – refer to Ciena documentation for RLS setup.)

**Managing Credentials Securely:** It’s important to protect login credentials for lab and production devices. Avoid storing plain-text passwords in inventory files or playbooks. Instead, use **Ansible Vault** to encrypt sensitive data. For example, you can create an encrypted file for passwords (group_vars/all/vault.yml) and reference variables like ansible_password: "{{ vault_ciena_password }}", where vault_ciena_password is defined in an encrypted file. Ansible Vault ensures that even if someone views your playbooks or inventory, the actual passwords remain encrypted. Additionally, consider using SSH key authentication for CLI/SSH access to devices when possible, which can eliminate the need for stored passwords (for NETCONF, many devices also support key-based auth via SSH).

**Connection Testing:** Once your inventory and credentials are set, test connectivity to each device:

-   For Linux servers, one might use ansible -m ping all, but Ciena devices don’t run a Python shell, so the normal **ping module** isn’t applicable. Instead, use Ansible’s network connectivity modules. For example, the **network ping** (raw SSH) or simply attempt to gather facts. You can run an ad-hoc command to ensure the device is reachable and credentials work. For instance, try retrieving basic facts:

-   ansible -i inventory.ini waveserver5 -m ciena.waveserver5.waveserver5_facts -a "gather_subset=minimal"

    Or use a simple NETCONF check:

    ansible -i inventory.ini all -m ansible.netcommon.net_ping

    (The net_ping action will attempt an echo request via network connection plugins.)

-   Alternatively, create a quick playbook to fetch the hostname from each device. For Waveserver Ai using CLI, you could use the ciena.waveserverai.waveserverai_command module to run a harmless command (like show system). For Waveserver 5 (NETCONF-only), you might use waveserver5_facts to gather info as a test. If these tasks execute without error, your connections are set up correctly.

**Common connection issues and fixes:** If a connection fails, double-check:

-   Host IP/DNS and port (e.g., ensure the device’s NETCONF service is on port 830 and not blocked by a firewall).

-   Correct username/password and that the user has sufficient privileges (Ciena devices often require a **Superuser**/admin role for configuration changes via NETCONF).

-   For SSH key auth, confirm the key is installed on the device and use ansible_private_key_file if needed.

-   Known host keys: you may need to set ansible_ssh_common_args='-o StrictHostKeyChecking=no' for initial tests or pre-add host keys.

-   NETCONF session limits: RLS and others might have a limit on simultaneous NETCONF sessions. If you hit a *session refused* error, ensure you don’t exceed the allowed sessions or disconnect unused sessions (the RLS has commands to view/clear NETCONF sessions if needed).

**Common Automation Tasks**

Using Ansible, you can automate many repetitive tasks on Ciena optical devices. Below are common use cases and how to approach them:

-   **Device Discovery and Inventory Reporting:** You can automatically **gather facts** about each device – such as software version, serial numbers, interface inventory, optical power levels, etc. The Ciena modules include “facts” modules for this purpose. For example, ciena.waveserver5.waveserver5_facts and ciena.waveserverai.waveserverai_facts will retrieve a broad set of operational data from the device. Use the gather_subset parameter to control scope (e.g., gather_subset: [inventory, config] if supported). The facts modules return data as structured JSON which you can register and then format into a report. For instance, you might gather all devices’ serial numbers and output a table or CSV for your records. If a “facts” module is not available for RLS, you can still retrieve data via NETCONF queries (e.g., use ansible.netcommon.netconf_get with appropriate YANG path for inventory data) or via CLI commands (though NETCONF/YANG will provide structured data).

-   **Configuration Backup and Retrieval:** Maintaining backups of device configurations is critical in both lab and production. Since Ciena devices support NETCONF and YANG, you can retrieve the entire configuration datastore. There are a couple of approaches:

    -   *Using NETCONF GET:* Ansible’s ansible.netcommon.netconf_get module can fetch configuration in XML form. For example, you could write a task to get the running config and save it to a file:

    -   \- name: Retrieve running config via NETCONF

    -   ansible.netcommon.netconf_get:

    -   source: running

    -   register: config_xml

    -   

    -   \- name: Save configuration to backup file

    -   copy:

    -   content: "{{ config_xml.content }}" \# XML content from NETCONF get

    -   dest: "backups/{{ inventory_hostname }}_{{ansible_date_time.date}}.xml"

    -   delegate_to: localhost

        This will fetch the full running configuration and then write it to a timestamped file on the control node. (Ensure the user has permission to run get-config – on some systems you might need to adjust user roles for NETCONF.)

    -   *Using Ciena Modules:* The Ciena resource modules are primarily for setting configuration, but the \*_facts modules may also retrieve config snippets. For instance, waveserver5_facts with gather_subset: [config] might retrieve configuration sections. If the collection provides a way to do config backup (some vendors’ modules have a backup: yes option), consult the module docs. In absence of a built-in method, the NETCONF approach above is recommended.

    -   *Using CLI commands:* For Waveserver Ai, you could fall back to CLI commands to show running configuration (if such a command exists in the CLI). Ansible’s ciena.waveserverai.waveserverai_command can run CLI commands on Waveserver Ai. For example, you might run admin show-config (if that prints the config) and capture output. This is less structured than NETCONF, but can be used as a quick backup in labs. Always remember to secure the backup files (they may contain sensitive info).

-   **Configuration Deployment (Provisioning Changes):** The true power of Ansible is making configuration changes in a consistent, repeatable way. With Ciena’s Ansible collections, you can use *resource modules* to declaratively configure aspects of the device:

    -   *Examples:* You might need to change an interface (enable/disable a port, set a description), adjust a service setting, or update device-level parameters like hostname or NTP servers. The Waveserver 5 module **waveserver5_ports** can manage port settings, **waveserver5_system** can manage system-wide config, and similarly **waveserverai_ports**, **waveserverai_system** for Waveserver Ai.

    -   *Declarative config with state:* These modules allow you to describe **what configuration you want** rather than how to type it. For example, to enable a specific port on Waveserver 5 and set its administrative state to *enabled*, you could do:

    -   \- name: Enable client port 5-1 on Waveserver5

    -   ciena.waveserver5.waveserver5_ports:

    -   config:

    -   \- port_id: "5-1"

    -   properties:

    -   admin_state: enabled

    -   state: merged

        Here, state: merged tells Ansible to merge this config with the existing configuration (i.e. enable port 5-1 without removing other ports). The module will handle applying only the necessary change via NETCONF. In this declarative style, if the port is already enabled, Ansible will detect no change and skip making modifications, ensuring **idempotency**. Other supported state options may include deleted (to remove a config item) or overridden (to replace the entire config section with what you specify) – check the module docs for exact supported states.

    -   *Pushing multiple changes:* You can specify multiple config entries in one task (e.g., enable several ports, or set multiple system parameters like NTP servers and syslog). The modules will iterate through the list and apply all changes in a single NETCONF transaction. This is efficient and also ensures all changes go in together. Always include meaningful name fields for tasks so it’s clear in output what is being done.

-   **Firmware or Software Image Management:** Automating software upgrades can save time and reduce errors. While Ciena’s Ansible collections may not have a dedicated “upgrade” module, you can use Ansible to orchestrate the upgrade process:

    -   *Upload image to device:* If the device supports fetching images via SCP/FTP/HTTP, you could use Ansible to push the file to a staging server or use the device’s API. For example, Waveserver devices might allow an image to be uploaded via SCP to their file system. You can use Ansible’s **copy** or **fetch** modules to move files around (or the ciena.waveserverai.waveserverai_command module to run CLI commands like copy ftp://... image if such exists).

    -   *Activate the new image:* Often you must instruct the device to load the new software. Some devices have a NETCONF RPC or a CLI command to install or activate the downloaded image. (For instance, the Waveserver YANG model includes a software management RPC, which the Ansible module might expose in the future. In absence of a module, you could use ansible.netcommon.netconf_rpc to call that RPC directly, or run a CLI command via waveserverai_command.)

    -   *Reboot if required:* Schedule the reboot or switchover at a controlled time. You can use Ansible’s **serial** play execution to upgrade devices one by one, or use **wait_for** module to monitor when a device comes back online after reboot.

        **Tip:** Always verify image checksums and compatibility before automating a rollout. In lab, test the upgrade manually first, then script it. You might incorporate checks in your playbook (e.g., verify the current software version via \*_facts and skip upgrade if it’s already at desired version).

-   **Monitoring Health Status and Alarm Retrieval:** Ansible can also be used to periodically check device health or collect alarm/status information:

    -   *Polling alarms:* Using the facts modules or command modules, you can retrieve current alarms. For instance, on Waveserver Ai, you could run a CLI command like show alarms via waveserverai_command to get active alarms, then use Ansible to parse or email the output. If a YANG model for alarms is available (the Waveserver YANG includes an alarm model), you could use waveserver5_facts or waveserverai_facts to get alarm counts or details in structured form.

    -   *Performance monitoring:* The Waveserver 5 collection includes a module waveserver5_pm (likely for Performance Monitoring data). This could retrieve metrics like optical power levels, error counts, etc. Similarly, waveserverai_xcvrs can fetch transceiver details on Waveserver Ai (serial numbers, optical power). You can schedule playbooks (using tools like Ansible Tower/AAP or cron + ansible-playbook) to run these modules and store the results, giving you historical data.

    -   *Device latency or connectivity:* Ansible can also simply ping devices or do traceroutes via CLI if needed. While not as real-time as dedicated NMS, this on-demand automation approach is useful for spot-checking many devices quickly.

**Grouping tasks and playbooks:** You might create separate playbooks for each category (one for backups, one for deployments, one for monitoring) and run them as needed or in a sequence. By grouping tasks logically, new or intermediate users can run a specific automation (e.g., "take nightly backups") without triggering unrelated changes.

**Device-Specific Notes**

Each Ciena device family has its own nuances. Understanding these will help you tailor your Ansible approach for lab vs production:

-   **Ciena 6500 RLS (Reconfigurable Line System):** The RLS is essentially an advanced optical line system (ROADMs, amplifiers, etc.) packaged in the 6500 platform. It was built with openness in mind – supporting **standard YANG data models and NETCONF** for provisioning and monitoring. In practice, this means you can control the RLS via YANG models (potentially aligning with Open ROADM standards or Ciena-specific models).

    -   *API endpoints/CLI:* The RLS likely provides NETCONF YANG models for common optical functions (such as channel provisioning, amplifier settings, etc.). Check Ciena’s documentation for the exact model (for example, power calibration or wavelength routing might be done through specific containers in the YANG). If you must use CLI, note that the 6500 family traditionally used TL1 commands for optical provisioning, but newer RLS software may also have a modern CLI. Ansible does not have a built-in TL1 module, so NETCONF is strongly preferred for automation here.

    -   *Idiosyncrasies:* **Enabling NETCONF** – ensure the RLS has NETCONF enabled and accessible (by default it might require a config change to allow it, as mentioned earlier). Also, the RLS may have a limit on concurrent NETCONF sessions (monitor and close sessions as needed to avoid reaching limits). Another note: RLS devices typically have no “commit” concept (changes via NETCONF apply immediately to running config), but if using candidate datastores, be sure to \<commit\> appropriately.

    -   *Best practices:* Because the RLS directly affects live optical channels, test changes in a controlled environment. For example, you might simulate certain YANG calls on a lab RLS or use Ciena’s **Emulation Cloud** to model the device. Avoid making large-scale changes (like reconfiguring ROADM filter plans) during peak traffic without verifying the impact. Automate gradual steps (e.g., adding one wavelength at a time, verifying power levels via Ansible playbook, then adding next).

-   **Ciena Waveserver 5:** Waveserver 5 is a compact DCI platform running a modern network OS (SAOS-based) with a rich YANG/NETCONF interface. All management on WS5 is intended to be via API – either NETCONF or a RESTCONF/REST API (the device offers a REST API that mirrors the YANG models). The provided Ansible collection uses NETCONF under the hood for all modules.

    -   *API endpoints/CLI:* Key YANG endpoints include system config (/waveserver-system for things like hostname, time, etc.), port config (/waveserver-ports for enabling/disabling ports, setting client mappings), transceiver info (/waveserver-xcvrs), and so on. The Ansible modules abstract these – for example, using waveserver5_ports actually sends NETCONF \<edit-config\> to the /waveserver-ports YANG path with your provided data.

    -   There is also a CLI available (for local access/troubleshooting), but automation is expected to use the API. The CLI is not integrated with Ansible modules. If you need to run a quick command on WS5, you could try using the **Netmiko** connection via Ansible (community.network.netmiko module) or expect scripts, but generally stick to the official modules.

    -   *Known limitations:* The Waveserver5 Ansible collection supports only NETCONF (no direct SSH/CLI). Ensure NETCONF is reachable. Another practical note: some configuration changes may **disrupt traffic** (e.g., disabling a port). In production, consider using Ansible’s **confirmation prompts** or carefully planned maintenance windows. In lab, you can be more liberal. Also, WS5 might require certain containers to be fully specified – if a module complains about missing required fields, consult the YANG model to supply all needed params (the Ansible module docs will list required sub-keys).

    -   *Best practices:* Use the **state: merged** (or appropriate state) to make non-intrusive changes. Because the YANG models allow *declarative merges*, you can often add a configuration without inadvertently wiping other settings. Also, use the **facts module** to get a baseline of current config before pushing changes; this can help you determine what exactly will change.

-   **Ciena Waveserver Ai:** Waveserver Ai is an earlier-generation DCI platform (1RU) that also supports open automation interfaces. It has both NETCONF/YANG and a more traditional CLI. The Ansible collection for Waveserver Ai allows using either method, which is convenient:

    -   *API endpoints/CLI:* The YANG models for WS Ai are similar in concept to WS5 (covering system, ports, transceivers, etc.), and the collection’s modules reflect that (e.g., waveserverai_ports, waveserverai_system, etc.). Additionally, the waveserverai_command module lets you send raw CLI commands if needed – this is useful for operations that might not yet have a YANG model or just for quick diagnostics (e.g., running show interface stats). When using CLI via Ansible, the collection’s **CLI plugin** handles login and parsing prompts specific to Waveserver Ai.

    -   *Idiosyncrasies:* One limitation to note – when using the CLI mode (network_cli), you cannot gather facts using the \*_facts module (those require NETCONF). So, if you need detailed info, you might have to switch the connection to netconf in your play or run a separate play to gather facts. Also, the CLI on Waveserver Ai might have interactive commands that are not easily automated (avoid anything that requires confirmation prompts unless you know how to handle them with expect or prompt module). The device may have an older software base, so ensure it’s running a software version that supports the Ansible collection (the collection was tested on certain releases).

    -   *Best practices:* For consistency and idempotency, prefer NETCONF for configuration changes on Waveserver Ai as well. Use the CLI module primarily for read-only operations or those not exposed in YANG. If mixing modes, be careful – for example, do not use CLI to change config and then NETCONF in the same run, as the NETCONF client might not pick up changes made via CLI until a new session (though usually config is config). Finally, like WS5, test playbooks in a lab environment. Waveserver Ai devices can also be emulated or lab-tested; Ciena’s Emulation Cloud might support an emulated Waveserver Ai for safe testing of playbooks.

**Summary of Device API Support:**

-   *RLS:* Managed via NETCONF/YANG (open models). No official Ansible modules – use generic methods.

-   *Waveserver 5:* Managed via NETCONF/YANG (Ciena-provided modules). **No direct CLI in Ansible.**

-   *Waveserver Ai:* Managed via NETCONF/YANG (modules) or CLI (command module). Both supported in Ansible.

By understanding these specifics, you can adapt the examples and tasks to each device and know where to look if something doesn’t work out-of-the-box (for instance, when to use a different module or adjust connection type).

**Example Playbooks**

Below are example Ansible playbooks demonstrating common workflows. Each playbook is written in YAML with comments explaining the steps. These examples assume you have set up your inventory and installed the necessary Ciena collections.

**1. Configuration Backup Playbook**

This playbook connects to all Waveserver devices and backs up their running configuration to files on the Ansible control node. It uses the NETCONF connection for structured data retrieval.

\# playbook: backup_ciena_config.yml

\- name: BACKUP running config of Ciena devices (Waveserver 5 & Ai)

hosts: waveserver_devices \# inventory group containing WS5 and WS Ai

connection: ansible.netcommon.netconf

gather_facts: false

vars:

backup_dir: "backups/{{ ansible_date_time.date }}"

pre_tasks:

\- name: "Ensure backup directory exists on control node"

file:

path: "{{ backup_dir }}"

state: directory

delegate_to: localhost

tasks:

\- name: Retrieve running configuration (NETCONF) on {{ inventory_hostname }}

ansible.netcommon.netconf_get:

source: running

register: config_data

\- name: Save {{ inventory_hostname }} config to file

copy:

content: "{{ config_data.content }}" \# XML content of running config

dest: "{{ backup_dir }}/{{ inventory_hostname }}.xml"

delegate_to: localhost

when: config_data.content is defined

\- name: Report backup completion for {{ inventory_hostname }}

debug:

msg: "Config backed up for {{ inventory_hostname }} to {{ backup_dir }}/{{ inventory_hostname }}.xml"

**Explanation:** This play runs against both Waveserver 5 and Ai hosts (tagged as waveserver_devices). It uses the ansible.netcommon.netconf_get module to fetch the running config of each device. The config is stored in config_data.content (as XML text). We then use a local copy task (delegated to localhost) to write that content to a file named after the device. We created a backup directory named with the current date for organization. After saving, we print a message. In a real scenario, you might want to use Ansible Vault if you plan to archive these off the control node, since configs may contain sensitive info (or at least ensure the backup directory is secured). You could also compress or Git-version-control the backups for change tracking.

*(If you wanted to back up RLS configs similarly, you could include the RLS hosts in this play as well. Since RLS also uses NETCONF, the netconf_get task should work, provided you have the proper YANG schemas on the device to return config. You might need to add a filter specifying the subtree for config if the RLS has a very large config.)*

**2. Configuration Deployment Playbook**

This example shows how to **enable an interface and set the hostname** on a Waveserver device using Ansible modules. We will do two plays: one for Waveserver 5 (NETCONF) and one for Waveserver Ai (using CLI command for demonstration).

\# playbook: deploy_config_ciena.yml

\- name: Configure Waveserver 5 device settings

hosts: waveserver5 \# inventory group for WS5 devices

connection: ansible.netcommon.netconf

gather_facts: false

collections:

\- ciena.waveserver5 \# ensure we use the WS5 collection

tasks:

\- name: Ensure client port 5-1 is enabled (WS5)

ciena.waveserver5.waveserver5_ports:

config:

\- port_id: "5-1"

properties:

admin_state: enabled \# set port admin state to "enabled"

state: merged \# merge with existing config (non-disruptive):contentReference[oaicite:46]{index=46}

when: inventory_hostname == "ws5-device1"

\# \^(Optional) you can scope to specific hosts or use conditions if needed

\- name: Set device hostname to "LAB-WS5-Device1"

ciena.waveserver5.waveserver5_system:

config:

host_name:

config_host_name: "LAB-WS5-Device1"

state: merged

\# The above will change the hostname; state: merged ensures we only update that field:contentReference[oaicite:47]{index=47}.

\# Note: If the device requires a different container for hostname, adjust accordingly.

\- name: Configure Waveserver Ai device via CLI

hosts: waveserver_ai \# inventory group for WS Ai devices

connection: ansible.netcommon.network_cli

gather_facts: false

collections:

\- ciena.waveserverai

tasks:

\- name: Enable client port 1-1 on WS Ai (CLI command)

ciena.waveserverai.waveserverai_command:

commands:

\- "port set port-num 1-1 admin-state enabled"

\# \^ Example CLI command; actual syntax depends on device's CLI.

register: port_cmd

\- name: Show port status to verify (CLI command)

ciena.waveserverai.waveserverai_command:

commands:

\- "show port 1-1"

register: port_status

\- name: Display port 1-1 status

debug:

msg: "{{ port_status.stdout[0] }}"

\# stdout[0] will contain the output of the "show port 1-1" command from above.

**Explanation:** The first play targets Waveserver 5 devices using the ciena.waveserver5 collection. We demonstrate two configuration tasks: enabling a port and setting the hostname. The waveserver5_ports module is used to enable port "5-1". We pass the desired config in a structured way (port ID and the property admin_state). We specify state: merged to add this config without wiping other port settings. The second task uses waveserver5_system to update the device’s hostname to "LAB-WS5-Device1" by merging that into the system config. If these changes were already present (port already enabled, hostname already set), Ansible would report **OK** with no changes – demonstrating idempotency.

The second play targets Waveserver Ai devices, but instead of using netconf modules, it shows use of the CLI command module (waveserverai_command). We switch the connection to network_cli for this play. In the first task, we send a CLI command to enable port 1-1 (note: the actual CLI syntax may differ; replace with the correct command from WS Ai’s CLI reference). We then issue a show port 1-1 command to retrieve the status and use a debug task to print a portion of the output. In a real scenario, you would likely use the netconf modules for consistency, but this demonstrates that you can fall back to CLI for quick tasks or for commands that have no API equivalent. Using the CLI also shows the output as text (in stdout), which you might need to parse if you want to make decisions in Ansible (you could use regex with ansible.builtin.regex_findall filter, etc., to parse port_status.stdout[0] for certain values).

*Note:* The Waveserver Ai play could have been done with netconf as well (using waveserverai_ports module similar to WS5). If using netconf, the syntax would be analogous to the WS5 example. We showed CLI here mainly to illustrate usage of the waveserverai_command module. When using CLI mode in production, remember that it’s not as inherently idempotent – sending the same CLI command twice might produce an error or repetitive change. Thus, use CLI for read-only or one-off tasks, and prefer the structured modules for config changes.

**3. Monitoring/Verification Playbook (Snippet)**

Finally, a short example snippet to **verify optical power levels** on all transceivers of Waveserver Ai using an Ansible loop. This uses the waveserverai_xcvrs module to gather transceiver (XCVR) data:

\- name: Check optical power levels on Waveserver Ai devices

hosts: waveserver_ai

connection: ansible.netcommon.netconf

gather_facts: false

collections:

\- ciena.waveserverai

tasks:

\- name: Get transceiver details

ciena.waveserverai.waveserverai_xcvrs:

\# No config provided, by default this might gather all XCVRs (operational data)

\# Some modules support state: gathered or use of empty config for facts.

register: xcvr_data

\- name: Report Rx power for each transceiver

debug:

msg: "Port {{ item.port_id }} receive power: {{ item.rx_power }} dBm"

loop: "{{ xcvr_data.transceivers \| default([]) }}"

loop_control:

label: "{{ item.port_id }}"

In this hypothetical example, after running the waveserverai_xcvrs module (which would retrieve details of all transceivers/optics in the device), we loop over the returned data and print the receive optical power for each port. The actual keys (port_id, rx_power) depend on the module’s returned structure (you would adjust those to real field names as documented). This kind of play is useful in both lab and production: for instance, after provisioning new channels, you can run it to ensure power levels are within expected ranges. It’s read-only and safe to run anytime.

These example playbooks illustrate the pattern of how to interact with the devices. In practice, you might combine multiple steps (e.g., configure, then verify) in one playbook, or separate them for clarity. Always include comments (as shown) to explain each step, which helps team members (and your future self) understand the automation workflow.

**Troubleshooting and Best Practices**

Automating network devices can be complex, but following best practices and knowing how to troubleshoot common issues will make the process smoother:

**Common Errors and Resolutions:**

-   *Connection Timeouts:* If a playbook hangs or fails on a task with a timeout, first verify basic reachability (ping the device’s management IP, ensure the correct port is used). NETCONF timeouts could mean the device isn’t responding – check if NETCONF is enabled and accessible. For RLS, remember it might not use the default port 830 (consult docs if it uses a custom port or if you need to SSH port-forward to reach it). Increasing the Ansible timeout is possible (e.g., ansible_command_timeout), but timeouts usually indicate a deeper issue (like wrong IP or device is overloaded/unreachable).

-   *Authentication Failures:* Ansible will report “FAILED! =\> Authentication error” if credentials are wrong. Verify the username/password (for NETCONF on Ciena, the user should have a role allowing netconf – typically the same admin credentials as CLI). If using Vault, make sure you decrypted the vault or provided --ask-vault-pass. For key auth, ensure the key path is correct and the key is authorized on the device.

-   *Host Key or SSH Issues:* If you see errors about host key verification, you may disable strict checking for initial runs as noted earlier, or add the host keys to \~/.ssh/known_hosts. For NETCONF, host key checking still applies since it’s over SSH.

-   *Module Not Found:* If Ansible says “module is not found in configured module paths”, it means the Ciena collection isn’t installed or not referenced. Make sure you installed the collection (ansible-galaxy collection list to verify) and that your playbook either specifies the collection at the top (with collections:) or uses the fully qualified name (e.g., use ciena.waveserver5.waveserver5_system in tasks, not just waveserver5_system, if you didn’t specify the collection globally). If you see a message about ansible_network_os not recognized, double-check the value – it should match the plugin name exactly (typos or forgetting the prefix like ciena. can cause fallback to unknown OS).

-   *NETCONF Schema/Model Errors:* Sometimes a NETCONF \<edit-config\> can fail because of invalid data (Ansible will report the RPC error with details). For instance, you might get an error if you provide a wrong port ID or a value out of range. Use the error message to adjust your play. If you suspect the YANG model, you can retrieve the YANG schema via NETCONF or check Ciena’s documentation for the model definitions (the error might cite a specific model and line number). In lab, you could intentionally trigger a smaller change to see what the acceptable values are (or use \*_facts to see current valid values).

-   *Playbook Structure Issues:* YAML syntax errors or mis-indentation are common for newcomers. Use ansible-lint or yamllint to validate your playbooks’ syntax. Also, watch out for using tabs (YAML requires spaces). Ansible will point to a line number if a playbook is malformed.

-   *CLI Prompt Issues:* If using network_cli and the play hangs or fails during command execution, it may be due to Ansible expecting a different prompt. The Ciena collection’s CLI plugin should handle the typical Waveserver Ai prompt, but if the device shows additional banners or multi-line prompts (e.g., on first login), Ansible might get confused. In such cases, you might need to adjust the **terminal prompt regex** in the plugin or use an expect module to handle the interactive portion. This is advanced usage – in general, if you encounter prompt issues, try using NETCONF which avoids interactive prompts altogether.

-   *Too Many NETCONF Sessions:* On devices like RLS or others, if you run playbooks frequently, you might accidentally leave NETCONF sessions open (especially if a playbook fails mid-way). The device could hit a limit and refuse new connections. To address this, design playbooks to properly close (Ansible does this automatically at end of play, but a crash might leave a session). You can also log into the device CLI and manually clear sessions if needed (Ciena often has a command like show sessions or a way to terminate them). As a preventive measure, do not run an excessive number of playbook processes in parallel against the same device.

**Ansible Execution Best Practices:**

-   *Use Check Mode and Diff:* Ansible’s **check mode** (ansible-playbook --check) is extremely useful for network changes. In check mode, Ansible will go through the motions without actually applying changes, and many modules will report what they **would** change. For example, the Ciena resource modules should support check mode, giving you a preview of config differences (Ansible will often show a diff of the configuration if the module provides it). Always test with --check in a lab environment to ensure your playbook does what you expect. Additionally, using -D or --diff with ansible-playbook will show configuration diffs for supported modules, which is great for review. In production, running with --check first (when possible) can catch mistakes without impacting the devices.

-   *Use Verbose Mode for Debugging:* If a playbook is failing and you can’t tell why, run ansible-playbook -vvv playbook.yml for increased verbosity. This will show detailed logs, including the NETCONF XML being sent/received (in many cases) and any Python stack traces if a module crashed. Verbose output can help pinpoint if the issue is with the module’s input, the device’s response, or Ansible’s logic. Just be mindful that verbose logs may include sensitive info (like passwords or config) – handle them carefully.

-   *Idempotency and Rollback:* Aim to write your playbooks to be **idempotent** – meaning you can run them multiple times and the result is the same, with changes applied only when needed. Using the Ciena resource modules with state: merged or appropriate states facilitates this, as they won’t reapply identical settings. Avoid using brute-force CLI commands that, for example, add a config unconditionally (like adding a user that already exists – that might error on second run). If you must run non-idempotent actions (like a command to reboot a device), use conditions or **run_once** when appropriate, and clearly separate those in your playbook.

    For rollback strategies, it’s wise to always take a backup (as shown in the backup playbook) *before* making changes. In case something goes wrong, you can quickly reapply the last known good configuration. You might even automate a rollback playbook that detects a failure and pushes the saved config back. However, applying a full config on an optical device in production needs caution (for example, pushing an old config could disrupt new circuits). A safer rollback might be to have plays that revert only the specific changes made. Using Ansible’s **block** and **rescue** syntax, you can catch failures in a block of tasks and then execute recovery tasks. For instance, if enabling a port fails and triggers alarms, the rescue block could disable that port again or perform a cleanup action. Testing these scenarios in lab is crucial to make sure your rollback does what you expect.

-   *Organize Playbooks and Variables:* As your automation grows, keep things organized. Use **group_vars** and **host_vars** to store device-specific info (like unique parameters, credentials, etc.). For example, if certain ports should be enabled only in lab devices, you can define a variable in the lab inventory group and use it in conditions. Consider writing **roles** for repetitive patterns (maybe a role for "backup device config" that you can reuse for different device groups). This not only avoids code duplication but also makes it easier to handle differences between RLS, WS5, and WS Ai in one role (using conditionals internally).

-   *Testing in Lab vs Production:* Always test your automation in a lab environment or on a simulated device before touching production. Ciena offers the **Emulation Cloud** service which can emulate Waveserver devices, allowing you to run Ansible playbooks against a virtual instance safely. Take advantage of this for trying out new playbooks or modules. In the lab, use devices with representative software versions and configurations. When moving to production, do so in phases if possible – try on one or two devices during a maintenance window, validate the outcome, and then proceed with larger batches. Ansible’s ability to target groups and use serial execution (e.g., serial: 1 to do one device at a time) can be very helpful to prevent widespread issues.

-   *Documentation and Comments:* Keep your playbooks well-documented. As seen in the examples, use comments to explain not just *what* a task is doing, but *why*. This helps team members understand the intent. Additionally, maintain an external document or even comments at the top of the playbook about any prerequisites (e.g., "NETCONF must be enabled on RLS via CLI command X before running this playbook") or known impacts ("Running this playbook will cause a momentary traffic hit on the links when the firmware is upgraded").

-   *Utilize Ansible Vault and AWX/Tower:* For production, it’s worth integrating with Ansible Tower or AWX (the web UI for Ansible) to schedule and control playbook runs, especially for regular tasks like backups or monitoring. These platforms also store credentials securely (similar to vault) and provide logging of all automation runs – useful for compliance. Whether using Tower or not, always log the results of your playbooks. You might configure Ansible to output to a log file, or even have tasks that record key changes (e.g., send a Slack/Teams message or email when a deployment is done).

-   *Stay Updated:* The Ansible modules for Ciena devices might be updated by the community or Ciena over time. Keep an eye on Ansible Galaxy for new versions of ciena.waveserver5 and ciena.waveserverai. New releases might bring in additional modules (for example, a future release might add an RLS collection or more capabilities like software upgrade modules). Also, keep your Ansible version reasonably up to date to ensure compatibility with these collections.

In conclusion, automating Ciena RLS, Waveserver 5, and Waveserver Ai with Ansible can greatly streamline operations in both lab and production. You have open APIs at your disposal (NETCONF/YANG and even REST), and community-supported collections that abstract many details. By setting up a solid inventory, securing your credentials, and writing idempotent playbooks that handle common tasks (backups, config deploys, monitoring), you can reduce manual effort and human error. Always test changes in a controlled environment and follow best practices for network automation. With careful use, Ansible will become a powerful tool in managing your Ciena optical network seamlessly across lab validations and live deployments.

