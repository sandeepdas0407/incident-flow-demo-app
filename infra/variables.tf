variable "prefix" {
  type    = string
  default = "incidentflow"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "vm_size" {
  type        = string
  description = "Azure VM SKU. Must stay within the agent's allowlist."
  validation {
    condition     = contains(["Standard_B1s", "Standard_B1ms", "Standard_B2s", "Standard_B2ms"], var.vm_size)
    error_message = "vm_size must be one of Standard_B1s, Standard_B1ms, Standard_B2s, Standard_B2ms."
  }
}

variable "admin_username" {
  type    = string
  default = "azureuser"
}

variable "admin_ssh_public_key" {
  type        = string
  description = "SSH public key for the VM admin user (set via TF_VAR_admin_ssh_public_key)."
}

variable "ssh_source_cidr" {
  type        = string
  description = "CIDR allowed to SSH in. Restrict to your IP."
  default     = "0.0.0.0/32"
}

variable "dns_label" {
  type        = string
  description = "Globally unique DNS label -> <label>.<region>.cloudapp.azure.com"
}

variable "app_repo_url" {
  type        = string
  description = "Public HTTPS git URL of this repository (cloned onto the VM)."
}

variable "tags" {
  type = map(string)
  default = {
    project = "incident-flow-demo"
  }
}
