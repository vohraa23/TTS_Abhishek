export RUNPOD_NETWORK_VOLUME_PATH="/workspace"

if [ -n "$RUNPOD_ENDPOINT_ID" ]; then
    export RUNPOD_NETWORK_VOLUME_PATH="/runpod-volume"
fi

export HF_HOME="$RUNPOD_NETWORK_VOLUME_PATH/hf-files"
export XDG_CACHE_HOME="$RUNPOD_NETWORK_VOLUME_PATH/cache"
export PATH="$RUNPOD_NETWORK_VOLUME_PATH/venv/bin:$PATH"

python $RUNPOD_NETWORK_VOLUME_PATH/handler.py
