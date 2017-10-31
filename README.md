# Installation Instructions
Create a PostgreSQL database instance and set the following env variables:

  • db_name

  • db_host

  • db_user

  • db_pass

**Run**

```
pip install -r requirements.txt
python seed.py
```

# Usage Instructions

**Notes**

  • BC years are written as negative integers. 500BC —> -500

**Run API**

```
python app.py
```

**Endpoints**

`/api/characters/<character>` for a list of characters.

`/api/born_on/` for a list of years with a corresponding number of characters born on that given year.

`/api/born_on/<year>` for the amount of characters born on a given year.
