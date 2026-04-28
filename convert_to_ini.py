import yaml
import sys
import json

def yaml_to_ini(yaml_file, ini_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    with open(ini_file, 'w') as f:
        # Global vars [all:vars]
        if 'all' in data and 'vars' in data['all']:
            f.write("[all:vars]\n")
            for k, v in data['all']['vars'].items():
                f.write(f"{k}={v}\n")
            f.write("\n")

        # Process children
        if 'all' in data and 'children' in data['all']:
            for group, content in data['all']['children'].items():
                f.write(f"[{group}]\n")
                if 'hosts' in content:
                    for host, host_vars in content['hosts'].items():
                        line = host
                        if host_vars:
                            for k, v in host_vars.items():
                                if isinstance(v, (list, dict)):
                                    v_str = json.dumps(v)
                                    line += f" {k}='{v_str}'"
                                else:
                                    line += f" {k}={v}"
                        f.write(line + "\n")
                f.write("\n")

if __name__ == "__main__":
    yaml_to_ini(sys.argv[1], sys.argv[2])
