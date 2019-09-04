# ChatSite
A simple chat app created with django + channels + channels_redis


Requirements:

1) Python>=3.6

2) redis-server


Functionality:

Authentication:

1) Login (accounts/login)

2) Logout (accounts/logout)


Chat:

1) User to user chatrooms (messages/<username>)
  
2) Create chatroom (messages/<username>)
  
3) List created chatrooms (messages)


Restrictions:

1) Can only create new user with admin iterface ('admin/')

2) Can only create new chatroom by appending username to url (messages/<username>)
