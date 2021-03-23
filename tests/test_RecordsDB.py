import pytest
import os

import LabWeaver_analysis as lw_ana


DB_DIR = os.path.abspath("tests/assets/db")


@pytest.fixture
def existing_records_db():
	db_path = os.path.join(DB_DIR, "records_existing.db")
	return lw_ana.RecordsDB(db_path)


def test_fetch(existing_records_db):
	fetched_record = existing_records_db.filter_records(
								("experiment = 'X2021-03-17'", 
								 "meas_id = '0001'"))[0]
	assert fetched_record == {"experiment": "X2021-03-17", 
							  "meas_id": "0001", 
							  "cooldown": "CDX1", 
							  "meas_type": "Qubit Rabi amplitude"}


def test_fetch_multiple(existing_records_db):
	fetched_records = existing_records_db.filter_records(
											("cooldown = 'CDX1'",))
	assert fetched_records == [{"experiment": "X2021-03-17", 
							    "meas_id": "0001", 
							    "cooldown": "CDX1", 
							    "meas_type": "Qubit Rabi amplitude"},
							   {"experiment": "X2021-03-17", 
							    "meas_id": "0002", 
							    "cooldown": "CDX1", 
							    "meas_type": "Qubit Ramsey"}]


@pytest.fixture
def new_records_db(scope="function"):
	db_path = os.path.join(DB_DIR, "records_temp.db")
	## Return as yield to allow for teardown/destructor
	yield lw_ana.RecordsDB(db_path)
	## Teardown - delete temp file
	os.remove(db_path)


@pytest.fixture
def new_single_record_db(new_records_db, scope="function"):
	## Add a new record to the database
	new_record = {"experiment": "X2021-03-17", 
				  "meas_id": "0001", 
				  "cooldown": "CDX1", 
				  "meas_type": "Qubit Rabi amplitude"}
	new_records_db.add_record(new_record)
	yield new_records_db


def test_create_assign_fetch(new_single_record_db):
	## Fetch the record by uids and compare
	fetched_record = new_single_record_db.filter_records(
								("experiment = 'X2021-03-17'", 
								 "meas_id = '0001'"))[0]
	assert fetched_record == {"experiment": "X2021-03-17", 
							  "meas_id": "0001", 
							  "cooldown": "CDX1", 
							  "meas_type": "Qubit Rabi amplitude"}


def test_create_assign_delete(new_single_record_db):
	## Delete record
	new_single_record_db.delete_record(("X2021-03-17", "0001"))
	## Ensure no records are left
	assert new_single_record_db.head() == []

