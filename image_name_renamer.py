import os

# ✅ 1. SET YOUR FOLDER PATH HERE
folder_path = r"C:\Users\Vilma E. Agripo\Documents\JednazLonestamp\Projects\Computer.Programs\ShelterOfPraise\Database\ShelterOfPraise-AssemblyOfGod-Database-Hosting\Public\photos\events\2025\grandFellowship2025\part_3"

# ✅ 2. SET DESIRED NEW NAME FORMAT HERE
base_name = "grandFellowship_part3_2025_"

# Get all files in folder
files = os.listdir(folder_path)

# Sort files so the sequence is correct
files.sort()

number = 1

for file in files:
    # Only rename images
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        old_path = os.path.join(folder_path, file)

        # Create new name: grandFellowship_part1_2025_1.jpg
        extension = file.split(".")[-1]  # keeps original file extension
        new_name = f"{base_name}{number}.{extension}"
        new_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {file} → {new_name}")

        number += 1

print("\n✅ Done! All images renamed successfully.")
