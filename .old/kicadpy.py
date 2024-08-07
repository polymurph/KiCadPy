import pcbnew
import numpy as np
import math

def _KicadPol2cartDEG(phi,r):
    x = r*np.sin(np.radians(phi+90))
    y = r*np.cos(np.radians(phi+90))
    return x, y

def placeVia(
    boardObject,
    x_mm,
    y_mm,
    drillDiameter_mm,
    width_mm,
    netName):
    # TODO implement netName definition
    via =pcbnew.PCB_VIA(boardObject)
    via.SetPosition(pcbnew.VECTOR2I(int((x_mm) * 1E6), int((y_mm) * 1E6)))
    via.SetDrill(int((drillDiameter_mm) * 1E6))
    via.SetWidth(int((width_mm) * 1E6))
    boardObject.Add(via)

def polarPlaceVia(
    boardObject,
    center_x_mm,
    center_y_mm,
    radius_mm,
    angle_DEG,
    drillDiameter_mm,
    width_mm,
    netName):
    # TODO implement netName definition
    via =pcbnew.PCB_VIA(boardObject)
    x, y = _KicadPol2cartDEG(angle_DEG, radius_mm)
    x += center_x_mm
    y += center_y_mm
    via.SetPosition(pcbnew.VECTOR2I(int((x) * 1E6), int((y) * 1E6)))
    via.SetDrill(int((drillDiameter_mm) * 1E6))
    via.SetWidth(int((width_mm) * 1E6))
    boardObject.Add(via)

def setComponentToFront(
    boardObject,
    referenceDesignator,
    front):
    footprint = boardObject.FindFootprintByReference(referenceDesignator)
    if front:
        footprint.SetLayerAndFlip(pcbnew.F_Cu)
        return
    footprint.SetLayerAndFlip(pcbnew.B_Cu)

def isComponentOnTopOfPCB(
    boardObject,
    referenceDesignator):
    footprint = boardObject.FindFootprintByReference(referenceDesignator)
    return not(footprint.IsFlipped())

def setComponentsToFront(
    boardObject,
    referenceDesignatorList,
    front):
    for refDes in referenceDesignatorList:
        setComponentToFront(boardObject,
                             refDes,
                             front)
        
def placeViasCircularArray(
    boardObject,
    centerX_mm,
    centerY_mm,
    placementRadius_mm,
    drillDiameter_mm,
    width_mm,
    startAngle_DEG,
    endAngle_DEG,
    n_vias,
    netName):

    delta = (endAngle_DEG - startAngle_DEG)/n_vias

    for angle in np.linspace(startAngle_DEG,endAngle_DEG - delta,n_vias):
    #for angle in np.linspace(startAngle_DEG,endAngle_DEG,n_vias):

        x, y = _KicadPol2cartDEG(angle,placementRadius_mm)
        x += centerX_mm
        y += centerY_mm
        
        placeVia(
            boardObject,
            x,
            y,
            drillDiameter_mm,
            width_mm,
            netName)
        
def placeTrack(
    boardObject,
    startX_mm,
    srartY_mm,
    endX_mm,
    endY_mm,
    width_mm,
    layer,
    netName):
    ''' Place a Track
    
    '''
    track = pcbnew.PCB_TRACK(boardObject)
    track.SetStart(pcbnew.VECTOR2I(int((startX_mm) * 1E6), int((srartY_mm) * 1E6)))
    track.SetEnd(pcbnew.VECTOR2I(int((endX_mm) * 1E6), int((endY_mm) * 1E6)))
    track.SetWidth(int(width_mm * 1e6))
    track.SetLayer(layer)
    boardObject.Add(track)
    # TODO: add functionality to set net name

def addTrackArcAngles(
        boardObject,
        startAngle_DEG,
        endAngle_DEG,
        radius_mm,
        center_mm,
        width_mm,
        layer,
        netName):
    # TODO: solve 180° offset and ccw fault
    start_angle = math.radians(-startAngle_DEG)
    end_angle = math.radians(-endAngle_DEG)

    if start_angle > end_angle and True:
        endAngle_DEG += math.radians(180)

    start = (radius_mm * math.cos(start_angle) + center_mm[0], radius_mm * math.sin(start_angle)+ center_mm[1])
    end = (radius_mm * math.cos(end_angle)+ center_mm[0], radius_mm * math.sin(end_angle)+ center_mm[1])

    #mid_angle = startAngle_DEG + (endAngle_DEG - startAngle_DEG) / 2
    mid_angle = start_angle + (end_angle - start_angle) / 2

    mid = (radius_mm * math.cos(mid_angle) + center_mm[0], radius_mm * math.sin(mid_angle)+ center_mm[1])

    arc = pcbnew.PCB_ARC(boardObject)
    arc.SetStart(pcbnew.VECTOR2I(int((start[0]) * 1E6), int((start[1]) * 1E6)))
    arc.SetMid(pcbnew.VECTOR2I(int((mid[0]) * 1E6), int((mid[1]) * 1E6)))
    arc.SetEnd(pcbnew.VECTOR2I(int((end[0]) * 1E6), int((end[1]) * 1E6)))
    arc.SetLayer(layer)
    arc.SetWidth(int(width_mm * 1e6))
    
    #a = pcbnew.NETINFO_ITEM_ClassOf(arc)
    #a.SetNetname(netName)
    #arc.SetNetname(netName)
    #print(arc.GetNetname())
    #arc.SetNet(netName)
    
    boardObject.Add(arc)
    #pcbnew.Refresh()
    #input("wainting")

