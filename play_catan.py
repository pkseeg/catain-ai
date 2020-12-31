from catan_utils import *

if __name__=='__main__':
    tile_nums = [12,2,3,3,11,11,4,4,10,10,5,5,9,9,6,6,8,8]
    resources = ['St','St','St','Br','Br','Br','Wh','Wh','Wh','Wh','Wo','Wo','Wo','Wo','Lu','Lu','Lu','Lu','De']
    ports = ['Wh','St','Th','Wo','Th','Th','Br','Wo','Th']
    random_init = True
    game = CatanGame(random_init, tile_nums, resources, ports)
    print('game')
    game.play()