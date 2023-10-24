#!/bin/bash

# Nome de usuário da outra máquina
USER=$MACHINE_USER

# Endereço IP da outra máquina
OUTHER_MACHINE_IP=$MACHINE_IP

# Intervalo em minutos para enviar o IP
INTERVAL_MINUTES=$INTERVAL

# Nome do serviço colocado no arquivo de log
SERVICE_NAME=$SERVICE

while true; do
    # Obter o endereço IP atual
    CURRENT_IP=$(curl -s ifconfig.me)

    # Enviar o endereço IP para a outra máquina
    ssh $USER@$OUTHER_MACHINE_IP "echo $CURRENT_IP >> $SERVICE_NAME.txt"

    # Aguardar o próximo intervalo
    sleep $(($INTERVAL_MINUTES * 60))
done
