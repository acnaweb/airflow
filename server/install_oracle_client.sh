#!/bin/bash

export ORACLE_INSTANT_CLIENT=instantclient-basic-linux.x64-23.4.0.24.05
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/oracle/instantclient
export TNS_ADMIN=/opt/oracle/instantclient/network/admin

mkdir -p /opt/oracle
rm -f ${ORACLE_INSTANT_CLIENT}.zip
wget https://download.oracle.com/otn_software/linux/instantclient/2340000/${ORACLE_INSTANT_CLIENT}.zip
unzip -o ${ORACLE_INSTANT_CLIENT}.zip
mv instantclient*/ /opt/oracle/instantclient/

rm -f ${ORACLE_INSTANT_CLIENT}.zip
rm -rf instantclient*
rm -rf META-INF*