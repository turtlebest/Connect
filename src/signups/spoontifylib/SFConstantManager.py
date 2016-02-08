import Singleton
@Singleton.singleton
class SFConstantManager(object):
	def __init__(self):
		self.SF_DEBUG = True