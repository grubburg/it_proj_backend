# CGHMN Item Storage API
Flask back end for the Compu-Global-Hyper-Mega-Net object storage application. 

## Technology Stack
Server: Flask
Database: Firestore

## Server application structure:

```
app.py
|
|--user
|   |---user_routes.py
|       
|       Routes related to user management.
|
|--family
|   |---family_routes.py
|
|       Routes related to family management.
|
|--items
|   |---item_routes.py
|
|       Routes related to item management. 
|
|
|---schemas
|     |   Python class definitions for firebase schama
|     |
|     |---user.py
|     |---family.py
      |---item.py
```

