import random
import time

class Tile:
    def __init__(self,resource,number):
        self.res = resource
        self.num = number
    
    def __str__(self):
        s = self.res
        if 1 < self.num < 10:
            s += '0'
        s += str(self.num)
        return s

class Edge:
    def __init__(self,l_intr=None,r_intr=None):
        self.player = 0
        self.l_intr = l_intr
        self.r_intr = r_intr
    
    def setIntrs(self,l_intr,r_intr):
        self.l_intr = l_intr
        self.r_intr = r_intr
    
    def claim(self, player):
        self.player = player
    
    def __str__(self):
        s = str(self.player)
        return s
    
class Intersection:
    def __init__(self, l_tile=None, m_tile=None, r_tile=None, l_edge=None, m_edge=None, r_edge=None):
        '''
        building: E (empty), S (settlement), C (city)
        '''
        self.player = 0
        self.building = 'E'
        self.port = ''
        self.lt = l_tile
        self.mt = m_tile
        self.rt = r_tile
        self.le = l_edge
        self.me = m_edge
        self.re = r_edge
    
    def claim(self, player):
        self.player = player
        self.building = 'S'
    
    def upgrade(self):
        self.building = 'C'
        
    def setPort(self, port):
        self.port = port
        
    def __str__(self):
        s = self.building
        s += str(self.player)
        return s
    
