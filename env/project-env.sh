export MIHOST=$(hostname -s)

export PROJECTNAME=upload-datasets-2-zenodo-repository
export PROJECTFOLDER=proyectos/NeoMapas
export SCRIPTDIR=$HOME/$PROJECTFOLDER/$PROJECTNAME

case $MIHOST in
terra)
  export GISDATA=/opt/gisdata
  export GISDB=/opt/gisdb/ecosphere
  export WORKDIR=$HOME/tmp/$PROJECTNAME
  source $HOME/.profile
  ;;
roraima)
  export GISDATA=$HOME/gisdata
  export GISDB=$HOME/gisdb/ecosphere
  export WORKDIR=$HOME/tmp/$PROJECTNAME
  source $HOME/.profile
  ;;
*)
  echo "I DON'T KNOW WHERE I AM, please customize project-env.sh file"
  ;;
esac


# export ZIPDIR=$WORKDIR/zenodo_upload
# export XMLDIR=$WORKDIR/xml-output
# export GTIFDIR=$WORKDIR/output-rasters/geotiff
# export PFLDIR=$WORKDIR/output-rasters/geotiff-eck4
# export PNGDIR=$WORKDIR/output-rasters/profile-png
# export JSNDIR=$WORKDIR/output-vectors/json

# mkdir -p $ZIPDIR
# mkdir -p $XMLDIR
# mkdir -p $GTIFDIR
# mkdir -p $PNGDIR
# mkdir -p $PFLDIR
# mkdir -p $JSNDIR
