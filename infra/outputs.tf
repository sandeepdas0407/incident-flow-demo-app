output "resource_group" {
  value = azurerm_resource_group.rg.name
}

output "vm_name" {
  value = azurerm_linux_virtual_machine.vm.name
}

output "vm_size" {
  value = azurerm_linux_virtual_machine.vm.size
}

output "app_url" {
  value = "http://${azurerm_public_ip.pip.fqdn}"
}
