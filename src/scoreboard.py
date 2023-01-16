from .textfield import TextField

class ScoreBoard:
    def __init__(self,surface):
        self.scores = []
        self.scores_textfields = []
        self.surface = surface
        self.textfield = TextField((0, 0), (800, 100), 'BEST SCORES', 60, self.surface)
        self.load_from_file()

    def draw(self):
        self.textfield.draw()
        for textfield in self.scores_textfields:
            textfield.draw()

    def load_from_file(self):
        self.scores_textfields = []
        with open('src/scores.txt',"r") as f:
            self.scores = sorted([line[:-1].split() for line in f],reverse=True,key = lambda x: int(x[1]))[:5]

        for i in range(len(self.scores)):
            self.scores_textfields.append(
                TextField((0,100*(i+1)),(800,100),f'{i+1}. {self.scores[i][0]} - {self.scores[i][1]}',30,self.surface)
            )

    def append_file(self,value):
        with open('src/scores.txt',"a") as f:
            f.write(value)
        self.load_from_file()



