.PHONY: all fetch analyze clean
all: analyze
fetch:
	@echo "--- Fetching data ---"
	bash	./fetch_metars.sh
analyze:fetch
	@echo "--- Analyzing data ---"
	bash	./analyze_data.sh
	@echo "--- Pipeline complete ---"
clean:
	@echo "--- Cleaning up ---"
	rm -rf weather_report.csv
	rm -rf raw_metars
