def singleton(class_):
	instances = {}
	def share_instance(*args, **kwargs):
		if class_ not in instances:
			instances[class_] = class_(*args, **kwargs)
		return instances[class_]
	return share_instance

