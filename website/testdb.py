from website.models import *
count=User.query.count()
data=User.query.all()
print(data[count-1].id)