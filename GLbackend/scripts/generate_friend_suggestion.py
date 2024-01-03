from datetime import timedelta
import django
import os
import sys
from django.utils import timezone
from django.db.models import Q

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GLbackend.settings")
django.setup()

from account.models import User

#calling iterator on each queryset to get an iterator obj instead of a list

users = User.objects.all().iterator() 

for user in users:
    user.people_you_may_know.clear() # clear the suggestion list
    
    print('Find friends for:',user)
    
    for friend in user.friends.all().iterator():
        print('Is friend with:', friend)
        
        for friendsfriend in friend.friends.all().iterator():       
            if friendsfriend not in user.friends.all() and friendsfriend != user:
                user.people_you_may_know.add(friendsfriend)
                
    print()


