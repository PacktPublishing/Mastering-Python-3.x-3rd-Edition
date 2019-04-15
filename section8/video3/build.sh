pyinstaller --name=oware-client --add-binary oware/client/data/:oware/client/data/ --add-data LICENSE:. --add-data README.md:. --noconsole main.py