def setRefDesSilkVisibility(board, referenceDesignatorList, visible):
    for ref in referenceDesignatorList:
        footprint = board.FindFootprintByReference(ref)
        refDes = footprint.Reference() 
        refDes.SetVisible(visible)

def rotateComponent(board, referenceDesignator, rotationAngleDEG):
    footprint = board.FindFootprintByReference(referenceDesignator)
    footprint.SetOrientationDegrees(rotationAngleDEG)

def placeComponent(
        boardObject,
        referenceDesignator,
        x_mm,
        y_mm,
        rotationAngle_DEG,
        setToFront = True):
    footprint = boardObject.FindFootprintByReference(referenceDesignator)
    rotateComponent(boardObject,referenceDesignator,rotationAngle_DEG)
    footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint(x_mm*1e6,y_mm*1e6)))
    setComponentToFront(boardObject,referenceDesignator, setToFront)

def relativePlaceComponent(
        boardObject,
        referenceDesignator,
        ref_x_mm,
        ref_y_mm,
        rel_x_mm,
        rel_y_mm,
        rotationAngleDEG,
        setToFront = True):
    placeComponent(boardObject, referenceDesignator, ref_x_mm + rel_x_mm, ref_y_mm + rel_y_mm, rotationAngleDEG, setToFront)

def placeComponentsInCircle(
        board,
        referenceDesignators,
        x_c,
        y_c,
        radius,
        relativeComponentOrientationDEG,
        initialPlacementAngleDEG,
        clockwise,
        setToFront = True):
    
    N = len(referenceDesignators)
    angleStep_rad = 2 * np.pi / N
    angleIndex_rad = np.deg2rad(initialPlacementAngleDEG)

    for component in referenceDesignators:
        # TODO: replace angleIndex_rad with angleIndex_rad + np.pi()
        #x_p = radius * np.sin(angleIndex_rad + 0.5*np.pi) + x_c
        #y_p = radius * -np.cos(angleIndex_rad + 0.5*np.pi) + y_c
        x_p, y_p = _KicadPol2cartDEG(np.rad2deg(angleIndex_rad),radius)

        x_p += x_c
        y_p += y_c
        
        placeComponent(
            board,
            component,
            x_p,
            y_p,
            relativeComponentOrientationDEG+(np.rad2deg(angleIndex_rad)),
            setToFront)
        
        if clockwise:
            angleIndex_rad -= angleStep_rad
            continue
        angleIndex_rad += angleStep_rad

def placeComponentsInCircleWithAngle(
        board,
        tupelList,
        x_c,
        y_c,
        radius,
        relativeComponentOrientationDEG,
        clockwise):
    
    for item in tupelList:
        part = item[0]
        placementAngle = item[1]
        placeComponentsInCircle(board,
                                [part],
                                x_c,
                                y_c,
                                radius,
                                relativeComponentOrientationDEG,
                                placementAngle,
                                clockwise)

def polarPlacePart(
        boardObject,
        referenceDesignator,
        centerX_mm,
        centerY_mm,
        radius_DEG,
        angle_mm,
        partRotationAngle_DEG,
        setToFront = True):
    
    setComponentToFront(boardObject,referenceDesignator,setToFront)

    x, y = _KicadPol2cartDEG(angle_mm, radius_DEG)
    # offset cartesian coordinates
    x += centerX_mm
    y += centerY_mm

    placeComponent(boardObject,referenceDesignator,x,y,partRotationAngle_DEG,setToFront)

def polarPlacePartList(
        boardObject,
        list):
    ''' Place all component in a list in polar system

    The list must consist of the following structure.
    [[reference Designator, center x mm, center y mm, radius DEG, angle DEG, part Rotation angel DEG, set to front],
     [...],
     ...]
    
    '''
    
    for part in list:
        polarPlacePart(boardObject,part[0], part[1], part[2], part[3],part[4],-part[5], part[6])

