from data_storage.metadata_manupulator.enums import SOURCE










class SmaSetting:
    def __init__(self, sma_length: int = 14, source: SOURCE = SOURCE.CLOSE):
        self.sma_length = sma_length
        self.source = source

    def __str__(self):
        return f"EmaSetting(length={self.sma_length})"