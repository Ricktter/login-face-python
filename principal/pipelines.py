def get_gender(backend, strategy, details, response, user=None, *args, **kwargs):

    if backend.name == 'facebook':
    	user.last_name = response['last_name']
    	user.gender = response['gender']
    	#user.birthday = response['user_birthday']
    	user.save()


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):

	url = None
	if backend.name == 'facebook':
		url = "https://graph.facebook.com/%s/picture?type=large" %response['id']
		
 
	if url:
		user.avatar = url
		user.save()


def user_details(strategy, details, response, is_new=False, user=None, *args, **kwargs):
	"""Update user details using data from provider."""
	if user and is_new:
		changed = False # flag to track changes 
		protected = strategy.setting('PROTECTED_USER_FIELDS', [])
		keep = ('username', 'id', 'pk') + tuple(protected)

		for name, value in details.items():
			# do not update username, it was already generated
			# do not update configured fields if user already existed
			if name not in keep and hasattr(user, name):
				if value and value != getattr(user, name, None):
					try:
						setattr(user, name, value)
						changed = True
					except AttributeError:
						pass

		if changed:
			strategy.storage.user.changed(user)