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

`/api/characters/` for a list of characters. Use the `born_near` parameter to find characters born on the same year as the character you give by id. You can also use the `years` parameter in conjunction with `born_near` to get a list of characters that are born within the number of years you provide relative to the character specified by id in `born_near`.

`/api/born_on/` for a list of years with a corresponding number of characters born on that given year.

`/api/born_on/<year>` for the amount of characters born on a given year.

`/api/houses/` for aggregate statistics on the amount of characters for a given house id.
