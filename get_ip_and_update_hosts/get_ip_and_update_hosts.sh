#!/bin/bash

# Caminho do arquivo de log
service_file=$SERVICE_LOG_PATH

# Nome do serviço para o qual você está monitorando o IP
issuer=$SERVICE_ISSUER

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
    service_log_ip=$(get_ip_on_logs "$service_file")

    # Verificando se os ips já existem no /etc/hosts
    verify_if_already_exist "$issuer" "$service_log_ip"

    # Obter o IP atual do serviço no /etc/hosts
    service_on_hosts=$(grep -oP "(?<=\b$issuer\b[[:space:]]+)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" $hosts_file)

    # Mudar arquivo /etc/hosts se o ip tiver mudado
    verify_ip_alteration "$service_log_ip" "$service_on_hosts" "$issuer"

    # Aguardar o intervalo de verificação antes de verificar novamente
    sleep $interval
done
