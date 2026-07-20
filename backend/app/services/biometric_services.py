from sqlalchemy.orm import Session
from datetime import datetime 
from app.repositories.biometricrepository import BiometricRepository  
from app.models.biometric_information import BiometricInformation

class BiometricService:
    def __init__(self, db: Session):
        self.repository = BiometricRepository(db)

    def register_biometric(self, biometric_data: dict) -> BiometricInformation:
        if not biometric_data.get("student_id"):
            raise ValueError("El ID del estudiante es obligatorio.")
        if not biometric_data.get("face_vector"):
            raise ValueError("El vector facial es obligatorio para el reconocimiento biométrico.")
        if not biometric_data.get("encryption_hash"):
            raise ValueError("El hash de encriptación de seguridad es obligatorio.")

        if not biometric_data.get("enrollment_date"):
            biometric_data["enrollment_date"] = datetime.now()

        existing = self.repository.getBiometricByStudentId(biometric_data.get("student_id"))
        if existing:
            raise ValueError("El estudiante ya cuenta con información biométrica registrada.")
            
        return self.repository.registerBiometric(biometric_data)

    def get_biometric_by_student_id(self, student_id: int) -> BiometricInformation:
        biometric = self.repository.getBiometricByStudentId(student_id)
        if not biometric:
            raise ValueError(f"No se encontró información biométrica para el estudiante con ID {student_id}")
        return biometric

    def delete_biometric(self, student_id: int) -> bool:
        deleted = self.repository.deleteBiometric(student_id)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: No existe información biométrica para el estudiante {student_id}")
        return True