import tkinter as tk
from tkinter import messagebox

from Src.db.Schema import BulkUploads, SystemSettings
from Src.log.Logger import Logger
from Src.login import AccessInfo

class BaseRegistration:
    def __init__(self, model, entity_name, key_column):
        self._model = model
        self._settings = SystemSettings()
        self.entity_name = entity_name
        self.key_column = key_column
        self.selected_key = None

    def delete_record(self, record_key=None):
        try:
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
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not delete {self.entity_name}. Please try again.")


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

    def import_records(self,upload_type,file_path,success_count,failed_count):
        try:  
            BulkUploads().insert(
            upload_type=upload_type,
            file_name=file_path.split("/")[-1],
            success_count=success_count,
            failed_count=failed_count,
            uploaded_by=AccessInfo.USER_ID
        )

        except Exception as e:
            Logger.log(f"Failed to record bulk upload log: {e}")

