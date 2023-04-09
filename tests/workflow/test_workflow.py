import os
import subprocess as sp
from unittest.mock import patch

import luigi
from workflow.workflow import execute_command, ExtractLoadAirportData, DbtDeps, DbtSeedAirports, DbtRunAirports, ScrapeLoadArrivalData, DbtSeedArrivals, DbtRunAnalysis

def test_extract_load_airport_data_output():
    task = ExtractLoadAirportData()
    assert isinstance(task.output(), luigi.LocalTarget)
    assert task.output().path == '0_ExtractLoadAirportData.output'

def test_dbt_deps_output():
    task = DbtDeps()
    assert isinstance(task.output(), luigi.LocalTarget)
    assert task.output().path == '1_DbtDeps.output'

def test_dbt_seed_airports_output():
    task = DbtSeedAirports()
    assert isinstance(task.output(), luigi.LocalTarget)
    assert task.output().path == '2_DbtSeedAirports.output'

def test_dbt_run_airports_output():
    task = DbtRunAirports()
    assert isinstance(task.output(), luigi.LocalTarget)
    assert task.output().path == '3_DbtRunAirports.output'

def test_scrape_load_arrival_data_output():
    task = ScrapeLoadArrivalData()
    assert isinstance(task.output(), luigi.LocalTarget)
    assert task.output().path == '4_ScrapeLoadArrivalData.output'

def test_dbt_seed_arrivals_output():
    task = DbtSeedArrivals()
    assert isinstance(task.output(), luigi.LocalTarget)
    assert task.output().path == '5_DbtSeedArrival.output'

def test_dbt_run_analysis_output():
    task = DbtRunAnalysis()
    assert isinstance(task.output(), luigi.LocalTarget)
    assert task.output().path == '6_DbtRunAnalysis.output'

@patch("workflow.workflow.execute_command", return_value="Mocked output")
def test_extract_load_airport_data_run(mocked_output):
    task = ExtractLoadAirportData()
    task.run()
    assert os.path.isfile(task.output().path)
    with open(task.output().path, "r") as f:
        assert f.read() == "Mocked output"
    os.remove(task.output().path)


