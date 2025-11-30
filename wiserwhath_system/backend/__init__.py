"""Módulo Backend - API e armazenamento."""
from .api import APIClient
from .storage import LocalStorage

__all__ = ['APIClient', 'LocalStorage']
