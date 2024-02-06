import importlib
import os
import subprocess
import re
import tkinter as tk
from tkinter import ttk
from hotloaded_plugins import plugins

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

PLUGINS_PACKAGE = "hotloaded_plugins"

plugin_pattern = re.compile(r'^plugin[0-9]+\.py$')
plugins_list = []


def reload_plugins():
    # Update and reload the plugins package
    try:
        subprocess.run(["poetry", "update", PLUGINS_PACKAGE], check=True)
        print(f"Successfully updated package '{PLUGINS_PACKAGE}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update package '{PLUGINS_PACKAGE}'. Error: {e}")

    importlib.reload(plugins)

    print(f"Reloaded package '{PLUGINS_PACKAGE}'")


def store_plugins():
    """
    Dynamically load the plugins from hotloaded_plugins and store them in the
    plugins list
    """
    plugins_list.clear()

    package_path = os.path.dirname(os.path.abspath(plugins.__file__))
    plugin_files = [f for f in os.listdir(package_path)
                    if plugin_pattern.match(f)]

    for file in plugin_files:

        # Load the plugin module
        module_name = file[:-3]
        module_path = f"hotloaded_plugins.plugins.{module_name}"
        imported_module = importlib.import_module(module_path)

        # Store the plugin class
        class_name = module_name.capitalize()

        try:
            plugin_class = getattr(imported_module, class_name)
            plugins_list.append(plugin_class())
        except AttributeError:
            print(f"Could not find class {class_name} in module {module_path}")

    print(f"Loaded {len(plugins_list)} plugins")


def populate_table(table):
    # Clear existing data in the table
    for item in table.get_children():
        table.delete(item)

    # Extract data from plugins and populate the table
    for plugin in plugins_list:
        name = plugin.get_name()
        description = plugin.get_description()

        table.insert('', 'end', values=(name, description))


def handle_reload_click(root, table):
    root.config(cursor="watch")
    root.update()

    reload_plugins()
    store_plugins()
    populate_table(table)

    root.config(cursor="")
    root.update()


def build_gui():
    root = tk.Tk()
    root.title("Hotloaded Server")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Create a label widget
    title_label = tk.Label(root, text="Hotloaded Plugins", font=("Arial", 16))
    title_label.pack(pady=10)

    # Add a table area
    columns = {
        "name": {
            "width": int(WINDOW_WIDTH * 0.4),
            "anchor": "center"
        },
        "description": {
            "width": int(WINDOW_WIDTH * 0.6),
            "anchor": "w"
        }
    }

    table = ttk.Treeview(root, columns=list(columns.keys()), show="headings")

    for col, kw in columns.items():
        table.column(col, **kw)
        table.heading(col, text=col.capitalize())

    # Insert data
    populate_table(table)

    # Save the table
    table.pack(expand=True, fill='both')

    # Add a 'Reload' button
    reload_button = tk.Button(root, text="Reload", font=("Arial", 12),
                              command=lambda: handle_reload_click(root, table))
    reload_button.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()


def run():
    """
    Load the plugins from hotloaded_plugins and then build the GUI
    """
    store_plugins()
    build_gui()


if __name__ == "__main__":
    run()
