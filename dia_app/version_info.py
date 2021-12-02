import sys, os

class VersionInfo:
    
    limit=3 #to truncate version str()
    sep='.'
    version_info=[]
    
    def __init__(self, version_info):
        self.version_info=list(version_info)
        
    def __getitem__(self, item):
        return self.version_info[item]
    
    def __repr__(self):
        return self.sep.join(list(map(str,self.version_info))[0:self.limit])

python_version_info=VersionInfo(sys.version_info)
python2 = False
python3 = False
if (python_version_info[0] == 2):
    python2 = True
elif (python_version_info[0] == 3):
    python3 = True
else:
    raise(Exception("Unsupported python version"))

