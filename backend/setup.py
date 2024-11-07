from setuptools import setup, find_namespace_packages

setup(
    name="trumptracker",
    version="1.0.0",
    packages=find_namespace_packages(include=["*"]),
    install_requires=[
        'fredapi==0.5.2',
        'flask==3.0.0',
        'flask-cors==4.0.0',
        'flask-limiter>=3.5.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'python-dateutil>=2.8.2',
        'requests>=2.31.0',
        'anthropic>=0.18.0',
        'sqlalchemy>=2.0.0',
        'python-dotenv>=1.0.0',
        'typing-extensions>=4.7.0'
    ],
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-asyncio>=0.21.0',
            'pytest-mock>=3.10.0'
        ]
    },
    python_requires='>=3.8',
)
