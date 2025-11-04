#!/usr/bin/env python3
"""
update_ccc_network.py

Manage the CCC Network YAML database:
 - Add new houses
 - Add members to a house
 - List all houses and leaders
"""

import yaml
import argparse
from datetime import datetime
from pathlib import Path

YAML_FILE = Path("ccc_network.yaml")

def load_yaml():
    if not YAML_FILE.exists():
        return {"ccc_network": []}
    with open(YAML_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(data):
    class IndentDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(IndentDumper, self).increase_indent(flow, False)

    with open(YAML_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, Dumper=IndentDumper, indent=2)

    print(f"✅ Saved updates to {YAML_FILE}")

def add_house(house_name, leader):
    data = load_yaml()
    for house in data["ccc_network"]:
        if house["house_name"].lower() == house_name.lower():
            print(f"⚠️ House '{house_name}' already exists.")
            return

    data["ccc_network"].append({
        "house_name": house_name,
        "leader": leader,
        "members": [],
        "status": "Active",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_yaml(data)
    print(f"🏠 Added new house '{house_name}' with leader '{leader}'")

def add_member(house_name, member_name):
    data = load_yaml()
    for house in data["ccc_network"]:
        if house["house_name"].lower() == house_name.lower():
            if member_name in house["members"]:
                print(f"⚠️ Member '{member_name}' already exists in {house_name}.")
                return
            house["members"].append(member_name)
            house["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_yaml(data)
            print(f"👥 Added '{member_name}' to {house_name}")
            return
    print(f"❌ House '{house_name}' not found.")

def list_houses():
    data = load_yaml()
    print("\n📘 CCC Network Houses:\n")
    for i, house in enumerate(data.get("ccc_network", []), start=1):
        print(f"{i}. {house['house_name']} — Leader: {house['leader']} | Members: {len(house['members'])}")
    print("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC Network YAML Manager")
    parser.add_argument("--add-house", nargs=2, metavar=("HOUSE_NAME", "LEADER"), help="Add a new house and leader")
    parser.add_argument("--add-member", nargs=2, metavar=("HOUSE_NAME", "MEMBER"), help="Add member to a house")
    parser.add_argument("--list", action="store_true", help="List all houses")

    args = parser.parse_args()

    if args.add_house:
        add_house(args.add_house[0], args.add_house[1])
    elif args.add_member:
        add_member(args.add_member[0], args.add_member[1])
    elif args.list:
        list_houses()
    else:
        parser.print_help()
