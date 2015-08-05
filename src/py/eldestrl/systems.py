from ecs.models import System
from 


class RenderSys(System):
    def __init__(self, con):
        self.con = con

    def update(self, dt):
        from eldestrl.components import Char
        for (e, renderinfo) in dt.pairs_for_type(Char):
            z 
