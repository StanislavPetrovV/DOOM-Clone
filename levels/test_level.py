from settings import *
from texture_id import *

_ = None


SETTINGS = {
    'seed': 21315,
    'cam_pos': (1, CAM_HEIGHT, 1),
    'cam_target': (5, CAM_HEIGHT, 5)
}


# points
P_00 = (0.0, 0.0)
P_01 = (16.0, 0.0)
P_02 = (16.0, 9.0)
P_03 = (0.0, 9.0)
# column
P_04 = (3.0, 4.25)
P_05 = (3.0, 4.75)
P_06 = (3.5, 4.75)
P_07 = (3.5, 4.25)
#
P_08 = (8.0, 0.0)
P_09 = (8.0, 9.0)
P_10 = (6.0, 4.5)
#
P_11 = (12.0, 2.0)
P_12 = (14.5, 4.5)
P_13 = (12.0, 7.0)
P_14 = (9.5, 4.5)
#
P_15 = (15.0, 9.0)
P_16 = (15.0, 9.5)
P_17 = (13.0, 9.5)
P_18 = (13.0, 9.0)
#
P_19 = (25.0, 9.5)
P_20 = (25.0, 22.5)
P_21 = (3.0, 22.5)
P_22 = (3.0, 9.5)
#
P_23 = (21.0, 13.5)
P_24 = (7.0, 13.5)
P_25 = (7.0, 18.5)
P_26 = (21.0, 18.5)
#
P_27 = (11.0, 3.5)
P_28 = (13.0, 3.5)
P_29 = (13.0, 5.5)
P_30 = (11.0, 5.5)
#
P_31 = (10.0, 9.0)
P_32 = (11.0, 9.0)
P_33 = (11.0, 9.5)
P_34 = (10.0, 9.5)
#
P_35 = (9.0, 15.75)
P_36 = (9.0, 16.25)
P_37 = (19.0, 16.25)
P_38 = (19.0, 15.75)


SECTOR_DATA = {
    0: dict(
        floor_h=0.0, ceil_h=3.0,
        floor_tex_id=FlatTexID.TEST_3, ceil_tex_id=FlatTexID.TEST_5
    ),
    1: dict(
        floor_h=-0.3, ceil_h=2.7, nested_sector_ids=[2, ],
        ceil_tex_id=FlatTexID.TEST_4
    ),
    2: dict(
        floor_h=-0.5, ceil_h=3.0,
        floor_tex_id=FlatTexID.TEST_1, ceil_tex_id=FlatTexID.TEST_5,
        nested_sector_ids=[6, ],
    ),
    3: dict(
        floor_h=0.25, ceil_h=1.75,
        floor_tex_id=FlatTexID.TEST_1, ceil_tex_id=FlatTexID.TEST_1
    ),
    4: dict(
        floor_h=-0.5, ceil_h=3.5, nested_sector_ids=[5, ],
        floor_tex_id=FlatTexID.TEST_3, ceil_tex_id=FlatTexID.TEST_4
    ),
    5: dict(
        floor_h=-0.2, ceil_h=3.0,
        floor_tex_id=FlatTexID.TEST_2, ceil_tex_id=FlatTexID.TEST_5
    ),
    6: dict(
        floor_h=0.50, ceil_h=2.5,
        floor_tex_id=FlatTexID.TEST_3, ceil_tex_id=FlatTexID.TEST_4,
    ),
    7: dict(
        floor_h=-0.3, ceil_h=2.00,
        floor_tex_id=FlatTexID.TEST_1, ceil_tex_id=FlatTexID.TEST_1
    )
}


