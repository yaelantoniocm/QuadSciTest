app/
│
├── backend/
│ ├── application
│     └── api.py
│
│ ├── dashboard
│     └── dashboard.py
│
│ ├── launches_resources
│     └── launches_filter_sort.py
│
│ ├── rocket_resources
│     └── rocket_filter_sort.py
│
│ ├── spaceX
│     └── spaceX_data.py
│
│ ├── starlink_resources
│     └── starlink_filter_sort.py
│
│ └── storage.py
│
├── helpers/
│   └── query_filter_sort.py
│
├── log/
│   └── # Log files
│
├── data/
│ └── rockets/
│     └── # JSONs with rockets information
│ └── launches/
│     └── # JSONs with launches information
│ └── starlink/
│     └── # JSONs with Starlink satellite information
│
├── databases
│     └── models.py # SQLAlchemy Models
|
├── backup/
│ └── rockets/
│     └── # JSON with old rockets data
│ └── launches/
│     └── # JSON with old launches data
│ └── starlink/
│     └── # JSON with old Starlink satellite data
│
├── windows/
│ ├── setup_database.bat # Script to configure the database on Windows
│ └── install_dependencies.bat # Script to install dependencies on Windows
│
├── linux/
│ ├── setup_database.sh # Script to configure the database on Linux/Mac
│ └── install_dependencies.sh # Script to install dependencies on Linux/Mac
│
│
├── app.py # Flask Core App
├── .env # File with the database credentials
├── config.py # Database configuration file
├── setup_database.py # Script to configure the database
├── requirements.txt # Python dependency file