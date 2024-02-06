import importlib
import os
import sys
import subprocess
import re


PLUGINS_PACKAGE_NAME = "hotloaded_plugins"
PLUGINS_MODULE_PATTERN = re.compile(r'^plugin[0-9]+\.py$')


def get_plugins_package():
    return importlib.import_module(PLUGINS_PACKAGE_NAME)


def reload_plugins():
    """
    Update the hotloaded_plugins package to the latest version.
    """
    # Update and reload the plugins package
    try:
        subprocess.run(["poetry", "update", PLUGINS_PACKAGE_NAME], check=True)
        print(f"Successfully updated package '{PLUGINS_PACKAGE_NAME}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update package '{PLUGINS_PACKAGE_NAME}'. Error: {e}")

    # Delete the package from sys.modules
    package_submodules = [mod for mod in sys.modules
                          if mod.startswith(PLUGINS_PACKAGE_NAME)]

    for submodule in package_submodules:
        del sys.modules[submodule]

    # Reload the package
    new_package = get_plugins_package()

    print(f"Reloaded package '{PLUGINS_PACKAGE_NAME}'")

    return new_package


def get_plugins_list(plugins_module) -> list:
    """
    Dynamically load the plugins from hotloaded_plugins and store them in the
    plugins list
    """
    plugins_list = []

    # Extract the list of plugin#.py files
    package_path = os.path.join(
        os.path.dirname(os.path.abspath(plugins_module.__file__)),
        "plugins")

    plugin_files = [f for f in os.listdir(package_path)
                    if PLUGINS_MODULE_PATTERN.match(f)]

    # Load each plugin and store it in the plugins list
    for file in plugin_files:
        module_name = file[:-3]
        module_path = f"{PLUGINS_PACKAGE_NAME}.plugins.{module_name}"
        imported_module = importlib.import_module(module_path)

        # Store the plugin class
        class_name = module_name.capitalize()

        try:
            plugin_class = getattr(imported_module, class_name)
            plugins_list.append(plugin_class())
        except AttributeError:
            print(f"Could not find class {class_name} in module {module_path}")

    print(f"Loaded {len(plugins_list)} plugins")
    return plugins_list
