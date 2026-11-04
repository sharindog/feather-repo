#!/usr/bin/env python3
import json, plistlib, zipfile, sys, re, datetime, os
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
OWNER=os.environ.get('GITHUB_REPOSITORY','sharindog/feather-repo')

def inspect(ipa):
    with zipfile.ZipFile(ipa) as z:
        infos=[n for n in z.namelist() if re.fullmatch(r'Payload/[^/]+\.app/Info.plist',n)]
        if len(infos)!=1: raise ValueError('IPA must contain exactly one Payload/*.app/Info.plist')
        prefix=infos[0].removesuffix('Info.plist')
        info=plistlib.loads(z.read(infos[0]))
        bid=info.get('CFBundleIdentifier'); ver=info.get('CFBundleShortVersionString') or info.get('CFBundleVersion')
        if not bid or not ver: raise ValueError('Missing bundle ID or version')
        name=info.get('CFBundleDisplayName') or info.get('CFBundleName') or bid
        icon=None
        candidates=[]
        icons=info.get('CFBundleIcons',{}).get('CFBundlePrimaryIcon',{}).get('CFBundleIconFiles',[])
        for candidate in icons:
            candidates += [prefix+candidate+'.png',prefix+candidate+'@2x.png',prefix+candidate+'@3x.png']
        candidates += [n for n in z.namelist() if n.startswith(prefix) and re.search(r'AppIcon.*\.png$',n,re.I)]
        for c in reversed(candidates):
            if c in z.namelist(): icon=z.read(c); break
        return dict(bundleIdentifier=str(bid),version=str(ver),name=str(name),icon=icon)

def main():
    ipa=Path(sys.argv[1]); tag=sys.argv[2]; filename=ipa.name
    if not zipfile.is_zipfile(ipa) or ipa.suffix.lower()!='.ipa': raise ValueError('Not a valid IPA zip')
    meta=inspect(ipa)
    target=ROOT/'apps.json'
    source=json.loads(target.read_text())
    bid=meta['bundleIdentifier']; ver=meta['version']
    url=f'https://github.com/{OWNER}/releases/download/{quote(tag,safe="")}/{quote(filename)}'
    icon_path=f'icons/{re.sub(r"[^A-Za-z0-9._-]","_",bid)}.png'
    if meta['icon']:
        (ROOT/icon_path).write_bytes(meta['icon'])
    app=next((a for a in source['apps'] if a['bundleIdentifier']==bid),None)
    if app is None:
        app=dict(name=meta['name'],bundleIdentifier=bid,developerName='Independent Developer',subtitle='',localizedDescription='Imported IPA',iconURL=f'https://{OWNER.split("/")[0]}.github.io/{OWNER.split("/")[1]}/{icon_path}' if meta['icon'] else 'https://raw.githubusercontent.com/claration/feather/main/Images/Feather.png',tintColor='#6275EA',versions=[])
        source['apps'].append(app)
    app['name']=meta['name']
    if meta['icon']: app['iconURL']=f'https://{OWNER.split("/")[0]}.github.io/{OWNER.split("/")[1]}/{icon_path}'
    app['versions']=[v for v in app['versions'] if v['version']!=ver]
    app['versions'].insert(0,dict(version=ver,date=datetime.datetime.now(datetime.timezone.utc).date().isoformat(),downloadURL=url,size=ipa.stat().st_size,localizedDescription='Automated IPA import'))
    target.write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
    print(f'Published metadata: {bid} {ver} {url}')

if __name__=='__main__': main()
