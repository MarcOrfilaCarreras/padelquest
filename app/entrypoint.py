# -*- coding: utf-8 -*-
import importlib
import os

from app import app

if __name__ == "__main__":
    if os.path.isdir("plugins"):
        for plugin_folder in os.listdir('plugins'):
            if os.path.isdir(os.path.join('plugins', plugin_folder)):
                for plugin_file in os.listdir(os.path.join('plugins', plugin_folder)):
                    if plugin_file == 'entrypoint.py':
                        # Remove the '.py' extension from plugin_file
                        plugin_name = plugin_file[:-3]
                        plugin_module = importlib.import_module(
                            f'plugins.{plugin_folder}.{plugin_name}')
                        plugin_module.register_plugin(app)
    app.run()
