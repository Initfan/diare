from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from app.ml.constants import NUMERIC_FEATURES, CATEGORICAL_FEATURES, EXPECTED_CATEGORIES

def build_preprocessor():
    """
    Builds the ColumnTransformer for preprocessing.
    Numeric features: KBinsDiscretizer (quantile, 5 bins)
    Categorical features: OrdinalEncoder with known categories
    """
    # Tetapkan urutan categories sesuai EXPECTED_CATEGORIES
    categorical_categories = [
        EXPECTED_CATEGORIES[col] for col in CATEGORICAL_FEATURES
    ]
    
    numeric_transformer = KBinsDiscretizer(
        n_bins=5,
        encode="ordinal",
        strategy="quantile",
        subsample=None
    )
    
    categorical_transformer = OrdinalEncoder(
        categories=categorical_categories,
        handle_unknown='error'  # Tolak kategori asing secara eksplisit
    )
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    
    return preprocessor
