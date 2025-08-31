import tkinter as tk
from tkinter import messagebox
from core.data_manager import load_crops, save_crops, export_csv, save_settings, load_settings
from core.scheduler import Scheduler
from core.models import Crop
from core.utils import status_label
from datetime import datetime

class HarvestApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Crop Harvest Calendar")
        self.scheduler = Scheduler()

        # Inputs
        tk.Label(root, text="Crop Name").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, sticky="we")

        tk.Label(root, text="Harvest Date (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=1, column=1, sticky="we")

        tk.Label(root, text="Type (optional)").grid(row=2, column=0, sticky="w")
        self.type_entry = tk.Entry(root)
        self.type_entry.grid(row=2, column=1, sticky="we")

        # Actions
        tk.Button(root, text="Add Crop", command=self.add_crop).grid(row=4, column=0, columnspan=2, sticky="we")
        tk.Button(root, text="Remove Selected", command=self.remove_selected).grid(row=5, column=0, sticky="we")
        tk.Button(root, text="Update Selected", command=self.update_selected).grid(row=5, column=1, sticky="we")

        # View toggle
        self.view_fifo = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Show NORMAL (FIFO) view", variable=self.view_fifo,
                       command=self.refresh_list).grid(row=6, column=0, columnspan=2, sticky="w")

        # List
        self.listbox = tk.Listbox(root, width=60)
        self.listbox.grid(row=7, column=0, columnspan=2, sticky="we")

        # Export
        tk.Button(root, text="Export CSV", command=self.export).grid(row=8, column=0, columnspan=2, sticky="we")

        # Layout
        root.grid_columnconfigure(1, weight=1)

        self.refresh_list()

    def on_delay_change(self):
        save_settings({"weather_delay_days": int(self.delay_var.get())})
        self.refresh_list()

    def add_crop(self):
        name = self.name_entry.get().strip()
        date_str = self.date_entry.get().strip()
        crop_type = self.type_entry.get().strip()
        if not name or not date_str:
            messagebox.showerror("Error", "Please fill name and date")
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be YYYY-MM-DD")
            return

        crops = load_crops()
        crops.append(Crop(name, date_str, crop_type=crop_type))
        save_crops(crops)
        self.refresh_list()

    def _selected_crop_name(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        text = self.listbox.get(sel[0])
        return text.split(" - ", 1)[0]

    def remove_selected(self):
        name = self._selected_crop_name()
        if not name:
            messagebox.showerror("Error", "Select a crop to remove")
            return
        crops = [c for c in load_crops() if c.name != name]
        save_crops(crops)
        self.refresh_list()

    def update_selected(self):
        name = self._selected_crop_name()
        if not name:
            messagebox.showerror("Error", "Select a crop to update")
            return
        new_date = self.date_entry.get().strip()
        if not new_date:
            messagebox.showerror("Error", "Enter a new date (YYYY-MM-DD)")
            return
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be YYYY-MM-DD")
            return

        crops = load_crops()
        for c in crops:
            if c.name == name:
                c.harvest_date = datetime.strptime(new_date, "%Y-%m-%d")
                break
        save_crops(crops)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        crops = load_crops()
        self.scheduler = Scheduler()
        for c in crops:
            self.scheduler.add_crop(c)

        rows = (self.scheduler.get_normal_fifo()
                if self.view_fifo.get()
                else self.scheduler.get_schedule())

        for d, crop in rows:
            label = status_label(d)
            idx = self.listbox.size()
            self.listbox.insert(tk.END, f"{crop.name} - {d} ({label})")
            color = "red" if label == "URGENT" else ("green" if label == "READY" else "yellow")
            try:
                self.listbox.itemconfig(idx, {'fg': color})
            except Exception:
                pass

    def export(self):
        crops = load_crops()
        file = export_csv(crops)
        messagebox.showinfo("Export", f"CSV saved to {file}")

def run():
    root = tk.Tk()
    app = HarvestApp(root)
    root.mainloop()