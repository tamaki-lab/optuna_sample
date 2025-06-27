# optuna_sample

- 公式ドキュメント<https://hydra.cc/docs/plugins/optuna_sweeper/>
- 勉強会<https://nitechict.sharepoint.com/:p:/r/sites/tamaki_lab_prv2/Shared%20Documents/General/11%E5%8B%89%E5%BC%B7%E4%BC%9A%E3%83%BB%E3%82%BC%E3%83%9F%E3%81%AE%E8%B3%87%E6%96%99/2025%E5%B9%B4%E5%BA%A6%E5%8B%89%E5%BC%B7%E4%BC%9A/20250704%E5%8B%89%E5%BC%B7%E4%BC%9A%EF%BC%9Ahydra_optuna.pptx?d=w0817860b2fd5436db64c9155617a233c&csf=1&web=1&e=VaMJd4>

## 実行手順

1. `python3 -m venv ~/.optuna_sample`
2. `source ~/.optuna_sample/bin/activate`
3. `pip install -r requirements.txt`
4. `python main.py -m`

## 結果の確認

- `python main.py -m`実行後に,`multirun`ディレクトリが自動作成され，そのなかに`optimization_results.yaml`が作成される．そのファイルに結果が出力されている．
以下がその例である．

`optimization_results.yaml`

```yaml
name: optuna
best_params:
  model.alpha: 0.01 # 最適なハイパーパラメータ
best_value: 0.2634885689894083 # 最小化(最大化)した変数の最も良かった解解

```

## 自分のコードで実装する手順

1. ライブラリのインストール

```
pip install hydra-core --upgrade
pip install hydra-optuna-sweeper --upgrade
```

2. ライブラリのimport

```python
import hydra
from omegaconf import DictConfig
```

3. `config.yaml`の`defaults:`に以下を追加

```yaml
  - override hydra/sweeper: optuna
  - override hydra/sweeper/sampler: tpe
```

4. `config.yaml`などに上書きしたいoptunaの設定を記述

```yaml
hydra:
  sweeper:
    _target_: hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper
    study_name: ridge_cv_optimization
    direction: minimize
    storage: null
    n_trials: 30
    n_jobs: 1
    params:
      model.alpha: "float(0.01, 10.0)"
    pruner:
      _target_: optuna.pruners.MedianPruner
      n_startup_trials: 5
      n_warmup_steps: 0
      interval_steps: 1
```

5. main関数の返り値を最小化(最大化)したい変数にする．

## 各設定の説明

```yaml
hydra:
  sweeper:
    sampler:
      _target_: optuna.samplers.TPESampler      # サンプラーの設定.デフォルトはTPE (Tree-structured Parzen Estimator)
      seed: null                                # 乱数シード
      consider_prior: true
      prior_weight: 1.0
      consider_magic_clip: true
      consider_endpoints: false
      n_startup_trials: 10
      n_ei_candidates: 24
      multivariate: false
      warn_independent_sampling: true
    _target_: hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper  # Optunaスイーパーの指定
    direction: minimize                         # 最適化の方向性（minimize: 最小化, maximize: 最大化）
    storage: null
    study_name: ridge_cv_optimization           # 最適化のログ名
    n_trials: 30                                # 最適化の試行回数
    n_jobs: 1                                   # 並列実行数（1は逐次実行）
    search_space: null
    params:
      model.alpha: float(0.01, 10.0)            # 最適化するパラメータ（0.01〜10.0の範囲でalpha値を探索）
    custom_search_space: null
```

## 以下AI生成文

### 主要な設定項目の詳細説明

#### Sampler（サンプラー）設定

