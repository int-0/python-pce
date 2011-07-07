#!/usr/bin/env python
#

def build_mask(frame_stack):
    # Get max dimension
    resX = []
    resY = []
    for frame in frame_stack.frames:
        resX.append(frame.get_width())
        resY.append(frame.get_height())
    resX = max(resX)
    resY = max(resY)

    # Build empty mask
    mask = []
    for column in range(resX):
        line = [0] * resY
        mask.append(line)

    # Fill mask
    for frame in frame_stack.frames:
        ofsX = int((resX - frame.get_width()) / 2)
        ofsY = int((resY - frame.get_height()) / 2)

        for x in range(frame.get_width()):
            for y in range(frame.get_height()):
                color = frame.get_at((x, y))
                if tuple(color) != (0, 0, 0):
                    mask[x + ofsX][y + ofsY] = 1

    return mask
