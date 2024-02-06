import tkinter as tk
from tkinter import ttk
from .reload_logic import reload_plugins, get_plugins_list, get_plugins_package


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400


def populate_table(table, plugins_list):
    """
    Populates the table with a list of plugins and their descriptions
    """
    # Clear existing data in the table
    for item in table.get_children():
        table.delete(item)

    # Extract data from plugins and populate the table
    for plugin in plugins_list:
        name = plugin.get_name()
        description = plugin.get_description()

        table.insert('', 'end', values=(name, description))


def handle_reload_click(root, table):
    """
    When 'Reload' is pressed, fully reload the plugins package and
    update the table with the new list.
    """
    root.config(cursor="watch")
    root.update()

    plugins_module = reload_plugins()
    plugins_list = get_plugins_list(plugins_module)
    populate_table(table, plugins_list)

    root.config(cursor="")
    root.update()


def build_gui(plugins_list):
    """
    Build a basic tkinter GUI to display the list of plugins
    """
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
    populate_table(table, plugins_list)

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
    plugins_module = get_plugins_package()
    plugins_list = get_plugins_list(plugins_module)

    build_gui(plugins_list)


if __name__ == "__main__":
    run()
