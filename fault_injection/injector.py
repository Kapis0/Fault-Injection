from fault_injection.fault import InjectionS, InjectionID
from fault_injection.schedule import Event

class Injector(Event):
    
    def __init__(self):
        Event.__init__(self, self.occur_time, self.type, self.parameters)
        
    def inject(self, injection):
        self.injection = injection
        
        if injection["type"] == "superblock_corruption":
            InjectionS.injection_superblock(self)
        if injection["type"] == "superblock_corruption_random":
            InjectionS.injection_superblock(self)
        if injection["type"] == "i-node_corruption":
            InjectionID.injection_inode(self)
        if injection["type"] == "direct_block_corruption":
            InjectionID.injection_directblock(self)
            
