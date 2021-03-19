import sqlite3


## TODO outsource this to a configurable file
INDEX_KEYS = ("experiment", "meas_id")
RECORD_KEYS = ("experiment", "meas_id", "cooldown", "meas_type")
RECORD_PLACEHOLDER_STRING = "("+",".join(["?"]*len(RECORD_KEYS))+")"


def row2dict(row):
	"""Convert an sqlite3.Row object to a python dict
	"""
	keys_list = row.keys()
	out_dict = {key: value for key, value in zip(keys_list, row)}
	return out_dict


def format_records(rcursor, format="dict"):
	"""Format records from a cursor object
	"""
	## Get rows from cursor object
	rows = rcursor.fetchall()
	## Prepare values in requested format
	if format == "dict":
		return [row2dict(row) for row in rows]



class RecordsDB:
	"""Interface to the database of experimental records.

	The database can be accessed directly through the `db` attribute. Currently
	this is an sqlite3 database, however the backend implementation may change
	in the future which will almost certainly break user code that interfaces
	directly with the database object.
	"""


	def __init__(self, db_path):
		"""Initialize with the path to the database file
		"""
		self.db = sqlite3.connect(db_path)
		## Ensure Row objects will be returned 
		self.db.row_factory = sqlite3.Row
		## Create table - idempotent operation due to IF NOT
		self.db.execute('''CREATE TABLE IF NOT EXISTS records (
					experiment TEXT NOT NULL,
					meas_id TEXT NOT NULL,
					cooldown TEXT NOT NULL,
					meas_type TEXT NOT NULL,
					PRIMARY KEY (experiment, meas_id)
					)
				''')


	def __del__(self):
		self.db.close()


	def add_record(self, record_dict):
		"""Add a single record to the database

		The `record_dict` input should have all the keys present in `RECORD_KEYS`,
		even if some values are None.
		"""
		## Convert dict to ordered tuple with fixed order from RECORD_KEYS
		new_record = tuple(record_dict[key] for key in RECORD_KEYS)
		## Assign ordered tuple to database
		with self.db:
			self.db.execute("INSERT INTO records VALUES "
							+RECORD_PLACEHOLDER_STRING, (new_record))
		##


	def delete_record(self, target_values):
		"""Delete a single record from the database, based on the 
		`target_values` which is an ordered tuple of the `INDEX_KEYS` values.
		"""
		## Construct query string from index keys
		query_string = "DELETE * FROM records WHERE "+" AND ".join(["({} = ?)".format(param) for param in INDEX_KEYS])
		## Carry out deletion
		with self.db:
			self.db.execute(query_string, target_values)


	def filter_records(self, expressions, format="dict"):
		"""Get records matching the intersection (AND) of the SQL expressions given in `expressions`

		Use of this method is discouraged as the syntax depends on the 
		underlying sqlite3 backend.

		Note if a single expression is given, it should be provided as a tuple
		and not a string! ie use an extra comma:
		("my_val = 3",) instead of ("my_val = 3")
		If this is not done, the string will be parsed as a list of the 
		individual characters!
		"""
		## Construct query string
		query_string = "SELECT * FROM records WHERE "+" AND ".join(["({})".format(expr) for expr in expressions])
		## Execute query string to get cursor object
		with self.db:
			rcursor = self.db.execute(query_string)
		## Return results via formatter
		return format_records(rcursor, format=format)


	def head(self, n_records=10, format='dict'):
		"""Preview `n_records` records from the top of the records db
		"""
		## Construct query string
		query_string = "SELECT * FROM records LIMIT ?"
		## Execute query string to get cursor object
		with self.db:
			rcursor = self.db.execute(query_string, (str(n_records),))
		## Return results via formatter
		return format_records(rcursor, format=format)


