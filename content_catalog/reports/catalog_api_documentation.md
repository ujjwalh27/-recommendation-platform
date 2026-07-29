# Content Catalog REST API Documentation

Base Path: `/api/catalog`

## Endpoints

### 1. Publish Processed Video
- **Method**: `POST`
- **Path**: `/api/catalog/publish`
- **Request Body**:
  ```json
  {
    "video_id": "daiv_s2_01",
    "video_file_path": "datasets/raw/msrvtt/daiv_s2_01.mp4",
    "pipeline_result": { ... }
  }
  ```
- **Response**:
  ```json
  {
    "video_id": "daiv_s2_01",
    "publication_status": "PUBLISHED",
    "publication_action": "CREATE",
    "duplicate_detected": false,
    "metadata_version": 1,
    "duration_ms": 12.4
  }
  ```

### 2. Retrieve Catalog Entry
- **Method**: `GET`
- **Path**: `/api/catalog/{video_id}`
- **Response**: Detailed `CatalogRecord` object.

### 3. Reprocess Video
- **Method**: `PUT`
- **Path**: `/api/catalog/reprocess/{video_id}`
- **Response**: Reprocessing status (`PUBLISHED` or `SKIPPED`).

### 4. View Processing & Publication Status
- **Method**: `GET`
- **Path**: `/api/catalog/status/{video_id}`

### 5. Retrieve Processing Audit History
- **Method**: `GET`
- **Path**: `/api/catalog/audit/{video_id}`
