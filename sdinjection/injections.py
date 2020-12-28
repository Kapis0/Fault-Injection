"""
Classe astratta Injection

"""
import os


class Injection:
    def __init__(self, dev):
        self.device = dev

    def inject(self):
        pass



class BlockInjection(Injection):
    """
    Il modello di iniezione più generale è quello che senza utilizzare il filesystem.
    Corrompo uno o più byte sovrascrivendoli. Uno strumento che mi permette di fare questo è dd.
    Posso scegliere da dove copiare il byte a dove compiarlo e quanti byte.
    """
    def __init__(self, file_in, file_out, bs, count, seek):
        self.file_in = file_in
        self.file_out = file_out
        self.bs = bs
        self.count = count
        self.seek = seek

    def __repr__(self):
        return "\n{} --> {} with {} {} {}".format(self.file_in, self.file_out, self.bs, self.count, self.seek)

    def inject(self):
        print("\n*** Loading Fault injection ***")
        os.system("dd if=" + self.file_in + " of=" + self.file_out +
                  " bs=" + str(self.bs) + " count=" + str(self.count) + " seek=" + str(self.seek) + "")


class Ext4Injection(Injection):
    pass


class InodeInjection(Ext4Injection):

    def __init__(self, dev, inode, parameters):
        super(InodeInjection, self).__init__(dev)
        self.inode = inode
        self.parameters = parameters

    def inject(self):
        if self.parameters["type"] == "clean":
            self.clean_inode()
        # other options

    def clean_inode(self):
        os.system("debugfs -R 'clri <" + str(self.inode) + ">' " + self.dev + " -w")

    def stat_inode(self):
        os.system("debugfs -R 'stat <" + str(self.inode) + ">' " + self.dev + "|grep '(0)'")

    def modify_inode(self):
        os.system("debugfs -R 'mi <" + str(self.inode) + ">' " + self.dev + " -w")


class SuperBlockInjection(Ext4Injection):

        def __init__(self, dev, file_in, file_out, bs, count, seek):
            super(InodeInjection, self).__init__(dev)
            self.block_inj = BlockInjection(file_in, file_out, bs, count, seek)
            self.file_in = file_in
            self.file_out = file_out
            self.bs = bs
            self.count = count
            self.seek = seek

        def __repr__(self):
            return "\n{} --> {} with {} {} {}".format(self.file_in, self.file_out, self.bs, self.count, self.seek)

        def inject(self):
            self.block_inj.inject()



