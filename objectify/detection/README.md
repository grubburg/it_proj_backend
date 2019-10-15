### Objectify object detection api route.

## Technology:

- Tensorflow 

## Routes:

- Detection
  `/detection/`
  
  - Request format:
  
    ```json
    {
      'image': '<firestore-ref>'
    }
    ```
  
  - Returns:
    ```json
    {
      'tags': '[<tag-array>]'
    }
    ```
  
