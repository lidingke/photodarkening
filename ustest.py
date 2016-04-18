from user import User
from user import UserManager
import pdb
us = User()
us.setName('lidingke')
us.setPassword('12345')

us1 = User()
us1.setName('lidingke')
us1.setPassword('12345')

a1 = us.isPass('123')
print(a1)
b1 = us.isPass('12345')
print(b1)
usm = UserManager()
usm.insertUser(us.name,us)
usm.saveUsers()
usm.getUsers()
# pdb.set_trace()
