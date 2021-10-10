import sys
from ExportScene.FBXScene3D import FBXScene3D
from FbxCommon import *

if __name__ == "__main__":

    lSdkManager, lScene = InitializeSdkObjects()
    if len(sys.argv) > 1:
        print("\n\n解析文件: %s\n" % sys.argv[1])
        lResult = LoadScene(lSdkManager, lScene, sys.argv[1])
    else:
        lResult = False

        print("\n\nUsage: ImportScene <FBX file name>\n")

    if not lResult:
        print("\n\nAn error occurred while loading the scene...")
    else:
        scene = FBXScene3D(lScene, sys.argv[1] , sys.argv[2])
        scene.witeFile()
    lSdkManager.Destroy()

    sys.exit(0)
