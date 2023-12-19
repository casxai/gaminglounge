import pusher

pusher_client = pusher.Pusher(
  app_id='1725847',
  key='122926f4663427b23929',
  secret='fcac78ecc03cb83bc6a3',
  cluster='ap1',
  ssl=True
)

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NTY4NDEzLCJpYXQiOjE3MDI5NzY0MTMsImp0aSI6IjdlM2ZlOTQ1NzI5ZDRhYTFhNjdjMTQ3NzJiNmQ1OGI0IiwidXNlcl9pZCI6IjNhYmNiYzllLTE2ZjEtNGQwNi1iYWNmLTgzMWEwODg5OGUxYyJ9.0mWjUq2xbvm5ZBlL1OlAf04xF2gQXgkFqwwqeZRQwu4