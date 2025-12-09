"""
Script principal para treinar o modelo
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_processing import DataProcessor
from model_trainer import ModelTrainer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Função principal para treinar o modelo"""
    
    # Caminhos - tentar usar imoveis-df.csv primeiro, depois dataZAP.csv
    data_path_imoveis = Path(__file__).parent.parent / "data" / "imoveis-df.csv"
    data_path_zap = Path(__file__).parent.parent / "data" / "dataZAP.csv"
    
    if data_path_imoveis.exists():
        data_path = data_path_imoveis
        logger.info(f"Usando dataset: {data_path.name}")
    elif data_path_zap.exists():
        data_path = data_path_zap
        logger.info(f"Usando dataset: {data_path.name}")
    else:
        raise FileNotFoundError("Nenhum dataset encontrado. Verifique se imoveis-df.csv ou dataZAP.csv existe em data/")
    
    models_dir = Path(__file__).parent / "models"
    
    logger.info("=" * 60)
    logger.info("TREINAMENTO DO MODELO ALUGAI")
    logger.info("=" * 60)
    
    # 1. Processar dados
    logger.info("\n[1/3] Processando dados...")
    processor = DataProcessor(str(data_path))
    processed_df = processor.process()
    
    # 2. Separar features e target
    X, y = processor.get_features_and_target()
    logger.info(f"Shape final: {X.shape[0]} amostras, {X.shape[1]} features")
    
    # 3. Treinar modelo
    logger.info("\n[2/3] Treinando modelo...")
    trainer = ModelTrainer(model_dir=str(models_dir))
    
    # Preparar dados
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.prepare_data(X, y)
    
    # Treinar
    trainer.train_xgboost(X_train, y_train, X_val, y_val)
    
    # Avaliar
    logger.info("\n[3/3] Avaliando modelo...")
    metrics = trainer.evaluate(X_test, y_test)
    
    # Validação cruzada
    X_all = trainer.scaler.transform(X)
    cv_mae, cv_std = trainer.cross_validate(X_all, y)
    
    # Feature importance
    logger.info("\nTop 10 Features mais importantes:")
    for i, (feature, importance) in enumerate(trainer.get_feature_importance(10), 1):
        logger.info(f"  {i}. {feature}: {importance:.4f}")
    
    # Obter mapeamentos de encoding e valores únicos
    encoding_maps = processor.get_encoding_maps()
    unique_values = processor.get_unique_values()
    
    # Salvar modelo (incluindo encoding maps e unique values)
    logger.info("\nSalvando modelo...")
    model_path, scaler_path, metadata_path = trainer.save_model()
    version = metadata_path.stem.replace('metadata_', '')
    
    # Salvar encoding maps e unique values
    import json
    encoding_path = models_dir / f"encoding_{version}.json"
    with open(encoding_path, 'w', encoding='utf-8') as f:
        json.dump({
            'encoding_maps': encoding_maps,
            'unique_values': unique_values
        }, f, ensure_ascii=False, indent=2)
    logger.info(f"Mapeamentos de encoding salvos em {encoding_path}")
    
    logger.info("\n" + "=" * 60)
    logger.info("TREINAMENTO CONCLUÍDO!")
    logger.info("=" * 60)
    logger.info(f"MAE: R$ {metrics['MAE']:.2f} ({metrics['MAE_PCT']:.2f}%)")
    logger.info(f"RMSE: R$ {metrics['RMSE']:.2f}")
    logger.info(f"R²: {metrics['R2']:.4f}")
    logger.info(f"CV MAE: R$ {cv_mae:.2f} (+/- {cv_std:.2f})")


if __name__ == "__main__":
    main()