def getPartPosition(
        boardObject,
        referenceDesignator):
    footprint = boardObject.FindFootprintByReference(referenceDesignator)
    pos = footprint.GetPosition()
    x = pcbnew.ToMM(pos.x)
    y = pcbnew.ToMM(pos.y)
    return x, y

def getPadCoordinate(
        boardObject,
        referenceDesignator,
        padNumber):
    footprint = boardObject.FindFootprintByReference(referenceDesignator)
    for pad in footprint.Pads():
        if pad.GetNumber() == padNumber:
            pos = pad.GetPosition()
            x = pcbnew.ToMM(pos.x)
            y = pcbnew.ToMM(pos.y)
            return x, y
    return None

def addTrackStubToPin(
    boardObject,
    referenceDesignator,
    pinNumber,
    distanceToPinOrigin_mm,
    trackWidth_mm):

    # find out if it is right, left, abve or below the origin of the part
    footprint = boardObject.FindFootprintByReference(referenceDesignator)
    
    partOrientation = footprint.GetOrientation().AsDegrees()
    
    # undo any rotation for absolute determinaton of pin location
    rotateComponent(
        boardObject,
        referenceDesignator,
        0)
    
    x,y = getPadCoordinate(boardObject,referenceDesignator,pinNumber)
    
    x_min = x
    y_min = y
    x_max = x
    y_max = y
    c_x = 0
    c_y = 0
    
    # get box corner coordinates and determine
    # the shape of the footwprint
    for pad in footprint.Pads():
        pos = pad.GetPosition()
        xi = pcbnew.ToMM(pos.x)
        yi = pcbnew.ToMM(pos.y)
        if x_min > xi:
            x_min = xi
            c_x += 1
        elif y_min > yi:
            y_min = yi
            c_y += 1
        elif x_max < xi:
            x_max = xi
            c_x += 1
        elif y_max < yi:
            y_max = yi
            c_y += 1
        elif x_max == xi:
            c_x += 1
        elif x_min == xi:
            c_x += 1
        elif y_max == yi:
            c_y += 1
        elif y_min == yi:
            c_y += 1

    x,y = getPadCoordinate(boardObject,referenceDesignator,pinNumber)
    
    offsetAngle = 0 
    
    # TODO finish the c_x and c_y evaluation
    # for the corner conditions
    if x == x_max and y == y_max:
        print("first quadrant corner")
        if c_x > c_y:
            offsetAngle = 0
        else:
            offsetAngle = -90
    elif x == x_min and y == y_max:
        print("seccond quadrant corner")
        if c_x > c_y:
            print("a")
            offsetAngle = -180
        elif c_x == c_y:
            print("b")
            print(referenceDesignator)
            print(pinNumber)
            offsetAngle = -90
        else:
            print("c")
            offsetAngle = -90
    elif x == x_min and y == y_min:
        print("third quadrant corner")
        if c_x > c_y:
            print("debug1")
            #offsetAngle = -270
            offsetAngle = -180
        elif c_x == c_y:
            print("debug2")
            offsetAngle = -90
        else:
            offsetAngle = -90
    elif x == x_max and y == y_min:
        print("fourth quadrant corner")
    elif x == x_max:
        print("first quadrant")
        offsetAngle = 0
    elif y == y_max:
        print("seccond quadrant")
        if c_x == c_y:
            offsetAngle = 0
        else:
            offsetAngle = -90
    elif x == x_min:
        print("third quadrant")
        offsetAngle = -180 
    elif y == y_min:
        print("fourth quadrant")
        offsetAngle = -270
    
    # rotate back
    rotateComponent(
        boardObject,
        referenceDesignator,
        partOrientation)
    
    x,y = getPadCoordinate(boardObject,referenceDesignator,pinNumber)
    
    xv, yv = _KicadPol2cartDEG(partOrientation + offsetAngle, distanceToPinOrigin_mm)
    xv += x
    yv += y
    if isComponentOnTopOfPCB(boardObject,referenceDesignator):
        placeTrack(boardObject,x,y,xv,yv,trackWidth_mm,pcbnew.F_Cu,"")
    else:
        placeTrack(boardObject,x,y,xv,yv,trackWidth_mm,pcbnew.B_Cu,"")
    return xv, yv

def addViaToPin(
        boardObject,
        referenceDesignator,
        pinNumber,
        distanceToPinOrigin_mm,
        viaDrillDiameter_mm,
        viaWidth_mm,
        trackWidth_mm):
    
    xv,yv = addTrackStubToPin(
        boardObject,
        referenceDesignator,
        pinNumber,
        distanceToPinOrigin_mm,
        trackWidth_mm)
    
    print("refDes")
    print(referenceDesignator)
    print("pinNumber")
    print(pinNumber)
    placeVia(boardObject,xv,yv,viaDrillDiameter_mm,viaWidth_mm,"")
    return xv, yv
        




            


