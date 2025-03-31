terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.21.0"
    }
  }

  required_version = ">= 1.3.0"
}

provider "azurerm" {
  features {}

  subscription_id = "ec7c5548-5f40-45b1-931a-915c2b940c87"
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

resource "azurerm_resource_group" "this" {
  name     = "rg_cezarovsky_payg"
  location = "westeurope"
}

resource "azurerm_databricks_workspace" "this" {
  name                        = "databricks_cezarovsky"
  resource_group_name         = azurerm_resource_group.this.name
  location                    = azurerm_resource_group.this.location
  sku                         = "standard"

  public_network_access_enabled = true
}

provider "databricks" {
  alias = "this"
  azure_workspace_resource_id = azurerm_databricks_workspace.this.id
  azure_client_id             = var.client_id
  azure_client_secret         = var.client_secret
  azure_tenant_id             = var.tenant_id
}

resource "databricks_cluster" "dev_cluster" {
  provider               = databricks.this
  cluster_name           = "cezarovsky-test-cluster"
  spark_version          = "13.3.x-scala2.12"
  node_type_id           = "Standard_DS3_v2"
  autotermination_minutes = 15
  num_workers            = 1

  custom_tags = {
    "Environment" = "dev"
    "Owner"   = "Cezar"
  }
  depends_on = [azurerm_databricks_workspace.this]
}

