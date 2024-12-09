from swarm.framework import SwarmTool, SwarmState
from typing import Annotated, Dict, List, Union
import os
import subprocess
import sys
import shutil
import copy

class GetRootDir(SwarmTool):
    """
    Extracts the common root directory from file paths.
    """
    def run(self, files: Annotated[Dict[str, str], dict]) -> str:
        if not files:
            return "project-root/"

        paths = list(files.keys())
        common_prefix = os.path.commonpath(paths)

        # If no common prefix is found, default to project-root
        if not common_prefix or common_prefix == '/':
            return "project-root/"

        # Ensure trailing slash
        return common_prefix if common_prefix.endswith('/') else f"{common_prefix}/"


class CheckAndInstallPackages(SwarmTool):
    """
    Checks if packages are installed and installs them if needed.
    """
    def run(self, packages: Annotated[List[str], list]) -> Dict[str, Dict[str, Union[bool, str]]]:
        results = {}

        for package in packages:
            if not package:  # Skip empty package names
                continue

            base_package = package.split('.')[0]  # Get root package name

            if not base_package:
                results[package] = {
                    'installed': False,
                    'message': 'Invalid package name'
                }
                continue

            try:
                __import__(base_package)
                results[package] = {
                    'installed': True,
                    'message': 'Already installed'
                }
            except ImportError:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    results[package] = {
                        'installed': True,
                        'message': 'Successfully installed'
                    }
                except subprocess.CalledProcessError:
                    results[package] = {
                        'installed': False,
                        'message': 'Installation failed'
                    }

        return results


class WriteFiles(SwarmTool):
    """
    Writes files to a specified base path.
    """
    def run(self, base_path: Annotated[str, str], files: Annotated[Dict[str, str], dict]) -> None:
        for filename, content in files.items():
            full_path = os.path.join(base_path, filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)


class CreateRepository(SwarmTool):
    """
    Creates a repository structure and writes files, including test files.
    """
    def run(self, base_path: Annotated[str, str], documents: Annotated[Dict, dict]) -> None:
        os.makedirs(base_path, exist_ok=True)

        for filename in os.listdir(base_path):
            file_path = os.path.join(base_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

        files = copy.deepcopy(documents['code'])
        root_dir = GetRootDir().run(files)

        coverage = """[run]\nomit =\n    */__init__.py\n    tests/*\n"""

        files.update({
            f'{root_dir}tests/unit/test_module.py': documents['unit_tests']['test_module'],
            f'{root_dir}tests/unit/__init__.py': '',
            f'{root_dir}tests/acceptance/test_features.py': documents['acceptance_tests']['test_features'],
            f'{root_dir}tests/acceptance/__init__.py': '',
            f'{root_dir}docs/PRD.md': documents['PRD'],
            f'{root_dir}docs/UML_class.md': documents['UML_class'],
            f'{root_dir}docs/UML_sequence.md': documents['UML_sequence'],
            f'{root_dir}docs/architecture_design.md': documents['architecture_design'],
            f'{root_dir}requirements.txt': documents['requirements'],
            f'{root_dir}.coveragerc': coverage,
        })

        WriteFiles().run(base_path, files)

# Registering tools in the SWARM framework
tools = [
    GetRootDir(),
    CheckAndInstallPackages(),
    WriteFiles(),
    CreateRepository()
]
