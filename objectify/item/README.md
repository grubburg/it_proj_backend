# Item route blueprint

##Routes
  - `/item/list/`
    - List all the items visible to the currest user
    - Request format:
      - GET request with bearer token header
    - Reponse format:
        ```json
        {
          'item1': '<item1JSON>'
        }
        ```
