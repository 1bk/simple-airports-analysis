.PHONY: clean

clean:
	rm -rfv extract_load/output
	rm -fv dbt/data/*.csv

