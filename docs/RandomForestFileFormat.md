# Format Layout for writing Random Forests in File

## Metadata
- `NFeatures`
  - Number of features
  - Type: int (32-bit)
- `NClasses`
  - Number of classes
  - Type: int (32-bit)
- `NOutputs`
  - Description:
  - Type: int (32-bit)
- `NEstimators`
  - Description:
  - Type: int (32-bit)
- `Estimator Sizes`
  - Description:
  - Type: int* (NEstimators * 32-bit)
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
Each `RandomForest` is an ensemble of multiple `DecisionTrees`. In this case, each tree (`Estimator`) is written in the file, after metadata, with a layout as in [DecisionTreeFileFormat.md](./DecisionTreeFileFormat.md). 

**NOTE** each tree does not store any information about the feature names. This information is kept only once in the metadata of the `RandomForest`.