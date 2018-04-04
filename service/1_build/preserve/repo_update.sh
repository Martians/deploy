
sudo apt-get install createrepo -y

REPO=$(cd "$(dirname "$0")"; pwd)
createrepo --update $REPO
# createrepo $REPO

