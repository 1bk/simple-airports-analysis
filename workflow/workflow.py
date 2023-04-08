#!/usr/bin/env python3
"""
Created on 16 February 2020

@author: Lee Boon Keong
@github: 1bk
"""

import os
import subprocess as sp

import luigi

# A hacky way to allow rerunning of workflow.py
print('Clearing root directory of .output files.')
for file in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    if '.output' in file:
        try:
            os.unlink(file)
            print(f'\t >>> "{file}" deleted.')
        except Exception as e:
            print(f'\t >>> Could not delete "{file}"! Please manually delete.')


class ExtractLoadAirportData(luigi.Task):

    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget('0_ExtractLoadAirportData.output')

    def run(self):
        exe_cmd = sp.getoutput('python ./extract_load/airports.py')

        print('=' * 150)
        print(exe_cmd)
        print('=' * 150)

        with self.output().open('w') as outfile:
            outfile.write(exe_cmd)


class DbtDeps(luigi.Task):
    def requires(self):
        return ExtractLoadAirportData()

    def output(self):
        return luigi.LocalTarget('1_DbtDeps.output')

    def run(self):
        exe_cmd = sp.getoutput('cd ./dbt/ && dbt deps')

        print('=' * 150)
        print(exe_cmd)
        print('=' * 150)

        with self.output().open('w') as outfile:
            outfile.write(exe_cmd)


class DbtSeedAirports(luigi.Task):
    def requires(self):
        return DbtDeps()

    def output(self):
        return luigi.LocalTarget('2_DbtSeedAirports.output')

    def run(self):
        exe_cmd = sp.getoutput('cd ./dbt/ && dbt seed --profiles-dir ./')

        print('=' * 150)
        print(exe_cmd)
        print('=' * 150)

        with self.output().open('w') as outfile:
            outfile.write(exe_cmd)


class DbtRunAirports(luigi.Task):
    def requires(self):
        return DbtSeedAirports()

    def output(self):
        return luigi.LocalTarget('3_DbtRunAirports.output')

    def run(self):
        exe_cmd = sp.getoutput('cd ./dbt/ && dbt run --profiles-dir ./ --model tag:cleaned_airports')

        print('=' * 150)
        print(exe_cmd)
        print('=' * 150)

        with self.output().open('w') as outfile:
            outfile.write(exe_cmd)


class ScrapeLoadArrivalData(luigi.Task):

    def requires(self):
        return DbtRunAirports()

    def output(self):
        return luigi.LocalTarget('4_ScrapeLoadArrivalData.output')

    def run(self):

        print('=' * 150)
        print('Scraping and Loading Arrival Data - This may take some time...')
        exe_cmd = sp.getoutput('python ./extract_load/arrivals.py')
        print(exe_cmd)
        print('=' * 150)

        with self.output().open('w') as outfile:
            outfile.write(exe_cmd)


class DbtSeedArrivals(luigi.Task):
    def requires(self):
        return ScrapeLoadArrivalData()

    def output(self):
        return luigi.LocalTarget('5_DbtSeedArrival.output')

    def run(self):
        exe_cmd = sp.getoutput('cd ./dbt/ && dbt seed --profiles-dir ./')

        print('=' * 150)
        print(exe_cmd)
        print('=' * 150)

        with self.output().open('w') as outfile:
            outfile.write(exe_cmd)


class DbtRunAnalysis(luigi.Task):
    def requires(self):
        return DbtSeedArrivals()

    def output(self):
        return luigi.LocalTarget('6_DbtRunAnalysis.output')

    def run(self):
        exe_cmd = sp.getoutput('cd ./dbt/ && dbt run --profiles-dir ./ --exclude tag:cleaned_airports')

        print('=' * 150)
        print(exe_cmd)
        print('=' * 150)

        with self.output().open('w') as outfile:
            outfile.write(exe_cmd)


if __name__ == '__main__':
    luigi.run()
