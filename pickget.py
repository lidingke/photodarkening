import pickle
import pdb
from user import User

pickname = 'lastlog.pickle'
pick = dict()
# with open(pickname,'rb') as f:
#      pick = pickle.load(f)
ak = User()
ak.setName('kklong')
ak.setPassword('123')
pick['kklong'] = ak


# pdb.set_trace()

with open(pickname,'wb') as f:
     pickle.dump(pick,f)
