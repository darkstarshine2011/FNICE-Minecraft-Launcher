# Minecraft Launcher By FNICE

import minecraft_launcher_lib
import subprocess
import threading
import json

MinecraftFolder = minecraft_launcher_lib.utils.get_minecraft_directory()

class API:
    def __init__(self):
        self.window = None

    def _js(self, code):
        try:
            self.window.evaluate_js(code)
        except:
            pass
        
    def get_versions(self):
        versions = minecraft_launcher_lib.utils.get_version_list()
        result = [v["id"] for v in versions if v["type"] == "release"]
        return json.dumps(result)
    
    def get_modloader_versions(self, mc_version, modloader):

        try:
            if modloader == "fabric":
                versions = minecraft_launcher_lib.fabric.get_all_loader_versions()
                result = [v["version"] for v in versions]

            elif modloader == "forge":
                all_versions = minecraft_launcher_lib.forge.list_forge_versions()
                result = [v for v in all_versions if v.startswith(mc_version + "-")]

            elif modloader == "neoforge":
                all_versions = minecraft_launcher_lib.neoforge.list_neoforge_versions()
                mc_parts = mc_version.split(".")
                major = mc_parts[1] 
                result = [
                    v for v in all_versions
                    if v.startswith(major + ".") or v.startswith(mc_version + "-")
                ]
            else:
                result = []

            return json.dumps(result[:30])   
        
        except Exception as e:
            return json.dumps([])
 
    def install_and_launch(self, mc_version, modloader, modloader_version, username):

        def task():
            callback = {
                "setStatus":   lambda s: self._js(f'updateStatus("{s}")'),
                "setProgress": lambda v: self._js(f'updateProgress({v})'),
                "setMax":      lambda v: self._js(f'setMaxProgress({v})'),
            }

            try:

                if modloader == "vanilla":
                    self._js('updateStatus("Installing Minecraft...")')
                    minecraft_launcher_lib.install.install_minecraft_version(
                        mc_version, MinecraftFolder, callback=callback
                    )
                    launch_version = mc_version

                elif modloader == "fabric":

                    self._js('updateStatus("Installing Minecraft...")')
                    minecraft_launcher_lib.install.install_minecraft_version(
                        mc_version, MinecraftFolder, callback=callback
                    )


                    self._js('updateStatus("Installing Fabric...")')
                    minecraft_launcher_lib.fabric.install_fabric(
                        mc_version,
                        MinecraftFolder,
                        loader_version=modloader_version,
                        callback=callback
                    )

                    launch_version = f"fabric-loader-{modloader_version}-{mc_version}"

                elif modloader == "forge":
                    self._js('updateStatus("Installing Forge...")')
                    minecraft_launcher_lib.forge.install_forge_version(
                        modloader_version,  # مثلاً "1.20.1-47.2.0"
                        MinecraftFolder
                    )
                    forge_build = modloader_version.split("-")[1]  # "47.2.0"
                    launch_version = f"{mc_version}-forge-{forge_build}"

                elif modloader == "neoforge":
                    self._js('updateStatus("Installing NeoForge...")')
                    minecraft_launcher_lib.neoforge.install_neoforge_version(
                        modloader_version,
                        MinecraftFolder
                    )
                    launch_version = f"neoforge-{modloader_version}"


                options = minecraft_launcher_lib.utils.generate_test_options()
                options["username"] = username

                self._js('updateStatus("Launching...")')
                command = minecraft_launcher_lib.command.get_minecraft_command(
                    launch_version, MinecraftFolder, options
                )


                subprocess.Popen(command)
                self._js('onLaunched()')

            except Exception as e:
                self._js(f'updateStatus("ERROR: {str(e)}")')
                self._js('document.getElementById("launch-btn").disabled = false')

        threading.Thread(target=task, daemon=True).start()