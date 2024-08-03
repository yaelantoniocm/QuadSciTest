app/
│
├── backend/
│ ├── api.py
│ └── storage.py
│
├── helpers/
│ └── logger.py
│
├── log/
│ └── # Log files
├── data/
│ └── rockets/
│ └── # JSONs with rockets information
│ └── launches/
│ └── # JSONs with launches information
│ └── starlink/
│ └── # JSONs with Starlink satellite information
├── backup/
│ └── rockets/
│ └── # JSON with old rockets data
│ └── launches/
│ └── # JSON with old launches data
│ └── starlink/
│ └── # JSON with old Starlink satellite data
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
├── models.py # SQLAlchemy Models
├── setup_database.py # Script to configure the database
├── requirements.txt # Python dependency file
