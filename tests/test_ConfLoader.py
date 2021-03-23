import pytest
import os

import LabWeaver_analysis as lw_ana


CONF_DIR = os.path.abspath("tests/assets/conf")

@pytest.fixture
def conf_loader():
	return lw_ana.ConfLoader(CONF_DIR)


conf_load_list = [
	("", {
		"env": "default", 
		"save_figures": False, 
		"show_figures": True
		}),
	("CDX1", {
		"env": "CDX1",
		"save_figures": False,
		"show_figures": False,
		}),
	("CDX2", {
		"env": "CDX2",
		"save_figures": False,
		"show_figures": True,
		"return_data": True,
		"numeric_param": 23.4e6,
		"numeric_expression": "2*pi*23e6", # evaluated later
		}),
	("CDX1/X2021-03-17", {
		"env": "X2021-03-17",
		"save_figures": True,
		"show_figures": True,
		}),
	("CDX1/X2021-03-18/0004", {
		"env": "X2021-03-18_0004",
		"save_figures": False,
		"show_figures": False,
		"return_data": True,
		"bootstrap_fitting": True,
		}),
]

@pytest.mark.parametrize("conf_path,target_conf", conf_load_list)
def test_load_confs(conf_loader, conf_path, target_conf):
	conf_loader.load_conf_from_tree(conf_path)
	assert conf_loader.loaded_conf == target_conf

