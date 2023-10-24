#!/bin/bash

# Caminho do arquivo de log
OTP_FILE=$OTP_LOG_PATH

CONNECT_FILE=$CONNECT_LOG_PATH

HUB_FILE=$HUB_LOG_PATH

RISK_FILE=$RISK_LOG_PATH


# Nome do serviço para o qual você está monitorando o IP
connect_service="connect.appliance.local"
hub_service="hub.appliance.local"
risk_service="risk.appliance.local"
otp_service="otp.appliance.local"


# Caminho do arquivo hosts
hosts_file="/etc/hosts"


# Intervalo de verificação em segundos (exemplo: 300 segundos = 5 minutos)
interval=$OPERATION_INTERVAL


# Função para extrair o IP do último registro do arquivo de log
get_ip_on_log() {
    tail -n 1 $1 | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"
}


# Função para adicionar ou atualizar o IP no arquivo /etc/hosts
change_hosts() {
    new_ip=$1
    sed -i "/$2/d" $hosts_file
    echo "$new_ip 	$2" >> $hosts_file
}


verify_ip_alteration() {
    # Verificar se o IP mudou
    if [ "$1" != "$2" ]; then
        echo "IP do serviço $3 mudou de $2 para $1"

        # Atualizar o arquivo /etc/hosts
        change_hosts "$1" "$3"
    fi

}



# Verificar se o arquivo hosts contém o serviço
verify_if_already_exist() {
    	if grep -q "$1" "$hosts_file"; then
	    echo "O serviço $1 já está no arquivo /etc/hosts."
	else
            # Se não estiver no arquivo, adicione o IP do último registro do log
    	    initial_ip=$2
    	    echo "Adicionando $1 ao /etc/hosts com IP inicial: $initial_ip"
    	    echo "$initial_ip    $1" >> $hosts_file
	fi
}


# Loop infinito para monitorar o log
while true
do


    # Obter o IP do último registro do log
    otp_log_ip=$(get_ip_on_logs "$OTP_FILE")
    connect_log_ip=$(get_ip_on_logs "$CONNECT_FILE")
    risk_log_ip=$(get_ip_on_logs "$RISK_FILE")
    hub_log_ip=$(get_ip_on_logs "$HUB_FILE")

    # Verificando se os ips já existem no /etc/hosts
    verify_if_already_exist "$connect_service" "$connect_log_ip"
    verify_if_already_exist "$hub_service" "$hub_log_ip"
    verify_if_already_exist "$risk_service" "$risk_log_ip"
    verify_if_already_exist "$otp_service" "$otp_log_ip"

    # Obter o IP atual do serviço no /etc/hosts
    otp_on_hosts=$(grep -oP "(?<=\b$otp_service\b[[:space:]]+)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" $hosts_file)
    connect_on_hosts=$(grep -oP "(?<=\b$connect_service\b[[:space:]]+)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" $hosts_file)
    hub_on_hosts=$(grep -oP "(?<=\b$hub_service\b[[:space:]]+)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" $hosts_file)
    risk_on_hosts=$(grep -oP "(?<=\b$risk_service\b[[:space:]]+)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" $hosts_file)

    # Mudar arquivo /etc/hosts se o ip tiver mudado
    verify_ip_alteration "$connect_log_ip" "$connect_on_hosts" "$connect_service"
    verify_ip_alteration "$hub_log_ip" "$hub_on_hosts" "$hub_service"
    verify_ip_alteration "$risk_log_ip" "$risk_on_hosts" "$risk_service"
    verify_ip_alteration "$otp_log_ip" "$otp_on_hosts" "$otp_service"

    # Aguardar o intervalo de verificação antes de verificar novamente
    sleep $interval
done
