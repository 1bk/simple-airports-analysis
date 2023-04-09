#!/usr/bin/env python3
"""
Created on 16 February 2020

@author: Lee Boon Keong
@github: 1bk
"""

import os
import subprocess as sp
import sys

import luigi


def execute_command(command):
    try:
        result = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE, text=True, shell=True, check=True)
        return result.stdout
    except sp.CalledProcessError as e:
        print(f'Error: Command exited with code {e.returncode}\n{e.stderr}', file=sys.stderr)
        sys.exit(e.returncode)


# A hacky way to allow rerunning of workflow.py
print('Clearing root directory of .output files.')
for file in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    if '.output' in file:
        try:
            os.unlink(file)
            print(f'\t >>> "{file}" deleted.')
        except Exception as e:
            print(f'\t >>> Could not delete "{file}"! Please manually delete.')

class CliTask(luigi.Task):
    cmd = None
    output_filename = None

    def output(self):
        return luigi.LocalTarget(self.output_filename)

    def run(self):
        if self.cmd:
            exe_cmd = execute_command(self.cmd)

            print('=' * 150)
            print(exe_cmd)
            print('=' * 150)

            with self.output().open('w') as outfile:
                outfile.write(exe_cmd)
        else:
            raise NotImplementedError("Please specify a command to run in the 'cmd' attribute.")


class ExtractLoadAirportData(CliTask):
    cmd = 'python ./extract_load/airports.py'
    output_filename = '0_ExtractLoadAirportData.output'

    def requires(self):
        return None


class DbtDeps(CliTask):
    cmd = 'cd ./dbt/ && dbt deps'
    output_filename = '1_DbtDeps.output'

    def requires(self):
        return ExtractLoadAirportData()


class DbtSeedAirports(CliTask):
    cmd = 'cd ./dbt/ && dbt seed --profiles-dir ./'
    output_filename = '2_DbtSeedAirports.output'

    def requires(self):
        return DbtDeps()


class DbtRunAirports(CliTask):
    cmd = 'cd ./dbt/ && dbt run --profiles-dir ./ --model tag:cleaned_airports'
    output_filename = '3_DbtRunAirports.output'

    def requires(self):
        return DbtSeedAirports()


class ScrapeLoadArrivalData(CliTask):
    cmd = 'python ./extract_load/arrivals.py'
    output_filename = '4_ScrapeLoadArrivalData.output'

    def requires(self):
        return DbtRunAirports()


class DbtSeedArrivals(CliTask):
    cmd = 'cd ./dbt/ && dbt seed --profiles-dir ./'
    output_filename = '5_DbtSeedArrival.output'

    def requires(self):
        return ScrapeLoadArrivalData()


class DbtRunAnalysis(CliTask):
    cmd = 'cd ./dbt/ && dbt run --profiles-dir ./ --exclude tag:cleaned_airports'
    output_filename = '6_DbtRunAnalysis.output'

    def requires(self):
        return DbtSeedArrivals()


if __name__ == '__main__':
    luigi.run()

