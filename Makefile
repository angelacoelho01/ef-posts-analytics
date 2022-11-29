all: data-collection data-export

data-collection:
	python.exe ./src/main.py

data-export: data-collection
	python.exe ./src/api/google_sheets.py

clean:
	rm -r out