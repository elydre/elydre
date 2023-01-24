# automatisation de l'installation de earnapp avec docker par elydre
# ATTENTION: fonctionne uniquement sur ubuntu 20.04

if [ -d $HOME/earnapp ]; then
    echo $HOME"/earnapp Already exists"
else
    mkdir $HOME/earnapp
    echo $HOME"/earnapp create"
fi

DATA=$HOME"/earnapp/data"$1
NAME="earnapp"$1

echo
echo "data folder: "$DATA
echo "docker name: "$NAME
echo

if [ -d $DATA ]; then
    echo "ERROR 2 containers cannot have the same name"
else
    mkdir $DATA
    sudo docker run -d --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v $DATA:/etc/earnapp --name $NAME fazalfarhan01/earnapp
    sleep 10

    sudo docker exec -it $NAME earnapp stop
    sleep 2

    sudo docker exec -it $NAME earnapp start
    sleep 2

    sudo docker exec -it $NAME earnapp register

    echo "for stop run:"
    echo "sudo docker stop $NAME && sudo docker rm $NAME && rm -Rf $DATA"
fi