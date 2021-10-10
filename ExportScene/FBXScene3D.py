import json
import os

from ImportScene.DisplayCommon import *
from ExportScene.FBXNode import FBXNode
from ExportScene.FBXMesh import FBXMesh
import ExportScene.FBXUnit as FBXUnit
import fbx


class FBXScene3D(FBXNode):
    def __init__(self, pScene, filePath, outPath):
        FBXNode.__init__(self, self, {})
        FBXUnit.SetGlobalFactio(
            pScene.GetGlobalSettings().GetSystemUnit().GetConversionFactorTo(
                fbx.FbxSystemUnit.m))
        filepath, tmpfilename = os.path.split(filePath)
        shotname, extension = os.path.splitext(tmpfilename)
        pathDir = outPath + "/" + shotname
        FBXUnit.makeDir(pathDir)
        FBXUnit.ResetInstanID()
        FBXUnit.SetOutPath(pathDir)
        self.setType("Sprite3D")
        # self.analysis(pScene)
        self.analysisNodeContent(pScene.GetRootNode())

        for key in self._map:
            if isinstance(self._map[key], FBXMesh):
                self._map[key].analysisMeshConten()

        self.nodeName = shotname
        pass

    def analysis(self, pScene):
        lGlobalLightSettings = pScene.GlobalLightSettings()
        self.addProp(
            "ambientColor",
            FBXUnit.ColorToArray(lGlobalLightSettings.GetAmbientColor()))
        self.addProp("enableFog", lGlobalLightSettings.GetFogEnable())
        self.addProp("fogColor",
                     FBXUnit.ColorToArray(lGlobalLightSettings.GetFogColor()))
        self.addProp("fogStart", lGlobalLightSettings.GetFogStart())
        self.addProp(
            "fogRange",
            lGlobalLightSettings.GetFogEnd() -
            lGlobalLightSettings.GetFogStart())
        self.addProp("lightmaps", [])

    def toJson(self):
        outdata = {"version": "LAYASCENE3D:02", "data": self.toExportObject()}
        return json.dumps(outdata)

    def witeFile(self):
        childNumber = len(self._children)
        for i in range(childNumber):
            print(self._children[i].nodeName)
            pass
        url = self.absolutepath(self.nodeName + ".lh")
        file = open(url, "w")
        file.writelines(self.toJson())
        file.close()
