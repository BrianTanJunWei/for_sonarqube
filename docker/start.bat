@echo off
echo.
echo ***********************************************
echo ************* PROCESS STARTED *****************
echo ***********************************************
docker-compose down
docker-compose build
docker-compose up --detach --remove-orphans
echo.
echo ***********************************************
echo ************** PROCESS ENDED ********************
echo ***********************************************
