#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,struct
TARGET='fbb161d7b8dd10f279c436519d738c31aa321302019d53ca22d41300bfd55460'
NORMAL_FIRST=0x193746
NORMAL_SIG=bytes.fromhex('82 65 F0 79 F0 2F')
EVENT1=0x19069E
EVENT1_EXPECT=bytes.fromhex('82 65 82 89 82 92 82 93 82 94 81 40 82 73 F0 61 F0 37')
EVENT2=0x191DFC
EVENT2_EXPECT=bytes.fromhex('82 64 82 75 F0 4C 82 73 81 46 81 40 82 65 82 89 82 92 F0 2F 81 40 82 73 F0 61 F0 37')
MTE=0x39F0C3+0x79*9
MTE_EXPECT=bytes.fromhex('02 49 52 00 00 00 00 00 00')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('rom');a=ap.parse_args();r=Path(a.rom).read_bytes();h=hashlib.sha256(r).hexdigest()
 checks={
  'sha256': h==TARGET,
  'normal_First_signature_0x193746': r[NORMAL_FIRST:NORMAL_FIRST+len(NORMAL_SIG)]==NORMAL_SIG,
  'EVENT_First_Trial_1_explicit_First': r[EVENT1:EVENT1+len(EVENT1_EXPECT)]==EVENT1_EXPECT,
  'EVENT_First_Trial_2_no_F079': r[EVENT2:EVENT2+len(EVENT2_EXPECT)]==EVENT2_EXPECT,
  'F079_dictionary_unchanged_ir': r[MTE:MTE+9]==MTE_EXPECT,
  'checksum': struct.unpack('<H',r[-2:])[0]==(sum(r[:-2])&0xffff),
 }
 for k,v in checks.items(): print(k,'PASS' if v else 'FAIL')
 print('sha256',h);print('checksum',f'{struct.unpack("<H",r[-2:])[0]:04X}')
 raise SystemExit(0 if all(checks.values()) else 1)
if __name__=='__main__': main()
