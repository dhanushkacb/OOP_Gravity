import tkinter as tk
from tkinter import messagebox

class BaseRegistration:
    def __init__(self, model, entity_name, key_column):
        self._model = model
        self.entity_name = entity_name
        self.key_column = key_column
        self.selected_key = None

    def delete_record(self, record_key=None):
        if not messagebox.askyesno("Delete", f"Are you sure you want to delete this {self.entity_name}?"):
            return

        row_value = record_key or self.selected_key
        if not row_value:
            messagebox.showerror("Error", f"Select a {self.entity_name} to delete")
            return

        if self._model.delete(self.key_column, row_value):
            messagebox.showinfo("Success", f"{self.entity_name} deleted successfully!")
            self.load_records()  # must exist in child
        else:
            messagebox.showerror("Error", f"Failed to delete {self.entity_name}.")

    def on_tree_item_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not row_id or not col:
            return

        values = self.tree.item(row_id, "values")
        record_key = values[0]  # assumes first col is key

        if col == f"#{len(self.tree['columns'])}":  # last column = delete
            self.delete_record(record_key)

