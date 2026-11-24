# Remote state in Azure Storage. Values are supplied at init time:
#   terraform init \
#     -backend-config="resource_group_name=<tfstate-rg>" \
#     -backend-config="storage_account_name=<tfstate-account>" \
#     -backend-config="container_name=tfstate" \
#     -backend-config="key=incidentflow.tfstate"
terraform {
  backend "azurerm" {
    use_oidc         = true
    use_azuread_auth = true
  }
}
