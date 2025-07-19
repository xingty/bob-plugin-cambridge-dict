#!/usr/bin/env python3
import json
import sys
import os
import hashlib
import subprocess
from pathlib import Path
from typing import Optional

def read_json_file(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(file_path: str, data: dict) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calculate_sha256(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def update_info_json(version: str) -> None:
    info_path = 'src/info.json'
    info_data = read_json_file(info_path)
    
    if info_data['version'] != version:
        print(f"Updating the version of the info.json from => {info_data['version']} to => {version}")
        info_data['version'] = version
        write_json_file(info_path, info_data)

def update_appcast_json(version: str, desc: str, sha256: str) -> None:
    appcast_path = 'appcast.json'
    appcast_data = read_json_file(appcast_path)
    
    # Check if version already exists
    version_exists = False
    for ver in appcast_data['versions']:
        if ver['version'] == version:
            ver['sha256'] = sha256
            version_exists = True
            print(f"The sha256 for {version} has been updated")
            break
    
    if not version_exists:
        # Add new version entry
        new_version = {
            'version': version,
            'desc': desc,
            'sha256': sha256,
            'url': f'https://github.com/xingty/bob-plugin-cambridge-dict/releases/download/v{version}/bob-plugin-cambridge-dict_v{version}.bobplugin',
            'minBobVersion': '0.5.0'
        }
        appcast_data['versions'].insert(0, new_version)
    
    write_json_file(appcast_path, appcast_data)

def main(version: str, desc: Optional[str] = None):
    if not desc:
        desc = f"Release v{version}"
    
    # Ensure build directory exists
    Path('build').mkdir(exist_ok=True)
    
    # Update info.json version
    update_info_json(version)
    
    # Run build script
    print(f"Building version: {version}")
    subprocess.run(['bash', './build.sh', version], check=True)
    
    # Calculate SHA256 for the built plugin
    plugin_path = f'build/bob-plugin-cambridge-dict_v{version}.bobplugin'
    if not os.path.exists(plugin_path):
        print(f"Error: Built plugin not found at {plugin_path}")
        sys.exit(1)
    
    sha256 = calculate_sha256(plugin_path)
    print(f"sha256: {sha256}")
    
    # Update appcast.json
    update_appcast_json(version, desc, sha256)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: release.py [version] [desc(optional)]")
        sys.exit(1)
    
    version = sys.argv[1]
    desc = sys.argv[2] if len(sys.argv) > 2 else None
    main(version, desc)
