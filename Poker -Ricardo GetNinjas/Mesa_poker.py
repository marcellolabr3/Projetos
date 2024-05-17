import pygetwindow as gw
import json
import tkinter as tk
from tkinter import ttk
import os
import subprocess

class WindowManager:
    def __init__(self):
        self.loaded_presets = set()

    def capture_window_positions(self):
        chrome_windows = gw.getWindowsWithTitle("Google Chrome")
        window_positions = {}
        for window in chrome_windows:
            window_positions[window.title] = {
                "left": window.left,
                "top": window.top,
                "width": window.width,
                "height": window.height,
                "maximized": window.isMaximized
            }
        return window_positions

    def save_layout(self, layout_name, window_positions):
        with open(f"{layout_name}.json", "w") as file:
            json.dump(window_positions, file)

    def load_layout(self, layout_name):
        with open(f"{layout_name}.json", "r") as file:
            return json.load(file)

    def rearrange_windows(self, window_positions):
        for title, position in window_positions.items():
            window = gw.getWindowsWithTitle(title)
            if window:
                window = window[0]
                window.restore()  # Garante que a janela não está maximizada
                window.moveTo(position["left"], position["top"])
                window.resizeTo(position["width"], position["height"])
                if position["maximized"]:
                    window.maximize()  # Maximiza se estava maximizada

    def load_preset(self, preset_name):
        window_positions = self.load_layout(preset_name)
        if window_positions:
            self.rearrange_windows(window_positions)
            self.loaded_presets.add(preset_name)

class LayoutManager:
    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager

        # Interface de usuário
        self.layout_name_label = ttk.Label(root, text="Nome do Layout:")
        self.layout_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.layout_name_entry = ttk.Entry(root)
        self.layout_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(root, text="Salvar Layout", command=self.save_layout_and_update_combobox)
        self.save_button.grid(row=0, column=2, padx=5, pady=5)

        self.layout_combobox = ttk.Combobox(root, state="readonly")
        self.layout_combobox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.layout_combobox.bind("<<ComboboxSelected>>", self.load_selected_preset)

        self.load_button = ttk.Button(root, text="Carregar Layout", command=self.load_selected_preset)
        self.load_button.grid(row=1, column=2, padx=5, pady=5)

        # Carrega presets salvos ao iniciar
        self.load_saved_presets()

    def save_layout_and_update_combobox(self):
        layout_name = self.layout_name_entry.get()
        window_positions = self.window_manager.capture_window_positions()
        if window_positions:
            self.window_manager.save_layout(layout_name, window_positions)
            self.window_manager.loaded_presets.add(layout_name)  # Adiciona o preset à lista de presets carregados
            self.layout_combobox["values"] = sorted(list(self.window_manager.loaded_presets))

    def load_selected_preset(self, event=None):
        preset_name = self.layout_combobox.get()
        if preset_name in self.window_manager.loaded_presets:
            self.window_manager.load_preset(preset_name)

    def load_saved_presets(self):
        saved_presets = [filename.split(".")[0] for filename in os.listdir(".") if filename.endswith(".json")]
        for preset_name in saved_presets:
            self.window_manager.loaded_presets.add(preset_name)
        self.layout_combobox["values"] = sorted(list(self.window_manager.loaded_presets))

# Interface de usuário
root = tk.Tk()
root.title("Gerenciador de Layouts")

window_manager = WindowManager()
layout_manager = LayoutManager(root, window_manager)

root.mainloop()
