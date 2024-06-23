from settings import *
from models import Models, WallModel
from data_types import *


class ViewRenderer:
    def __init__(self, engine):
        self.engine = engine
        self.map_renderer = self.engine.map_renderer
        #
        self.segments: list[Segment] = engine.bsp_builder.segments
        self.camera = engine.camera
        self.segment_ids_to_draw = self.engine.bsp_traverser.seg_ids_to_draw
        self.sectors = self.engine.level_data.sectors
        #
        self.models = Models(engine)
        self.wall_models = self.models.wall_models
        self.flat_models = self.models.flat_models
        #
        self.walls_to_draw = set()
        self.mid_walls_to_draw = {}  # as ordered set
        #
        self.screen_tint = WHITE_COLOR

    def update(self):
        self.walls_to_draw.clear()
        self.mid_walls_to_draw.clear()

        for seg_id in self.segment_ids_to_draw:
            # walls
            for wall_id in self.segments[seg_id].wall_model_ids:
                wall = self.wall_models[wall_id]
                #
                if wall.wall_type == WallType.PORTAL_MID:
                    self.mid_walls_to_draw[wall_id] = wall
                else:
                    self.walls_to_draw.add(wall)

    def draw(self):
        # draw flats
        for sec_id in self.sectors:
            #
            floor, ceil = self.flat_models[sec_id]
            ray.draw_model(ceil.model, VEC3_ZERO, 1.0, self.screen_tint)
            ray.draw_model(floor.model, VEC3_ZERO, 1.0, self.screen_tint)

        # draw walls
        for wall in self.walls_to_draw:
            ray.draw_model(wall.model, VEC3_ZERO, 1.0, self.get_tint(wall))

        # draw portal_mid walls from back to front
        for wall in reversed(self.mid_walls_to_draw.values()):
            ray.draw_model(wall.model, VEC3_ZERO, 1.0, self.get_tint(wall))

    def get_tint(self, wall: WallModel):
        if wall.is_shaded:
            if self.map_renderer.should_draw:
                return SHADING_DARK_COLOR
            return SHADING_COLOR
        return self.screen_tint

    def update_screen_tint(self):
        self.screen_tint = (
            DARK_GRAY_COLOR if self.map_renderer.should_draw else WHITE_COLOR
        )
