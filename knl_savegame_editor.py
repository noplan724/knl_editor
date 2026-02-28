import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import re
import random
import os
import shutil

# --- Global Settings ---
CURRENT_FILE_PATH = "storage_v34_AUTO.dat"

# Modern UI Setup
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def create_backup():
    backup_path = CURRENT_FILE_PATH + "#bckp"
    if os.path.exists(CURRENT_FILE_PATH) and not os.path.exists(backup_path):
        try:
            shutil.copy2(CURRENT_FILE_PATH, backup_path)
            log("Backup created: " + backup_path)
        except Exception as e:
            log(f"Error creating backup: {e}")

def load_savegame():
    try:
        with open(CURRENT_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log(f"Error: File '{CURRENT_FILE_PATH}' not found!")
        return None
    except Exception as e:
        log(f"Read error: {e}")
        return None

def save_savegame(data):
    create_backup()
    try:
        with open(CURRENT_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(',', ':'))
        return True
    except Exception as e:
        log(f"Write error: {e}")
        return False

def get_next_archer_ids(data):
    objects = data.get("objects", [])
    max_x = 0
    used_ids = set()
    for obj in objects:
        name = obj.get("name", "")
        uid = obj.get("uniqueID", "")
        match_name = re.search(r"Archer P(\d+)", name)
        if match_name:
            max_x = max(max_x, int(match_name.group(1)))
        match_uid = re.search(r"--(\d+)", uid)
        if match_uid:
            used_ids.add(int(match_uid.group(1)))
    next_id = max(used_ids) + 1 if used_ids else 10000
    return max_x + 1, next_id

def add_archer(side):
    data = load_savegame()
    if not data: return
    try:
        amount = int(entry_amount.get())
        if amount <= 0:
            log("Please enter a number greater than 0.")
            return
    except ValueError:
        log("Error: Invalid number entered.")
        return

    next_x_id, next_uid = get_next_archer_ids(data)
    target_guard_side = -1 if side == "left" else 1
    
    existing_archer = None
    for obj in data.get("objects", []):
        if "Archer" in obj.get("name", ""):
            for comp in obj.get("componentData2", []):
                if comp.get("name") == "Archer":
                    try:
                        archer_data = json.loads(comp.get("data", "{}"))
                        if archer_data.get("guardSide") == target_guard_side:
                            existing_archer = obj
                            break
                    except:
                        pass
            if existing_archer:
                break 

    side_text = "Left" if side == "left" else "Right"
    added_count = 0

    for _ in range(amount):
        if existing_archer:
            base_x = existing_archer["localPosition"]["x"]
            new_y = existing_archer["localPosition"]["y"]
            new_z = existing_archer["localPosition"]["z"]
            x_str = str(base_x)
            if "." in x_str:
                int_part, frac_part = x_str.split(".")
                if len(frac_part) > 0:
                    new_frac = "".join([str(random.randint(0, 9)) for _ in range(len(frac_part))])
                    new_x = float(f"{int_part}.{new_frac}")
                else:
                    new_x = float(int_part) + random.random()
            else:
                new_x = float(base_x) + random.random()
        else:
            base_int = -11 if side == "left" else 11
            random_fraction = random.randint(100000000000000, 999999999999999)
            new_x = float(f"{base_int}.{random_fraction}")
            new_y = 0.8824997544288635
            new_z = 0.7518225908279419

        new_archer = {
            "name": f"Archer P{next_x_id}",
            "parentObject": { "linkedObjectID": "" },
            "hierarchyPath": "Level/GameLayer/",
            "prefabPath": "Prefabs/Characters/Archer",
            "uniqueID": f"Archer P{next_x_id}--{next_uid}",
            "mode": 0,
            "createOrder": -1,
            "linkOrder": 0,
            "localPosition": {"x": new_x, "y": new_y, "z": new_z},
            "localScale": { "x": 1.0 if side == "right" else -1.0, "y": 1.0, "z": 1.0 },
            "componentData2": [
                { "name": "Wallet", "type": "WalletData", "data": "{\"coins\":1}" },
                { "name": "Character", "type": "CharacterData", "data": "{\"isGrabbed\":false,\"inert\":false}" },
                { "name": "Archer", "type": "ArcherData", "data": f"{{\"tower\":{{\"linkedObjectID\":\"\"}},\"knight\":{{\"linkedObjectID\":\"\"}},\"guardSide\":{target_guard_side}}}" },
                { "name": "Damageable", "type": "DamageableData", "data": "{\"hitPoints\":0,\"invulnerable\":false}" }
            ]
        }
        data.get("objects", []).append(new_archer)
        next_x_id += 1
        next_uid += 1
        added_count += 1
    
    if save_savegame(data):
        log(f"Success: Added {added_count} archer(s) ({side_text})!")

def set_banker_coins():
    data = load_savegame()
    if not data: return
    found = False
    for obj in data.get("objects", []):
        if obj.get("name") == "Banker(Clone)":
            for comp in obj.get("componentData2", []):
                if comp.get("name") == "Banker":
                    comp["data"] = "{\"stashedCoins\":999}"
                    found = True
                    break
    if found:
        if save_savegame(data):
            log("Success: The banker now has 999 coins!")
    else:
        log("Error: Banker not found in save file.")

def set_player_coins():
    data = load_savegame()
    if not data: return
    found = False
    for obj in data.get("objects", []):
        if obj.get("name") == "Player(Clone)":
            for comp in obj.get("componentData2", []):
                if comp.get("name") == "Wallet":
                    try:
                        wallet_data = json.loads(comp["data"])
                        wallet_data["coins"] = 40
                        comp["data"] = json.dumps(wallet_data, separators=(',', ':'))
                        found = True
                    except json.JSONDecodeError:
                        pass
                    break
            if found: break
    if found:
        if save_savegame(data):
            log("Success: Your wallet is now full (40 coins)!")
    else:
        log("Error: Player not found in save file.")

def set_shrine_time():
    data = load_savegame()
    if not data: return
    found_any = False
    for obj in data.get("objects", []):
        name = obj.get("name", "")
        if name in ["Statue Archer(Clone)", "Statue Worker(Clone)"]:
            for comp in obj.get("componentData2", []):
                if comp.get("name") == "Statue":
                    try:
                        statue_data = json.loads(comp["data"])
                        statue_data["currentCharge"] = 999.0
                        comp["data"] = json.dumps(statue_data, separators=(',', ':'))
                        found_any = True
                    except json.JSONDecodeError:
                        pass
    if found_any:
        if save_savegame(data):
            log("Success: Shrines are now active for 999 days!")
    else:
        log("Error: No statues (Archer/Worker) found in save file.")

def set_portal_hp():
    data = load_savegame()
    if not data: return
    found_any = False
    for obj in data.get("objects", []):
        if "Portal" in obj.get("name", ""):
            for comp in obj.get("componentData2", []):
                if comp.get("name") == "Damageable":
                    try:
                        dmg_data = json.loads(comp["data"])
                        if dmg_data.get("hitPoints", 0) > 1:
                            dmg_data["hitPoints"] = 1.0
                            comp["data"] = json.dumps(dmg_data, separators=(',', ':'))
                            found_any = True
                    except json.JSONDecodeError:
                        pass
    if found_any:
        if save_savegame(data):
            log("Success: All intact portals now have 1 HP!")
    else:
        log("Notice: No active portals found or HP is already 1.")

def show_howto():
    howto_text = (
        "Welcome to the Kingdom: New Lands Save Editor!\n\n"
        "This tool edits the underlying savegame file of your game.\n\n"
        "--- IMPORTANT ---\n"
        "Some functions are only possible if the game is completely CLOSED. "
        "If the game is running while you edit the file, it might overwrite your changes or fail to load them. "
        "Always save and quit your game before clicking the cheat buttons!\n\n"
        "A backup file (*.dat#bckp) is automatically created the first time you modify your save."
    )
    messagebox.showinfo("Instructions", howto_text)

def change_file():
    global CURRENT_FILE_PATH
    filepath = filedialog.askopenfilename(
        title="Select Kingdom: New Lands Savegame",
        filetypes=(("DAT files", "*.dat"), ("Text files", "*.txt"), ("All files", "*.*"))
    )
    if filepath:
        CURRENT_FILE_PATH = filepath
        lbl_file.configure(text=f"...{filepath[-40:]}")
        log(f"New file selected. (Backup will be created on first edit)")

def log(message):
    text_log.configure(state="normal")
    text_log.insert("end", "> " + message + "\n")
    text_log.see("end")
    text_log.configure(state="disabled")

# --- App Window ---
app = ctk.CTk()
app.title("Kingdom: New Lands - Save Editor")
app.geometry("580x720") # Fenster etwas höher für den Exit-Button
app.resizable(False, False)

# --- Header ---
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(pady=20, fill="x")

ctk.CTkLabel(header_frame, text="Kingdom: New Lands", font=ctk.CTkFont(size=24, weight="bold")).pack()
ctk.CTkLabel(header_frame, text="Savegame Editor", font=ctk.CTkFont(size=16), text_color="gray").pack()

btn_howto = ctk.CTkButton(header_frame, text="📘 Instructions / HowTo", fg_color="#455A64", hover_color="#37474F", command=show_howto)
btn_howto.pack(pady=10)

# --- File Section ---
file_frame = ctk.CTkFrame(app)
file_frame.pack(padx=20, pady=10, fill="x")

lbl_file = ctk.CTkLabel(file_frame, text=CURRENT_FILE_PATH, text_color="gray")
lbl_file.pack(side="left", padx=15, pady=10)

btn_file = ctk.CTkButton(file_frame, text="Change File", width=100, command=change_file)
btn_file.pack(side="right", padx=15, pady=10)

# --- Cheats Section ---
cheats_frame = ctk.CTkFrame(app)
cheats_frame.pack(padx=20, pady=10, fill="x")

# Grid Layout for Buttons
cheats_frame.columnconfigure(0, weight=1)
cheats_frame.columnconfigure(1, weight=1)

# Archer Input
archer_frame = ctk.CTkFrame(cheats_frame, fg_color="transparent")
archer_frame.grid(row=0, column=0, columnspan=2, pady=(15, 10))
ctk.CTkLabel(archer_frame, text="Archers per click:").pack(side="left", padx=10)
entry_amount = ctk.CTkEntry(archer_frame, width=60, justify="center")
entry_amount.insert(0, "5")
entry_amount.pack(side="left")

# Cheat Buttons
btn_arch_l = ctk.CTkButton(cheats_frame, text="🏹 Add Archers (LEFT)", fg_color="#00695C", hover_color="#004D40", command=lambda: add_archer("left"))
btn_arch_l.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

btn_arch_r = ctk.CTkButton(cheats_frame, text="🏹 Add Archers (RIGHT)", fg_color="#00695C", hover_color="#004D40", command=lambda: add_archer("right"))
btn_arch_r.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

btn_banker = ctk.CTkButton(cheats_frame, text="💰 Banker: 999 Coins", fg_color="#F57F17", hover_color="#FBC02D", text_color="black", command=set_banker_coins)
btn_banker.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

btn_player = ctk.CTkButton(cheats_frame, text="👛 Wallet: Full (40 Coins)", fg_color="#F57F17", hover_color="#FBC02D", text_color="black", command=set_player_coins)
btn_player.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

btn_shrine = ctk.CTkButton(cheats_frame, text="⚡ Shrines: 999 Days", fg_color="#6A1B9A", hover_color="#4A148C", command=set_shrine_time)
btn_shrine.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

btn_portal = ctk.CTkButton(cheats_frame, text="🌌 Portals: 1 HP", fg_color="#C62828", hover_color="#B71C1C", command=set_portal_hp)
btn_portal.grid(row=3, column=1, padx=10, pady=(10, 15), sticky="ew")

# --- Log Section ---
text_log = ctk.CTkTextbox(app, height=100, font=ctk.CTkFont(family="Consolas", size=13))
text_log.pack(padx=20, pady=(10, 5), fill="both", expand=True)
text_log.configure(state="disabled")

# --- Exit Button ---
btn_exit = ctk.CTkButton(app, text="❌ Exit Program", fg_color="#D32F2F", hover_color="#B71C1C", command=app.quit)
btn_exit.pack(pady=(5, 15))

# Initial Check
if not os.path.exists(CURRENT_FILE_PATH):
    log(f"Warning: File '{CURRENT_FILE_PATH}' not found.")
    log("Please select your savegame using the 'Change File' button.")
else:
    log("Ready! Save file found.")

# Start Mainloop
app.mainloop()