import pandas as pd
from pathlib import Path

class JTLParser:
    @staticmethod
    def parse(jtl_path):
        if not Path(jtl_path).exists():
            raise FileNotFoundError(f"JTL file not found: {jtl_path}")
            
        df = pd.read_csv(jtl_path)
        
        # Calculate overall metrics
        total_requests = len(df)
        if total_requests == 0:
            return {"p95": 0, "error_rate": 0.0}

        errors = len(df[df['success'] == False])
        error_rate = errors / total_requests

        p95 = df['Elapsed'].quantile(0.95) if 'Elapsed' in df.columns else df['elapsed'].quantile(0.95)

        return {
            "p95": float(p95),
            "error_rate": float(error_rate)
        }
