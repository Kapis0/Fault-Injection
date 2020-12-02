from fault_injection.main import InjectionS, InjectionID
from fault_injection.schedule import Event

class Injector(Event, InjectionS, InjectionID):

    def __init__(self):
        Event.__init__(self, self.occur_time, self.type, self.parameters)
        
    def inject(self):
        
        if self.type == "superblock_corruption":
            InjectionS.injection_superblock(self)
        if self.type == "superblock_corruption_random":
            InjectionS.injection_superblock(self)
        if self.type == "i-node_corruption":
            InjectionID.injection_inode(self)
        if self.type == "direct_block_corruption":
            InjectionID.injection_directblock(self)

            
