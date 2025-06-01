"""main."""
import hydra
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    print(f"running with config: {cfg}")

if __name__ == "__main__":
    main()