SEGMENTS_OF_SECTOR_BOUNDARIES = [
    # seg points(p0 p1), sector ids(front sector, back sector adj), textures(lo mid up)
    # sector 0
    [(P_00, P_08), (0, _), (_, _, _)],
    [(P_09, P_03), (0, _), (_, _, _)],
    [(P_03, P_00), (0, _), (_, _, _)],
    # sector 1
    [(P_08, P_01), (1, _), (_, _, _)],
    [(P_01, P_02), (1, _), (_, _, _)],
    [(P_02, P_15), (1, _), (_, _, _)],
    [(P_15, P_18), (1, 3), (_, WallTexID.TEST_4, _)],
    [(P_18, P_32), (1, _), (_, _, _)],
    [(P_32, P_31), (1, 7), (_, _, _)],
    [(P_31, P_09), (1, _), (_, _, _)],
    [(P_09, P_10), (1, 0), (_, _, _)],
    [(P_10, P_08), (1, 0), (_, _, _)],
    # sector 2 (nested in 1)
    [(P_11, P_12), (2, 1), (_, _, _)],
    [(P_12, P_13), (2, 1), (_, _, _)],
    [(P_13, P_14), (2, 1), (_, _, _)],
    [(P_14, P_11), (2, 1), (_, _, _)],
    # sector 3
    [(P_15, P_16), (3, _), (_, WallTexID.TEST_2, _)],
    [(P_17, P_18), (3, _), (_, WallTexID.TEST_2, _)],
    # sector 4
    [(P_17, P_16), (4, 3), (WallTexID.TEST_1, _, WallTexID.TEST_1)],
    [(P_16, P_19), (4, _), (_, WallTexID.TEST_1, _)],
    [(P_19, P_20), (4, _), (_, WallTexID.TEST_1, _)],
    [(P_20, P_21), (4, _), (_, WallTexID.TEST_1, _)],
    [(P_21, P_22), (4, _), (_, WallTexID.TEST_1, _)],
    [(P_22, P_34), (4, _), (_, WallTexID.TEST_1, _)],
    [(P_34, P_33), (4, 7), (WallTexID.TEST_1, _, WallTexID.TEST_1)],
    [(P_33, P_17), (4, _), (_, WallTexID.TEST_1, _)],
    # sector 5 (nested in 4)
    [(P_23, P_24), (4, 5), (WallTexID.TEST_2, _, WallTexID.TEST_2)],
    [(P_24, P_25), (4, 5), (WallTexID.TEST_2, WallTexID.TEST_6, WallTexID.TEST_2)],
    [(P_25, P_26), (4, 5), (WallTexID.TEST_2, WallTexID.TEST_6, WallTexID.TEST_2)],
    [(P_26, P_23), (4, 5), (WallTexID.TEST_2, WallTexID.TEST_6, WallTexID.TEST_2)],
    # sector 6 (nested in 2)
    [(P_28, P_27), (2, 6), (WallTexID.TEST_1, WallTexID.TEST_5, WallTexID.TEST_1)],
    [(P_29, P_28), (2, 6), (WallTexID.TEST_1, WallTexID.TEST_5, WallTexID.TEST_1)],
    [(P_30, P_29), (2, 6), (WallTexID.TEST_1, WallTexID.TEST_5, WallTexID.TEST_1)],
    [(P_27, P_30), (2, 6), (WallTexID.TEST_1, WallTexID.TEST_5, WallTexID.TEST_1)],
    # sector 7 (door)
    [(P_32, P_33), (7, _), (_, WallTexID.TEST_2, _)],
    [(P_34, P_31), (7, _), (_, WallTexID.TEST_2, _)],
]


SEGMENTS_WITHIN_SECTORS = [
    # sector 0
    # column
    [(P_04, P_05), (0, _), (_, WallTexID.TEST_2, _)],
    [(P_05, P_06), (0, _), (_, WallTexID.TEST_2, _)],
    [(P_06, P_07), (0, _), (_, WallTexID.TEST_2, _)],
    [(P_07, P_04), (0, _), (_, WallTexID.TEST_2, _)],
    # sector 5
    # wall
    [(P_35, P_36), (5, _), (_, WallTexID.TEST_3, _)],
    [(P_36, P_37), (5, _), (_, WallTexID.TEST_3, _)],
    [(P_37, P_38), (5, _), (_, WallTexID.TEST_3, _)],
    [(P_38, P_35), (5, _), (_, WallTexID.TEST_3, _)],
]
