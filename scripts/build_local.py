"""Reproducible standalone APK build with explicit official SDK inputs and a private signing key."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

p=argparse.ArgumentParser()
p.add_argument('--android-jar',type=Path,required=True)
p.add_argument('--build-tools',type=Path,required=True)
p.add_argument('--ecj',type=Path,required=True)
p.add_argument('--keystore',type=Path,required=True)
p.add_argument('--password-file',type=Path,required=True)
a=p.parse_args()
ROOT=Path(__file__).resolve().parents[1]
work=ROOT/'build/standalone';work.mkdir(exist_ok=True,parents=True)
for name in ('classes','dex','generated'):(work/name).mkdir(exist_ok=True)
build=(ROOT/'app/build.gradle').read_text()
version=re.search(r"versionName '([^']+)'",build)[1];code=re.search(r'versionCode (\d+)',build)[1]
ns='http://schemas.android.com/apk/res/android';ET.register_namespace('android',ns)
manifest=ET.parse(ROOT/'app/src/main/AndroidManifest.xml');r=manifest.getroot()
r.set('package','io.github.timekillr.ffredit.companion');r.set('{'+ns+'}versionCode',code);r.set('{'+ns+'}versionName',version)
r.find('application').set('{'+ns+'}debuggable','false')
manifest.write(work/'AndroidManifest.xml',encoding='utf-8',xml_declaration=True)
def run(args):subprocess.run([str(x) for x in args],check=True)
run([a.build_tools/'aapt2','compile','--dir',ROOT/'app/src/main/res','-o',work/'compiled.zip'])
run([a.build_tools/'aapt2','link','-o',work/'resources.apk','--manifest',work/'AndroidManifest.xml','-I',a.android_jar,'--java',work/'generated','--min-sdk-version','26','--target-sdk-version','37','-A',ROOT/'app/src/main/assets',work/'compiled.zip'])
sources=list((ROOT/'app/src/main/java').rglob('*.java'))+list((work/'generated').rglob('*.java'))
run(['java','-jar',a.ecj,'-1.8','-proc:none','-bootclasspath',str(a.android_jar)+os.pathsep+str(a.build_tools/'core-lambda-stubs.jar'),'-d',work/'classes',*sources])
run(['java','-cp',a.build_tools/'lib/d8.jar','com.android.tools.r8.D8','--release','--min-api','26','--lib',a.android_jar,'--output',work/'dex',*list((work/'classes').rglob('*.class'))])
unsigned=work/'unsigned.apk';unsigned.write_bytes((work/'resources.apk').read_bytes())
with zipfile.ZipFile(unsigned,'a',zipfile.ZIP_DEFLATED) as z:z.write(work/'dex/classes.dex','classes.dex')
out=ROOT/'artifacts';out.mkdir(exist_ok=True);apk=out/'FFR_Edit_Companion.apk'
run(['java','-jar',a.build_tools/'lib/apksigner.jar','sign','--ks',a.keystore,'--ks-key-alias','ffr-edit-companion','--ks-pass','file:'+str(a.password_file),'--out',apk,unsigned])
run(['java','-jar',a.build_tools/'lib/apksigner.jar','verify','--verbose','--print-certs',apk])
print('Built and signature-verified',apk)
