from sqlalchemy.orm import Session
from app.models.biometric_information import BiometricInformation  

class BiometricRepository:
    def __init__(self, db: Session):
        self.db = db

    # Registrar información biométrica (Enrolamiento)
    def registerBiometric(self, biometric_data: dict) -> BiometricInformation:
        db_biometric = BiometricInformation(**biometric_data)
        self.db.add(db_biometric)
        self.db.commit()
        self.db.refresh(db_biometric)
        return db_biometric

    # Buscar biométrico por ID de estudiante
    def getBiometricByStudentId(self, student_id: int) -> BiometricInformation:
        return self.db.query(BiometricInformation).filter(BiometricInformation.student_id == student_id).first()

    # Traer todos los registros biométricos (usado para poblar la caché de comparación de RF-03)
    def getAllBiometrics(self) -> list[BiometricInformation]:
        return self.db.query(BiometricInformation).all()

    # Eliminar información biométrica
    def deleteBiometric(self, student_id: int) -> bool:
        db_biometric = self.getBiometricByStudentId(student_id)
        if db_biometric:
            self.db.delete(db_biometric)
            self.db.commit()
            return True
        return False