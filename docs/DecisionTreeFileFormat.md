# Format Layout for writing Decision Trees in File

## Metadata
- `NFeatures`
  - Number of features
  - Type: int (32-bit)
- `NClasses`
  - Number of classes
  - Type: int (32-bit)
- `NodeCount`
  - Description:
  - Type: int (32-bit)
- `MaxDepth`
  - Description:
  - Type: int (32-bit)
- `Classes`
  - Description:
  - Type: int* (NClasses * 32-bit)
- `Feature Names Sizes`
  - Description:
  - Type: int* (NFeatures * 32-bit)
- `Feature Names`
  - Description:
  - Type: char** (sum(Feature Names Sizes) * 8-bit)

## Data
- `Left`
  - Description:
  - Type: int* (NodeCount * 32-bit)
- `Right`
  - Description:
  - Type: int* (NodeCount * 32-bit)
- `Threshold`
  - Description:
  - Type: double* (NodeCount * 64-bit)
- `Feature`
  - Description:
  - Type: int* (NodeCount * 32-bit)
- `Values`
  - Description:
  - Type: double** (NodeCount * NClasses * 64-bit)