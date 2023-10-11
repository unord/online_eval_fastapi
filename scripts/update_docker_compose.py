import yaml

service_name = "worker"
docker_image_name = "robounord/online_eval_fastapi"

def update_docker_compose(version: str) -> int:
    with open("docker-compose.yml", 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    if 'services' in data:
        if service_name in data['services']:
            print(f"Updating image from {data['services'][service_name]['image']} to {docker_image_name}:{version}")
            data['services'][service_name]['image'] = f"{docker_image_name}:{version}"
        else:
            print(f"Service '{service_name}' not found in docker-compose.yml.")
            return 1  # Error status
    else:
        print("Key 'services' not found in docker-compose.yml.")
        return 1  # Error status

    with open("docker-compose.yml", 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    return 0  # Success status


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python update_docker_compose.py <new_version>")
        sys.exit(1)

    new_version = sys.argv[1]
    sys.exit(update_docker_compose(new_version))  # Exit with the status returned by the function
