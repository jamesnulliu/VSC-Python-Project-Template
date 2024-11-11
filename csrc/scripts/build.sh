# Env Variables: CC, CXX, NVCC_CCBIN

# [TODO]
# |- Only keep the required paths in PATH
prune_env_path() {
    IFS=':' read -r -a paths <<< "$PATH"
    new_path=""
    # Remove duplicates from PATH
    unique_paths=()
    for path in "${paths[@]}"; do
        if [[ ! " ${unique_paths[@]} " =~ " ${path} " ]]; then
            if [ -n "$new_path" ]; then
                new_path+=":"
            fi
            new_path+="$path"
            unique_paths+=("$path")
        fi
    done
    # Update PATH
    PATH=$new_path
}

prune_env_path

SOURCE_DIR=.
BUILD_DIR=./build
BUILD_TYPE=Release
CXX_STANDARD=20
CUDA_STANDARD=20

while [[ $# -gt 0 ]]; do
    case $1 in
        -S|--source-dir)
            SOURCE_DIR=$2; shift ;;
        -B|--build-dir)
            BUILD_DIR=$2; shift ;;
        Release|Debug)
            BUILD_TYPE=$1 ;;
        --stdc++=*)
            CXX_STANDARD="${1#*=}" ;;
        --stdcuda=*)
            CUDA_STANDARD="${1#*=}" ;;
        *)
            # [TODO] Add detailed help message
            echo "Unknown argument: $1"; exit 1 ;;
    esac
    shift
done

cmake -G Ninja -S $SOURCE_DIR -B $BUILD_DIR  \
    -DCMAKE_BUILD_TYPE=$BUILD_TYPE \
    -DCMAKE_CXX_STANDARD=$CXX_STANDARD \
    -DCMAKE_CUDA_STANDARD=$CUDA_STANDARD 

cmake --build ./build -j $(nproc)