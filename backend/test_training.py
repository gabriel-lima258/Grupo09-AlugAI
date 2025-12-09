"""
Script de teste rápido do pipeline de treinamento
Usa apenas uma amostra pequena para validação
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
    """Teste rápido do pipeline"""
    
    # Caminhos
    data_path = Path(__file__).parent.parent / "data" / "dataZAP.csv"
    models_dir = Path(__file__).parent / "models"
    
    logger.info("=" * 60)
    logger.info("TESTE RÁPIDO DO PIPELINE ALUGAI")
    logger.info("=" * 60)
    
    try:
        # 1. Processar dados (amostra pequena)
        logger.info("\n[1/3] Processando dados (amostra de 5000 registros)...")
        processor = DataProcessor(str(data_path))
        processor.load_data()
        
        # Limitar para teste rápido
        processor.df = processor.df.head(5000)
        logger.info(f"Usando amostra de {len(processor.df)} registros")
        
        # Usar o método process() completo
        processed_df = processor.process()
        logger.info(f"✓ Dados processados: {len(processed_df)} registros finais")
        
        # 2. Separar features e target
        X, y = processor.get_features_and_target()
        logger.info(f"✓ Features: {X.shape[1]} colunas, {X.shape[0]} amostras")
        logger.info(f"✓ Target: média R$ {y.mean():.2f}, min R$ {y.min():.2f}, max R$ {y.max():.2f}")
        
        # 3. Teste rápido de treinamento (modelo pequeno)
        logger.info("\n[2/3] Testando treinamento (modelo reduzido)...")
        trainer = ModelTrainer(model_dir=str(models_dir))
        
        # Preparar dados
        X_train, X_val, X_test, y_train, y_val, y_test = trainer.prepare_data(X, y)
        
        # Treinar modelo pequeno para teste
        logger.info("Treinando modelo XGBoost (configuração rápida)...")
        trainer.model = trainer.model = __import__('xgboost').XGBRegressor(
            n_estimators=10,  # Poucas árvores para teste rápido
            max_depth=3,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        trainer.model.fit(X_train, y_train)
        logger.info("✓ Modelo treinado com sucesso!")
        
        # Avaliar
        logger.info("\n[3/3] Avaliando modelo...")
        metrics = trainer.evaluate(X_test, y_test)
        
        logger.info("\n" + "=" * 60)
        logger.info("TESTE CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)
        logger.info(f"MAE: R$ {metrics['MAE']:.2f} ({metrics['MAE_PCT']:.2f}%)")
        logger.info(f"RMSE: R$ {metrics['RMSE']:.2f}")
        logger.info(f"R²: {metrics['R2']:.4f}")
        logger.info("\n✓ Pipeline funcionando corretamente!")
        logger.info("✓ Você pode executar train_model.py para treinar o modelo completo")
        
    except Exception as e:
        logger.error(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

