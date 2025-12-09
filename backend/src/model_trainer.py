"""
Módulo de treinamento do modelo de Machine Learning
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
from datetime import datetime
import logging

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Classe para treinamento do modelo de regressão"""
    
    def __init__(self, model_dir: str = "models"):
        """
        Inicializa o treinador de modelo
        
        Args:
            model_dir: Diretório para salvar modelos
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.metrics = {}
        
    def prepare_data(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.15, val_size: float = 0.15):
        """
        Prepara dados para treinamento (70% treino, 15% validação, 15% teste)
        
        Args:
            X: Features
            y: Target
            test_size: Proporção do conjunto de teste
            val_size: Proporção do conjunto de validação (do restante após teste)
        """
        logger.info("Preparando dados para treinamento...")
        
        # Primeira divisão: treino+val (85%) e teste (15%)
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Segunda divisão: treino (70%) e validação (15%)
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=42
        )
        
        logger.info(f"Treino: {len(X_train)}, Validação: {len(X_val)}, Teste: {len(X_test)}")
        
        # Salvar nomes das features
        self.feature_names = list(X_train.columns)
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        return (X_train_scaled, X_val_scaled, X_test_scaled, 
                y_train, y_val, y_test)
    
    def train_xgboost(self, X_train, y_train, X_val, y_val):
        """
        Treina modelo XGBoost
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
            X_val: Features de validação
            y_val: Target de validação
        """
        logger.info("Treinando modelo XGBoost...")
        
        # Parâmetros do modelo
        params = {
            'objective': 'reg:squarederror',
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'n_jobs': -1
        }
        
        self.model = xgb.XGBRegressor(**params)
        
        # Treinar modelo (compatível com diferentes versões do XGBoost)
        # Em versões mais recentes, early_stopping_rounds deve estar no construtor
        # Em versões antigas, pode estar no fit ou não existir
        try:
            # Versão mais recente: early_stopping_rounds no construtor
            self.model = xgb.XGBRegressor(**params, early_stopping_rounds=10)
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                verbose=False
            )
        except TypeError:
            # Versão intermediária: early_stopping_rounds no fit
            try:
                self.model = xgb.XGBRegressor(**params)
                self.model.fit(
                    X_train, y_train,
                    eval_set=[(X_val, y_val)],
                    early_stopping_rounds=10,
                    verbose=False
                )
            except TypeError:
                # Versão antiga: sem early stopping
                self.model = xgb.XGBRegressor(**params)
                self.model.fit(X_train, y_train, verbose=False)
        
        logger.info("Modelo treinado com sucesso!")
        return self.model
    
    def evaluate(self, X_test, y_test):
        """
        Avalia o modelo
        
        Args:
            X_test: Features de teste
            y_test: Target de teste
        """
        logger.info("Avaliando modelo...")
        
        y_pred = self.model.predict(X_test)
        
        # Calcular métricas
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # MAE como porcentagem da média
        mae_pct = (mae / y_test.mean()) * 100
        
        self.metrics = {
            'MAE': float(mae),
            'RMSE': float(rmse),
            'R2': float(r2),
            'MAE_PCT': float(mae_pct),
            'mean_actual': float(y_test.mean()),
            'mean_predicted': float(y_pred.mean())
        }
        
        logger.info(f"MAE: R$ {mae:.2f} ({mae_pct:.2f}%)")
        logger.info(f"RMSE: R$ {rmse:.2f}")
        logger.info(f"R²: {r2:.4f}")
        
        return self.metrics
    
    def cross_validate(self, X, y, cv: int = 5):
        """
        Validação cruzada
        
        Args:
            X: Features
            y: Target
            cv: Número de folds
        """
        logger.info(f"Executando validação cruzada (k={cv})...")
        
        # Criar modelo sem early stopping para validação cruzada
        # (early stopping requer eval_set que não está disponível em CV)
        params = {
            'objective': 'reg:squarederror',
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'n_jobs': -1
        }
        
        cv_model = xgb.XGBRegressor(**params)
        
        scores = cross_val_score(
            cv_model, X, y, 
            cv=cv, 
            scoring='neg_mean_absolute_error',
            n_jobs=-1
        )
        
        cv_mae = -scores.mean()
        cv_std = scores.std()
        
        logger.info(f"CV MAE: R$ {cv_mae:.2f} (+/- {cv_std:.2f})")
        
        return cv_mae, cv_std
    
    def get_feature_importance(self, top_n: int = 10):
        """Retorna importância das features"""
        if self.model is None:
            raise ValueError("Modelo não treinado")
        
        importance = self.model.feature_importances_
        feature_importance = list(zip(self.feature_names, importance))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        # Converter para tipos Python nativos para serialização JSON
        result = [(name, float(imp)) for name, imp in feature_importance[:top_n]]
        return result
    
    def save_model(self, version: str = None):
        """
        Salva o modelo treinado
        
        Args:
            version: Versão do modelo (se None, usa timestamp)
        """
        if self.model is None:
            raise ValueError("Modelo não treinado")
        
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        model_path = self.model_dir / f"model_{version}.pkl"
        scaler_path = self.model_dir / f"scaler_{version}.pkl"
        metadata_path = self.model_dir / f"metadata_{version}.json"
        
        # Salvar modelo
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        logger.info(f"Modelo salvo em {model_path}")
        
        # Salvar scaler
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        logger.info(f"Scaler salvo em {scaler_path}")
        
        # Salvar metadados (garantir que todos os valores são serializáveis)
        metadata = {
            'version': version,
            'timestamp': datetime.now().isoformat(),
            'metrics': {k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
                       for k, v in self.metrics.items()},
            'feature_names': self.feature_names,
            'feature_importance': self.get_feature_importance(20)
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadados salvos em {metadata_path}")
        
        return model_path, scaler_path, metadata_path
    
    def load_model(self, version: str):
        """
        Carrega modelo salvo
        
        Args:
            version: Versão do modelo
        """
        model_path = self.model_dir / f"model_{version}.pkl"
        scaler_path = self.model_dir / f"scaler_{version}.pkl"
        metadata_path = self.model_dir / f"metadata_{version}.json"
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            self.feature_names = metadata['feature_names']
            self.metrics = metadata.get('metrics', {})
        
        logger.info(f"Modelo {version} carregado com sucesso!")
        return self.model

