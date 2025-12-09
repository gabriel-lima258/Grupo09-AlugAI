"""
Script de teste completo da aplicação AlugAI
"""

import sys
import subprocess
from pathlib import Path
import importlib.util

def check_python_version():
    """Verifica versão do Python"""
    print("=" * 60)
    print("TESTE DA APLICAÇÃO ALUGAI")
    print("=" * 60)
    print()
    
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  AVISO: Python 3.8+ recomendado")
    print()

def check_dependencies(requirements_file):
    """Verifica se as dependências estão instaladas"""
    print("Verificando dependências...")
    
    if not Path(requirements_file).exists():
        print(f"✗ Arquivo {requirements_file} não encontrado")
        return False
    
    with open(requirements_file, 'r') as f:
        deps = [line.strip().split('>=')[0].split('==')[0] for line in f if line.strip() and not line.startswith('#')]
    
    missing = []
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} (não instalado)")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Dependências faltando: {', '.join(missing)}")
        print(f"   Execute: pip install -r {requirements_file}")
        return False
    
    print("✓ Todas as dependências estão instaladas\n")
    return True

def check_data_file():
    """Verifica se o arquivo de dados existe"""
    print("Verificando arquivo de dados...")
    
    data_file = Path("data/dataZAP.csv")
    if data_file.exists():
        size_mb = data_file.stat().st_size / (1024 * 1024)
        print(f"✓ Arquivo encontrado: {data_file} ({size_mb:.1f} MB)")
        print()
        return True
    else:
        print(f"✗ Arquivo não encontrado: {data_file}")
        print()
        return False

def check_backend_structure():
    """Verifica estrutura do backend"""
    print("Verificando estrutura do backend...")
    
    required_files = [
        "backend/src/data_processing.py",
        "backend/src/model_trainer.py",
        "backend/train_model.py",
        "backend/api/app.py",
        "backend/requirements.txt"
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (não encontrado)")
            all_ok = False
    
    print()
    return all_ok

def check_frontend_structure():
    """Verifica estrutura do frontend"""
    print("Verificando estrutura do frontend...")
    
    required_files = [
        "frontend/app.py",
        "frontend/pages/buscar_imoveis.py",
        "frontend/pages/estimativa_preco.py",
        "frontend/utils/config.py",
        "frontend/utils/helpers.py",
        "frontend/requirements.txt"
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (não encontrado)")
            all_ok = False
    
    print()
    return all_ok

def check_model_exists():
    """Verifica se existe modelo treinado"""
    print("Verificando modelos treinados...")
    
    models_dir = Path("backend/models")
    if not models_dir.exists():
        print(f"  ✗ Diretório {models_dir} não existe")
        print()
        return False
    
    model_files = list(models_dir.glob("model_*.pkl"))
    if model_files:
        latest = max(model_files, key=lambda p: p.stat().st_mtime)
        print(f"  ✓ Modelo encontrado: {latest.name}")
        print()
        return True
    else:
        print(f"  ⚠️  Nenhum modelo encontrado")
        print(f"     Execute: cd backend && python train_model.py")
        print()
        return False

def test_backend_imports():
    """Testa imports do backend"""
    print("Testando imports do backend...")
    
    try:
        sys.path.insert(0, str(Path("backend/src")))
        from data_processing import DataProcessor
        from model_trainer import ModelTrainer
        print("  ✓ Imports do backend OK")
        print()
        return True
    except Exception as e:
        print(f"  ✗ Erro nos imports: {e}")
        print()
        return False

def test_frontend_imports():
    """Testa imports do frontend"""
    print("Testando imports do frontend...")
    
    try:
        sys.path.insert(0, str(Path("frontend")))
        import streamlit
        import pandas
        import plotly
        print("  ✓ Imports do frontend OK")
        print()
        return True
    except Exception as e:
        print(f"  ✗ Erro nos imports: {e}")
        print()
        return False

def test_data_processing():
    """Testa processamento de dados (amostra pequena)"""
    print("Testando processamento de dados...")
    
    try:
        sys.path.insert(0, str(Path("backend/src")))
        from data_processing import DataProcessor
        
        data_path = Path("data/dataZAP.csv")
        if not data_path.exists():
            print("  ⚠️  Arquivo de dados não encontrado")
            print()
            return False
        
        processor = DataProcessor(str(data_path))
        
        # Carregar apenas algumas linhas para teste rápido
        print("  Carregando amostra de dados...")
        processor.load_data()
        
        # Filtrar apenas algumas linhas para teste
        processor.df = processor.df.head(1000)
        
        processor.filter_rental_properties()
        processor.select_features()
        processor.handle_missing_values()
        
        print(f"  ✓ Processamento OK ({len(processor.df)} registros processados)")
        print()
        return True
        
    except Exception as e:
        print(f"  ✗ Erro no processamento: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

def main():
    """Função principal de teste"""
    results = {}
    
    # Testes básicos
    check_python_version()
    
    results['data_file'] = check_data_file()
    results['backend_structure'] = check_backend_structure()
    results['frontend_structure'] = check_frontend_structure()
    
    # Testes de dependências
    print("=" * 60)
    print("VERIFICAÇÃO DE DEPENDÊNCIAS")
    print("=" * 60)
    print()
    
    results['backend_deps'] = check_dependencies("backend/requirements.txt")
    results['frontend_deps'] = check_dependencies("frontend/requirements.txt")
    
    # Testes de imports
    print("=" * 60)
    print("TESTES DE IMPORTS")
    print("=" * 60)
    print()
    
    results['backend_imports'] = test_backend_imports()
    results['frontend_imports'] = test_frontend_imports()
    
    # Testes funcionais
    print("=" * 60)
    print("TESTES FUNCIONAIS")
    print("=" * 60)
    print()
    
    results['model_exists'] = check_model_exists()
    
    if results['backend_imports'] and results['data_file']:
        results['data_processing'] = test_data_processing()
    else:
        results['data_processing'] = False
        print("⚠️  Pulando teste de processamento (dependências faltando)")
        print()
    
    # Resumo
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print()
    
    for test_name, result in results.items():
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{test_name:.<40} {status}")
    
    print()
    
    # Recomendações
    print("=" * 60)
    print("PRÓXIMOS PASSOS")
    print("=" * 60)
    print()
    
    if not results['backend_deps']:
        print("1. Instalar dependências do backend:")
        print("   cd backend && pip install -r requirements.txt")
        print()
    
    if not results['frontend_deps']:
        print("2. Instalar dependências do frontend:")
        print("   cd frontend && pip install -r requirements.txt")
        print()
    
    if not results['model_exists']:
        print("3. Treinar o modelo:")
        print("   cd backend && python train_model.py")
        print()
    
    if results['backend_deps'] and results['frontend_deps']:
        print("4. Para iniciar a aplicação:")
        print("   Terminal 1 (API):")
        print("     cd backend/api && python app.py")
        print()
        print("   Terminal 2 (Frontend):")
        print("     cd frontend && streamlit run app.py")
        print()
    
    # Status final
    all_critical = (
        results['backend_structure'] and
        results['frontend_structure'] and
        results['data_file']
    )
    
    if all_critical:
        print("=" * 60)
        print("✓ ESTRUTURA BÁSICA OK")
        print("=" * 60)
    else:
        print("=" * 60)
        print("✗ PROBLEMAS ENCONTRADOS")
        print("=" * 60)

if __name__ == "__main__":
    main()