- **_target_**: `optuna.samplers.TPESampler` - 使用するサンプラーのクラスを指定
- **seed**: `null` - 乱数シードの設定。`null`の場合は毎回異なる結果、数値を指定すると再現可能な結果
- **consider_prior**: `true` - 事前分布を考慮するかどうか。Trueの場合、より妥当なパラメータ範囲に重みを与える
- **prior_weight**: `1.0` - 事前分布の重み。値が大きいほど事前分布の影響が強くなる
- **consider_magic_clip**: `true` - Magic Clip手法の使用。極端な値を避けてより安定した最適化を行う
- **consider_endpoints**: `false` - パラメータ範囲の端点を特別に考慮するかどうか
- **n_startup_trials**: `10` - 初期のランダムサンプリング回数。この回数はTPEではなくランダムに探索
- **n_ei_candidates**: `24` - 期待改善(Expected Improvement)の候補数。内部的な最適化で使用
- **multivariate**: `false` - 多変量TPEの使用。Trueの場合、パラメータ間の相関を考慮
- **warn_independent_sampling**: `true` - 独立サンプリングの警告表示。パフォーマンス低下時に警告

#### Sweeper（スイーパー）設定

- **_target_**: `hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper` - Optunaスイーパーのクラス指定
- **direction**: `minimize` - 最適化の方向性
  - `minimize`: 目的関数の値を最小化（MSE、損失関数など）
  - `maximize`: 目的関数の値を最大化（精度、F1スコアなど）
- **storage**: `null` - 結果の保存先データベース
  - `null`: メモリ内のみ（一時的）
  - `"sqlite:///study.db"`: SQLiteファイルに保存
  - `"mysql://user:pass@host/db"`: MySQLデータベース
- **study_name**: `ridge_cv_optimization` - 最適化研究の名前（識別子として使用）
- **n_trials**: `30` - 最適化の試行回数。多いほど良い解が見つかる可能性が高い
- **n_jobs**: `1` - 並列実行数
  - `1`: 逐次実行
  - `2以上`: 指定した数で並列実行
  - `-1`: 利用可能なCPUコア数すべてを使用
- **search_space**: `null` - カスタム検索空間の設定（通常はnullで自動設定）
- **custom_search_space**: `null` - 追加のカスタム検索空間設定

#### パラメータ設定

- **params**: 最適化するハイパーパラメータを定義
  - `float(min, max)`: 浮動小数点数の範囲指定
  - `int(min, max)`: 整数の範囲指定
  - `choice([値1, 値2, ...])`: 離散値の選択
  - `log_uniform(low, high)`: 対数スケールの浮動小数点数
  - `categorical([値1, 値2, ...])`: カテゴリ変数の選択

### 各設定項目の行ごとの説明

以下は設定ファイルの各行について詳細に説明したものです：

```yaml
hydra:                                          # Hydraフレームワークの設定開始
  sweeper:                                      # スイーパー（最適化アルゴリズム）の設定
    sampler:                                    # サンプラー（パラメータ選択手法）の設定開始
      _target_: optuna.samplers.TPESampler      # TPEサンプラーのクラスを指定
      seed: null                                # 乱数シード（null=毎回異なる結果）
      consider_prior: true                      # 事前分布を考慮（推奨範囲に重み付け）
      prior_weight: 1.0                         # 事前分布の影響度（0.0〜1.0）
      consider_magic_clip: true                 # Magic Clip手法で極端値を抑制
      consider_endpoints: false                 # 範囲の端点を特別扱いしない
      n_startup_trials: 10                      # 初期ランダム探索の試行回数
      n_ei_candidates: 24                       # 期待改善候補数（内部最適化用）
      multivariate: false                       # 多変量TPE（パラメータ相関考慮）を無効
      warn_independent_sampling: true           # 独立サンプリング警告を表示
    _target_: hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper  # Optunaスイーパークラス
    direction: minimize                         # 最適化方向（minimize/maximize）
    storage: null                               # 結果保存先（null=メモリのみ）
    study_name: ridge_cv_optimization           # 研究名（識別子）
    n_trials: 30                                # 総試行回数
    n_jobs: 1                                   # 並列実行数（1=逐次実行）
    search_space: null                          # カスタム検索空間（null=自動設定）
    params:                                     # 最適化対象パラメータの定義開始
      model.alpha: float(0.01, 10.0)            # alphaパラメータ（0.01〜10.0の範囲）
    custom_search_space: null                   # 追加検索空間設定（通常null）
```
