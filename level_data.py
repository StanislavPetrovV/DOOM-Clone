from settings import *
from data_types import *
from levels.test_level import *


class LevelData:
    def __init__(self, engine):
        self.engine = engine
        #
        self.settings = SETTINGS
        #
        self.sector_data = SECTOR_DATA
        self.segments_of_sector_boundaries = SEGMENTS_OF_SECTOR_BOUNDARIES
        self.segments_within_sectors = SEGMENTS_WITHIN_SECTORS
        #
        self.sectors = {}
        self.handle_sector_data()
        #
        self.sector_segments = {sector_id: [] for sector_id in self.sector_data}
        #
        self.raw_segments = []
        #
        self.handle_segments_of_sector_boundaries()
        self.handle_segments_within_sectors()

    def handle_sector_data(self):
        for sec_id, sector_data in self.sector_data.items():
            #
            sector = Sector(
                floor_h=sector_data['floor_h'],
                ceil_h=sector_data['ceil_h'],
                floor_tex_id=sector_data.get('floor_tex_id', 0),
                ceil_tex_id=sector_data.get('ceil_tex_id', 0),
                nested_sector_ids=sector_data.get('nested_sector_ids', None),
            )
            self.sectors[sec_id] = sector

    def handle_segments_of_sector_boundaries(self):
        for (p0, p1), sector_ids, textures in self.segments_of_sector_boundaries:
            #
            seg = self.get_segment(p0, p1, sector_ids, textures)
            self.raw_segments.append(seg)
            #
            self.check_reverse_segment(seg, p0, p1, sector_ids, textures)
            #
            for sector_id in sector_ids:
                if sector_id is not None:
                    self.sector_segments[sector_id].append((p0, p1))

    def check_reverse_segment(self, seg, p0, p1, sector_ids, textures):
        if seg.back_sector_id is not None:
            #
            ceil_h = self.sector_data[seg.sector_id]['ceil_h']
            back_ceil_h = self.sector_data[seg.back_sector_id]['ceil_h']

            # reverse portal_up case
            if ceil_h < back_ceil_h:
                # no need to build upper
                seg.has_portal_up = False

                # create and add a reverse segment
                new_seg = self.get_segment(p1, p0, sector_ids[::-1], textures)

                # no need to build lower
                new_seg.has_portal_low = False
                new_seg.has_portal_mid = False
                #
                self.raw_segments.append(new_seg)

            # reverse portal_mid case
            if seg.mid_tex_id is not None:
                # create and add a reverse segment
                new_seg = self.get_segment(p1, p0, sector_ids[::-1], textures)
                new_seg.has_portal_low = False
                new_seg.has_portal_up = False
                #
                self.raw_segments.append(new_seg)

    def handle_segments_within_sectors(self):
        for (p0, p1), sector_ids, textures in self.segments_within_sectors:
            #
            seg = self.get_segment(p0, p1, sector_ids, textures)
            self.raw_segments.append(seg)

    def get_segment(self, p0, p1, sector_ids, textures):
        seg = Segment(
            p0=p0,
            p1=p1,
            #
            sector_id=sector_ids[0],
            back_sector_id=sector_ids[1],
            #
            low_tex_id=textures[0],
            mid_tex_id=textures[1],
            up_tex_id=textures[2],
        )
        return seg
