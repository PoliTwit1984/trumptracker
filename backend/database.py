from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
Base = declarative_base()
DB_PATH = os.path.join(os.path.dirname(__file__), 'fred_data.db')
engine = create_engine(f'sqlite:///{DB_PATH}', pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)

class FREDSeries(Base):
    """Model for storing FRED series metadata"""
    __tablename__ = 'fred_series'
    
    id = Column(Integer, primary_key=True)
    series_id = Column(String, unique=True, nullable=False)
    title = Column(String)
    units = Column(String)
    last_updated = Column(DateTime)
    frequency = Column(String)
    latest_analysis = Column(Text)  # New column for storing AI analysis
    analysis_timestamp = Column(DateTime)  # New column for tracking when analysis was performed
    
    def __repr__(self):
        return f"<FREDSeries(series_id='{self.series_id}', title='{self.title}')>"

class FREDData(Base):
    """Model for storing FRED series data points"""
    __tablename__ = 'fred_data'
    
    id = Column(Integer, primary_key=True)
    series_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    value = Column(Float)
    
    # Create indexes for faster querying
    __table_args__ = (
        Index('idx_series_date', 'series_id', 'date'),
    )
    
    def __repr__(self):
        return f"<FREDData(series_id='{self.series_id}', date='{self.date}', value={self.value})>"

def init_db():
    """Initialize the database, creating all tables if they don't exist"""
    try:
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def get_session():
    """Get a new database session"""
    return Session()

def store_series_data(session, series_id: str, data_points: list, metadata: dict):
    """Store series data and metadata in the database"""
    try:
        # Store or update series metadata
        series = session.query(FREDSeries).filter_by(series_id=series_id).first()
        if not series:
            series = FREDSeries(
                series_id=series_id,
                title=metadata.get('title'),
                units=metadata.get('units'),
                frequency=metadata.get('frequency'),
                last_updated=datetime.now()
            )
            session.add(series)
        else:
            series.last_updated = datetime.now()
            series.title = metadata.get('title', series.title)
            series.units = metadata.get('units', series.units)
            series.frequency = metadata.get('frequency', series.frequency)
        
        # Store data points
        for point in data_points:
            existing = session.query(FREDData).filter_by(
                series_id=series_id,
                date=point['date']
            ).first()
            
            if not existing:
                data_point = FREDData(
                    series_id=series_id,
                    date=point['date'],
                    value=point['value']
                )
                session.add(data_point)
        
        session.commit()
        logger.info(f"Successfully stored data for series {series_id}")
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error storing data for series {series_id}: {str(e)}")
        raise

def store_series_analysis(session, series_id: str, analysis: str):
    """Store AI analysis for a series"""
    try:
        series = session.query(FREDSeries).filter_by(series_id=series_id).first()
        if series:
            series.latest_analysis = analysis
            series.analysis_timestamp = datetime.now()
            session.commit()
            logger.info(f"Successfully stored analysis for series {series_id}")
        else:
            logger.error(f"Series {series_id} not found")
            raise ValueError(f"Series {series_id} not found")
    except Exception as e:
        session.rollback()
        logger.error(f"Error storing analysis for series {series_id}: {str(e)}")
        raise

def get_series_data(session, series_id: str, start_date=None, end_date=None):
    """Retrieve series data from the database"""
    query = session.query(FREDData).filter(FREDData.series_id == series_id)
    
    if start_date:
        query = query.filter(FREDData.date >= start_date)
    if end_date:
        query = query.filter(FREDData.date <= end_date)
    
    return query.order_by(FREDData.date).all()

def backup_database():
    """Create a backup of the database"""
    try:
        import shutil
        backup_path = f"{DB_PATH}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(DB_PATH, backup_path)
        logger.info(f"Database backed up to {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Error backing up database: {str(e)}")
        return False
