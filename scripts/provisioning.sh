#!/bin/bash

vagrantup --provider=azure

fab -f ./deployment/fabfile.py -H vagrant@bot-calendario-telegram-vm.southcentralus.cloudapp.azure.com InstallApp
fab -f ./deployment/fabfile.py -H vagrant@bot-calendario-telegram-vm.southcentralus.cloudapp.azure.com StartApp
