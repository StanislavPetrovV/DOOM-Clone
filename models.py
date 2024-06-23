from settings import *
from data_types import *
from ground.base import get_context
from sect.triangulation import Triangulation
from textures import Textures

ctx = get_context()
Contour, Point, Polygon = ctx.contour_cls, ctx.point_cls, ctx.polygon_cls


class Models:
    def __init__(self, engine):
        self.engine = engine
        self.textures = Textures()
        #
        self.sectors = engine.level_data.sectors
        self.raw_segments = engine.level_data.raw_segments
        self.segments = engine.bsp_builder.segments
        self.sector_segments = engine.level_data.sector_segments
        #
        self.wall_id = 0
        self.wall_models: list[WallModel] = []
        self.build_wall_models()
        #
        self.flat_models: list[list[FlatModel, FlatModel]] = []
        self.build_flat_models()

    def build_flat_models(self):
        for sector_id in self.sector_segments:
            #
            floor_model = FlatModel(self, sector_id)
            ceil_model = FlatModel(self, sector_id, is_floor=False)
            #
            self.flat_models.extend([[floor_model, ceil_model]])

    def build_wall_models(self):
        for seg in self.raw_segments:
        # for seg in self.segments:
            #
            if seg.back_sector_id is None:
                # solid wall
                wall = WallModel(self, seg)
                self.add_wall_model(wall, seg)

            else:
                front_sector = self.sectors[seg.sector_id]
                back_sector = self.sectors[seg.back_sector_id]

                # portal_low wall
                if seg.has_portal_low:
                    if abs(front_sector.floor_h - back_sector.floor_h) > EPS:
                        wall = WallModel(self, seg, wall_type=WallType.PORTAL_LO)
                        self.add_wall_model(wall, seg)

                # portal_up wall
                if seg.has_portal_up:
                    if abs(front_sector.ceil_h - back_sector.ceil_h) > EPS:
                        wall = WallModel(self, seg, wall_type=WallType.PORTAL_UP)
                        self.add_wall_model(wall, seg)

                # portal_middle wall
                if seg.has_portal_mid:
                    if seg.mid_tex_id is not None:
                        wall = WallModel(self, seg, wall_type=WallType.PORTAL_MID)
                        self.add_wall_model(wall, seg)

    def add_wall_model(self, wall_model, segment):
        self.wall_models.append(wall_model)
        #
        segment.wall_model_ids.add(self.wall_id)
        self.wall_id += 1


class FlatModel:
    def __init__(self, models, sector_id, is_floor=True):
        self.engine = models.engine
        self.textures = models.textures
        self.sector_segments = self.engine.level_data.sector_segments
        self.sectors = self.engine.level_data.sectors
        #
        self.sector_id = sector_id
        self.sector = self.sectors[sector_id]
        self.is_floor = is_floor
        #
        self.model: ray.Model = self.get_model()

    def get_texture(self):
        if self.is_floor:
            return self.textures.flats[self.sector.floor_tex_id]
        return self.textures.flats[self.sector.ceil_tex_id]

    def get_model(self):
        mesh = self.get_polygon_mesh()
        model = ray.load_model_from_mesh(mesh)
        model.materials[0].maps[ray.MATERIAL_MAP_DIFFUSE].texture = self.get_texture()
        return model

    def get_outline(self, sector_segments):
        segs = sector_segments.copy()
        #
        outline = [segs[0][0]]
        i = 0
        while len(outline) != len(segs) + 1:
            seg = segs[i]
            #
            if outline[-1] in seg:
                point = seg[1] if outline[-1] == seg[0] else seg[0]
                outline.append(point)
            i = (i + 1) % len(segs)
            #
        return outline[:-1]

    def get_triangles(self):
        segs = self.sector_segments[self.sector_id]
        sector_verts = self.get_outline(segs)

        # polygon outline shape
        shape = Contour([Point(*vert) for vert in sector_verts])

        hole_list = []
        if self.sector.nested_sector_ids is not None:
            #
            for nested_sector_id in self.sector.nested_sector_ids:
                segs = self.sector_segments[nested_sector_id]
                hole_verts = self.get_outline(segs)
                #
                hole_list.append(hole_verts)
                sector_verts += hole_verts

        holes = [Contour([Point(*vert) for vert in hole]) for hole in hole_list]

        triangles = Triangulation.constrained_delaunay(
            Polygon(shape, holes), context=ctx).triangles()

        return triangles, sector_verts

    def get_indices(self, triangles, outline_verts):
        indices = []
        for triangle in triangles:
            vertices = triangle.vertices[::-1] if self.is_floor else triangle.vertices
            # vertices = triangle.vertices
            for v in vertices:
                indices.append(outline_verts.index((v.x, v.y)))
        return indices

    def get_vertices(self, outline_verts):
        height = self.sector.floor_h if self.is_floor else self.sector.ceil_h
        return [vec3(v[0], height, v[1]) for v in outline_verts]

    def get_polygon_mesh(self) -> ray.Mesh:
        # triangulation
        triangles, sector_verts = self.get_triangles()
        #
        triangle_count = len(triangles)
        vertex_count = len(sector_verts)

        # get normal
        normal = vec3(0, 1, 0) if self.is_floor else vec3(0, -1, 0)
        normals = glm.array([normal] * vertex_count)

        # get vertices
        vertices = self.get_vertices(sector_verts)
        vertices = glm.array(vertices)

        # get tex coords
        tex_coords = [glm.vec2(v) for v in sector_verts]
        tex_coords = tex_coords if self.is_floor else [glm.vec2(v.x, -v.y) for v in tex_coords]
        tex_coords = glm.array(tex_coords)

        # get indices
        indices = self.get_indices(triangles, sector_verts)
        indices = glm.array.from_numbers(glm.uint16, *indices)

        # get mesh
        mesh = ray.Mesh()
        #
        mesh.triangleCount = triangle_count
        mesh.vertexCount = vertex_count
        #
        mesh.vertices = ray.ffi.from_buffer("float []", vertices)
        mesh.indices = ray.ffi.from_buffer("unsigned short []", indices)
        mesh.texcoords = ray.ffi.from_buffer("float []", tex_coords)
        mesh.normals = ray.ffi.from_buffer("float []", normals)

        ray.upload_mesh(mesh, False)
        return mesh


