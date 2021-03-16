import os
import setuptools
import sys

## README for long description
with open('README.md', encoding='utf-8') as rdme:
	_readme = rdme.read()

_mydir = os.path.abspath(os.path.dirname(sys.argv[0]))
_requires = [ r for r in open('requirements.txt', "r").read().split('\n') if len(r)>1 ]

setuptools.setup(
	name='LabWeaver-analysis',
	version="0.0.1",
	description="A scientific analysis \"server\", including dynamic configuration, provenance, and caching.",
	long_description=_readme+"\n\n",
	long_description_content_type="text/markdown",
	url="https://github.com/SamWolski/LabWeaver-analysis",
	author="Sam Wolski",
	author_email="wolski.samp@gmail.com",
	python_requires=">=3.9.*",
	license="MIT",
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3.9",
		"Topic :: Scientific/Engineering",
	],
	packages=["LabWeaver_analysis"],
	install_requires=_requires,
	# entry_points={
	# 	"console_scripts": [
	# 		"lw-analyze = labweaver_analysis.cli:run",
	# 	]
	# },
)
