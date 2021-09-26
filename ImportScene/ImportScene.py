"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""

import sys

import fbx
from fbx import FbxThumbnail, FbxNodeAttribute, FbxNode

from ImportScene.DisplayGlobalSettings  import *
from ImportScene.DisplayHierarchy       import DisplayHierarchy
from ImportScene.DisplayMarker          import DisplayMarker
from ImportScene.DisplayMesh            import DisplayMesh
from ImportScene.DisplayUserProperties  import DisplayUserProperties
from ImportScene.DisplayPivotsAndLimits import DisplayPivotsAndLimits
from ImportScene.DisplaySkeleton        import DisplaySkeleton
from ImportScene.DisplayNurb            import DisplayNurb
from ImportScene.DisplayPatch           import DisplayPatch
from ImportScene.DisplayCamera          import DisplayCamera
from ImportScene.DisplayLight           import DisplayLight
from ImportScene.DisplayLodGroup        import DisplayLodGroup
from ImportScene.DisplayPose            import DisplayPose
from ImportScene.DisplayAnimation       import DisplayAnimation
from ImportScene.DisplayGenericInfo     import DisplayGenericInfo


def DisplayMetaData(pScene):
    sceneInfo = pScene.GetSceneInfo()
    if sceneInfo:
        print("\n\n--------------------\nMeta-Data\n--------------------\n")
        print("    Title: %s" % sceneInfo.mTitle.Buffer())
        print("    Subject: %s" % sceneInfo.mSubject.Buffer())
        print("    Author: %s" % sceneInfo.mAuthor.Buffer())
        print("    Keywords: %s" % sceneInfo.mKeywords.Buffer())
        print("    Revision: %s" % sceneInfo.mRevision.Buffer())
        print("    Comment: %s" % sceneInfo.mComment.Buffer())

        thumbnail = sceneInfo.GetSceneThumbnail()
        if thumbnail:
            print("    Thumbnail:")

            if thumbnail.GetDataFormat() == FbxThumbnail.eRGB_24 :
                print("        Format: RGB")
            elif thumbnail.GetDataFormat() == FbxThumbnail.eRGBA_32:
                print("        Format: RGBA")

            if thumbnail.GetSize() == FbxThumbnail.eNOT_SET:
                print("        Size: no dimensions specified (%ld bytes)", thumbnail.GetSizeInBytes())
            elif thumbnail.GetSize() == FbxThumbnail.e64x64:
                print("        Size: 64 x 64 pixels (%ld bytes)", thumbnail.GetSizeInBytes())
            elif thumbnail.GetSize() == FbxThumbnail.e128x128:
                print("        Size: 128 x 128 pixels (%ld bytes)", thumbnail.GetSizeInBytes())

def DisplayContent(pScene):
    lNode = pScene.GetRootNode()

    if lNode:
        for i in range(lNode.GetChildCount()):
            DisplayNodeContent(lNode.GetChild(i))

def DisplayNodeContent(pNode):
    if pNode.GetNodeAttribute() == None:
        print("NULL Node Attribute\n")
    else:
        lAttributeType = (pNode.GetNodeAttribute().GetAttributeType())

        if lAttributeType == FbxNodeAttribute.eMarker:
            DisplayMarker(pNode)
        elif lAttributeType == FbxNodeAttribute.eSkeleton:
            DisplaySkeleton(pNode)
        elif lAttributeType == FbxNodeAttribute.eMesh:
            DisplayMesh(pNode)
        elif lAttributeType == FbxNodeAttribute.eNurbs:
            DisplayNurb(pNode)
        elif lAttributeType == FbxNodeAttribute.ePatch:
            DisplayPatch(pNode)
        elif lAttributeType == FbxNodeAttribute.eCamera:
            DisplayCamera(pNode)
        elif lAttributeType == FbxNodeAttribute.eLight:
            DisplayLight(pNode)

    DisplayUserProperties(pNode)
    DisplayTarget(pNode)
    DisplayPivotsAndLimits(pNode)
    DisplayTransformPropagation(pNode)
    DisplayGeometricTransform(pNode)

    for i in range(pNode.GetChildCount()):
        DisplayNodeContent(pNode.GetChild(i))

def DisplayTarget(pNode):
    if pNode.GetTarget():
        DisplayString("    Target Name: ", pNode.GetTarget().GetName())

def DisplayTransformPropagation(pNode):
    print("    Transformation Propagation")
    
    # Rotation Space
    lRotationOrder = pNode.GetRotationOrder(FbxNode.eSourcePivot)

    print("        Rotation Space:",)

    if lRotationOrder == fbx.eEulerXYZ:
        print("Euler XYZ")
    elif lRotationOrder == fbx.eEulerXZY:
        print("Euler XZY")
    elif lRotationOrder == fbx.eEulerYZX:
        print("Euler YZX")
    elif lRotationOrder == fbx.eEulerYXZ:
        print("Euler YXZ")
    elif lRotationOrder == fbx.eEulerZXY:
        print("Euler ZXY")
    elif lRotationOrder == fbx.eEulerZYX:
        print("Euler ZYX")
    elif lRotationOrder == fbx.eSphericXYZ:
        print("Spheric XYZ")
    
    # Use the Rotation space only for the limits
    # (keep using eEULER_XYZ for the rest)
    if pNode.GetUseRotationSpaceForLimitOnly(FbxNode.eSourcePivot):
        print("        Use the Rotation Space for Limit specification only: Yes")
    else:
        print("        Use the Rotation Space for Limit specification only: No")


    # Inherit Type
    lInheritType = pNode.GetTransformationInheritType()

    print("        Transformation Inheritance:",)

    if lInheritType == fbx.FbxTransform.eInheritRrSs:
        print("RrSs")
    elif lInheritType == fbx.FbxTransform.eInheritRSrs:
        print("RSrs")
    elif lInheritType == fbx.FbxTransform.eInheritRrs:
        print("Rrs")


def DisplayGeometricTransform(pNode):
    print("    Geometric Transformations")

    # Translation
    lTmpVector = pNode.GetGeometricTranslation(FbxNode.eSourcePivot)
    print("        Translation: %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    # Rotation
    lTmpVector = pNode.GetGeometricRotation(FbxNode.eSourcePivot)
    print("        Rotation:    %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

    # Scaling
    lTmpVector = pNode.GetGeometricScaling(FbxNode.eSourcePivot)
    print("        Scaling:     %f %f %f" % (lTmpVector[0], lTmpVector[1], lTmpVector[2]))

def DisPlayScene(lScene):
    # DisplayMetaData(lScene)
    # print("\n\n---------------------\nGlobal Light Settings\n---------------------\n")
    # DisplayGlobalLightSettings(lScene)

    # print("\n\n----------------------\nGlobal Camera Settings\n----------------------\n")
    # DisplayGlobalCameraSettings(lScene)

    # print("\n\n--------------------\nGlobal Time Settings\n--------------------\n")
    # DisplayGlobalTimeSettings(lScene.GetGlobalSettings())

    # print("\n\n---------\nHierarchy\n---------\n")
    # DisplayHierarchy(lScene)

    # print("\n\n------------\nNode Content\n------------\n")
    # DisplayContent(lScene)

    # print("\n\n----\nPose\n----\n")
    # DisplayPose(lScene)

    print("\n\n---------\nAnimation\n---------\n")
    DisplayAnimation(lScene)

    #now display generic information
    # print("\n\n---------\nGeneric Information\n---------\n")
    # DisplayGenericInfo(lScene)
