from abc import ABC, abstractmethod

class Website(ABC):
    def __init__(self):
        self.results = []
    @abstractmethod
    def search(self, search_term):
        pass
    
    def get_results(self):
        return self.results
