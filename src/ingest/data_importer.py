"""
Generic CSV Data Importer with Schema Validation

Handles import of gold supply chain data from various sources.
Validates against schema definitions and enforces data quality rules.

Implements Rule Set 3 (Data-First Discipline):
- Every record must have phase_id, unit, source_type
- Missing data marked as OPAQUE
- No interpolation or speculation
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validates data against gold supply chain schema"""
    
    REQUIRED_FIELDS = {
        'gold_supply_chain_metrics': [
            'phase_id', 'entity', 'country', 'date', 
            'metric_name', 'metric_value', 'unit', 'source_type'
        ],
        'custody_and_flow': [
            'from_phase', 'to_phase', 'custodian', 'ownership_change'
        ]
    }
    
    VALID_PHASES = [0, 1, 2, 3, 4, 5, 6, 7]
    
    VALID_SOURCE_TYPES = ['public', 'paid', 'private', 'inferred', 'OPAQUE']
    
    VALID_TRANSPARENCY = ['High', 'Medium', 'Low', 'Medium-High']
    
    def __init__(self, schema_dir="../schema"):
        self.schema_dir = Path(schema_dir)
        self.phases = self._load_phases()
    
    def _load_phases(self) -> pd.DataFrame:
        """Load phase definitions"""
        phases_file = self.schema_dir / "supply_chain_phases.csv"
        return pd.read_csv(phases_file)
    
    def validate_metrics(self, df: pd.DataFrame) -> tuple[bool, List[str]]:
        """
        Validate metrics dataframe
        
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        missing_fields = set(self.REQUIRED_FIELDS['gold_supply_chain_metrics']) - set(df.columns)
        if missing_fields:
            errors.append(f"Missing required fields: {missing_fields}")
        
        if len(errors) > 0:
            return False, errors
        
        # Validate phase_id
        invalid_phases = df[~df['phase_id'].isin(self.VALID_PHASES)]
        if not invalid_phases.empty:
            errors.append(f"Invalid phase_id values: {invalid_phases['phase_id'].unique()}")
        
        # Validate source_type
        invalid_sources = df[~df['source_type'].isin(self.VALID_SOURCE_TYPES)]
        if not invalid_sources.empty:
            errors.append(f"Invalid source_type values: {invalid_sources['source_type'].unique()}")
        
        # Check for units
        missing_units = df[df['unit'].isna()]
        if not missing_units.empty:
            errors.append(f"{len(missing_units)} records missing unit field")
        
        # Check for numeric values
        non_numeric = df[pd.to_numeric(df['metric_value'], errors='coerce').isna()]
        if not non_numeric.empty:
            errors.append(f"{len(non_numeric)} records have non-numeric metric_value")
        
        return len(errors) == 0, errors
    
    def validate_flow(self, df: pd.DataFrame) -> tuple[bool, List[str]]:
        """Validate custody/flow dataframe"""
        errors = []
        
        missing_fields = set(self.REQUIRED_FIELDS['custody_and_flow']) - set(df.columns)
        if missing_fields:
            errors.append(f"Missing required fields: {missing_fields}")
            return False, errors
        
        # Validate phase transitions
        invalid_from = df[~df['from_phase'].isin(self.VALID_PHASES)]
        if not invalid_from.empty:
            errors.append(f"Invalid from_phase: {invalid_from['from_phase'].unique()}")
        
        invalid_to = df[~df['to_phase'].isin(self.VALID_PHASES)]
        if not invalid_to.empty:
            errors.append(f"Invalid to_phase: {invalid_to['to_phase'].unique()}")
        
        # Check ownership_change is boolean
        if not df['ownership_change'].dtype == bool:
            try:
                df['ownership_change'] = df['ownership_change'].astype(bool)
            except:
                errors.append("ownership_change must be boolean")
        
        return len(errors) == 0, errors


class GoldDataImporter:
    """Import and validate gold supply chain data"""
    
    def __init__(self, schema_dir="../schema", data_dir="../data"):
        self.schema_dir = Path(schema_dir)
        self.data_dir = Path(data_dir)
        self.validator = SchemaValidator(schema_dir)
        
        # Load existing schema files
        self.metrics_schema = self.schema_dir / "gold_supply_chain_metrics.csv"
        self.flow_schema = self.schema_dir / "custody_and_flow.csv"
    
    def import_metrics(
        self, 
        source_file: Path, 
        validate: bool = True,
        append: bool = True
    ) -> bool:
        """
        Import metrics data from CSV
        
        Args:
            source_file: Path to source CSV file
            validate: Whether to validate against schema
            append: Whether to append to existing data or create new file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Importing metrics from {source_file}")
            
            # Read source data
            df = pd.read_csv(source_file)
            
            # Validate
            if validate:
                is_valid, errors = self.validator.validate_metrics(df)
                
                if not is_valid:
                    logger.error("Validation failed:")
                    for error in errors:
                        logger.error(f"  - {error}")
                    return False
                
                logger.info("✓ Validation passed")
            
            # Assign record IDs if not present
            if 'record_id' not in df.columns or df['record_id'].isna().all():
                # Get next ID from existing data
                if self.metrics_schema.exists() and append:
                    existing = pd.read_csv(self.metrics_schema)
                    if len(existing) > 0 and 'record_id' in existing.columns:
                        next_id = existing['record_id'].max() + 1
                    else:
                        next_id = 1
                else:
                    next_id = 1
                
                df['record_id'] = range(next_id, next_id + len(df))
            
            # Save
            output_file = self.data_dir / "processed" / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(output_file, index=False)
            
            logger.info(f"✓ Saved {len(df)} records to {output_file}")
            
            # Optionally append to master schema file
            if append:
                if self.metrics_schema.exists():
                    existing = pd.read_csv(self.metrics_schema)
                    combined = pd.concat([existing, df], ignore_index=True)
                else:
                    combined = df
                
                combined.to_csv(self.metrics_schema, index=False)
                logger.info(f"✓ Appended to master schema: {len(df)} new records")
            
            return True
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return False
    
    def import_flow(self, source_file: Path, validate: bool = True) -> bool:
        """Import custody/flow data"""
        try:
            logger.info(f"Importing flow data from {source_file}")
            
            df = pd.read_csv(source_file)
            
            if validate:
                is_valid, errors = self.validator.validate_flow(df)
                
                if not is_valid:
                    logger.error("Validation failed:")
                    for error in errors:
                        logger.error(f"  - {error}")
                    return False
                
                logger.info("✓ Validation passed")
            
            # Assign flow IDs
            if 'flow_id' not in df.columns or df['flow_id'].isna().all():
                if self.flow_schema.exists():
                    existing = pd.read_csv(self.flow_schema)
                    next_id = existing['flow_id'].max() + 1 if len(existing) > 0 else 1
                else:
                    next_id = 1
                
                df['flow_id'] = range(next_id, next_id + len(df))
            
            # Save
            output_file = self.data_dir / "processed" / f"flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(output_file, index=False)
            
            logger.info(f"✓ Saved {len(df)} flow records to {output_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Flow import failed: {e}")
            return False
    
    def mark_opaque(
        self, 
        phase_id: int, 
        entity: str, 
        reason: str
    ) -> Dict:
        """
        Explicitly mark a data point as OPAQUE
        
        Implements Rule Set 3: "Missing data is a finding, not a failure"
        """
        record = {
            'phase_id': phase_id,
            'entity': entity,
            'country': 'N/A',
            'date': datetime.now().date(),
            'metric_name': 'data_availability',
            'metric_value': 0,
            'unit': 'boolean',
            'source_type': 'OPAQUE',
            'source_name': 'Structural opacity',
            'url': None,
            'notes': reason
        }
        
        logger.info(f"Marked OPAQUE: Phase {phase_id}, Entity {entity} - {reason}")
        
        return record
    
    def get_transparency_report(self) -> pd.DataFrame:
        """Generate transparency report by phase"""
        if not self.metrics_schema.exists():
            logger.warning("No metrics data found")
            return pd.DataFrame()
        
        df = pd.read_csv(self.metrics_schema)
        
        # Group by phase and source type
        report = df.groupby(['phase_id', 'source_type']).size().reset_index(name='record_count')
        
        # Merge with phase names
        phases = self.validator.phases[['phase_id', 'phase_name', 'transparency_level']]
        report = report.merge(phases, on='phase_id', how='left')
        
        return report


def main():
    """Example usage"""
    importer = GoldDataImporter()
    
    logger.info("Gold Supply Chain Data Importer initialized")
    logger.info("Use importer.import_metrics() or importer.import_flow() to load data")
    
    # Example: Mark Phase 6 (Logistics & Vaulting) as structurally opaque
    opaque_record = importer.mark_opaque(
        phase_id=6,
        entity="Global Vault Network",
        reason="Custodial secrecy, jurisdictional controls, insurance limits"
    )
    
    logger.info(f"Example OPAQUE record: {opaque_record}")


if __name__ == "__main__":
    main()

