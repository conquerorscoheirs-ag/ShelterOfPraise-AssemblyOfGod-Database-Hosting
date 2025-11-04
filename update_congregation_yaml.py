#!/usr/bin/env python3
"""
update_congregation_yaml.py

Scans public/photos/albums/<member_folder>/ for image files and updates
checklist_congregation.yaml automatically:
 - Adds new members (if missing)
 - Updates each member's "images" list
 - Maintains/updates a summary and an update_log with timestamps

Safe against missing YAML keys or empty YAML file.
"""

import os
import yaml
from datetime import datetime

# === CONFIGURATION ===
ALBUMS_PATH = "public/photos/albums"
YAML_FILE = "checklist_congregation.yaml"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")


# ---------- Load / Base Structure ----------
def safe_load_yaml(path):
    """Safely load existing YAML or return None if not found."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Warning: failed to parse YAML ({e}). Starting fresh.")
            return None


def ensure_base_structure(data):
    """Ensure YAML has required top-level keys."""
    if data is None:
        data = {}

    data.setdefault("meta", {
        "church": "Shelter of Praise | Assembly of God",
        "house": "Ascend House",
        "created_by": "CCC Network Admin Team",
        "date_created": str(datetime.now().date()),
        "purpose": "To track congregation members' appointment, participation, and inclusion status"
    })

    data.setdefault("status_legend", {
        "✅": "Completed / Included",
        "❌": "Pending / Not Yet Included",
        "🕓": "Ongoing / In Progress"
    })

    data.setdefault("members", [])
    data.setdefault("summary", {
        "total_members": 0,
        "completed": 0,
        "ongoing": 0,
        "pending": 0,
        "updated_at": str(datetime.now())
    })
    data.setdefault("update_log", [])
    return data


# ---------- Folder Scanning ----------
def scan_albums(path):
    """Return list of (folder_name, [images...]) found under path."""
    found = []
    if not os.path.exists(path):
        print(f"📁 Albums path does not exist: {path}")
        return found

    for entry in sorted(os.listdir(path)):
        folder_path = os.path.join(path, entry)
        if not os.path.isdir(folder_path):
            continue

        folder_name = entry.strip()

        images = [
            fname for fname in sorted(os.listdir(folder_path))
            if fname.lower().endswith(IMAGE_EXTENSIONS)
        ]

        if not images:
            continue

        found.append((folder_name, images))
    return found


# ---------- Update Members ----------
def update_members_with_scan(data, scanned):
    """Update members list based on scanned folders. Returns list of new names."""
    members = data.get("members", [])
    names_existing = {m.get("name"): m for m in members}
    newly_added = []

    for folder_name, images in scanned:
        member = names_existing.get(folder_name)

        if not member:
            new_entry = {
                "name": folder_name,
                "role": "Undefined",
                "contact": "N/A",
                "status": "❌",
                "remarks": f"Auto-added from folder scan. {len(images)} image(s) found.",
                "images": images,
                "added_at": str(datetime.now())
            }
            members.append(new_entry)
            names_existing[folder_name] = new_entry
            newly_added.append(folder_name)
        else:
            member["images"] = images

    data["members"] = members
    return newly_added


# ---------- Summary ----------
def recompute_summary(data):
    """Recalculate summary stats from members."""
    members = data.get("members", [])
    total = len(members)
    completed = sum(1 for m in members if str(m.get("status", "")).strip() == "✅")
    ongoing = sum(1 for m in members if str(m.get("status", "")).strip() == "🕓")
    pending = sum(1 for m in members if str(m.get("status", "")).strip() == "❌")

    data["summary"].update({
        "total_members": total,
        "completed": completed,
        "ongoing": ongoing,
        "pending": pending,
        "updated_at": str(datetime.now())
    })


# ---------- Log ----------
def append_update_log(data, added, scanned_count):
    data.setdefault("update_log", [])
    entry = {
        "timestamp": str(datetime.now()),
        "scanned_folders": scanned_count,
        "added_members": added,
        "note": f"Auto-scan completed: {scanned_count} folders scanned, {len(added)} new members added."
    }
    data["update_log"].append(entry)


# ---------- Save YAML (Enhanced Formatting) ----------
def save_yaml(path, data):
    """Save YAML file with human-readable formatting and spacing."""
    
    class IndentDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(IndentDumper, self).increase_indent(flow, False)

    # Write with indentation
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
            Dumper=IndentDumper,
            indent=2,
            default_flow_style=False,
            width=1000
        )

    # Add blank lines between members
    with open(path, "r+", encoding="utf-8") as f:
        content = f.read()
        content = content.replace("- name:", "\n- name:")
        if not content.endswith("\n"):
            content += "\n"
        f.seek(0)
        f.write(content)
        f.truncate()

    print(f"📘 Saved YAML with clear formatting to {path}")


# ---------- Main ----------
def main():
    print("🔍 Starting congregation scan...\n")

    raw = safe_load_yaml(YAML_FILE)
    data = ensure_base_structure(raw)

    scanned = scan_albums(ALBUMS_PATH)
    if not scanned:
        print("⚠️ No album folders with images were found.")
    else:
        print(f"📸 Found {len(scanned)} folders with images.")

    added = update_members_with_scan(data, scanned)
    recompute_summary(data)
    append_update_log(data, added, scanned_count=len(scanned))
    save_yaml(YAML_FILE, data)

    print("\n✅ Update complete.")
    print(f"📦 Total folders scanned: {len(scanned)}")
    print(f"🆕 New members added: {len(added)}")
    if added:
        for name in added:
            print(f"   ➕ {name}")


if __name__ == "__main__":
    main()
