import tkinter as tk
from tkinter import messagebox
import json

class Spell:
    def __init__(self, name, level, type, time, target, distance, action, description):
        self.name = name
        self.level = level
        self.type = type
        self.time = time
        self.target = target
        self.distance = distance
        self.action = action
        self.description = description

#----------------------------------------------------------------
# Necessário criar uma maneira de editar as spells de maneira eficiente
# Considerar mudar o pacote de GUI para um mais moderno
#-----------------------------------------------------------------

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.attributes = ['name', 'level', 'type', 'time', 'target', 'distance', 'action', 'description'] 
        self.pack()
        self.create_widgets()
        self.spells = self.load_spells()  # Make sure this line is present
        self.spell_listbox.bind('<<ListboxSelect>>', self.display_spell)

    def load_spell(self):
        try:
            with open('spell.json', 'r') as file:
                spell_dict = json.load(file)
        except FileNotFoundError:
            spell_dict = {}
            with open('spell.json', 'w') as file:
                json.dump(spell_dict, file)
        return spell_dict

    def load_spells(self):
        try:
            spell_dict = self.load_spell()
            for name in spell_dict:
                self.spell_listbox.insert(tk.END, name)
        except FileNotFoundError:
            with open('spell.json', 'w') as file:
                json.dump({}, file)
        if not spell_dict:
            return {}
        return spell_dict    
        
    def save_spell(self, spell_dict):
        with open('spell.json', 'w') as file:
            json.dump(spell_dict, file)

    def delete_spell(self, name):
        spell_dict = self.load_spell()
        if name in spell_dict:
            del spell_dict[name]
            self.save_spell(spell_dict)

    def list_spells(self):
        spell_dict = self.load_spell()
        for name in spell_dict.keys():
            print(name)        

    def create_widgets(self):
        self.name_label = tk.Label(self, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.level_label = tk.Label(self, text="Level")
        self.level_label.pack()
        self.level_entry = tk.Entry(self)
        self.level_entry.pack()

        self.type_label = tk.Label(self, text="Type")
        self.type_label.pack()
        self.type_entry = tk.Entry(self)
        self.type_entry.pack()

        self.time_label = tk.Label(self, text="Time")
        self.time_label.pack()
        self.time_entry = tk.Entry(self)
        self.time_entry.pack()

        self.target_label = tk.Label(self, text="Target")
        self.target_label.pack()
        self.target_entry = tk.Entry(self)
        self.target_entry.pack()

        self.distance_label = tk.Label(self, text="Distance")
        self.distance_label.pack()
        self.distance_entry = tk.Entry(self)
        self.distance_entry.pack()

        self.action_label = tk.Label(self, text="Action")
        self.action_label.pack()
        self.action_entry = tk.Entry(self)
        self.action_entry.pack()

        self.description_label = tk.Label(self, text="Description")
        self.description_label.pack()
        self.description_entry = tk.Entry(self)
        self.description_entry.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.create_button = tk.Button(self.button_frame)
        self.create_button["text"] = "Create Spell"
        self.create_button["command"] = self.create_spell
        self.create_button.grid(row=0, column=0)

        self.delete_button = tk.Button(self.button_frame)
        self.delete_button["text"] = "Delete Spell"
        self.delete_button["command"] = self.delete_spell
        self.delete_button.grid(row=0, column=1)

        self.modify_label = tk.Label(self, text="Select attribute to modify:")
        self.modify_label.pack()

        self.attribute_var = tk.StringVar(self)
        self.attribute_var.set(self.attributes[0])  
        self.attribute_menu = tk.OptionMenu(self, self.attribute_var, *self.attributes)
        self.attribute_menu.pack()

        self.new_value_entry = tk.Entry(self)
        self.new_value_entry.pack()
        
        self.modify_button = tk.Button(self, text="Modify Spell", command=self.modify_spell)
        self.modify_button.pack()
        
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.spell_text = tk.Text(self)
        self.spell_text.pack(side=tk.RIGHT)
        
        self.scrollbar.config(command=self.spell_text.yview)
        
        self.spell_listbox = tk.Listbox(self)
        self.spell_listbox.pack()
        
    def create_spell(self):
        name = self.name_entry.get()
        level = self.level_entry.get()
        type = self.type_entry.get()
        time = self.time_entry.get()
        target = self.target_entry.get()
        distance = self.distance_entry.get()
        action = self.action_entry.get()
        description = self.description_entry.get()

        spell = Spell(name, level, type, time, target, distance, action, description)

        spell_dict = self.load_spell()
        spell_dict[name] = {
            'name' : name,
            'level': level,
            'type': type,
            'time': time,
            'target': target,
            'distance': distance,
            'action': action,
            'description': description,
        }

        with open('spell.json', 'w') as f:
            json.dump(spell_dict, f)

        self.spell_listbox.insert(tk.END, name)

        messagebox.showinfo("Success", "Spell created successfully")
        self.spells = self.load_spells()
        
    def delete_spell(self):
        name = self.spell_listbox.get(self.spell_listbox.curselection())
        spell_dict = self.load_spell()
        if name in spell_dict:
            del spell_dict[name]
            with open('spell.json', 'w') as f:
                json.dump(spell_dict, f)
            self.spell_listbox.delete(tk.ACTIVE)
            messagebox.showinfo("Success", "Spell deleted successfully")
        else:
            messagebox.showerror("Error", "Spell not found")
        self.spells = self.load_spells()
    
    def modify_spell(self):
        # Get the selected attribute and the new value
        attribute = self.attribute_var.get()
        new_value = self.new_value_entry.get()

        # Load the spell dictionary
        spell_dict = self.load_spell()

        # Get the selected spell
        spell_name = self.spell_listbox.get(self.spell_listbox.curselection())

        # Check if the spell and the attribute exist
        if spell_name in spell_dict and attribute in spell_dict[spell_name]:
            # Modify the attribute and save the spell dictionary
            spell_dict[spell_name][attribute] = new_value
            with open('spell.json', 'w') as f:
                json.dump(spell_dict, f)
            messagebox.showinfo("Success", f"Spell {spell_name} modified successfully")
            self.update_spell_listbox()
        else:
            messagebox.showerror("Error", "Spell or attribute not found")
            
            # Check if the spell and the attribute exist
            if attribute in spell_dict:
                # Modify the attribute and save the spell dictionary
                spell_dict[attribute] = new_value
            self.save_spell(spell_dict)


    def update_spell_listbox(self):
        # Clear the spell_listbox widget
        self.spell_listbox.delete(0, tk.END)

        # Load the spell dictionary
        spell_dict = self.load_spell()

        # Update the spell_listbox widget with the modified spell
        for spell_name in spell_dict:
            self.spell_listbox.insert(tk.END, spell_name)
            
    def display_spell(self, event):
        # Get the selected spell
        spell_name = self.spell_listbox.get(self.spell_listbox.curselection())

        # Load the spell dictionary
        spell_dict = self.load_spell()

        # Check if the spell exists
        if spell_name in spell_dict:
            # Get the spell
            spell = spell_dict[spell_name]

            # Check if the spell has all the necessary attributes
            attributes = ['name', 'level', 'type', 'time', 'target', 'distance', 'action', 'description']
            if all(attribute in spell for attribute in attributes):
                # Display the spell in the GUI
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, spell['name'])
                self.level_entry.delete(0, tk.END)
                self.level_entry.insert(0, spell['level'])
                self.type_entry.delete(0, tk.END)
                self.type_entry.insert(0, spell['type'])
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, spell['time'])
                self.target_entry.delete(0, tk.END)
                self.target_entry.insert(0, spell['target'])
                self.distance_entry.delete(0, tk.END)
                self.distance_entry.insert(0, spell['distance'])
                self.action_entry.delete(0, tk.END)
                self.action_entry.insert(0, spell['action'])
                self.description_entry.delete(0, tk.END)
                self.description_entry.insert(0, spell['description'])
            else:
                messagebox.showerror("Error", "Spell does not have all the necessary attributes")
        else:
            messagebox.showerror("Error", "Spell not found")       
        
root = tk.Tk()
app = Application(master=root)
app.mainloop()