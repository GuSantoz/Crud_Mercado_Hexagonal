from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.Infrastructure.http.whats_app import WhatsAppService

class UserService:
    @staticmethod
    def create_user(name, email, password, phone=None):
        whats_app_service = WhatsAppService()
        activation_code = whats_app_service.generate_activation_code()
        
        user = User.create(name=name, email=email, password=password, phone=phone, status=False, activation_code=activation_code)
        
        if phone:
            whats_app_service.send_activation_message(phone, activation_code)
        
        return UserDomain(user.id, user.name, user.email, user.password, user.phone, user.status, user.activation_code)

    @staticmethod
    def activate_user(email, activation_code):
        try:
            user = User.get((User.email == email) & (User.activation_code == activation_code))
            user.status = True
            user.save()
            return True
        except User.DoesNotExist:
            return False
