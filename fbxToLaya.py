import sys
from ExportScene.FBXScene3D import FBXScene3D
from FbxCommon import *
from ImportScene.ImportScene import DisPlayScene

if __name__ == "__main__":

    # Prepare the FBX SDK.
    lSdkManager, lScene = InitializeSdkObjects()
    # Load the scene.

    # The example can take a FBX file as an argument.
    # sys.argv = ["", "res/chafu.fbx"]
    # sys.argv = ["","res/ceshi.FBX"]
    # sys.argv = ["", "res/03.fbx"]
    # sys.argv = ["", "res/SambaDancing.fbx"]
    # sys.argv = ["", "res/mengpi.FBX"]
    if len(sys.argv) > 1:
        print("\n\nFile: %s\n" % sys.argv[1])
        lResult = LoadScene(lSdkManager, lScene, sys.argv[1])
    else:
        lResult = False

        print("\n\nUsage: ImportScene <FBX file name>\n")

    if not lResult:
        print("\n\nAn error occurred while loading the scene...")
    else:
        # scene = FBXScene3D(lScene,sys.argv[2],sys.argv[1])
        # scene.witeFile()
        DisPlayScene(lScene)
    lSdkManager.Destroy()

    sys.exit(0)

