#!/usr/bin/env python3
"""
PyDex GUI: A Graphical Pokedex
A modern, beautiful tkinter-based GUI for looking up Pokémon information from the PokéAPI.
"""

import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

class PokedexGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyDex")
        self.root.geometry("1100x800")
        self.root.resizable(False, False)
        
        # Set pokeball icon
        try:
            icon = Image.open("pokeball.png")
            icon_photo = ImageTk.PhotoImage(icon)
            self.root.iconphoto(True, icon_photo)
        except:
            pass  # If icon not found, continue without it
        
        # Beautiful modern color palette
        self.bg_gradient_top = "#dd3315"  # Red
        self.bg_gradient_bottom = "#764ba2"  # Deep purple
        self.bg_main = "#f8fafc"  # Light gray
        self.card_bg = "#ffffff"
        self.accent = "#dd3315"
        self.accent_hover = "#8c251a"
        self.text_primary = "#1e293b"
        self.text_secondary = "#64748b"
        self.text_light = "#94a3b8"
        
        # Type colors
        self.type_colors = {
            'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0',
            'electric': '#F8D030', 'grass': '#78C850', 'ice': '#98D8D8',
            'fighting': '#C03028', 'poison': '#A040A0', 'ground': '#E0C068',
            'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
            'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8',
            'dark': '#705848', 'steel': '#B8B8D0', 'fairy': '#EE99AC'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Gradient header - narrower
        header = tk.Frame(self.root, bg=self.bg_gradient_top, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Title only (no subtitle)
        title_frame = tk.Frame(header, bg=self.bg_gradient_top)
        title_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(title_frame, text="Pokédex", font=("Helvetica", 28, "bold"),
                bg=self.bg_gradient_top, fg="white").pack()
        
        # Main container
        main = tk.Frame(self.root, bg=self.bg_main)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Search bar
        search_container = tk.Frame(main, bg=self.bg_main)
        search_container.pack(pady=20)
        
        search_card = tk.Frame(search_container, bg=self.card_bg, relief=tk.FLAT)
        search_card.pack()
        
        # Add shadow effect with border
        search_inner = tk.Frame(search_card, bg=self.card_bg)
        search_inner.pack(padx=3, pady=3)
        
        search_frame = tk.Frame(search_inner, bg=self.card_bg)
        search_frame.pack(padx=20, pady=12)
        
        # Entry field
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     font=("Helvetica", 14), width=35,
                                     relief=tk.FLAT, bg="#f1f5f9",
                                     fg=self.text_primary, borderwidth=0)
        self.search_entry.pack(side=tk.LEFT, ipady=10, padx=(0, 15))
        self.search_entry.bind("<Return>", lambda e: self.search_pokemon())
        
        # Search button with modern style
        search_btn = tk.Button(search_frame, text="Search", command=self.search_pokemon,
                              bg=self.accent, fg="white", font=("Helvetica", 12, "bold"),
                              relief=tk.FLAT, padx=30, pady=10, cursor="hand2",
                              activebackground=self.accent_hover, activeforeground="white",
                              borderwidth=0)
        search_btn.pack(side=tk.LEFT)
        
        # Content area
        content = tk.Frame(main, bg=self.bg_main)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Pokemon card (no scrollbar needed)
        self.pokemon_card = tk.Frame(content, bg=self.card_bg, relief=tk.FLAT)
        self.pokemon_card.pack(fill=tk.BOTH, expand=True)
        
        # Initial welcome state
        self.show_welcome()
    
    def show_welcome(self):
        # Clear card
        for widget in self.pokemon_card.winfo_children():
            widget.destroy()
        
        # Content frame centered in canvas
        content_frame = tk.Frame(self.pokemon_card, bg=self.card_bg)
        content_frame.pack(expand=True, pady=180)
        
        # Load and display pokeball image
        try:
            pokeball_img = Image.open("pokeball.png")
            pokeball_img = pokeball_img.resize((120, 120), Image.Resampling.LANCZOS)
            pokeball_photo = ImageTk.PhotoImage(pokeball_img)
            pokeball_label = tk.Label(content_frame, image=pokeball_photo, bg=self.card_bg)
            pokeball_label.image = pokeball_photo  # Keep a reference
            pokeball_label.pack(pady=(0, 20))
        except:
            # If image not found, show emoji
            tk.Label(content_frame, text="⚪", font=("Helvetica", 60),
                    bg=self.card_bg).pack(pady=(0, 20))
        
        tk.Label(content_frame, text="Search for any Pokémon", font=("Helvetica", 24, "bold"),
                bg=self.card_bg, fg=self.text_primary).pack()
        tk.Label(content_frame, text="Enter a name or ID number in the search bar above", font=("Helvetica", 14),
                bg=self.card_bg, fg=self.text_secondary).pack(pady=(10, 0))
    
    def search_pokemon(self):
        query = self.search_var.get().strip().lower()
        if not query:
            messagebox.showwarning("Empty Search", "Please enter a Pokémon name or ID")
            return
        
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{query}")
            if response.status_code == 200:
                data = response.json()
                self.display_pokemon(data)
            else:
                messagebox.showerror("Not Found", f"Pokémon '{query}' not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data:\n{str(e)}")
    
    def display_pokemon(self, data):
        # Clear card
        for widget in self.pokemon_card.winfo_children():
            widget.destroy()
        
        # Main layout: left (sprite) | right (info)
        left_panel = tk.Frame(self.pokemon_card, bg=self.card_bg, width=320)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=25, pady=20)
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(self.pokemon_card, bg=self.card_bg)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 25), pady=20)
        
        # LEFT PANEL - Sprite
        sprite_container = tk.Frame(left_panel, bg="#f8fafc")
        sprite_container.pack(expand=True, fill=tk.BOTH)
        
        sprite_url = data['sprites']['front_default']
        if sprite_url:
            try:
                img_response = requests.get(sprite_url)
                img_data = Image.open(BytesIO(img_response.content))
                img_data = img_data.resize((250, 250), Image.Resampling.LANCZOS)
                sprite = ImageTk.PhotoImage(img_data)
                sprite_label = tk.Label(sprite_container, image=sprite, bg="#f8fafc")
                sprite_label.image = sprite
                sprite_label.pack(expand=True)
            except:
                tk.Label(sprite_container, text="🖼️", font=("Helvetica", 60),
                        bg="#f8fafc", fg=self.text_light).pack(expand=True)
        
        # Pokédex number badge
        number_badge = tk.Label(left_panel, text=f"#{data['id']:03d}",
                               font=("Helvetica", 14, "bold"), bg=self.accent,
                               fg="white", padx=16, pady=6)
        number_badge.pack(pady=(10, 0))
        
        # RIGHT PANEL - Info
        
        # Name
        name = data['name'].title()
        tk.Label(right_panel, text=name, font=("Helvetica", 28, "bold"),
                bg=self.card_bg, fg=self.text_primary).pack(anchor=tk.W, pady=(0, 10))
        
        # Types
        type_frame = tk.Frame(right_panel, bg=self.card_bg)
        type_frame.pack(anchor=tk.W, pady=(0, 12))
        
        for type_info in data['types']:
            type_name = type_info['type']['name'].title()
            type_color = self.type_colors.get(type_info['type']['name'], '#999')
            
            type_badge = tk.Label(type_frame, text=type_name, font=("Helvetica", 12, "bold"),
                                 bg=type_color, fg="white", padx=16, pady=6)
            type_badge.pack(side=tk.LEFT, padx=(0, 8))
        
        # Stats section
        tk.Label(right_panel, text="Base Stats", font=("Helvetica", 15, "bold"),
                bg=self.card_bg, fg=self.text_primary).pack(anchor=tk.W, pady=(0, 8))
        
        stats_container = tk.Frame(right_panel, bg=self.card_bg)
        stats_container.pack(fill=tk.BOTH, expand=True)
        
        stat_names = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        
        for i, (name, stat_data) in enumerate(zip(stat_names, data['stats'])):
            value = stat_data['base_stat']
            
            # Stat row
            row = tk.Frame(stats_container, bg=self.card_bg)
            row.pack(fill=tk.X, pady=3)
            
            # Name
            tk.Label(row, text=name, font=("Helvetica", 11, "bold"),
                    bg=self.card_bg, fg=self.text_secondary, width=10, anchor=tk.W).pack(side=tk.LEFT)
            
            # Value
            tk.Label(row, text=str(value), font=("Helvetica", 11, "bold"),
                    bg=self.card_bg, fg=self.text_primary, width=4, anchor=tk.E).pack(side=tk.LEFT, padx=(0, 10))
            
            # Bar background
            bar_bg = tk.Frame(row, bg="#e2e8f0", height=18)
            bar_bg.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Bar fill
            percentage = min(value / 255, 1.0)
            bar_color = self.get_stat_color(value)
            
            bar_fill = tk.Frame(bar_bg, bg=bar_color, height=18)
            bar_fill.place(relwidth=percentage, relheight=1)
        
        # Physical info section
        tk.Label(right_panel, text="Physical Info", font=("Helvetica", 15, "bold"),
                bg=self.card_bg, fg=self.text_primary).pack(anchor=tk.W, pady=(12, 8))
        
        info_grid = tk.Frame(right_panel, bg=self.card_bg)
        info_grid.pack(fill=tk.X)
        
        # Height
        height_m = data['height'] / 10
        feet = int(height_m * 3.28084)
        inches = int((height_m * 3.28084 - feet) * 12)
        
        info_item(info_grid, "Height", f"{height_m:.1f}m ({feet}'{inches:02d}\")", 0, 0)
        
        # Weight  
        weight_kg = data['weight'] / 10
        lbs = weight_kg * 2.20462
        
        info_item(info_grid, "Weight", f"{weight_kg:.1f}kg ({lbs:.1f} lbs)", 1, 0)
        
        # Abilities
        abilities = [a['ability']['name'].replace('-', ' ').title() 
                    for a in data['abilities'] if not a['is_hidden']]
        ability_text = ", ".join(abilities) if abilities else "None"
        
        info_item(info_grid, "Abilities", ability_text, 0, 1)
        
        # Hidden Ability
        hidden_abilities = [a['ability']['name'].replace('-', ' ').title() 
                           for a in data['abilities'] if a['is_hidden']]
        hidden_text = ", ".join(hidden_abilities) if hidden_abilities else "None"
        
        info_item(info_grid, "Hidden Ability", hidden_text, 1, 1)
    
    def get_stat_color(self, value):
        """Return color gradient based on stat value"""
        if value >= 120:
            return "#10b981"  # Emerald
        elif value >= 90:
            return "#22c55e"  # Green
        elif value >= 70:
            return "#84cc16"  # Lime
        elif value >= 50:
            return "#eab308"  # Yellow
        elif value >= 30:
            return "#f59e0b"  # Amber
        else:
            return "#ef4444"  # Red

def info_item(parent, label, value, col, row):
    """Helper to create info grid items"""
    frame = tk.Frame(parent, bg="#f8fafc", padx=10, pady=8)
    frame.grid(row=row, column=col, sticky="ew", padx=(0, 6 if col == 0 else 0), pady=(0, 6 if row == 0 else 0))
    parent.grid_columnconfigure(col, weight=1)
    
    tk.Label(frame, text=label, font=("Helvetica", 9),
            bg="#f8fafc", fg="#64748b").pack(anchor=tk.W)
    tk.Label(frame, text=value, font=("Helvetica", 11, "bold"),
            bg="#f8fafc", fg="#1e293b").pack(anchor=tk.W, pady=(2, 0))

def main():
    root = tk.Tk()
    app = PokedexGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
