from settings import *
from enum import IntEnum, auto
from texture_id import *

TEX_PATH = 'assets/textures/'
#
WALL_TEX_PATH = TEX_PATH + 'walls/'
FLAT_TEX_PATH = TEX_PATH + 'flats/'


class Textures:
    def __init__(self):
        self.walls = self.get_textures(WALL_TEX_PATH, WallTexID)
        self.flats = self.get_textures(FLAT_TEX_PATH, FlatTexID)

    def get_textures(self, dir_path: str, texture_ids: IntEnum):
        textures = []
        for i in range(len(texture_ids)):
            texture = self.load_texture(dir_path + f'{i}.png', texture_ids)
            textures.append(texture)
        return textures

    def load_texture(self, file_path, texture_ids):
        image = ray.load_image(file_path)
        ray.image_mipmaps(image)
        #
        texture = ray.load_texture_from_image(image)
        ray.set_texture_filter(texture, ray.TEXTURE_FILTER_ANISOTROPIC_16X)
        ray.unload_image(image)
        #
        return texture

    def release(self):
        [ray.unload_texture(tex) for tex in self.walls]
        [ray.unload_texture(tex) for tex in self.ceils]
        [ray.unload_texture(tex) for tex in self.floors]
