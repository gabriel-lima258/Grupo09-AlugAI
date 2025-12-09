"""
Módulo de processamento e engenharia de features
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Classe para processamento de dados e feature engineering"""
    
    def __init__(self, data_path: str):
        """
        Inicializa o processador de dados
        
        Args:
            data_path: Caminho para o arquivo CSV
        """
        self.data_path = data_path
        self.df = None
        self.processed_df = None
        
    def load_data(self) -> pd.DataFrame:
        """Carrega os dados do CSV"""
        logger.info(f"Carregando dados de {self.data_path}")
        try:
            self.df = pd.read_csv(self.data_path, sep=';', low_memory=False)
            logger.info(f"Dados carregados: {len(self.df)} registros")
            logger.info(f"Colunas encontradas: {list(self.df.columns)}")
            return self.df
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def filter_rental_properties(self) -> pd.DataFrame:
        """Filtra apenas imóveis para aluguel"""
        logger.info("Filtrando imóveis para aluguel...")
        
        # Verificar qual formato de dataset estamos usando
        if 'preco' in self.df.columns:
            # Novo formato: imoveis-df.csv (já são todos para aluguel)
            # Filtrar apenas valores válidos de preço
            # Converter preco para numérico primeiro
            self.df['preco'] = pd.to_numeric(self.df['preco'], errors='coerce')
            mask = (
                (self.df['preco'].notna()) &
                (self.df['preco'] > 0) &
                (self.df['preco'] < 100000)  # Remover outliers extremos
            )
            self.df = self.df[mask].copy()
            logger.info(f"Imóveis válidos: {len(self.df)} registros")
        elif 'listing.pricingInfo.isRent' in self.df.columns:
            # Formato antigo: dataZAP.csv
            mask = (
                (self.df['listing.pricingInfo.isRent'] == True) &
                (self.df['listing.pricingInfo.rentalPrice'].notna()) &
                (self.df['listing.pricingInfo.rentalPrice'] > 0)
            )
            self.df = self.df[mask].copy()
            logger.info(f"Imóveis para aluguel: {len(self.df)} registros")
        else:
            # Se não tem filtro, manter todos
            logger.info("Nenhum filtro aplicado, mantendo todos os registros")
        
        return self.df
    
    def select_features(self) -> pd.DataFrame:
        """Seleciona e renomeia features relevantes"""
        logger.info("Selecionando features...")
        
        # Verificar qual formato de dataset estamos usando
        if 'preco' in self.df.columns:
            # Novo formato: imoveis-df.csv
            feature_map = {
                'preco': 'rent_amount',
                'area': 'area',
                'quartos': 'bedrooms',
                'tipo': 'property_type',
                'bairro': 'neighborhood'
            }
            
            # Selecionar e renomear colunas existentes
            available_cols = {k: v for k, v in feature_map.items() if k in self.df.columns}
            self.df = self.df[list(available_cols.keys())].copy()
            self.df = self.df.rename(columns=available_cols)
            
            # Adicionar colunas faltantes com valores padrão
            if 'bathrooms' not in self.df.columns:
                self.df['bathrooms'] = 1  # Padrão: 1 banheiro
            if 'parking_spaces' not in self.df.columns:
                self.df['parking_spaces'] = 0  # Padrão: sem vaga
            if 'hoa' not in self.df.columns:
                self.df['hoa'] = 0  # Padrão: sem condomínio
            if 'furnished' not in self.df.columns:
                self.df['furnished'] = False  # Padrão: não mobiliado
            if 'suites' not in self.df.columns:
                self.df['suites'] = 0  # Padrão: sem suíte
            if 'city' not in self.df.columns:
                # Todos os dados são do DF, usar "Brasília" como padrão
                self.df['city'] = 'Brasília'
            
        elif 'listing.pricingInfo.rentalPrice' in self.df.columns:
            # Formato antigo: dataZAP.csv
            feature_map = {
                'listing.pricingInfo.rentalPrice': 'rent_amount',
                'listing.usableAreas': 'area',
                'listing.bedrooms': 'bedrooms',
                'listing.bathrooms': 'bathrooms',
                'listing.parkingSpaces': 'parking_spaces',
                'listing.address.city': 'city',
                'listing.address.neighborhood': 'neighborhood',
                'listing.address.state': 'state',
                'listing.furnished': 'furnished',
                'listing.pricingInfo.monthlyCondoFee': 'hoa',
                'listing.propertyType': 'property_type',
                'listing.suites': 'suites'
            }
            
            # Selecionar apenas colunas que existem
            available_cols = {k: v for k, v in feature_map.items() if k in self.df.columns}
            self.df = self.df[list(available_cols.keys())].copy()
            self.df = self.df.rename(columns=available_cols)
        else:
            raise ValueError("Formato de dataset não reconhecido")
        
        logger.info(f"Features selecionadas: {list(self.df.columns)}")
        return self.df
    
    def handle_missing_values(self) -> pd.DataFrame:
        """Trata valores faltantes"""
        logger.info("Tratando valores faltantes...")
        
        # Converter colunas numéricas para float, tratando strings e valores inválidos
        numeric_cols = ['area', 'bedrooms', 'bathrooms', 'parking_spaces', 'hoa', 'suites', 'rent_amount']
        for col in numeric_cols:
            if col in self.df.columns:
                # Converter para numérico, tratando vírgulas e valores inválidos
                if self.df[col].dtype == 'object':
                    # Substituir vírgulas por pontos e converter
                    self.df[col] = self.df[col].astype(str).str.replace(',', '.', regex=False)
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                # Preencher NaN com mediana
                if self.df[col].isna().sum() > 0:
                    median_val = self.df[col].median()
                    if pd.isna(median_val):
                        median_val = 0  # Se mediana for NaN, usar 0
                    self.df[col].fillna(median_val, inplace=True)
                    logger.info(f"{col}: convertido e preenchido {self.df[col].isna().sum()} valores com mediana {median_val}")
        
        # Categóricos: preencher com 'Desconhecido'
        categorical_cols = ['city', 'neighborhood', 'state', 'property_type']
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)
                self.df[col].fillna('Desconhecido', inplace=True)
                self.df[col] = self.df[col].replace('nan', 'Desconhecido')
        
        # Furnished: converter para booleano
        if 'furnished' in self.df.columns:
            self.df['furnished'] = pd.to_numeric(self.df['furnished'], errors='coerce')
            self.df['furnished'] = self.df['furnished'].fillna(0).astype(bool)
        
        return self.df
    
    def remove_outliers(self) -> pd.DataFrame:
        """Remove outliers usando IQR"""
        logger.info("Removendo outliers...")
        
        initial_len = len(self.df)
        
        # Remover outliers do target
        if 'rent_amount' in self.df.columns:
            Q1 = self.df['rent_amount'].quantile(0.25)
            Q3 = self.df['rent_amount'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            mask = (self.df['rent_amount'] >= lower_bound) & (self.df['rent_amount'] <= upper_bound)
            self.df = self.df[mask].copy()
            logger.info(f"Outliers removidos do target: {initial_len - len(self.df)} registros")
        
        # Remover outliers da área
        if 'area' in self.df.columns:
            Q1 = self.df['area'].quantile(0.25)
            Q3 = self.df['area'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = max(0, Q1 - 1.5 * IQR)  # Área não pode ser negativa
            upper_bound = Q3 + 1.5 * IQR
            
            mask = (self.df['area'] >= lower_bound) & (self.df['area'] <= upper_bound)
            self.df = self.df[mask].copy()
            logger.info(f"Outliers removidos da área: {initial_len - len(self.df)} registros")
        
        return self.df
    
    def create_derived_features(self) -> pd.DataFrame:
        """Cria features derivadas"""
        logger.info("Criando features derivadas...")
        
        # Preço por m²
        if 'rent_amount' in self.df.columns and 'area' in self.df.columns:
            self.df['price_per_sqm'] = self.df['rent_amount'] / self.df['area']
            self.df['price_per_sqm'] = self.df['price_per_sqm'].replace([np.inf, -np.inf], np.nan)
            self.df['price_per_sqm'].fillna(self.df['price_per_sqm'].median(), inplace=True)
            logger.info("Feature 'price_per_sqm' criada")
        
        return self.df
    
    def encode_categorical_features(self) -> pd.DataFrame:
        """Aplica encoding em features categóricas"""
        logger.info("Codificando features categóricas...")
        
        # One-Hot Encoding para features de baixa cardinalidade
        low_cardinality_cols = ['furnished', 'property_type']
        for col in low_cardinality_cols:
            if col in self.df.columns:
                if col == 'furnished':
                    # Já é booleano, converter para int
                    self.df[col] = self.df[col].astype(int)
                else:
                    # One-Hot Encoding
                    dummies = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
                    self.df = pd.concat([self.df, dummies], axis=1)
                    self.df.drop(col, axis=1, inplace=True)
        
        # Para city e neighborhood (alta cardinalidade), usar target encoding ou agrupar
        # Por enquanto, vamos usar target encoding simples
        self.city_encoding_map = {}
        self.neighborhood_encoding_map = {}
        self.mean_rent = self.df['rent_amount'].mean()
        
        if 'city' in self.df.columns:
            city_means = self.df.groupby('city')['rent_amount'].mean()
            self.city_encoding_map = city_means.to_dict()
            self.df['city_encoded'] = self.df['city'].map(city_means)
            self.df['city_encoded'].fillna(self.mean_rent, inplace=True)
            self.df.drop('city', axis=1, inplace=True)
        
        if 'neighborhood' in self.df.columns:
            # Agrupar bairros com poucos exemplos
            neighborhood_counts = self.df['neighborhood'].value_counts()
            rare_neighborhoods = neighborhood_counts[neighborhood_counts < 10].index
            self.df['neighborhood'] = self.df['neighborhood'].replace(rare_neighborhoods, 'Outros')
            
            # Target encoding
            neighborhood_means = self.df.groupby('neighborhood')['rent_amount'].mean()
            self.neighborhood_encoding_map = neighborhood_means.to_dict()
            self.df['neighborhood_encoded'] = self.df['neighborhood'].map(neighborhood_means)
            self.df['neighborhood_encoded'].fillna(self.mean_rent, inplace=True)
            self.df.drop('neighborhood', axis=1, inplace=True)
        
        # Remover state se existir (não vamos usar)
        if 'state' in self.df.columns:
            self.df.drop('state', axis=1, inplace=True)
        
        return self.df
    
    def process(self) -> pd.DataFrame:
        """Executa todo o pipeline de processamento"""
        logger.info("Iniciando pipeline de processamento...")
        
        self.load_data()
        self.filter_rental_properties()
        self.select_features()
        self.handle_missing_values()
        self.remove_outliers()
        self.create_derived_features()
        self.encode_categorical_features()
        
        # Salvar DataFrame processado
        self.processed_df = self.df.copy()
        
        logger.info(f"Processamento concluído: {len(self.processed_df)} registros finais")
        return self.processed_df
    
    def get_features_and_target(self) -> tuple:
        """Retorna features (X) e target (y) separados"""
        if self.processed_df is None:
            raise ValueError("Dados não processados. Execute process() primeiro.")
        
        # Separar target
        target_col = 'rent_amount'
        if target_col not in self.processed_df.columns:
            raise ValueError(f"Coluna '{target_col}' não encontrada")
        
        y = self.processed_df[target_col].copy()
        X = self.processed_df.drop(target_col, axis=1).copy()
        
        logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
        return X, y
    
    def get_encoding_maps(self) -> dict:
        """Retorna os mapeamentos de encoding para uso na API"""
        return {
            'city_encoding': self.city_encoding_map,
            'neighborhood_encoding': self.neighborhood_encoding_map,
            'mean_rent': float(self.mean_rent) if hasattr(self, 'mean_rent') else 0.0
        }
    
    def get_unique_values(self) -> dict:
        """Retorna valores únicos de features categóricas"""
        unique_values = {}
        
        # Usar dados antes do encoding (após select_features mas antes de encode_categorical_features)
        # Se já processamos, precisamos recarregar até o ponto de select_features
        if self.df is None or 'city' not in self.df.columns:
            # Recarregar até select_features
            self.load_data()
            self.filter_rental_properties()
            self.select_features()
        
        # Agora self.df tem as colunas originais (city, neighborhood, property_type)
        if 'city' in self.df.columns:
            cities = self.df['city'].dropna().unique().tolist()
            unique_values['cities'] = sorted([str(c) for c in cities if str(c) != 'nan'])
        if 'neighborhood' in self.df.columns:
            neighborhoods = self.df['neighborhood'].dropna().unique().tolist()
            unique_values['neighborhoods'] = sorted([str(n) for n in neighborhoods if str(n) != 'nan'])
        if 'property_type' in self.df.columns:
            property_types = self.df['property_type'].dropna().unique().tolist()
            unique_values['property_types'] = sorted([str(p) for p in property_types if str(p) != 'nan'])
        
        return unique_values

