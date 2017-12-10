import os


class Person:
    def __init__(self, id, name, refdir, outdir):
        # type: (int, str, str, str) -> None
        self.id = id
        self.name = name
        self.refdir = refdir
        self.outdir = outdir + str(self.id) + "/"

        if not os.path.isdir(self.outdir):
            os.makedirs(self.outdir)

            outfile = open(self.outdir + "person-info.txt", "w")
            outfile.write(str(self.id) + "\n")
            outfile.write(str(self.name) + "\n")
            outfile.close()
