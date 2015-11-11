#!/bin/sh


#  build_id is inherited from vRCS
DOWNLOAD_PATH=/tmp/deployment/${build_id}

echo "wget "$TargzFile" --no-check-certificate --directory-prefix="$DOWNLOAD_PATH

wget $TargzFile --no-check-certificate --directory-prefix=$DOWNLOAD_PATH

BASEDIR=$(dirname $0)
echo $BASEDIR

echo "=====clean up from last deployment======-"
rm -rf $HTTP_DOC/*

echo "=====install new artifact======"
cd $DOWNLOAD_PATH
tar -zxvf *${build_id}.tar.gz -C /tmp

mv /tmp/CS-Demo/www/* ${HTTP_DOC}

chmod -R 755 ${HTTP_DOC}/*

echo "====restarting apache====="
service httpd restart