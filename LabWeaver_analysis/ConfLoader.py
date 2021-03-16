import himl
import os


class ConfLoader:
	"""Loader for hierarchical configuration for analysis script parameters
	"""


	def __init__(self, conf_dir):
		"""Initialize with the root directory of the configuration tree

		This should be the directory that contains default.yaml (the final dir 
		will be prepended to match the himl convention).
		"""
		## Peel off the final dir to prepend to himl calls
		self.conf_folder = os.path.basename(os.path.normpath(conf_dir))
		## Set the root configuration directory
		self.conf_dirname = os.path.dirname(os.path.normpath(conf_dir))

		self.himl_processor = himl.ConfigProcessor()
		## Create attribute but leave it blank until loaded
		self.loaded_conf = None


	def load_conf_from_tree(self, conf_path="", **kwargs):
		"""Load the configuration given in the file specified by conf_path

		This should not include the root directory of the configuration tree 
		(unlike when using raw himl); it will be prepended automatically.
		"""
		self.conf_path = self.conf_folder+"/"+conf_path
		self.loaded_conf = self.himl_processor.process(
							cwd=self.conf_dirname,
							path=self.conf_path,
							output_format="json",
							**kwargs)