class Board:
    def __init__(self,random_init,tile_nums,resources,ports):
        '''
        random_init: True if random initialization of the board is desired, 
                    False when the order is specified by lists
        tile_nums: Length 18 array containing all tile numbers (Desert has no tile number)
        resources: Length 19 array containing all tile resources
        '''
        # if it's random initialization
        if random_init:
            random.shuffle(tile_nums)
            random.shuffle(resources)
            random.shuffle(ports)
        
        # initialize the tiles
        self.tiles = []
        ns = 0
        rs = 0
        for i in range(19):
            # The desert has a -1, always
            if resources[rs] == 'De':
                tile = Tile(resources[rs],-1)
                rs += 1
            else:
                tile = Tile(resources[rs],tile_nums[ns])
                rs += 1
                ns += 1
            self.tiles.append(tile)
        
        # initialize the edges
        self.edges = [0]*72
        for i in range(72):
            self.edges[i] = Edge()
        
        # initialize the intersections (this is easier than trying to figure out the loops lol)
        self.intrs = [0]*54
        # first row
        self.intrs[0] = Intersection(r_tile=self.tiles[0],m_edge=self.edges[0],r_edge=self.edges[1])
        self.intrs[1] = Intersection(m_tile=self.tiles[0],l_edge=self.edges[1],r_edge=self.edges[2])
        self.intrs[2] = Intersection(l_tile=self.tiles[0],r_tile=self.tiles[1],l_edge=self.edges[2],m_edge=self.edges[3],r_edge=self.edges[4])
        self.intrs[3] = Intersection(m_tile=self.tiles[1],l_edge=self.edges[4],r_edge=self.edges[5])
        self.intrs[4] = Intersection(l_tile=self.tiles[1],r_tile=self.tiles[2],l_edge=self.edges[5],m_edge=self.edges[6],r_edge=self.edges[7])
        self.intrs[5] = Intersection(m_tile=self.tiles[2],l_edge=self.edges[7],r_edge=self.edges[8])
        self.intrs[6] = Intersection(l_tile=self.tiles[2],l_edge=self.edges[8],r_edge=self.edges[9])
        # second row
        self.intrs[7] = Intersection(r_tile=self.tiles[3],m_edge=self.edges[10],r_edge=self.edges[11])
        self.intrs[8] = Intersection(m_tile=self.tiles[3],r_tile=self.tiles[0],l_edge=self.edges[11],m_edge=self.edges[0],r_edge=self.edges[12])
        self.intrs[9] = Intersection(l_tile=self.tiles[3],m_tile=self.tiles[0],r_tile=self.tiles[4],l_edge=self.edges[12],m_edge=self.edges[13],r_edge=self.edges[14])
        self.intrs[10] = Intersection(l_tile=self.tiles[0],m_tile=self.tiles[4],r_tile=self.tiles[1],l_edge=self.edges[14],m_edge=self.edges[3],r_edge=self.edges[15])
        self.intrs[11] = Intersection(l_tile=self.tiles[4],m_tile=self.tiles[1],r_tile=self.tiles[5],l_edge=self.edges[15],m_edge=self.edges[16],r_edge=self.edges[17])
        self.intrs[12] = Intersection(l_tile=self.tiles[1],m_tile=self.tiles[5],r_tile=self.tiles[2],l_edge=self.edges[17],m_edge=self.edges[6],r_edge=self.edges[18])
        self.intrs[13] = Intersection(l_tile=self.tiles[5],m_tile=self.tiles[2],r_tile=self.tiles[6],l_edge=self.edges[18],m_edge=self.edges[19],r_edge=self.edges[20])
        self.intrs[14] = Intersection(l_tile=self.tiles[2],m_tile=self.tiles[6],l_edge=self.edges[20],m_edge=self.edges[9],r_edge=self.edges[21])
        self.intrs[15] = Intersection(l_tile=self.tiles[6],l_edge=self.edges[21],m_edge=self.edges[22])
        # third row
        self.intrs[16] = Intersection(r_tile=self.tiles[7],m_edge=self.edges[23],r_edge=self.edges[24])
        self.intrs[17] = Intersection(m_tile=self.tiles[7],r_tile=self.tiles[3],l_edge=self.edges[24],m_edge=self.edges[10],r_edge=self.edges[25])
        self.intrs[18] = Intersection(l_tile=self.tiles[7],m_tile=self.tiles[3],r_tile=self.tiles[8],l_edge=self.edges[25],m_edge=self.edges[26],r_edge=self.edges[27])
        self.intrs[19] = Intersection(l_tile=self.tiles[3],m_tile=self.tiles[8],r_tile=self.tiles[4],l_edge=self.edges[27],m_edge=self.edges[13],r_edge=self.edges[28])
        self.intrs[20] = Intersection(l_tile=self.tiles[8],m_tile=self.tiles[4],r_tile=self.tiles[9],l_edge=self.edges[28],m_edge=self.edges[29],r_edge=self.edges[30])
        self.intrs[21] = Intersection(l_tile=self.tiles[4],m_tile=self.tiles[9],r_tile=self.tiles[5],l_edge=self.edges[30],m_edge=self.edges[16],r_edge=self.edges[31])
        self.intrs[22] = Intersection(l_tile=self.tiles[9],m_tile=self.tiles[5],r_tile=self.tiles[10],l_edge=self.edges[31],m_edge=self.edges[32],r_edge=self.edges[33])
        self.intrs[23] = Intersection(l_tile=self.tiles[5],m_tile=self.tiles[10],r_tile=self.tiles[6],l_edge=self.edges[33],m_edge=self.edges[19],r_edge=self.edges[34])
        self.intrs[24] = Intersection(l_tile=self.tiles[10],m_tile=self.tiles[6],r_tile=self.tiles[11],l_edge=self.edges[34],m_edge=self.edges[35],r_edge=self.edges[36])
        self.intrs[25] = Intersection(l_tile=self.tiles[6],m_tile=self.tiles[11],l_edge=self.edges[36],m_edge=self.edges[22],r_edge=self.edges[37])
        self.intrs[26] = Intersection(l_tile=self.tiles[11],l_edge=self.edges[37],m_edge=self.edges[38])
        # fourth row
        self.intrs[27] = Intersection(r_tile=self.tiles[7],m_edge=self.edges[23],r_edge=self.edges[39])
        self.intrs[28] = Intersection(m_tile=self.tiles[7],r_tile=self.tiles[12],l_edge=self.edges[39],m_edge=self.edges[40],r_edge=self.edges[41])
        self.intrs[29] = Intersection(l_tile=self.tiles[7],m_tile=self.tiles[12],r_tile=self.tiles[8],l_edge=self.edges[41],m_edge=self.edges[26],r_edge=self.edges[42])
        self.intrs[30] = Intersection(l_tile=self.tiles[12],m_tile=self.tiles[8],r_tile=self.tiles[13],l_edge=self.edges[42],m_edge=self.edges[43],r_edge=self.edges[44])
        self.intrs[31] = Intersection(l_tile=self.tiles[8],m_tile=self.tiles[13],r_tile=self.tiles[9],l_edge=self.edges[44],m_edge=self.edges[29],r_edge=self.edges[45])
        self.intrs[32] = Intersection(l_tile=self.tiles[13],m_tile=self.tiles[9],r_tile=self.tiles[14],l_edge=self.edges[45],m_edge=self.edges[46],r_edge=self.edges[47])
        self.intrs[33] = Intersection(l_tile=self.tiles[9],m_tile=self.tiles[14],r_tile=self.tiles[10],l_edge=self.edges[47],m_edge=self.edges[32],r_edge=self.edges[48])
        self.intrs[34] = Intersection(l_tile=self.tiles[14],m_tile=self.tiles[10],r_tile=self.tiles[15],l_edge=self.edges[48],m_edge=self.edges[49],r_edge=self.edges[50])
        self.intrs[35] = Intersection(l_tile=self.tiles[10],m_tile=self.tiles[15],r_tile=self.tiles[11],l_edge=self.edges[50],m_edge=self.edges[35],r_edge=self.edges[51])
        self.intrs[36] = Intersection(l_tile=self.tiles[15],m_tile=self.tiles[11],l_edge=self.edges[51],m_edge=self.edges[52],r_edge=self.edges[53])
        self.intrs[37] = Intersection(l_tile=self.tiles[11],l_edge=self.edges[53],m_edge=self.edges[38])
        # fifth row
        self.intrs[38] = Intersection(r_tile=self.tiles[12],m_edge=self.edges[40],r_edge=self.edges[54])
        self.intrs[39] = Intersection(m_tile=self.tiles[12],r_tile=self.tiles[16],l_edge=self.edges[54],m_edge=self.edges[55],r_edge=self.edges[56])
        self.intrs[40] = Intersection(l_tile=self.tiles[12],m_tile=self.tiles[16],r_tile=self.tiles[13],l_edge=self.edges[56],m_edge=self.edges[43],r_edge=self.edges[57])
        self.intrs[41] = Intersection(l_tile=self.tiles[16],m_tile=self.tiles[13],r_tile=self.tiles[17],l_edge=self.edges[57],m_edge=self.edges[58],r_edge=self.edges[59])
        self.intrs[42] = Intersection(l_tile=self.tiles[13],m_tile=self.tiles[17],r_tile=self.tiles[14],l_edge=self.edges[59],m_edge=self.edges[46],r_edge=self.edges[60])
        self.intrs[43] = Intersection(l_tile=self.tiles[17],m_tile=self.tiles[14],r_tile=self.tiles[18],l_edge=self.edges[60],m_edge=self.edges[61],r_edge=self.edges[62])
        self.intrs[44] = Intersection(l_tile=self.tiles[14],m_tile=self.tiles[18],r_tile=self.tiles[15],l_edge=self.edges[62],m_edge=self.edges[49],r_edge=self.edges[63])
        self.intrs[45] = Intersection(l_tile=self.tiles[18],m_tile=self.tiles[15],l_edge=self.edges[63],m_edge=self.edges[64],r_edge=self.edges[65])
        self.intrs[46] = Intersection(l_tile=self.tiles[15],l_edge=self.edges[65],m_edge=self.edges[52])
        # sixth row
        self.intrs[47] = Intersection(r_tile=self.tiles[16],m_edge=self.edges[55],r_edge=self.edges[66])
        self.intrs[48] = Intersection(m_tile=self.tiles[16],l_edge=self.edges[66],r_edge=self.edges[67])
        self.intrs[49] = Intersection(l_tile=self.tiles[16],r_tile=self.tiles[17],l_edge=self.edges[67],m_edge=self.edges[58],r_edge=self.edges[68])
        self.intrs[50] = Intersection(m_tile=self.tiles[17],l_edge=self.edges[68],r_edge=self.edges[69])
        self.intrs[51] = Intersection(l_tile=self.tiles[17],r_tile=self.tiles[18],l_edge=self.edges[69],m_edge=self.edges[61],r_edge=self.edges[70])
        self.intrs[52] = Intersection(m_tile=self.tiles[18],l_edge=self.edges[70],r_edge=self.edges[71])
        self.intrs[53] = Intersection(l_tile=self.tiles[18],l_edge=self.edges[71],m_edge=self.edges[64])
         
        # Fill the edges
        # first row
        self.edges[0].setIntrs(self.intrs[8],self.intrs[0])
        self.edges[1].setIntrs(self.intrs[0],self.intrs[1])
        self.edges[2].setIntrs(self.intrs[1],self.intrs[2])
        self.edges[3].setIntrs(self.intrs[10],self.intrs[2])
        self.edges[4].setIntrs(self.intrs[2],self.intrs[3])
        self.edges[5].setIntrs(self.intrs[3],self.intrs[4])
        self.edges[6].setIntrs(self.intrs[12],self.intrs[4])
        self.edges[7].setIntrs(self.intrs[4],self.intrs[5])
        self.edges[8].setIntrs(self.intrs[5],self.intrs[6])
        self.edges[9].setIntrs(self.intrs[14],self.intrs[6])
        # second row
        self.edges[10].setIntrs(self.intrs[17],self.intrs[7])
        self.edges[11].setIntrs(self.intrs[7],self.intrs[8])
        self.edges[12].setIntrs(self.intrs[8],self.intrs[9])
        self.edges[13].setIntrs(self.intrs[19],self.intrs[9])
        self.edges[14].setIntrs(self.intrs[9],self.intrs[10])
        self.edges[15].setIntrs(self.intrs[10],self.intrs[11])
        self.edges[16].setIntrs(self.intrs[21],self.intrs[11])
        self.edges[17].setIntrs(self.intrs[11],self.intrs[12])
        self.edges[18].setIntrs(self.intrs[12],self.intrs[13])
        self.edges[19].setIntrs(self.intrs[23],self.intrs[13])
        self.edges[20].setIntrs(self.intrs[13],self.intrs[14])
        self.edges[21].setIntrs(self.intrs[14],self.intrs[15])
        self.edges[22].setIntrs(self.intrs[25],self.intrs[15])
        # third row
        self.edges[23].setIntrs(self.intrs[27],self.intrs[16])
        self.edges[24].setIntrs(self.intrs[16],self.intrs[17])
        self.edges[25].setIntrs(self.intrs[17],self.intrs[18])
        self.edges[26].setIntrs(self.intrs[29],self.intrs[18])
        self.edges[27].setIntrs(self.intrs[18],self.intrs[19])
        self.edges[28].setIntrs(self.intrs[19],self.intrs[20])
        self.edges[29].setIntrs(self.intrs[31],self.intrs[20])
        self.edges[30].setIntrs(self.intrs[20],self.intrs[21])
        self.edges[31].setIntrs(self.intrs[21],self.intrs[22])
        self.edges[32].setIntrs(self.intrs[33],self.intrs[22])
        self.edges[33].setIntrs(self.intrs[22],self.intrs[23])
        self.edges[34].setIntrs(self.intrs[23],self.intrs[24])
        self.edges[35].setIntrs(self.intrs[35],self.intrs[24])
        self.edges[36].setIntrs(self.intrs[24],self.intrs[25])
        self.edges[37].setIntrs(self.intrs[25],self.intrs[26])
        self.edges[38].setIntrs(self.intrs[37],self.intrs[26])
        # fourth row
        self.edges[39].setIntrs(self.intrs[27],self.intrs[28])
        self.edges[40].setIntrs(self.intrs[38],self.intrs[28])
        self.edges[41].setIntrs(self.intrs[28],self.intrs[29])
        self.edges[42].setIntrs(self.intrs[29],self.intrs[30])
        self.edges[43].setIntrs(self.intrs[40],self.intrs[30])
        self.edges[44].setIntrs(self.intrs[30],self.intrs[31])
        self.edges[45].setIntrs(self.intrs[31],self.intrs[32])
        self.edges[46].setIntrs(self.intrs[42],self.intrs[32])
        self.edges[47].setIntrs(self.intrs[32],self.intrs[33])
        self.edges[48].setIntrs(self.intrs[33],self.intrs[34])
        self.edges[49].setIntrs(self.intrs[44],self.intrs[34])
        self.edges[50].setIntrs(self.intrs[34],self.intrs[35])
        self.edges[51].setIntrs(self.intrs[35],self.intrs[36])
        self.edges[52].setIntrs(self.intrs[46],self.intrs[36])
        self.edges[53].setIntrs(self.intrs[36],self.intrs[37])
        # fifth row
        self.edges[54].setIntrs(self.intrs[38],self.intrs[39])
        self.edges[55].setIntrs(self.intrs[47],self.intrs[39])
        self.edges[56].setIntrs(self.intrs[39],self.intrs[40])
        self.edges[57].setIntrs(self.intrs[40],self.intrs[41])
        self.edges[58].setIntrs(self.intrs[49],self.intrs[41])
        self.edges[59].setIntrs(self.intrs[41],self.intrs[42])
        self.edges[60].setIntrs(self.intrs[42],self.intrs[43])
        self.edges[61].setIntrs(self.intrs[51],self.intrs[43])
        self.edges[62].setIntrs(self.intrs[43],self.intrs[44])
        self.edges[63].setIntrs(self.intrs[44],self.intrs[45])
        self.edges[64].setIntrs(self.intrs[53],self.intrs[45])
        self.edges[65].setIntrs(self.intrs[45],self.intrs[46])
        # sixth row
        self.edges[66].setIntrs(self.intrs[47],self.intrs[48])
        self.edges[67].setIntrs(self.intrs[48],self.intrs[49])
        self.edges[68].setIntrs(self.intrs[49],self.intrs[50])
        self.edges[69].setIntrs(self.intrs[50],self.intrs[51])
        self.edges[70].setIntrs(self.intrs[51],self.intrs[52])
        self.edges[71].setIntrs(self.intrs[52],self.intrs[53])
        
        # initialize ports
        self.intrs[7].setPort(ports[0])
        self.intrs[8].setPort(ports[0])
        self.intrs[2].setPort(ports[1])
        self.intrs[3].setPort(ports[1])
        self.intrs[5].setPort(ports[2])
        self.intrs[6].setPort(ports[2])
        self.intrs[15].setPort(ports[3])
        self.intrs[25].setPort(ports[3])
        self.intrs[36].setPort(ports[4])
        self.intrs[46].setPort(ports[4])
        self.intrs[53].setPort(ports[5])
        self.intrs[52].setPort(ports[5])
        self.intrs[50].setPort(ports[6])
        self.intrs[49].setPort(ports[6])
        self.intrs[39].setPort(ports[7])
        self.intrs[38].setPort(ports[7])
        self.intrs[27].setPort(ports[8])
        self.intrs[16].setPort(ports[8])
        
        
    def __str__(self):
        i = 0
        e = 0
        t = 0
        rows = ['' for i in range(11)]
        
        # row 0
        i = 0
        e = 1
        s = '          '
        while i <= 6:
            if i % 2 == 1:
                s += str(self.edges[e])+' '
                e += 1
            s += str(self.intrs[i])+' '
            if i % 2 == 1:
                s += str(self.edges[e])+' '
                e += 2
            i += 1
        rows[0] = s
        
        
        # row 1
        s = '           '+str(self.edges[0])+'  '
        e = 3
        while e <= 9:
            s += str(self.tiles[t])+'   '
            s += str(self.edges[e])+'  '
            e += 3
            t += 1
        s += ''
        rows[1] = s
        
        # row 2
        i = 7
        e = 11
        s = '     '
        while i <= 15:
            if i % 2 == 0:
                s += str(self.edges[e])+' '
                e += 1
            s += str(self.intrs[i])+' '
            if i % 2 == 0:
                s += str(self.edges[e])+' '
                e += 2
            i += 1
        rows[2] = s
        
        # row 3
        s = '      '+str(self.edges[10])+'  '
        e = 13
        t = 3
        while e <= 22:
            s += str(self.tiles[t])+'   '
            s += str(self.edges[e])+'  '
            e += 3
            t += 1
        s += ''
        rows[3] = s
        
        # row 4
        i = 16
        e = 24
        s = ''
        while i <= 26:
            if i % 2 == 1:
                s += str(self.edges[e])+' '
                e += 1
            s += str(self.intrs[i])+' '
            if i % 2 == 1:
                s += str(self.edges[e])+' '
                e += 2
            i += 1
        rows[4] = s
        
        # row 5
        s = ' '+str(self.edges[23])+'  '
        e = 26
        t = 7
        while e <= 38:
            s += str(self.tiles[t])+'   '
            s += str(self.edges[e])+'  '
            e += 3
            t += 1
        s += ''
        rows[5] = s
        
        # row 6
        i = 27
        e = 39
        s = ''
        while i <= 37:
            if i % 2 == 0:
                s += str(self.edges[e])+' '
                e += 2
            s += str(self.intrs[i])+' '
            if i % 2 == 0:
                s += str(self.edges[e])+' '
                e += 1
            i += 1
        rows[6] = s
        
        # row 7
        s = '      '+str(self.edges[40])+'  '
        e = 43
        t = 12
        while e <= 52:
            s += str(self.tiles[t])+'   '
            s += str(self.edges[e])+'  '
            e += 3
            t += 1
        s += ''
        rows[7] = s
        
        # row 8
        i = 38
        e = 54
        s = '     '
        while i <= 46:
            if i % 2 != 0:
                s += str(self.edges[e])+' '
                e += 2
            s += str(self.intrs[i])+' '
            if i % 2 != 0:
                s += str(self.edges[e])+' '
                e += 1
            i += 1
        rows[8] = s
        
        # row 9
        s = '           '+str(self.edges[55])+'  '
        e = 58
        t = 16
        while e <= 64:
            s += str(self.tiles[t])+'   '
            s += str(self.edges[e])+'  '
            e += 3
            t += 1
        s += ''
        rows[9] = s
        
        # row 10
        i = 47
        e = 65
        s = '          '
        while i <= 53:
            if e!= 65:
                s += str(self.edges[e])+' '
            s += str(self.intrs[i])+' '
            i += 1
            e += 1
        rows[10] = s
        
        return '\n\n'.join(rows)
    
    
    def claimInt(self,player_num,int_num):
        self.intrs[int_num].claim(player_num)
    
    def upgradeInt(self,player_num,int_num):
        self.intrs[int_num].upgrade(player_num)
    
    def claimEdge(self,player_num,edge_num):
        self.edges[edge_num].claim(player_num)

