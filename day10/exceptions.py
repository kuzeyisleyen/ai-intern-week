
class WorkflowError(Exception):
    """
    Sistemimizdeki tüm özel hataların atası (Base class).
    Python'un standart Exception sınıfından miras alır.
    """
    pass


class DependencyUnavailableError(WorkflowError):
    """
    Qdrant veya Ollama gibi dış servislere hiç ulaşılamadığında (bağlantı koptuğunda vb.) fırlatılır.
    """
    pass

class DependencyTimeOutError(WorkflowError):
    """
    Bağlantı var fakat dış servislerden cevap çok geç geliyorsa fırlatılır.
    """
    pass

class WorkflowLimitError(WorkflowError):
    """
    Maksimum adım veya deneme sayısına ulaşıldıysa fırlatılır.
    """
    pass

class ResponseContractError(WorkflowError):
    """
    Modelden gelen cevap beklediğimiz JSON veya formata uymuyorsa fırlatılır.
    """
    pass

class ToolRuntimeError(WorkflowError):
    pass