import himl
import os


class ConfLoader:
	"""Loader for hierarchical configuration for analysis script parameters
	"""


	def __init__(self, conf_dir):
		"""Initialize with the root directory of the configuration tree

		This should be the directory that contains default.yaml; the remainder of the conf path will be appended when calling the loading methods.
		"""
		self.conf_dir = conf_dir
		# ## Peel off the final dir to prepend to himl calls
		# self.conf_folder = os.path.basename(os.path.normpath(conf_dir))
		# ## Set the root configuration directory
		# self.conf_dirname = os.path.dirname(os.path.normpath(conf_dir))

		self.himl_processor = himl.ConfigProcessor()
		## Create attribute but leave it blank until loaded
		self.loaded_conf = None


	def load_conf_from_tree(self, conf_path="", **kwargs):
		"""Load the configuration given in the file specified by conf_path

		This should not include the root directory of the configuration tree 
		(unlike when using raw himl); it will be prepended automatically.
		"""
		self.conf_path = os.path.join(self.conf_dir, conf_path)
		self.loaded_conf = self.himl_processor.process(
							cwd=None,
							path=self.conf_path,
							output_format="json",
							**kwargs)



