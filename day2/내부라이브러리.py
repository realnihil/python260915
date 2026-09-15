import os
import os.path
import glob

# print(f'운영체제이름: {os.name}')
# print(f'환경변수: {os.environ}')

#raw string : 문자열 앞에 r을 붙이면 이스케이프 문자를 무시하고 있는 그대로 문자열로 인식
fName = r'c:\python313\python.exe'

if os.path.exists(fName):
    print(f'{fName} 파일의 크기: {os.path.getsize(fName)} 바이트')
else:
    print(f'{fName} 파일이 존재하지 않습니다.')

files = glob.glob(r'c:\work\*.py')

if r'c:\work\상속01.py' in files:
    print("상속01.py 파일이 존재합니다.")
else:
    print("상속01.py 파일이 존재하지 않습니다.")