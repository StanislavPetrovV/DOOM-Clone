from settings import *


class MapRenderer:
    def __init__(self, engine):
        self.engine = engine
        self.camera = engine.camera
        #
        raw_segments = [seg.pos for seg in self.engine.level_data.raw_segments]
        self.x_min, self.y_min, self.x_max, self.y_max = self.get_bounds(raw_segments)
        #
        self.x_out_max, self.y_out_max = self.get_map_bounds()
        #
        self.raw_segments = self.remap_array(raw_segments)
        #
        self.segments = self.remap_array(
            [seg.pos for seg in self.engine.bsp_builder.segments])
        self.counter = 0.0
        #
        self.should_draw = False

    def get_map_bounds(self):
        dx = self.x_max - self.x_min
        dy = self.y_max - self.y_min
        #
        delta = min(MAP_WIDTH / dx, MAP_HEIGHT / dy)
        x_out_max = delta * dx
        y_out_max = delta * dy
        return x_out_max, y_out_max

    def draw(self):
        self.draw_raw_segments()
        self.draw_segments()
        self.draw_player()
        self.counter += 0.0025

    def draw_player(self, dist=100):
        x0, y0 = p0 = self.remap_vec2(self.camera.pos_2d)
        x1, y1 = p0 + self.camera.forward.xz * dist
        #
        ray.draw_line_v((x0, y0), (x1, y1), ray.WHITE)
        ray.draw_circle_v((x0, y0), 10, ray.GREEN)

    def draw_segments(self, seg_color=ray.ORANGE):
        segment_ids = self.engine.bsp_traverser.seg_ids_to_draw
        #
        for seg_id in segment_ids:
        # for seg_id in segment_ids[:int(self.counter) % (len(segment_ids) + 1)]:
            (x0, y0), (x1, y1) = p0, p1 = self.segments[seg_id]
            #
            ray.draw_line_v((x0, y0), (x1, y1), seg_color)
            self.draw_normal(p0, p1, seg_color)
            #
            ray.draw_circle_v((x0, y0), 2, ray.WHITE)
            ray.draw_circle_v((x1, y1), 2, ray.WHITE)

    def draw_normal(self, p0, p1, color, scale=10):
        p10 = p1 - p0
        normal = normalize(vec2(-p10.y, p10.x))
        n0 = (p0 + p1) * 0.5
        n1 = n0 + normal * scale
        #
        ray.draw_line_v((n0.x, n0.y), (n1.x, n1.y), color)

    def draw_raw_segments(self):
        for p0, p1 in self.raw_segments:
            (x0, y0), (x1, y1) = p0, p1
            ray.draw_line_v((x0, y0), (x1, y1), ray.DARKGRAY)

    def remap_array(self, arr: list[tuple[vec2]]):
        return [(self.remap_vec2(p0), self.remap_vec2(p1)) for p0, p1 in arr]

    def remap_vec2(self, p: vec2):
        x = self.remap_x(p.x)
        y = self.remap_y(p.y)
        return vec2(x, y)

    def remap_x(self, x, out_min=MAP_OFFSET):
        out_max = self.x_out_max
        return (x - self.x_min) * (out_max - out_min) / (self.x_max - self.x_min) + out_min

    def remap_y(self, y, out_min=MAP_OFFSET):
        out_max = self.y_out_max
        return (y - self.y_min) * (out_max - out_min) / (self.y_max - self.y_min) + out_min

    @staticmethod
    def get_bounds(segments: list[tuple[vec2]]):
        inf = float('inf')
        x_min, y_min, x_max, y_max = inf, inf, -inf, -inf
        #
        for p0, p1 in segments:
            x_min = p0.x if p0.x < x_min else p1.x if p1.x < x_min else x_min
            x_max = p0.x if p0.x > x_max else p1.x if p1.x > x_max else x_max
            #
            y_min = p0.y if p0.y < y_min else p1.y if p1.y < y_min else y_min
            y_max = p0.y if p0.y > y_max else p1.y if p1.y > y_max else y_max
        return x_min, y_min, x_max, y_max
