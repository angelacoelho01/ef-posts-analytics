all: data-collection data-export

data-collection:
	python.exe ./src/scraper/scraper.py

data-export: data-collection
	python.exe ./src/api/google_sheets.py

clean:
	rm -r out