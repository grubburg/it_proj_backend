# Item route blueprint

## Routes
  - `/item/list/`
    - List all the items visible to the currest user
    - Request format:
      - GET request with bearer token header
    - Reponse format:
        ```json
        {
          'item1': <item1JSON>
        }
        ```
        
   - `/item/add/`
    - Add an item to the current family for the current user. 
    - Request format:
      ```
      {
        'description': <itemdescription>,
        'image': <firestore reference>,
        'name': <item name>,
        'tags': <tag array>,
        'visibility': <member visibility array>
      }
      ```
      - Response format:
        - Returns item JSON
