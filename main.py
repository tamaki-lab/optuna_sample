# my_app.py

import hydra
from omegaconf import DictConfig, OmegaConf
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_regression # ダミーデータ生成用
import time

# ダミーデータの生成関数
def generate_dummy_data(n_samples: int, n_features: int, noise: float, random_state: int):
    """簡単な回帰用のダミーデータを生成する"""
    X, y = make_regression(
        n_samples=n_samples,
        n_features=n_features,
        noise=noise,
        random_state=random_state
    )
    return X, y

# 評価対象の目的関数
@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig) -> float:
    """
    目的関数。Hydraによって呼び出され、クロスバリデーションによる評価スコアを返す。
    cfgには、config.yamlの内容とOptunaがサンプリングしたハイパーパラメータが含まれる。
    """
    print("Current configuration:")
    print(OmegaConf.to_yaml(cfg)) # 現在の試行の設定を出力

    # 1. データの準備
    X, y = generate_dummy_data(
        n_samples=cfg.data.n_samples,
        n_features=cfg.data.n_features,
        noise=cfg.data.noise,
        random_state=cfg.data.random_state_data
    )

    # 2. クロスバリデーションの設定
    kf = KFold(
        n_splits=cfg.cv.n_splits,
        shuffle=cfg.cv.shuffle,
        random_state=cfg.cv.random_state_cv
    )

    # 3. モデルの準備 (Optunaがサンプリングしたハイパーパラメータを使用)
    # cfg.model.alpha のようにアクセス
    try:
        model_alpha = cfg.model.alpha
    except Exception as e:
        print(f"Error accessing model.alpha: {e}. Using default if available or failing.")
        raise e


    fold_mses = [] # 各フォールドのMSEを格納するリスト

    print(f"\nStarting Cross-Validation with alpha={model_alpha:.4f}")
    start_time_cv = time.time()

    for fold_idx, (train_index, val_index) in enumerate(kf.split(X)):
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        # モデルの初期化と学習
        model = Ridge(alpha=model_alpha)
        model.fit(X_train, y_train)

        # 検証データで予測と評価
        y_pred = model.predict(X_val)
        mse = mean_squared_error(y_val, y_pred)
        fold_mses.append(mse)
        print(f"  Fold {fold_idx+1}/{cfg.cv.n_splits}: MSE = {mse:.4f}")

    # クロスバリデーションの平均MSEを計算
    avg_mse = np.mean(fold_mses)
    end_time_cv = time.time()
    cv_duration = end_time_cv - start_time_cv

    print(f"Finished Cross-Validation for alpha={model_alpha:.4f}")
    print(f"  Average MSE: {avg_mse:.4f}")
    print(f"  CV Duration: {cv_duration:.2f} seconds\n")

    # Optunaはこの値を最小化/最大化する
    return avg_mse

if __name__ == "__main__":
    main()
