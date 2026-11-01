#!/usr/bin/env python3
"""Erzeugt index.json und je Programm ein Paket dist/<kennung>-<version>.tgz aus apps/ und packages/*.json.

  tools/gen-index.py <version> <url-der-pakete>     z. B. 2.8 https://github.com/cloke-tech/ClokeOS-Apps/releases/download/apps-2.8

Jedes .app unter apps/ ist ein Programm (Kennung aus Info.plist). Systemprogramme (System/...) gehören zum Image und sind
hier nur zur Ansicht und zum Wiederherstellen; alles unter Applications/ ist nachinstallierbar. Wie bei einer Linux-Paketquelle
liegt der Index im Repo, die Pakete als Release-Dateien.
"""
import hashlib, json, os, plistlib, sys, tarfile

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, '..')
version, base = sys.argv[1], sys.argv[2].rstrip('/')
dist = os.path.join(root, 'dist')
os.makedirs(dist, exist_ok=True)
apps = []
for dirpath, dirnames, _ in sorted(os.walk(os.path.join(root, 'apps'))):
    for d in sorted(dirnames):
        if not d.endswith('.app'):
            continue
        path = os.path.join(dirpath, d)
        rel = os.path.relpath(path, os.path.join(root, 'apps'))
        with open(os.path.join(path, 'Contents', 'Info.plist'), 'rb') as f:
            info = plistlib.load(f)
        ident = info['CFBundleIdentifier']
        tgz = os.path.join(dist, f'{ident}-{version}.tgz')
        with tarfile.open(tgz, 'w:gz') as t:
            t.add(path, arcname=rel, filter=lambda ti: (setattr(ti, 'uid', 0), setattr(ti, 'gid', 0), setattr(ti, 'uname', ''), setattr(ti, 'gname', ''), ti)[-1])
        data = open(tgz, 'rb').read()
        name_de = info['CFBundleName']
        strings = os.path.join(path, 'Contents', 'Resources', 'de.lproj', 'InfoPlist.strings')
        if os.path.exists(strings):
            for line in open(strings, encoding='utf-8'):
                if line.startswith('"CFBundleDisplayName"'):
                    name_de = line.split('=')[1].strip().strip(';').strip('"')
        apps.append({
            'id': ident, 'name': info['CFBundleName'], 'name_de': name_de, 'path': '/' + rel,
            'category': 'system' if rel.startswith('System/') else 'addon', 'version': version,
            'package': {'url': f'{base}/{os.path.basename(tgz)}', 'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data)},
            'recommends': ['webkit'] if ident == 'com.clokeos.search' else [],
        })
pkgs = [json.load(open(os.path.join(root, 'packages', p))) for p in sorted(os.listdir(os.path.join(root, 'packages'))) if p.endswith('.json')]
index = {'format': 1, 'repo': 'cloke-tech/ClokeOS-Apps', 'version': version, 'apps': apps, 'packages': pkgs}
with open(os.path.join(root, 'index.json'), 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)
    f.write('\n')
print(f'{len(apps)} Programme, {len(pkgs)} Pakete, Pakete in {dist}')