class WallModel:
    def __init__(self, models, segment, wall_type=WallType.SOLID):
        self.engine = models.engine
        self.textures = models.textures
        self.segment = segment
        self.sectors = self.engine.level_data.sectors
        self.wall_type = wall_type
        #
        self.is_shaded = self.get_shading()
        #
        self.model: ray.Model = self.get_model()

    def get_model(self):
        mesh = self.get_quad_mesh()
        model = ray.load_model_from_mesh(mesh)
        model.materials[0].maps[ray.MATERIAL_MAP_DIFFUSE].texture = self.get_texture()
        #
        return model

    def get_texture(self):
        if self.wall_type in {WallType.SOLID, WallType.PORTAL_MID}:
            tex_id = [tex := self.segment.mid_tex_id, 0][tex is None]
        #
        elif self.wall_type == WallType.PORTAL_LO:
            tex_id = [tex := self.segment.low_tex_id, 0][tex is None]
        #
        elif self.wall_type == WallType.PORTAL_UP:
            tex_id = [tex := self.segment.up_tex_id, 0][tex is None]
        #
        return self.textures.walls[tex_id]

    def get_shading(self):
        seg_vec = self.segment.pos[1] - self.segment.pos[0]
        light_vec = LIGHT_POS - self.segment.pos[0]
        return light_vec.x * seg_vec.y > light_vec.y * seg_vec.x

    def get_wall_height_data(self):
        front_sector = self.sectors[self.segment.sector_id]
        #
        if self.wall_type == WallType.SOLID:
            bottom, top = front_sector.floor_h, front_sector.ceil_h
            return bottom, top
        #
        back_sector = self.sectors[self.segment.back_sector_id]
        #
        if self.wall_type == WallType.PORTAL_LO:
            bottom, top = front_sector.floor_h, back_sector.floor_h
        elif self.wall_type == WallType.PORTAL_UP:
            bottom, top = front_sector.ceil_h, back_sector.ceil_h
        elif self.wall_type == WallType.PORTAL_MID:
            bottom, top = (
                max(front_sector.floor_h, back_sector.floor_h),
                min(front_sector.ceil_h, back_sector.ceil_h)
            )
        #
        bottom, top = min(bottom, top), max(top, bottom)
        return bottom, top

    def get_quad_mesh(self) -> ray.Mesh:
        triangle_count = 2
        vertex_count = 4

        # get seg coords
        (x0, z0), (x1, z1) = self.segment.pos

        # get normals
        delta = vec3(x1, 0, z1) - vec3(x0, 0, z0)
        normal = glm.normalize(vec3(-delta.z, delta.y, delta.x))
        normals = glm.array([normal] * vertex_count)

        # get tex coords
        width = glm.length(delta)
        #
        bottom, top = self.get_wall_height_data()
        # '-bottom, -top' - flip texture along Y axis
        uv0, uv1, uv2, uv3 = (0, -bottom), (width, -bottom), (width, -top), (0, -top)
        tex_coords = glm.array([glm.vec2(v) for v in [uv0, uv1, uv2, uv3]])

        # get vertices
        v0, v1, v2, v3 = (x0, bottom, z0), (x1, bottom, z1), (x1, top, z1), (x0, top, z0)
        vertices = glm.array([vec3(v) for v in [v0, v1, v2, v3]])

        # get indices
        indices = [0, 1, 2, 0, 2, 3]
        indices = glm.array.from_numbers(glm.uint16, *indices)

        # get mesh
        mesh = ray.Mesh()
        #
        mesh.triangleCount = triangle_count
        mesh.vertexCount = vertex_count
        #
        mesh.vertices = ray.ffi.from_buffer("float []", vertices)
        mesh.indices = ray.ffi.from_buffer("unsigned short []", indices)
        mesh.texcoords = ray.ffi.from_buffer("float []", tex_coords)
        mesh.normals = ray.ffi.from_buffer("float []", normals)

        ray.upload_mesh(mesh, False)
        return mesh