class Player:
    def __init__(self,number,species='human'):
        self.num = number
        self.species = species
        self.rsrcs = {'St':0, 'Br':0, 'Wh':0, 'Wo':0, 'Lu':0}
        self.dvlps = {'Kn':0, 'Vp':0, 'Yp':0, 'Mn':0, 'Rb':0}
        self.exchanges = {'St':4, 'Br':4, 'Wh':4, 'Wo':4, 'Lu':4}
        self.sttls = []
        self.cities = []
        self.longestRoad = False
        self.largestArmy = False
        self.score = 0
    
    def isHuman(self):
        return self.species=='human'

class CatanGame:
    def __init__(self, random_init, tile_nums, resources, ports):
        self.board = Board(random_init,tile_nums,resources,ports)
    
    def __setPlayers(self,n,p1Type,p2Type,p3Type,p4Type=None):
        self.n = n
        self.p1 = Player(1,species=p1Type)
        self.p2 = Player(2,species=p2Type)
        self.p3 = Player(3,species=p3Type)
        self.players = [self.p1, self.p2, self.p3]
        if self.n == 4:
            self.p4 = Player(4,species=p4Type)
            self.players.append(self.p4)
    
    def __roll(self):
        return random.randint(1,6) + random.randint(1,6)
            
    
    def play(self):
        print("Welcom to Catan!")
            
        # Set up the players
        n = int(input("How many players will you be playing with (1-4)? "))
        print("\nRoll for settlement selection!\nPlayer 1 will be going first.")
        time.sleep(2)
        p1Type = input("Player 1 Type (human/ai): ")
        p2Type = input("Player 2 Type (human/ai): ")
        p3Type = input("Player 3 Type (human/ai): ")
        if n == 4:
            p4Type = input("Player 4 Type (human/ai): ")
        else:
            p4Type = None
        self.__setPlayers(n,p1Type,p2Type,p3Type,p4Type)
        
        # Print the empty board
        print("Here's the empty board\n\n"+str(self.board))
        
        # Claim initial settlements
        for p in self.players:
            int_num = int(input('Player '+str(p.num)+"'s first intersection num: "))
            self.board.claimInt(p.num,int_num)
            road_num = int(input('Player '+str(p.num)+"'s first edge num: "))
            self.board.claimEdge(p.num,road_num)
            print("\nBoard\n"+str(self.board))
