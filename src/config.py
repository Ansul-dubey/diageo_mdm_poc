# Configuration file for schema definitions and file paths

FRB_SCHEMA_SOURCE = {
    "IBV_FRB_L0_CategoryI": "string",
    "IBV_FRB_L1_CategoryII": "string",
    "IBV_FRB_L2_CategoryIII": "string",
    "IBV_FRB_L3_CategoryIV": "string",
    "IBV_FRBPHL4_BrandFamily": "string",
    "IBV_FRBPHL5_BrandVariantI": "string",
    "IBV_FRBPHL6_BrandVariantII": "string",
    "IBV_FRBPHL7Description": "string",
    "IBV_SAPPHL5Description": "string",
    "Item_SAPPHL6Description": "string",
    "SKU_SAPPHL7Description": "string",
    "IBV_FRB_ExternalBrandReportingCategory": "string",
    "IBV_FRB_GlobalBrandReportingCategory": "string",
    "IBV_FRB_GlobalBrandPosition": "string",
    "IBV_FRB_Reserve": "string",
    "sum(SalesVolumeEquivalentUnit)": "float64",
}

MARKETING_SCHEMA_SOURCE = {
    "Brand_BrandOwner": "string",
    "IBV_FRB_L1_CategoryII": "string",
    "IBV_FRB_L2_CategoryIII": "string",
    "IBV_FRB_L3_CategoryIV": "string",
    "PUConsumerBrandName": "string",
    "Brand_SAPPHL3Description": "string",
    "IBV_SAPPHL5Description": "string",
    "Item_SAPPHL6Description": "string",
    "sum(MetricVolume)": "float64",
}

# File paths
INPUT_PATH_FILE_FRB = "data/input/input_frbv2.csv"
INPUT_PATH_FILE_MARKETING = "data/input/marketing_data.csv"

OUTPUT_FILE_PATH = "data/output/output.csv"

