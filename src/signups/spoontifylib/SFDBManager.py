import Singleton
import MySQLdb
import SFConstantManager

@Singleton.singleton
class SFDBManager(object):
	def __init__(self):
		## get constant singleton
		self.sf_constant_manager = SFConstantManager.SFConstantManager();
		## database configuration
		self.sf_db_host = '127.0.0.1'
		self.sf_db_username = 'root'
		self.sf_db_password = '0000'
		self.sf_db_dbname = 'Database'
		self.sf_db_port = 8889
		## Connect spoontify database.
		try:
			self.sf_db_conn = MySQLdb.connect(host=self.sf_db_host,
				user=self.sf_db_username,
				passwd=self.sf_db_password,
				db=self.sf_db_dbname,
				port=self.sf_db_port)
		except Exception, e:
			if self.sf_constant_manager.SF_DEBUG:
				print ("[DEBUG][DATABASE][connection failed]"+str(e))

	def execute_sql(self, sql_sentence, sets=[]):
		if len(sql_sentence) == 0:
			if self.sf_constant_manager.SF_DEBUG:
				print ("[DEBUG][DATABASE][sql_sentence can not be empty.]")
			return

		cursor = self.sf_db_conn.cursor()
		try:
			cursor.execute(sql_sentence, sets)
			self.sf_db_conn.commit()
			cursor.close()
			return True
		except Exception, e:
			self.sf_db_conn.rollback()
			cursor.close()
			if self.sf_constant_manager.SF_DEBUG:

				print ("[DEBUG][DATABASE][can not execute sql sentence] ["+sql_sentence +"]"+ str(e))
			return False

	def query_data(self, query_sql_sentence, sets=[]):
		## Get the cursor from the current database connection.
		cursor = self.sf_db_conn.cursor()

		## Execute query sql sentence and get result.
		cursor.execute(query_sql_sentence, sets)
		back_data = cursor.fetchall()
		cursor.close()

		## Return back data.
		return back_data



		
